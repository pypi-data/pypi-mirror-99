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
import time

from appy.px import Px
from appy.model.base import Base
from appy.model.fields import Show
from appy.ui.layout import Layouts
from appy.model.searches import Search
from appy.database.operators import or_
from appy.utils import string as sutils
from appy.model.fields.date import Date
from appy.utils.string import Normalize
from appy.model.utils import Object as O
from appy.model.fields.phase import Page
from appy.model.fields.group import Group
from appy.model.fields.string import String
from appy.model.fields.action import Action
from appy.model.fields.boolean import Boolean
from appy.model.fields.computed import Computed
from appy.model.fields.password import Password
from appy.model.workflow import standard as workflow
from appy.model.fields.select import Select, Selection

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
SCAN_DB    = 'Scanning all database objects...'
LOGIN_RN   = 'User "%s" has new login "%s".'
LOGIN_OP   = "Login change: local roles and/or history updated in %d/%d " \
             "object(s). Done in %.2f''."
O_WALKED   = '%d objects walked so far...'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class User(Base):
    '''Base class representing a user'''
    workflow = workflow.Owner
    noLoginUsers = ('system', 'anon')
    specialUsers = noLoginUsers + ('admin',)
    searchAdvanced = Search('advanced', actionsDisplay='inline')
    listColumns = ('title', 'name*15%|', 'login*20%|', 'roles*20%|',
                   'state*10%|')

    # The following users are always present in any Appy database
    defaultUsers = {'admin': ('Manager',), 'system': ('Manager',), 'anon': ()}

    def isAnon(self):
        '''Is the logged user anonymous ?'''
        return self.login == 'anon'

    def isSpecial(self, includeAdmin=True):
        '''Is this user a predefined user ?'''
        attr = 'specialUsers' if includeAdmin else 'noLoginUsers'
        return self.login in getattr(User, attr)

    @staticmethod
    def update(class_):
        '''Hide the title'''
        title = class_.fields['title']
        title.show = 'xml'
        title.page.icon = 'pageProfile.svg'

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Password
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # This page contains the single field "password" allowing to edit a local
    # user's password.

    def showPassword(self):
        '''Field "password" must be shown only for the local user allowed to
           modify it.'''
        mayEdit = (self.source == 'zodb') and (self.user.login == self.login)
        return 'edit' if mayEdit else None

    def showCancel(self):
        '''Do not show the "cancel" button on page "passwords" if the user is
           forced to change its password.'''
        return not self.changePasswordAtNextLogin

    pagePassword = Page('password', show=showPassword, showCancel=showCancel,
                        label='User_page_password', icon='pagePassword.svg')

    password = Password(multiplicity=(1,1), show=showPassword, label='User',
                        page=pagePassword)

    # The encrypted password, carriable via the XML layout
    def showEncrypted(self):
        '''Allow to show encrypted password to admins only, via the xml
           layout.'''
        if self.user.login == 'admin' and (self.source != 'sso'): return 'xml'

    encrypted = Computed(show=showEncrypted, label='User',
                         method=lambda o: o.values['password'])

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Title, name, first name
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    pm = {'page': Page('main', label='User_page_main', icon='pageProfile.svg'),
          'width': 28, 'layouts': Layouts.g, 'label': 'User',
          'group': Group('main', style='grid', hasLabel=False)}

    def getTitle(self, normalized=False, useName=True, nameFirst=False,
                 nameTransform=None, firstNameTransform=None):
        '''Returns a nice name for this user, based on available information:
           "first name"/"name" (if p_useName is True) or title or login. If
           p_normalized is True, special chars (like accents) are converted to
           ascii chars. When p_useName is True, if p_nameFirst is True, the
           result will be "name" / "first name", else it will be
           "first name" / "name".'''
        # A specified transform ("upper", "capitalize", etc) can be specified in
        # p_nameTransform and/or p_firstNameTransform.
        login = self.login
        r = None
        if useName:
            firstName = self.firstName
            name = self.name
            if firstName and name:
                # Apply a transform if requested
                if nameTransform:
                    name = eval('name.%s()' % nameTransform)
                if firstNameTransform:
                    firstName = eval('firstName.%s()' % firstNameTransform)
                # Concatenate first and last names in the right order
                r = '%s %s' % (name, firstName) if nameFirst \
                    else ('%s %s' % (firstName, name))
        r = r or self.title or login
        return Normalize.accents(r) if normalized else r

    def getTitleFromLogin(self, login, *args, **kwargs):
        '''Similar to p_getTitle, but for a user whose l_login is given (not
           p_self). If no user with this login exists, p_login is returned.'''
        user = self.search1('User', secure=False, login=login)
        return user.getTitle(*args, **kwargs) if user else login

    def updateTitle(self):
        '''Sets a title for this user'''
        self.title = self.getTitle(nameFirst=True)

    def ensureAdminIsManager(self):
        '''User "admin" must always have role "Manager"'''
        if self.id != 'admin': return
        roles = self.roles
        if 'Manager' not in roles:
            if not roles: roles = ['Manager']
            else: roles.append('Manager')
            self.roles = roles

    def showName(self):
        '''Name and first name, by default, can not be edited for non-local
           users.'''
        if (self.source != 'zodb'): return Show.E_
        return True

    name = String(show=showName, **pm)
    firstName = String(show=showName, **pm)

    def getFirstName(self):
        '''Return p_self's first name, or its login if the first name is
           undefined.'''
        return self.firstName or self.login

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Login
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    pm['multiplicity'] = (1,1)

    def showLogin(self):
        '''When must we show the login field ?'''
        if self.isTemp(): return 'edit'
        # The manager has the possibility to change the login itself (local
        # users only).
        if self.user.hasRole('Manager') and (self.source == 'zodb'):
            return True
        return Show.E_

    def validateLogin(self, login):
        '''Is this p_login valid ?'''
        # 2 cases: (1) The user is being created and has no login yet, or
        #          (2) The user is being edited and has already a login, that
        #              can potentially be changed.
        if not self.login or (login != self.login):
            # A new p_login is requested. Check if it is valid and free.
            # Some logins are not allowed.
            if login in self.specialUsers:
                return self.translate('login_reserved')
            # Check that no user or group already uses this login
            if self.count('User', login=login) or \
               self.count('Group', login=login):
                return self.translate('login_in_use')
        return True

    login = String(show=showLogin, validator=validateLogin, indexed=True, **pm)
    del pm['label']

    def getLogins(self, groupsOnly=False, compute=False, guard=None):
        '''Gets all the logins that can "match" this user: it own login
           (excepted if p_groupsOnly is True) and the logins of all the groups
           he belongs to.

           If p_compute is False, p_groupsOnly is False and p_self is the
           currently logged user, roles are retrieved from the guard, that
           caches it. Else, they are really computed.
        '''
        guard = guard or self.guard
        # Return the cached value on the guard when appropriate
        if not compute and not groupsOnly and (self.login == guard.userLogin):
            return guard.userLogins
        # Compute it
        r = [group.login for group in self.groups or ()]
        if not groupsOnly: r.append(self.login)
        return r

    def setLogin(self, old, new, reindex=True):
        '''Modifies p_self's login, from p_old to p_new'''
        start = time.time()
        self.login = new
        # Update the email if it corresponds to the login
        email = self.email
        if email == old:
            self.email = new
        # Update the title
        self.updateTitle()
        # Browse all objects of the database and update potential local roles
        # that referred to the old login.
        self.log(SCAN_DB)
        updated = total = 0
        for tree in self.H().dbConnection.root.iobjects.values():
            for o in tree.values():
                total += 1
                # Update local roles on this object
                rchanged = o.localRoles.replace(old, new)
                hchanged = o.history.replaceLogin(old, new)
                if rchanged or hchanged:
                    updated += 1
                    o.reindex()
                # Log progression
                if (total % 10000) == 0:
                    self.log(O_WALKED % total)
        self.log(LOGIN_RN % (old, new))
        self.log(LOGIN_OP % (updated, total, time.time()-start))
        # Reindex p_self, excepted if p_reindex is False
        if reindex: self.reindex()

    def getAllowedFrom(self, roles, logins):
        '''Gets for this user, the value allowing to perform searches regarding
           index "allowed". p_roles are user roles as computed by m_getRoles and
           p_logins are user logins as computed by m_getLogins.'''
        # Get the user roles. If a copy of the list is not done, user logins
        # will be added among user roles (again and again).
        r = roles[:]
        # Get the user logins
        if self.login != 'anon':
            for login in logins:
                r.append('user:%s' % login)
        return or_(*r)

    def getAllowedValue(self):
        '''Gets, for this user, the value allowing to perform searches regarding
           index "allowed".'''
        return self.getAllowedFrom(self.getRoles(), self.getLogins())

    def showEmail(self):
        '''In most cases, email is the login. Show the field only if it is not
           the case.'''
        # Is this user local ?
        isLocal = self.source == 'zodb'
        # Show the field nevertheless if it is not empty
        if isLocal and not self.isEmpty('email'): return True
        # Hide it if the login is an email
        login = self.login
        if login and String.EMAIL.match(login): return
        # Display the email (read-only if from an external source)
        if not isLocal: return Show.E_
        return True

    pm['label'] = 'User'
    email = String(show=showEmail, **pm)

    def getMailRecipient(self, normalized=True):
        '''Returns, for this user, the "recipient string" (first name, name,
           email) as can be used for sending an email.'''
        r = self.email or self.login
        # Ensure this is really an email
        if not String.EMAIL.match(r): return
        return '%s <%s>' % (self.getTitle(normalized=normalized), r)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Roles and permissions
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    pm['multiplicity'] = (0, None)
    del pm['width']

    def showRoles(self):
        '''Global roles are not visible or editable under all circumstances'''
        # Local users can't be granted global roles
        if self.container != self.tool: return
        # Only a Manager is allowed to grant global roles
        user = self.user
        if user.hasRole('Manager'): return True
        # The user itself, owner of himself, can consult his roles
        if user.hasRole('Owner', self): return Show.E_

    roles = Select(show=showRoles, indexed=True, width=40, height=10,
                   validator=Selection(lambda o: o.model.getGrantableRoles(o)),
                   render='checkbox', **pm)

    def getRoles(self, compute=False, guard=None):
        '''Returns all the global roles granted to this user. Not simply
           self.roles, but also "ungrantable roles" (like Anonymous or
           Authenticated) and roles inherited from group membership.

           If p_compute is False and p_self is the currently logged user, roles
           are retrieved from the guard, that caches it. Else, they are really
           computed.
        '''
        guard = guard or self.guard
        # Return the cached value on the guard when appropriate
        if not compute and (self.login == guard.userLogin):
            return guard.userRoles
        # Compute it
        r = list(self.roles)
        # Add ungrantable roles
        r.append('Anonymous' if self.isAnon() else 'Authenticated')
        # Add group global roles
        for group in self.groups:
            for role in group.roles:
                if role not in r: r.append(role)
        return r

    def hasRole(self, role, o=None):
        '''Has p_self this p_role? If p_o is None, check if this user has p_role
           globally; else, check if he has it in the context of p_o.

           p_role can also be a list/tuple of roles. In this case, the method
           returns True if the user has at least one of the listed roles.'''
        # Try with the user's global roles, excepted if p_o is in "local" mode
        noo = o is None
        if noo or not o.localRoles.only:
            r = sutils.stringIsAmong(role, self.getRoles())
            if noo or r: return r
        # Check now p_o(bject)'s local roles
        logins = self.getLogins()
        for login, roles in o.localRoles.items():
            if (login in logins) and sutils.stringIsAmong(role, roles):
                return True

    def ensureIsManager(self):
        '''Ensures p_self has role "Manager"'''
        roles = self.roles
        if 'Manager' not in roles:
            if not roles: roles = ['Manager']
            else: roles.append('Manager')
            self.roles = roles

    def hasPermission(self, permission, o):
        '''Has user p_self p_permission on p_o ?'''
        # What are the roles which are granted p_permission on p_o ?
        allowedRoles = o.getWorkflow().getRolesFor(o, permission)
        # Grant access based on global user roles (that include ungrantable
        # roles like Authenticated or Anonymous), excepted if p_o is in
        # "local" mode.
        if not o.localRoles.only:
            for role in self.getRoles():
                if role in allowedRoles: return True
        # Grant access based on local roles. Gets the logins of this user and
        # all its groups
        userLogins = self.getLogins()
        for login, roles in o.localRoles.items():
            # Ignore logins not corresponding to this user
            if login not in userLogins: continue
            for role in roles:
                if role in allowedRoles: return True

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Source
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Where is this user stored ? By default, in the ZODB. But the user can be
    # stored in an external LDAP (source='ldap').
    source = String(show='xml', default='zodb', layouts='f', label='User')

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Actions
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def doResetPassword(self, secure=True):
        '''Triggered from the UI, this method defines a new, automatically
           generated password for this user and returns it in the UI.'''
        user = self.user
        if secure and not user.allows('write'):
            self.raiseUnauthorized()
        password = self.getField('password').generate()
        self.password = password
        self.changePasswordAtNextLogin = True
        # If p_self corresponds to the currently logged user, update the
        # authentication cookie with its new password.
        if self == user:
            self.guard.Cookie.updatePassword(self.H(), password)
        return True, self.translate('new_password_text',
                                    mapping={'password': password})

    def showResetPassword(self):
        '''Action "reset password" is available to anyone having write access to
           the user, excepted the user himself.'''
        if (self.source == 'zodb') and self.guard.mayEdit(self) and \
           (self.user != self) and not self.isSpecial(includeAdmin=False):
            return 'buttons'

    resetPassword = Action(action=doResetPassword, show=showResetPassword,
                           confirm=True, label='User', icon='pagePassword.svg',
                           sicon='password.svg', render='icon')

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Hidden fields
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    hidden = {'show': False, 'layouts': 'f', 'label': 'User'}
    # For external users (source != "zodb"), we store the date of the last time
    # the external user and the local copy were synchronized.
    syncDate = Date(format=Date.WITH_HOUR, **hidden)
    # The date of the last login for this user
    lastLoginDate = Date(format=Date.WITH_HOUR, **hidden)
    # We may force a local user (source=zodb) to change its password at next
    # login (ie, for users created by an admin).
    changePasswordAtNextLogin = Boolean(**hidden)

    def getLanguage(self):
        '''Gets the language (code) for p_self'''
        handler = self.H()
        # There may be a forced language defined for everyone
        config = handler.config.ui
        if config.forcedLanguage: return config.forcedLanguage
        # Try to get the value from a cookie. Indeed, if such a cookie is
        # present, it means that the user has explicitly chosen this language
        # via the language selector.
        r = handler.req.AppyLanguage
        if r: return r
        # Try the "Accept-Language" header, which stores language preferences as
        # defined in the user's browser. Several languages can be listed, from
        # most to less wanted.
        r = handler.headers['Accept-Language']
        if not r:
            # Return the first language supported by the app
            return config.languages[0]
        # Browse prefered languages and return the first that is among app
        # language. If no language matches, return the first one as supported by
        # the app.
        supported = config.languages
        for lang in r.split(','):
            # Extract the 2-letter code
            code = None
            i = lang.find('-')
            if i != -1:
                code = lang[:i]
            else:
                i = lang.find(';')
                if i != -1:
                    code = lang[:i]
            code = (code or lang).strip()
            if code in supported:
                # Warn the user that this one has been chosen
                handler.resp.setHeader('Content-Language', code)
                return code
        # No supported language was found among user's prefered languages
        return supported[0]

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  PXs
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Display, in the user strip, links to the User instance of the logged user
    pxUserLink = Px('''
     <a if="cfg.userLink" href=":user.url">
      <img src=":url('user.svg')" class="icon"/>
      <span class="topText">:user.getFirstName()</span>
     </a>
     <x if="not cfg.userLink">:user.getFirstName()</x>''')

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Class methods
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    class System:
        '''Fake class representing the "system" user at places where its
           corresponding User instance is not available yet.'''
        login = 'system'
        logins = [login]
        roles = ['Manager', 'Authenticated']
        allowedValue = or_(*roles)

        def getLogins(self, **kwargs): return self.logins
        def getRoles(self, **kwargs): return self.roles
        def getAllowedFrom(self, roles, logins): return self.allowedValue
        def getLanguage(self): return 'en'
        def getInitiator(self): return
        def hasPermission(self, permission, o): return True
        def hasRole(self, role, o=None): return True

    @classmethod
    def identify(class_, guard):
        '''To identify a user means: get its login, password and authentication
           context. There are several places to look for this information: the
           Appy authentication cookie, HTTP authentication, or credentials from
           the login form.'''

        # If no user could be identified, the "anon" user, representing an
        # anonymous user, will nevertheless be identified.
        handler = guard.handler
        req = handler.req
        login = password = ctx = place = None
        # a. Identify the user from the authentication cookie
        try:
            login, password, ctx = guard.Cookie.read(handler)
        except Exception as e:
            handler.log('app', 'error', 'Unreadable cookie (%s)' % str(e))
        if login: place = 'cookie'
        # b. Identify the user from HTTP basic authentication
        if not login and ('_basic_auth_' in req):
            # Credentials from HTTP basic authentication are present, decode it
            creds = req._basic_auth_
            if creds.lower().startswith('basic '):
                try:
                    creds = creds.split(' ')[-1]
                    login, password = base64.decodestring(creds).split(':', 1)
                    if login: place = 'basic'
                except Exception:
                    pass
        # c. Identify the user from the authentication form
        if not login:
            login = req.login
            if login:
                login = handler.config.security.transformLogin(login.strip())
            password = req.password or ''
            ctx = req.context
            if login: place = 'form'
        # d. Identify the user from a SSO reverse proxy
        if not login or (login == '_s_s_o_'):
            sso = handler.config.security.sso
            if sso:
                login = sso.extractUserLogin(guard)
                if login: place = 'sso'
        # e. If all identification methods failed, identify the user as "anon"
        return login or 'anon', password, ctx, place

    @classmethod
    def authenticate(class_, guard):
        '''Authenticate the currently logged user and return its corresponding
           User instance.'''
        handler = guard.handler
        # Manage a non-HTTP request
        if handler.fake:
            # We are running in a specific context: at HTTP server startup, or
            # by a script. The "system" user, representing the running server
            # himself, must be used and returned. This user, for which a User
            # instance normally exists, may be requested before it is created
            # (on database initialization). This is why we may create here a
            # fake one.
            if hasattr(handler, 'connection'):
                user = handler.dbConnection.root.objects.get('system') or \
                       User.System()
            else:
                user = User.System()
            return user
        # Identify the user
        login, password, ctx, place = User.identify(guard)
        config = guard.config.security
        authContext = config.authContext
        tool = handler.tool
        if place == 'sso':
            # We have found a user already authenticated by a SSO (Single
            # Sign-On) reverse proxy: its credentials were carried in HTTP
            # headers. Simply return its local copy, or create it if not found.
            user = config.sso.getUser(tool, login, createIfNotFound=True)
        else:
            # In any other case, authentication must be performed
            user = None
            if place == 'form':
                # A user has typed its login and password from the ui (pxLogin).
                # If a LDAP server is defined, try to find it there.
                if config.ldap:
                    user = config.ldap.getUser(tool, login, password)
            # Get the user from the local database if it was not found yet
            user = user or tool.search1('User', login=login)
            # Authentication fails (and user "anon" is returned) if the user was
            # not found or inactive, its password was invalid or the required
            # authentication context was not found.
            if (user is None) or user.isAnon() or (user.state=='inactive') or \
               (not user.getField('password').check(user, password)) or \
               (not ctx and authContext and authContext.isMandatory(tool) and \
                (place != 'basic')):
                # Disable the authentication cookie
                guard.Cookie.disable(handler)
                user = handler.dbConnection.root.objects.get('anon')
            else:
                # The user is authenticated. Create an authentication cookie for
                # him. Set a default context when appropriate.
                if authContext and not ctx:
                    ctx = authContext.getDefaultContext(tool, user)
                guard.Cookie.write(handler, user.login, password, ctx)
        # Set, on the guard, when present, attributes related to the
        # authentication context.
        if ctx and authContext: authContext._setOnGuard(tool, user, guard, ctx)
        return user

    @classmethod
    def getOnline(class_, tool, expr=None, context=None):
        '''Returns a XHTML table showing users being currently connected'''
        # If p_expr is given, it must be an expression that will be evaluated on
        # every connected user. The user will be part ofthe result only if the
        # expression evaluates to True. The user is given to the expression as
        # variable "user".
        # ~~~
        # Get and count connected users
        users = list(tool.H().onlineUsers.items())
        users.sort(key=lambda u: u[1], reverse=True) # Sort by last access date
        count = len(users)
        # Prepare the expression's context when relevant
        if expr:
            if context is None: context = {}
        # Compute table rows
        rows = []
        for login, access in users:
            user = tool.search1('User', login=login)
            if not user: continue # Could have been deleted in the meanwhile
            if expr:
                # Update the p_expr's context with the current user
                context['user'] = user
                # Evaluate it
                if not eval(expr, context): continue
            rows.append('<tr><td><a href="%s">%s</a></td><td>%s</td></tr>' % \
                        (user.url, user.title, tool.formatDate(access)))
        # Create an empty row if no user has been found
        if not rows:
            rows.append('<tr><td colspan="2" align="center">%s</td></tr>' %
                        tool.translate('no_value'))
            count = 0
        else:
            count = len(rows)
        # Build the entire table
        r = '<table class="list"><tr><th>(%d)</th><th>%s</th></tr>' % \
            (count, tool.translate('last_user_access'))
        return r + '\n'.join(rows) + '</table>'

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Appy methods
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def onEdit(self, created):
        '''To do when a user is p_created or updated'''
        # For a freshly created local user, generate him a password (if not
        # already set).
        isLocal = self.source == 'zodb'
        message = None
        if created and isLocal and self.isEmpty('password') and \
           self.config.security.generatePassword:
            # Generate a clear password
            password = self.getField('password').generate()
            # Store it, encrypted
            self.password = password
            # Return the clear password to the UI
            message = self.translate('new_password_text',
                                     mapping={'password': password})
        page = self.req.page or 'main'
        if page == 'main':
            login = self.login
            # (re)-compute p_self's title, computed from other fields
            self.updateTitle()
            # Ensure correctness of some infos about this user
            if isLocal and (self.id == 'admin'): self.ensureIsManager()
            # p_self must be owned by itself
            self.localRoles.add(login, 'Owner')
            # If the user was created by anon|system, anon|system can't stay its
            # Owner.
            self.localRoles.delete(('anon', 'system'))
        elif page == 'password':
            # If p_self corresponds to the currently logged user, update the
            # authentication cookie with its new password.
            if self.user == self:
                self.guard.Cookie.updatePassword(self.H(), self.req.password)
            # Reset this flag
            self.changePasswordAtNextLogin = False
        return message

    def mayEdit(self):
        '''No one can edit users "system" and "anon"'''
        return not self.isSpecial(includeAdmin=False)

    def mayDelete(self):
        '''Special users cannot be deleted'''
        return not self.isSpecial()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
