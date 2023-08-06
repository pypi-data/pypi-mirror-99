'''Management of the Appy authentication cookie'''

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
import base64, urllib.parse

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Cookie:
    '''Represents the Appy authentication cookie, carrying user credentials. It
       will be set and read by an Appy app for authenticating a user.'''

    # Name of the Appy authentication cookie
    name = 'AppyAuth'

    @classmethod
    def read(class_, handler, onResponse=False):
        '''Returns the tuple (login, password, ctx) read from the authentication
           cookie read from the request. If no user is logged, its returns
           (None, None, None).'''
        # If p_onResponse, we get the cookie that has already been set on the
        # response, instead of the one coming from the request.
        if not onResponse:
            cookie = handler.req[Cookie.name]
        else:
            cookie = handler.resp.headers['Cookies'][Cookie.name]
        if not cookie: return None, None, None
        unquoted = urllib.parse.unquote(cookie).encode('utf-8')
        cookieValue = base64.decodestring(unquoted).decode('utf-8')
        if ':' not in cookieValue: return None, None, None
        # Extract the context from the cookieValue
        r, context = cookieValue.rsplit(':', 1)
        # Extract login and password
        login, password = r.split(':', 1)
        return login, password, context

    @classmethod
    def write(class_, handler, login, password, ctx=None):
        '''Encode p_login, p_password and p_ctx into the authentication
           cookie.'''
        r = '%s:%s:%s' % (login, password, ctx or '')
        r = base64.encodestring(r.encode('utf-8')).rstrip()
        handler.resp.setCookie(Cookie.name, urllib.parse.quote(r))

    @classmethod
    def update(class_, handler, ctx, onResponse=False):
        '''Updates the authentication context within the Appy authentication
           cookie. If p_onResponse is True, we get the cookie from the response
           headers instead of the request object.'''
        login, password, oldCtx = Cookie.read(handler, onResponse=onResponse)
        if login is None:
            # There is no cookie. When SSO is enabled, cookies are normally not
            # used, excepted if an authentication context comes into play. In
            # that case, the cookie is only used to store this context. In order
            # to represent this fact, set, in the cookie, a special value for
            # the user login:
            #                          _s_s_o_
            #
            # Such a cookie means: "this is a special cookie, only used to store
            # the authentication context. Check SSO to get the user login".
            login = '_s_s_o_'
        Cookie.write(handler, login, password, ctx)

    @classmethod
    def updatePassword(class_, handler, password):
        '''Updates the cookie with a new p_password'''
        login, oldPassword, ctx = Cookie.read(handler)
        Cookie.write(handler, login, password, ctx)

    @classmethod
    def disable(class_, handler):
        '''Disables the authentication cookie'''
        # Do it only if the cookie exists
        if Cookie.name in handler.req:
            handler.resp.setCookie(Cookie.name, 'deleted')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
