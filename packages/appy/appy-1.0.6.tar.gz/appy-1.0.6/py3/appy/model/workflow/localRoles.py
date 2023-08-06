'''Data structure storing local roles on every Appy object'''

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
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping

# Errors - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NO_LOGIN_OR_ROLE  = 'Empty login or role.'
NO_LOGIN_AND_ROLE = 'Empty login and role.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class LocalRoles(PersistentMapping):
    '''Dict-like data structure storing local roles on an Appy object'''

    # Dict has spec ~{s_login: [s_role]}~ and defines, for every user or group
    # login, the list of roles granted to him on the linked object.

    def __init__(self):
        PersistentMapping.__init__(self)
        # When boolean "only" is True, the workflow behaves differently: it only
        # checks local roles (and thus it ignores the user's global roles).
        # Read this attribute in the context of an object:
        #                     "o.localRoles.only"
        self.only = False

    def add(self, login, role, o=None):
        '''Grants to some p_login (or several if p_login is a list/tuple) a
           given local p_role (or several if p_role is a list/tuple). Returns
           the number of actually added local roles.'''

        # Security information for any object is indexed. So if the object being
        # modified is not the main object of a ui transaction (ie, not triggered
        # within m_onEdit), give it in p_o and security-related info on it will
        # be reindexed.

        if not login or not role: raise Exception(NO_LOGIN_OR_ROLE)
        r = 0
        # Standardise parameters
        login = (login,) if isinstance(login, str) else login
        role = (role,) if isinstance(role, str) else role
        # Browse logins to update
        for l in login:
            # Get or create the list of local roles for this login
            if l in self:
                roles = self[l]
            else:
                self[l] = roles = PersistentList()
            # Browse roles to grant
            for rol in role:
                if rol not in roles:
                    roles.append(rol)
                    r += 1
        # Reindex the security-related index on p_o if required
        if o: o.reindex(fields=('allowed',))
        return r

    def delete(self, login=None, role=None, o=None):
        '''Ungrants, for a given p_login, some local p_role. Returns the number
           of actually deleted local roles.'''

        # If p_login is None, is ungrants p_role for every login mentioned in
        # local roles. If p_login is a list/tuple, it ungrants p_role to those
        # p_logins.

        # If p_role is None, it ungrants all previously granted roles to
        # p_login. If p_role is a list/tuple, if ungrants those roles to
        # p_login.

        # For parameter p_o, same remark as for m_add.

        if not login and not role: raise Exception(NO_LOGIN_AND_ROLE)
        r = 0
        if not role:
            # Ungrant to p_login every previously granted role
            if isinstance(login, str): login = (login,)
            for l in login:
                if l in self:
                    del(self[l])
                    r += 1
        else:
            # To what login(s) must we ungrant p_role(s) ?
            if not login:
                # To anyone having local roles on this object
                login = list(self.keys())
            # Else: to the login(s) specified in p_login
            elif isinstance(login, str): login = (login,)
            # Ungrant roles
            if isinstance(role, str): role = (role,)
            for l in login:
                if l not in self: continue
                roles = self[l]
                for rol in role:
                    if rol in roles:
                        roles.remove(rol)
                        r += 1
                # Remove the entry if no more role is granted to this login
                if not roles:
                    del(self[l])
        # Reindex the security-related index if required
        if o: o.reindex(fields=('allowed',))
        return r

    def update(self, add, login=None, role=None, o=None):
        '''Shorthand for calling m_add if p_add is True, or m_delete else'''
        do = self.add if add else self.delete
        return do(login, role, o)

    def reset(self, o=None):
        '''Removes all local roles stored on p_self. If p_o is given, local role
           "Owner" is granted to p_o's creator.'''
        self.clear()
        if o: self.add(o.creator, 'Owner')

    def getLoginsHaving(self, role):
        '''Gets all logins having local p_role on this object'''
        r = set()
        for login, roles in self.items():
            if role in roles:
                r.add(login)
        return r

    def replace(self, login, new):
        '''Replace, if found, the entry whose key is this p_login with the same
           entry, but whose key has been replaced with this p_new login.
           r_ is True if the replacement has been done.'''
        if login not in self: return
        roles = self.pop(login)
        self[new] = roles
        return True
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
