'''Utility module related to URL manipulation'''

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
import urllib.parse

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def split(url):
    '''Returns a tuple (url, params), where "url" is p_url whose parameters have
       been removed, and "params" is a dict containing these params, or None if
       there is no param in p_url.'''
    # Extract the various p_url parts
    parsed = urllib.parse.parse(url)
    # Return the URL as-is if it contains no parameter
    if not parsed.query: return url, None
    # Compute the dict of parameters
    r = {}
    for param in parsed.query.split('&'):
        if '=' in param:
            name, value = param.split('=', 1)
            r[name] = value
        else:
            r[name] = None
    # Re-build the URL parts into an URL, but without params
    url = '%s://%s%s' % (parsed.scheme, parsed.netloc, parsed.path)
    return url, r

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def encode(params, ignoreNoneValues=True):
    '''Encode dict of p_params as a string of parameters ready to be
       incorporated into an URL. If p_ignoreNoneValues is True, every entry
       whose value is None is ignored.'''
    if not params: return params
    r = []
    for name, value in params.items():
        # Ignore entries whose value is None when appropriate
        if ignoreNoneValues and (value is None): continue
        # Convert the value to a str if not done yet
        value = value if isinstance(value, str) else str(value)
        # Add the encoded entry to the result
        r.append('%s=%s' % (name, value))
    return '&'.join(r)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
