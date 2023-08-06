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
from appy import Config
from appy.model.base import Base
from appy.model.user import User
from appy.model.fields import Show
from appy.ui.layout import Layouts
from appy.model.fields.ref import Ref
from appy.model.fields.string import String
from appy.model.workflow import standard as workflows
from appy.model.fields.select import Select, Selection
from appy.model.fields.group import Group as FieldGroup

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Group(Base):
    '''Base class representing a group'''
    workflows.Owner

    m = {'group': FieldGroup('main', style='grid', hasLabel=False),
         'width': 25, 'indexed': True, 'layouts': Layouts.g, 'label': 'Group'}

    @staticmethod
    def update(class_):
        title = class_.fields['title']
        title.group = Group.m['group']
        title.layouts = Layouts.g

    def showLogin(self):
        '''When must we show the login field ?'''
        return 'edit' if self.isTemp() else Show.TR

    def showGroups(self):
        '''Only the admin can view or edit roles'''
        return self.user.hasRole('Manager')

    def validateLogin(self, login):
        '''Is this p_login valid ?'''
        return True

    login = String(multiplicity=(1,1), show=showLogin,
                   validator=validateLogin, **m)

    # Field allowing to determine which roles are granted to this group
    roles = Select(validator=Selection(lambda o: o.model.getGrantableRoles(o)),
                   render='checkbox', multiplicity=(0,None), **m)

    users = Ref(User, multiplicity=(0,None), add=False, link='popup',
      height=15, back=Ref(attribute='groups', show=User.showRoles,
                          multiplicity=(0,None), label='User'),
      showHeaders=True, shownInfo=('title', 'login', 'state*100px|'),
      actionsDisplay='inline', label='Group', group=m['group'])
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
