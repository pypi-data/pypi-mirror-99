'''A "request" stores HTTP GET request parameters and/or HTTP POST form
   values.'''

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
import re, urllib.parse

from appy.model.utils import Object

# Entries considered as empty in a multipart message - - - - - - - - - - - - - -
emptyMultiparts = (b'', b'--\r\n')

# Regular expression for parsing a Content-Disposition (cd) directive  - - - - -
cdRex = re.compile(b'name="([^"]+)"(?:.+filename="([^"]*)")?')

# Errors - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
EMPTY_POST = 'No Content-Length header for request with Content-Type "%s".'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Request(Object):
    '''Represents data coming from a HTTP request'''

    @classmethod
    def create(class_, handler):
        '''Analyses various elements from an incoming HTTP request (GET
           parameters, POST form data, cookies) and creates a Request object for
           storing them. If no element is found, an empty Request is created.'''
        # Create the Request instance
        req = Request()
        # Get parameters from a GET request if any
        qs = handler.parsedPath.query
        if qs: req.parse(qs)
        # Get POST form data if any
        contentType = handler.headers['Content-Type']
        if contentType:
            # Get the request length and content
            length = handler.headers['Content-Length']
            if length is None:
                handler.log('app', 'warning', EMPTY_POST % contentType)
                return req
            content = handler.rfile.read(int(length))
            # Several content encodings are possible
            if contentType == 'application/x-www-form-urlencoded':
                # Form elements are encoded in a way similar to GET parameters
                req.parse(content.decode('utf-8'))
            elif contentType.startswith('multipart/form-data'):
                # Form elements are encoded in a "multi-part" message, whose
                # elements are separated by some boundary text.
                boundary = '--' + contentType[contentType.index('boundary=')+9:]
                req.parseMultiPart(content, boundary.encode())
        # Get Cookies
        cookieString = handler.headers['Cookie']
        if cookieString is not None:
            # Cookies' (name, value) pairs are separated by semicolons
            req.parse(cookieString, sep=';')
        return req

    def addValue(self, name, value):
        '''Adds, on this request, an new attribute named p_name with this
           p_value. Manage multiple entries having the same p_name by creating a
           single attribute holding a list of values.'''
        # Ensure any string value is stripped
        name = name.strip()
        # Manage multiple values
        if name in self:
            # Update an existing value
            values = self[name]
            if isinstance(values, list):
                values.append(value)
            else:
                values = [values, value]
            value = values
        self[name] = value

    def parse(self, params, sep='&'):
        '''Parse GET/POST p_param(eters) and add one attribute per parameter'''
        for param in params.split(sep):
            # Every param is of the form <name>=<value> or simply <name>
            if '=' in param:
                # <name>=<value>
                name, value = param.split('=', 1)
                value = urllib.parse.unquote_plus(value)
            else:
                # <name>
                name = param
                value = None
            self.addValue(name, value)

    def parseMultiPart(self, content, boundary):
        '''Parses multi-part form content (bytes) and add to p_self one
           attribute per form element.'''
        for entry in content.split(boundary):
            # Ignore empty entries
            if entry in emptyMultiparts: continue
            # Separate attribute metadata from its value
            metadata, value = entry.split(b'\r\n\r\n', 1)
            # Search the various elements within metadata. For a standard
            # attribute, simply retrieve its name. For a file, also retrieve
            # its MIME type and file name.
            name = fileName = fileType = None
            for part in metadata.split(b'\r\n'):
                if not part: continue # Ignore empty chunks
                if name is None:
                    # "part" contains the directive "Content-Disposition" that
                    # includes the name of the attribute and, if the entry is a
                    # binary file, the name of the file.
                    name, fileName = cdRex.search(part).groups()
                    name = name.decode()
                    if fileName is not None: fileName = fileName.decode()
                elif fileType is None:
                    # "part" contains directive "Content-Type" containing the
                    # file's MIME type.
                    fileType = part.split()[1].decode()
            # Remove trailing space
            value = value[:-2]
            # For a (non empty) file, assemble the name, type and content in an
            # Object instance.
            if fileName and value:
                value = Object(name=fileName, type=fileType, value=value)
            else:
                # Get the value as a string
                value = value.decode()
            # Find the element value
            self.addValue(name, value)

    def patchFromTemplate(self, o):
        '''p_o is a temp object that is going to be edited via px "edit". If a
           template object must be used to pre-fill the web form, patch the
           request with the values retrieved on this template object.'''
        # This has sense only for temporary objects
        if not o.isTemp(): return
        id = self.template
        if not id: return
        template = o.getObject(id)
        # Some fields may be excluded from the copy
        toExclude = o.class_.getCreateExclude(o)
        # Browse fields
        for field in o.getFields('edit'):
            if field.name in toExclude: continue
            field.setRequestValue(template)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
