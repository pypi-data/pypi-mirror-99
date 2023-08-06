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
from io import BytesIO
from http import HTTPStatus
import os.path, time, email.utils, urllib.parse, gzip

from appy.xml import xhtmlPrologue

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
BROKEN_PIPE = 'Broken pipe while serving %s.'
CONN_RESET  = 'Connection reset by peer while serving %s.'
OS_ERROR    = 'OS error (%s) while serving %s.'
RESP_ERR    = '%d - %s'
H_METH_KO   = 'Unsupported HTTP method "%s".'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Response:
    '''Represents the response that will be sent back to the client after having
       received a HTTP request.'''

    # Appy works with UTF-8
    encoding = 'utf-8'
    charset = 'charset=%s' % encoding

    # HTTP headers must be ISO-8859-1
    headersEncoding = 'iso-8859-1'

    # End of lines as written in HTTP responses
    eol = b'\r\n'

    # Types of dynamic responses a Appy server may produce
    types = {'html': 'text/html;%s' % charset,
             'xml' : 'text/xml;%s' % charset,
             'json': 'application/json;%s' % charset}

    # MIME type of files stored on disk, that will be compressed. CSS files are
    # not there, because the Appy server loads it in RAM.
    compressableFiles = {'image/svg+xml': None, 'application/javascript': None}

    # HTTP codes for which responses have no body
    noBodyCodes = (HTTPStatus.NO_CONTENT,
                   HTTPStatus.RESET_CONTENT,
                   HTTPStatus.NOT_MODIFIED)

    # Template error page
    errorTemplate = '''%s
     <html>
      <head><meta http-equiv="Content-Type" content="%s"><title>Error</title>
      </head>
      <body><p>Error code %%d</p></body>
     </html>''' % (xhtmlPrologue, types['html'])

    # When writing large amounts of data on the client socket, packets of BYTES
    # bytes will be written.
    BYTES = 60000

    def __init__(self, handler):
        # A link to the p_handler
        self.handler = handler
        # The HTTP code for the response, as a value of enum http.HTTPStatus
        self.code = HTTPStatus.OK
        # The phrase related to the code. Ie, phrase for code 200 is "OK".
        self.codePhrase = None
        # The message to be returned to the user
        self.message = None
        # Response base headers, returned for any response, be it static or
        # dynamic.
        if handler.fake:
            headers = {}
        else:
            headers = {
              'Server': handler.server.nameForClients,
              'Date': email.utils.formatdate(time.time(), usegmt=True),
              # For now, disable byte serving (value "bytes" instead of "none")
              'Accept-Ranges': 'none'}
        self.headers = headers
        # If the response content type is among Response.types, the
        # corresponding key in this dict is stored here.
        self.contentType = None
        # The HTTP version string
        self.httpVersion = handler.server.config.server.getProtocolString()
        # Has this response already been sent ? It may happen when producing
        # dynamic content whose result is a File.
        self.sent = False

    def setContentType(self, type):
        '''Sets the content type for this response'''
        self.headers['Content-Type'] = Response.types.get(type) or type
        self.contentType = type

    def initDynamic(self, contentType='html'):
        '''Complete p_self's headers with those being specific to a dynamic
           response.'''
        headers = self.headers
        self.setContentType(contentType)
        headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        headers['Expires'] = '0'
        # If it turns out that the dynamic content must be cached (it could
        # happen with File fields with cache=True), keys "Cache-Control" and
        # "Expires" will be removed afterwards.

    def setHeader(self, name, value):
        '''Adds (or replace) a HTTP header among response headers'''
        self.headers[name] = value

    def removeHeader(self, name):
        '''Ensure the header named p_name is absent from response headers'''
        if name in self.headers:
            del(self.headers[name])

    def setCookie(self, name, value):
        '''Adds a cookie among response headers, in special key "Cookies" that
           will be converted to as many "Set-Cookie" HTTP header entries as
           there are entries at this key.

           If p_value is "deleted", the cookie is built in such a way that it
           will be immediately disabled by the browser.'''
        # Create entry "Cookies" in response headers if it does not exist
        if 'Cookies' not in self.headers:
            self.headers['Cookies'] = {}
        # Set the value for the cookie. A special value is defined if the
        # objective is to disable the cookie.
        if value == 'deleted': value = '%s; Max-Age=0' % value
        self.headers['Cookies'][name] = '%s; Path=/' % value

    def deleteCookie(self, name):
        '''Deletes the cookie having this p_name'''
        self.setCookie(name, 'deleted')

    def addMessage(self, message):
        '''Adds a message to p_self.message'''
        if self.message is None:
            self.message = message
        else:
            self.message = '%s<br/>%s' % (self.message, message)

    def goto(self, url=None, message=None):
        '''Redirect the user to p_url'''
        if message: self.addMessage(message)
        self.code = HTTPStatus.SEE_OTHER # 303
        # Redirect to p_url or to the referer URL if no p_url has been given
        self.headers['Location'] = url or self.handler.headers['Referer']

    def write(self, s):
        '''Writes part p_s of the response to the client socket. Returns True if
           an error occurred.'''
        try:
            self.handler.clientSocket.sendall(s)
        except BrokenPipeError:
            self.handler.log('app', 'error', BROKEN_PIPE % self.handler.path)
            return True
        except ConnectionResetError:
            self.handler.log('app', 'error', CONN_RESET % self.handler.path)
            return True
        except OSError as err:
            self.handler.log('app', 'error', OS_ERROR % \
                                             (str(err), self.handler.path))

    def writeFile(self, path):
        '''Writes the file lying on the file system @ path to the client socket.
           Return True if an error occurred.'''
        r = False
        with open(path, 'rb') as f:
            while True:
                chunk = f.read(Response.BYTES)
                if not chunk: break
                error = self.write(chunk)
                if error:
                    r = True
                    break
        return r

    def formatHeaderLine(self, line):
        '''Return p_line as can be written as a response header'''
        r = line.encode(Response.headersEncoding, 'ignore')
        return b'%s%s' % (r, Response.eol)

    def writeHeaders(self):
        '''Writes, to the client socket, the response line and headers'''
        # Define the response line
        phrase = self.codePhrase or self.code.phrase or ''
        line = self.formatHeaderLine
        r = [line('%s %d %s' % (self.httpVersion, self.code, phrase))]
        add = r.append
        # Add HTTP headers
        for name, value in self.headers.items():
            # Manage special key containing cookies
            if name == 'Cookies':
                for key, v in value.items():
                    add(line('Set-Cookie: %s=%s' % (key, v)))
            else:
                # Manage any other key
                add(line('%s: %s' % (name, value)))
        # Terminate with a blank line
        add(Response.eol)
        # Write the complete result to the socket
        self.write(b''.join(r))

    def compress(self, content):
        '''Compresses p_content and add the appropriate response header
           "Content-Encoding". The compressed version of p_content is
           returned.'''
        # It must be compressed
        r = BytesIO()
        with gzip.GzipFile(fileobj=r, mode='wb') as f: f.write(content)
        self.headers['Content-Encoding'] = 'gzip'
        return r.getvalue()

    def prepareContent(self, content, path):
        '''Prepares the response body, that will be made of p_content (being a
           string) or the content of file at this p_path.'''
        # Returns a tuple (p_content, p_path).
        #  * If the file @p_path must be compressed, it will be loaded in
        #    p_content. Else, it will be left as is, and will be written to the
        #    client socket afterwards, by chunks of Response.BYTES bytes.
        #  * p_content will be compressed if being "textual".
        # This method also sets header key "Content-Length" accordingly.
        headers = self.headers
        toCompress = False
        type = headers.get('Content-Type')
        # Convert p_content to bytes if present
        if content:
            content = content.encode(Response.encoding)
        elif path and (type in Response.compressableFiles):
            # Loads the file @ p_path in p_content if it must be compressed
            with open(path, 'rb') as f: content = f.read()
            path = None
            toCompress = True
        # Determine header Content-Length in all cases
        if path:
            length = os.path.getsize(path)
        elif not content:
            # There is no content at all
            length = 0
        else:
            # Compress content when relevant and set header "Content-Length"
            # Compress p_content when appropriate
            if toCompress or \
               (type and (type.startswith('app') or type.startswith('text'))):
                content = self.compress(content)
            length = len(content)
        headers['Content-Length'] = length
        return content, path

    def build(self, content=None, path=None):
        '''Build and sent the response back to the browser'''
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # (a) | p_content is not None:
        #     |
        #     | p_content will be used as response body: it is supposed to be a
        #     | UTF-8 string and will be converted to bytes.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # (b) | p_path is not None:
        #     |
        #     | the content of the file at this (absolute) path will be used as
        #     | response body.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # (c) | p_content is None and p_path is None:
        #     |
        #     | the response will contain no body.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # This response may already have been sent. Do not sent it once more.
        if self.sent: return
        # Add p_self.message as a cookie if present
        handler = self.handler
        if self.message is not None:
            quoted = urllib.parse.quote(self.message)
            self.setCookie('AppyMessage', quoted)
        # Prepare the response content
        content, path = self.prepareContent(content, path)
        # Add key "Connection" when appropriate
        if handler.closeSocket:
            self.headers['Connection'] = 'close'
        # Send response headers
        self.writeHeaders()
        # Send response content when present. Variable "error" will be true if
        # an error occurs while writing the response body to the client socket.
        error = False
        if content: error = self.write(content)
        elif path:  error = self.writeFile(path)
        # Ensure the client socket will be closed if an error occurred
        if error:
            handler.closeSocket = True
        # Note this response as already been sent
        self.sent = True

    def buildError(self, code, message=None):
        '''Updates p_self to represent a HTTP error with this code, build it and
           log it.'''
        self.code = code
        message = message or code.phrase
        handler = self.handler
        # Log the error
        handler.log('app', 'error', RESP_ERR % (code, message))
        # Define a content when relevant
        if (code > 200) and (code not in Response.noBodyCodes):
            content = Response.errorTemplate % code
        else:
            content = None
        # Force the client socket to be closed
        handler.closeSocket = True
        # Build the response
        self.build(content=content)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
