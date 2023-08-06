'''Workflow-specific model elements'''

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

# Default Appy permissions - - - - - - - - - - - - - - - - - - - - - - - - - - -
r, w, d = 'read', 'write', 'delete'
emptyDict = {}

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class WorkflowException(Exception): pass

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Role:
    '''A role is a prerogative that is granted to a user or group'''
    # A role can be local or global.
    # --------------------------------------------------------------------------
    # Local  | A local role applies to (and is stored on) a single object.
    # Global | A global role applies throughout the whole app, independently of
    #        | any object.
    # --------------------------------------------------------------------------
    # These roles are the base roles shipped with Appy
    baseRoles = (
     'Manager',      # The most permissive role. A Manager can do everything.
     'Owner',        # Automatically granted to an object's creator
     'Anonymous',    # Automatically granted to any unlogged hit to the site
     'Authenticated' # Automatically granted to any logged user
    )
    # The following roles are all global, "Owner" excepted
    baseLocalRoles = ('Owner',)
    # The following roles are "ungrantable": Appy grants them automatically
    baseUngrantableRoles = ('Anonymous', 'Authenticated')

    def __init__(self, name, local=False, grantable=True):
        # The name of the role
        self.name = name
        # Is it local or global ?
        self.local = local
        # It is a base Appy role or an application-specific one ?
        self.base = name in Role.baseRoles
        if self.base and (name in Role.baseLocalRoles):
            self.local = True
        # Is it grantable ?
        self.grantable = grantable
        if self.base and (name in self.baseUngrantableRoles):
            self.grantable = False

    def match(self, base, local, grantable):
        '''Does this role match parameters ?'''
        # Every parameter can be True, False or None
        if (base is not None) and (base != self.base): return
        if (local is not None) and (local != self.local): return
        if (grantable is not None) and (grantable != self.grantable): return
        return True

    def getLabel(self, withDefault=False):
        '''Returns the i18n label corresponding to this role. If p_withDefault
           is True, it also returns the default value for the label. In this
           case the r_esult is a tuple (s_label, s_defaultValue).'''
        r = 'role_%s' % self.name
        return r if not withDefault else r, self.name

    def __repr__(self):
        local = self.local and ' (local)' or ''
        return '<role %s%s>' % (self.name, local)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
