'''An index for Rich fields, extracting pure text and splitting it into words'''

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
from appy.xml.extractor import Extractor
from appy.database.indexes.text import TextIndex

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class RichIndex(TextIndex):
    '''Index for Rich fields'''

    @classmethod
    def toIndexed(class_, value, field):
        '''Converts p_value, which is a chunk of XHTML code, into pure text and
           splits it into words.'''
        if not value: return
        # Use an XHTML text extractor. p_value represents a chunk of XHTML code,
        # but there is no guarantee that this code contains a single root tag,
        # so add one.
        extractor = Extractor(normalize=True, keepCRs=False)
        value = extractor.parse('<x>%s</x>' % value)
        # Tokenize the result, but text has already been normalized
        return TextIndex.toIndexed(value, field, normalize=False)

    @classmethod
    def toString(class_, o, value):
        '''Converts p_value to pure text via an XHTML text extractor'''
        # No need to normalize p_value here: it will be done by the global
        # "searchable" index.
        return Extractor(keepCRs=False).parse('<x>%s</x>' % value) if value \
                                                                   else None
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
