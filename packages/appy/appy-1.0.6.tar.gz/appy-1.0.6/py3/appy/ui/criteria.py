#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Copyright (C) 2007-2021 Gaetan Delannay

# This file is part of Appy.

# Appy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Appy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# Appy. If not, see <http://www.gnu.org/licenses/>.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import re
from DateTime import DateTime
from appy.utils import string as sutils

# Importing database operators is required when evaluating criteria expressions
from appy.database.operators import and_, or_, in_, not_

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Criteria:
    '''Represents a set of search criteria manipulated from the UI'''

    def __init__(self, tool):
        self.tool = tool
        # This attribute will store the dict of search criteria, ready to be
        # injected in a Search class for performing a search in the catalog.
        self.criteria = None

    @classmethod
    def readFromRequest(class_, handler):
        '''Unmarshalls, from request key "criteria", a dict that was marshalled
           from a dict similar to the one stored in attribute "criteria" in
           Criteria instances.'''
        # Get the cached criteria on the handler if found
        cached = handler.cache.criteria
        if cached: return cached
        # Criteria may be absent from the request
        criteria = handler.req.criteria
        if not criteria: return
        # Criteria are present but not cached. Get them from the request,
        # unmarshal and cache them.
        r = eval(criteria)
        handler.cache.criteria = r
        return r

    @classmethod
    def highlight(class_, handler, text):
        '''Highlights parts of p_text if we are in the context of a search whose
           keywords must be highlighted.'''
        # Must we highlight something ?
        criteria = class_.readFromRequest(handler)
        if not criteria or ('searchable' not in criteria): return text
        # Highlighting operators is not supported yet
        keywords = criteria['searchable']
        if not isinstance(keywords, str): return text
        # Highlight every variant of every keyword. Use preferably the words as
        # encoded by the user instead of their normalized version.
        keywords = handler.req.w_searchable or keywords
        for word in keywords.strip().split():
            for variant in (word, word.capitalize(), word.lower()):
                highlighted = '<span class="highlight">%s</span>' % variant
                text = re.sub('(?<= |\(|\>)?%s' % variant, highlighted, text)
        return text

    def getFromRequest(self, class_):
        '''Retrieve search criteria from the request after the user has filled
           an advanced search form and store them in p_self.criteria.'''
        r = {}
        req = self.tool.req
        # Retrieve criteria from the request
        for name, value in req.items():
            # On search form, every search field is prefixed with "w_"
            if not name.startswith('w_'): continue
            name = name[2:]
            # Get the corresponding field
            field = class_.fields.get(name)
            # Ignore this value if it is empty or if the field is inappropriate
            # for a search.
            if not field or not field.indexed or field.searchValueIsEmpty(req):
                continue
            # We have a(n interval of) value(s) that is not empty for a given
            # field. Get it.
            r[name] = field.getSearchValue(req)
        # Complete criteria with Ref info if the search is restricted to
        # referenced objects of a Ref field.
        info = req.ref
        if info: r['_ref'] = info
        self.criteria = r

    def asString(self):
        '''Returns p_self.criteria, marshalled in a string'''
        return sutils.getStringFrom(self.criteria, stringify=False, c='"')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
