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
from appy.px import Px
from appy.model.base import Base
from appy.ui.layout import Layouts
from appy.database.operators import or_
from appy.model.fields.group import Group
from appy.model.searches.modes import Mode
from appy.model.fields.string import String
from appy.model.fields.integer import Integer
from appy.model.fields.boolean import Boolean
from appy.model.workflow.standard import Owner
from appy.model.searches import Search, UiSearch
from appy.model.fields.select import Select, Selection

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Query(Base):
    '''Persistent and editable parameters for a Search'''

    workflow = Owner
    # Queries are not indexed by default
    indexable = False
    listColumns = ('title', 'className', 'states', 'sortBy', 'sortOrder','mode')
    pageListColumns = ('title', 'state')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                            Main parameters
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Fields in the main page are rendered in a grid group
    mainGroup = Group('main', ['250em', ''], style='grid', hasLabel=False)

    qp = {'label': 'Query', 'group': mainGroup}

    # The name of the root class for which instances are searched
    def listRootClasses(self):
        '''Lists the app's root classes'''
        return [(name, self.translate('%s_plural' % name)) \
                for name in self.config.model.rootClasses]

    className = Select(validator=Selection(listRootClasses),
                       multiplicity=(1,1), **qp)

    # Only objects being in one of the states defined in the hereabove field
    # will be part of the result.
    def listStates(self, className=None):
        '''Lists the states from the workflow tied to the class whose name is
           p_className.'''
        className = className or self.className
        r = []
        if not className: return r
        for state in self.model.classes[className].workflow.states.values():
            r.append((state.name, self.translate(state.labelId)))
        return r

    states = Select(validator=Selection(listStates), multiplicity=(1,None),
                    master=className, masterValue=listStates, **qp)

    # Technical indexed fields that the user cannot choose
    unselectableIndexes = ('allowed', 'cid')

    # Field used as sort key
    def listIndexedFields(self, className=None):
        '''Lists, for the class whose name is p_className, the fields being
           indexed.'''
        className = className or self.className
        r = []
        if not className: return r
        for field in self.model.classes[className].fields.values():
            # Ignore the field if it cannot be chose
            if field.name in Query.unselectableIndexes: continue
            if field.indexed:
                r.append((field.name, self.translate(field.labelId)))
        return r

    sortBy = Select(validator=Selection(listIndexedFields), multiplicity=(1,1),
                    master=className, masterValue=listIndexedFields, **qp)
    sortOrder = Select(validator=('asc', 'desc'), multiplicity=(1,1), **qp)
    mode = Select(validator=Mode.concrete, multiplicity=(1,1), **qp)
    maxPerPage = Integer(default=30, multiplicity=(1,1), width=2, **qp)
    showPods = Boolean(default=False, **qp)
    showTitle = Boolean(default=False, **qp)
    showNav = Select(validator=('top', 'bottom', 'both', 'none'),
                     default='both', multiplicity=(1,1), render='radio', **qp)
    navAlign = Select(validator=('left', 'center', 'right'),
                     default='center', multiplicity=(1,1), render='radio', **qp)
    showFilters = Boolean(default=True, **qp)

    def validViaPopup(self, value):
        '''Ensure p_value is valid to be stored in field "viaPopup"'''
        value = value.strip()
        # Value can be "False" or can contain pa popup's width and height, in
        # pixels.
        if not value or (value == 'False'): return True
        value = value.split()
        if len(value) > 2: return self.translate('wrong_via_popup')
        for v in value:
            if not v.endswith('px') or not v[:-2].isdigit():
                return self.translate('wrong_via_popup')
        return True

    viaPopup = String(layouts=Layouts.gd, validator=validViaPopup, **qp)
    pageLayoutOnView = String(layouts=Layouts.gd, **qp)

    def getSearch(self):
        '''Creates the Search and UiSearch instances corresponding to this
           query.'''
        # Get the expression related to p_self.states
        states = self.states
        if len(states) == 1:
            state = states[0]
        else:
            state = or_(states)
        # Get the "viaPopup" parameter
        viaPopup = self.viaPopup or ''
        if viaPopup == 'False':
            viaPopup = False
        elif ' ' in viaPopup: # Popup width and height are specified
            viaPopup = viaPopup.split()
            for i in (0, 1): viaPopup[i] = viaPopup[i].strip()
        elif viaPopup: # Only the popup width is specified
            viaPopup = viaPopup.strip()
        # Create the Search instance corresponding to p_self's attributes
        className = self.className
        class_ = self.model.classes.get(className)
        return Search(name=str(self.iid), maxPerPage=self.maxPerPage,
                      translated=self.translate('%s_plural' % className),
                      sortBy=self.sortBy, sortOrder=self.sortOrder,
                      showPods=self.showPods, showTitle=self.showTitle,
                      showNav=self.showNav, navAlign=self.navAlign,
                      showFilters=self.showFilters, container=class_,
                      viaPopup=viaPopup, pageLayoutOnView=self.pageLayoutOnView,
                      resultModes=(self.mode,), state=state)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                            PX rendering
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Simulate a HTTP GET on a search corresponding to this Query instance
    pxView = Px('''
     <x var="x=setattr(req, 'className', o.className);
             x=setattr(req, 'search', str(o.iid));
             x=Px.injectRequest(_ctx_, req, tool)">:tool.Search.results</x>''')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
