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
import copy
from appy.utils import sequenceTypes
from appy.model.workflow import Role

# Errors - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
PERMISSION_NOT_FOUND = 'permission "%s" is not among permissions dict for ' \
  'state %s in workflow %s.'
                            
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class State:
    '''Represents a workflow state'''
    def __init__(self, permissions, initial=False, phase=None):
        self.usedRoles = {}
        # Dict "permissions" lists, for every permission managed by a workflow,
        # the roles for which the permission is granted in this state. Standard
        # permissions are 'read', 'write' and 'delete'. p_permissions must be a
        # dict with format
        #            ~{s_permissionName:[s_roleName|Role_role]}~

        # It will be converted by m_standardizeRoles into format
        #            ~{s_permissionName:{s_roleName:Role_role}}~
        self.permissions = permissions
        self.initial = initial
        self.phase = phase
        # Standardize the way roles are expressed within self.permissions
        self.standardizeRoles()

    def init(self, workflow, name):
        '''Lazy initialisation'''
        self.workflow = workflow
        self.name = name
        self.labelId = '%s_%s' % (workflow.name, name)

    def __repr__(self):
        return '<state %s::%s>' % (self.workflow.name, self.name)

    def copyPerms(self):
        '''Gets a deep copy of this state's permissions dict'''
        return copy.deepcopy(self.permissions)

    def getRole(self, role):
        '''p_role can be the name of a role or a Role instance. If it is the
           name of a role, this method returns self.usedRoles[role] if it
           exists, or creates a Role instance, puts it in self.usedRoles and
           returns it else. If it is a Role instance, the method stores it in
           self.usedRoles if it is not in it yet and returns it.'''
        if isinstance(role, str):
            if role in self.usedRoles:
                return self.usedRoles[role]
            else:
                theRole = Role(role)
                self.usedRoles[role] = theRole
                return theRole
        else:
            if role.name not in self.usedRoles:
                self.usedRoles[role.name] = role
            return role

    def standardizeRoles(self):
        '''This method converts, within self.permissions, every role to a
           Role instance. Every used role is stored in self.usedRoles.'''
        for permission, roles in self.permissions.items():
            if isinstance(roles, str) or isinstance(roles, Role):
                role = self.getRole(roles)
                self.permissions[permission] = {role.name: role}
            elif isinstance(roles, dict):
                for name, role in roles.iteritems():
                    roles[name] = self.getRole(role)
            else:
                # "roles" is a list or tuple, or None (nobody may have this
                # permission).
                d = {}
                if roles is not None:
                    for role in roles:
                        role = self.getRole(role)
                        d[role.name] = role
                self.permissions[permission] = d

    def getUsedRoles(self): return self.usedRoles.values()

    def getRolesFor(self, permission):
        '''Gets the roles that are granted p_permission on this state. r_ is a
           dict ~{s_roleName: Role}.'''
        if permission not in self.permissions:
            raise Exception(PERMISSION_NOT_FOUND % (permission, self.name, \
                                                    self.workflow.name))
        return self.permissions[permission]

    def addRoles(self, roles, permissions=()):
        '''Adds p_roles in self.permissions. p_roles can be a role name, a Role
           instance or a list of names and/or Role instances. If p_permissions
           is specified, roles are added to those permissions only. Else, roles
           are added for every permission within self.permissions.'''
        # Standardize parameters
        if type(roles) not in sequenceTypes: roles = (roles,)
        if isinstance(permissions, str): permissions = (permissions,)
        for perm, existingRoles in self.permissions.items():
            if permissions and (perm not in permissions): continue
            for role in roles:
                # Do nothing if "role" is already among existing roles
                name = role if isinstance(role, str) else role.name
                if name in existingRoles: continue
                # Add the role for this permission
                existingRoles[name] = self.getRole(role)

    def removeRoles(self, roleNames, permissions=()):
        '''Removes p_roleNames within dict self.permissions. If p_permissions is
           specified, removal is restricted to those permissions. Else, removal
           occurs throughout the whole dict self.permissions.'''
        if isinstance(roleNames, str): roleNames = (roleNames,)
        if isinstance(permissions, str): permissions = (permissions,)
        for perm, roles in self.permissions.items():
            if permissions and (perm not in permissions): continue
            for name in roleNames:
                # Remove this role if present in roles for this permission
                if name in roles:
                    del roles[name]

    def setRoles(self, roleNames, permissions=()):
        '''Sets p_rolesNames for p_permissions if not empty, for every
           permission in self.permissions else.'''
        if isinstance(roleNames, str): roleNames = (roleNames,)
        if isinstance(permissions, str): permissions = (permissions,)
        for perm in self.permissions:
            if permissions and (perm not in permissions): continue
            roles = self.permissions[perm] = {}
            for name in roleNames:
                roles[name] = self.getRole(name)

    def replaceRole(self, oldRoleName, newRoleName, permissions=()):
        '''Replaces p_oldRoleName by p_newRoleName. If p_permissions is
           specified, the replacement is restricted to those permissions. Else,
           replacements apply to the whole dict self.permissions.'''
        if isinstance(permissions, str): permissions = (permissions,)
        for perm, roles in self.permissions.items():
            if permissions and (perm not in permissions): continue
            # Find and replace p_oldRoleName with p_newRoleName
            if oldRoleName in roles:
                del roles[oldRoleName]
                roles[newRoleName] = self.getRole(newRoleName)

    def copyRoles(self, sourcePermission, destPermission):
        '''Overrides p_destPermission's roles with (a deep copy of)
           p_sourcePermission's roles.'''
        copiedRoles = copy.deepcopy(self.permissions[sourcePermission])
        self.permissions[destPermission] = copiedRoles

    def isIsolated(self):
        '''Returns True if, from this state, we cannot reach another state.
           Modifying a workflow for getting a state with auto-transitions only
           is a common technique for disabling a state in a workflow.'''
        if self.initial: return
        for tr in self.workflow.transitions.values():
            # Ignore transitions that do not touch this state
            if not tr.hasState(self, True) and not tr.hasState(self, False):
                continue
            # Transition "tr" has this state as start or end state. If start and
            # end states are different, it means that the state is not
            # isolated.
            if tr.isSingle():
                for state in tr.states:
                    if state != self: return
            else:
                for start, end in tr.states:
                    # Bypass (start, end) pairs having nothing to do with self
                    if (start != self) and (end != self): continue
                    if (start != self) or (end != self): return
        # If we are here, either there was no transition starting from self,
        # either all transitions were auto-transitions: self is then isolated.
        return True
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
