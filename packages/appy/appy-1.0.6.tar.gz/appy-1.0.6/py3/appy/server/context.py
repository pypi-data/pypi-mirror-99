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
from appy.utils import noSwitchLayouts

from appy.server.cookie import Cookie

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class AuthenticationContext:
    '''When an application uses an authentication context, its users, when
       logging in, must, besides their login and password, choose a context
       among possible authentication contexts. Then, your application has access
       to the chosen context via the handler attribute "authContext".

       If you want to use authentication contexts in your Appy application, you
       must create a class that inherits from this one and overrides some of its
       methods (see below). Then, in your Config instance set an instance of
       your class in attribute config.security.authContext.
    '''
    traverse = {}

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                           W a r n i n g
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Several methods defined hereafter can be overridden by child classes
    # written by developers in Appy apps. These methods are called from within
    # the Appy authentication mechanism:
    #
    # getContexts
    # getDefaultContext
    # getObject

    # It means that, when these methods are called, security-related elements
    # may not be available yet. For example, within these overridden methods, do
    # not use property "user" on the tool or any other object: it has not been
    # set yet. Use, wherever available, parameter "user" instead. Do not use
    # anything requiring security mechanisms: they may not be ready yet (ie,
    # calls to methods like "do" or "search" with secure=True as parameter).

    # Methods starting with an underscore should not be overridden.

    # Part of the login form for choosing the context
    pxOnLogin = Px('''
     <x>:_('login_context')</x>
     <select id="__ac_ctx" name="__ac_ctx"
             var="ctxDefault=ctx.getDefaultContext(tool)">
      <option value="">:_('choose_a_value')</option>
      <option for="opt in ctx.getContexts(tool)" value=":opt[0]"
              selected=":opt[0] == ctxDefault">:opt[1]</option>
     </select>''')

    # Zone where to display (or switch) the context when the user is logged
    pxLogged = Px('''
     <x var="showSwitchOptions=ctx._showSwitchOptions(tool, layout)">
      <x if="showSwitchOptions"
         var2="options,present=ctx._getSwitchOptions(tool);
               selected=guard.authContext or ''">
       <select if="options" class="discreet" onchange="switchContext(this)">
        <!-- Set this option only to be able to select a single option -->
        <option if="not present and (len(options) == 1)"></option>
        <option for="opt in options" value=":opt[0]"
                selected=":opt[0] == selected">:opt[1]</option>
       </select>
      </x>
      <!-- Display the unswitchable authentication context -->
      <x if="not showSwitchOptions and guard.authContext">
       <i>:guard.authContextName</i> 
      </x>
     </x>''',

     js='''
      function switchContext(select) {
        goto(siteUrl + '/tool/AuthContext/switch?ctx=' + select.value) }''')

    def __init__(self, chooseOnLogin=True, noContextPosition='start',
                 homeAfterSwitch=False):
        # Must the user choose its context when logging in ?
        self.chooseOnLogin = chooseOnLogin
        # When choosing a context is not mandatory (see m_isMandatory) and the
        # special entry "no context" can thus be selected, this attribute
        # indicates it must be inserted in the list of available contexts: at
        # the "start" or at the "end". If you want this special entry not to be
        # available at all, set it to None. Indeed, a context may be declared as
        # not mandatory because not selectable when logging in, but, once
        # logged, it may be required to prevent the user from selecting entry
        # "no context".
        self.noContextPosition = noContextPosition
        # Note that chooseOnLogin=False & switchContext=False (see below) is
        # useless.
        # ~~~
        # By default, after switching the context, the user stays on the same
        # page. If you want him to be redirected to its home page, set the
        # following attribute to True.
        self.homeAfterSwitch = homeAfterSwitch

    def _showSwitchOptions(self, tool, layout):
        '''In some situations, switch options are not to be shown'''
        # On some pages, selectors can't be shown
        if layout in noSwitchLayouts: return
        # No switch option if switching is not allowed
        if not self.switchContext(tool): return
        return True

    def _getSwitchOptions(self, tool):
        '''Returns a tuple (options, present), where:
           - "options" is the list of values for the "switch" widget (=the list
             of possible contexts for the user);
           - "present" is a boolean value indicating if the current
             authentication context is in this list.
        '''
        # Get the available contexts
        r = self.getContexts(tool, tool.user) or []
        # Add "no context" switch option when relevant
        if not self.isMandatory(tool) and self.noContextPosition:
            no = ('', tool.translate('everything'))
            if self.noContextPosition == 'end':
                r.append(no)
            else: # 'start'
                r.insert(0, no)
        # Is the current authentication context in this list ?
        ctx = tool.guard.authContext or ''
        if not ctx and not r:
            # We consider the context to be present
            present = True
        else:
            present = False
            for id, name in r:
                if id == ctx:
                    present = True
                    break
        return r, present

    def _maySwitchTo(self, tool, option):
        '''Is p_option a valid option to switch to ?'''
        options, present = self._getSwitchOptions(tool)
        if not options: return
        for id, title in options:
            if id == option: return True

    def _check(self, tool):
        '''Returns True if there is no problem with the current configuration
           related to the authentication context.'''
        # Check that the current context is among the valid switch options
        options, present = self._getSwitchOptions(tool)
        return present

    def _setOnGuard(self, tool, user, guard, ctx):
        '''Set, on the the p_guard, authentication-p_ctx-related attributes'''
        # The authentication context in itself (a short identifier)
        guard.authContext = ctx
        # Its human-readable name
        guard.authContextName = self.getName(tool, user, ctx)
        # The corresponding object, if any
        guard.authObject = self.getObject(tool, user, ctx)

    def isMandatory(self, tool):
        '''When authentication contexts are activated, is the user forced to
           choose one ?'''
        return True

    def switchContext(self, tool):
        '''Is the user allowed to switch context once logged ?'''
        return True

    def getContexts(self, tool, user):
        '''Returns the application-specific authentication contexts, as a list
           of tuples (s_context, s_name). s_context is a short string that
           identifies the context, while s_name is a human-readable name that
           will be shown in the UI.'''

    def getDefaultContext(self, tool, user):
        '''Returns the default context among contexts as returned by
           m_getContexts.'''
        # Does not need to be overridden if there is no default context

    # This method must not be overridden
    def getName(self, tool, user, context):
        '''Returns the name of some given p_context'''
        for ctx, name in self.getContexts(tool, user):
            if ctx == context:
                return name

    def getObject(self, tool, user, context):
        '''If an authentication context corresponds to an object, this method
           must be overridden to return the object corresponding to the given
           p_context. Then, the object is available as attribute "authObject"
           on the guard.'''
        # Overriding this method optimizes performance. Indeed, your object is
        # "loaded" once per request and is available in guard.authObject: you
        # don't need to call o.geObject(context) every time you need to get
        # it.

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                           Class methods
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    traverse['switch'] = 'Authenticated'

    @classmethod
    def switch(class_, tool):
        '''Switches from one authentication context to another'''
        # Check that context switching is allowed
        authContext = tool.config.security.authContext
        req = tool.req
        ctx = req.ctx
        if not authContext or not authContext._maySwitchTo(tool, ctx):
            self.raiseUnauthorized()
        # Perform the switch by updating the authentication cookie and
        # user-related data structures stored on the guard.
        Cookie.update(tool.H(), ctx)
        authContext._setOnGuard(tool, tool.user, tool.guard, ctx)
        # Return to the URL specified in the request, or, by default:
        # a) return to the home page if we were displaying an error message or
        #    if required by the auhentication context;
        # b) else, stay on the same page (=go to the referer page).
        back = req.url
        if not back:
            back = tool.getHomePage() if authContext.homeAfterSwitch \
                                      else tool.referer
        tool.goto(back)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
