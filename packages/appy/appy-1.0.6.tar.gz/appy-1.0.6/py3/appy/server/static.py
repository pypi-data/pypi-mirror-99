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
from http import HTTPStatus
import inspect, pathlib, mimetypes, os.path, email.utils, collections

from DateTime import DateTime

import appy
from appy.utils.string import Normalize

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
MAP_VALUE_NOT_PATH = 'Values from the map must be pathlib.Path objects.'
PATH_NOT_FOUND     = 'Path "%s" was not found or is not a folder.'
RAM_ROOT_IN_MAP    = 'Ram root "%s" is also used as key for ' \
                     'appy.server.static.Config.map.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Config:
    '''Configuration options for static content served by the Appy HTTP
       server.'''
    def __init__(self, appPath, root='static'):
        # The root URL for all static content. Defaults to "static". Any static
        # content will be available behind URL starting with <host>:/<root>/...
        self.root = root
        # The following attribute identifies base URLs and their corresponding
        # folders on disk. For example, the entry with key "appy" maps any URL
        # <host>:/<root>/appy/<resource> to the actual <resource> on disk, at
        # /<some>/<path>/<resource>.
        appyPath = pathlib.Path(inspect.getfile(appy)).parent
        map = collections.OrderedDict()
        map['appy'] = appyPath / 'ui' / 'static'
        map[appPath.stem] = appPath / 'static'
        self.map = map
        # The above-mentioned attributes define how to map a URL to a resource
        # on disk. A second mechanism is available, mapping URLs to "RAM"
        # resources, directly loaded in memory as strings. Such RAM resources
        # will be stored in dict Static.ram defined on class Static below.
        # Attribute "ramRoot" hereafter defines the base path, after the
        # "static" part, allowing Appy to distinguish a RAM from a disk
        # resource. It defaults to "ram".
        self.ramRoot = 'ram'
        # Let's illustrate this mechanism with an example. Suppose that:
        # * ramRoot = "ram" ;
        # * the content of appy/ui/static/appy.css is loaded in a string
        #   variable named "appyCss";
        # * dict Static.ram = {'appy.css': appyCss}
        # The content of appy.css will be returned to the browser if request via
        #                  <host>/static/ram/appy.css
        # Beyond being probably a bit more performant than serving files from
        # the disk, this approach's great advantage it to be able to compute, at
        # server startup, the content of resources. The hereabove example was
        # not randomly chosen: Appy CSS files like appy.css are actually
        # template files containing variables that need to be replaced by their
        # actual values, coming from the app's (ui) config.
        # When adding keys in Static.ram, ensure the key is a filename-like
        # name: the MIME type will be deduced from the file extension.

        # Remember the date/time this instance has been created: it will be used
        # as last modification date for RAM resources.
        self.created = DateTime()

    def check(self):
        '''Checks that every entry in p_self.map is valid'''
        for key, path in self.map.items():
            # Paths must be pathlib.Path instances
            if not isinstance(path, pathlib.Path):
                raise Exception(MAP_VALUE_NOT_PATH)
            # Paths must exist and be folders
            if not path.is_dir():
                raise Exception(PATH_NOT_FOUND % path)
        # Ensure the RAM root is not used as key in self.map
        if self.ramRoot in self.map:
            raise Exception(RAM_ROOT_IN_MAP % self.ramRoot)

    def init(self, uiConfig):
        '''Reads all CSS files from all disk locations containing static content
           (in p_self.map) and loads them in Static.ram, after having replaced
           variables with their values from the app's (ui) config.'''
        for path in self.map.values():
            for cssFile in path.glob('*.css'):
                # Read the content of this file
                with cssFile.open('r') as f:
                    cssContent = f.read()
                    # Add it to Static.ram, with variables replaced
                    Static.ram[cssFile.name] = uiConfig.patchCss(cssContent)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Static:
    '''Class responsible for serving static content'''

    # The dict of RAM resources (see doc in class Config hereabove)
    ram = collections.OrderedDict()

    @classmethod
    def notFound(class_, handler, config):
        '''Raise a HTTP 404 error if the resource defined by p_handler.parts was
           not found.'''
        path = '/%s/%s' % (config.root, '/'.join(handler.parts))
        code = HTTPStatus.NOT_FOUND # 404
        handler.log('app', 'error', '%d @ %s' % (code.value, path))
        resp = handler.resp
        resp.code = code
        resp.build()

    @classmethod
    def writeUnchanged(class_, handler):
        '''Returns the ad-hoc response if the file has not changed since the
           last time the browser has downloaded it.'''
        resp = handler.resp
        resp.code = HTTPStatus.NOT_MODIFIED # 304
        resp.build()

    @classmethod
    def write(class_, handler, path, modified, content=None, fileInfo=None,
              disposition='attachment', downloadName=None, enableCache=True):
        '''Serves, to the browser, the content of the file whose path on disk is
           given in p_path or whose content in RAM is given in p_content.'''
        # ~~~
        # If the file @ p_path has not changed since the last time the browser
        # asked it, return an empty response with code 304 "Not Modified". Else,
        # return file content with a code 200 "OK".
        # ~~~
        # If p_path corresponds to a DB-controlled file, his corresponding
        # p_fileInfo is given. In that case, p_disposition will be taken into
        # account. Else, it will be ignored, unless p_downloadName is specified.
        # ~~~
        # For privacy reasons, p_enableCache may be disabled (ie, for
        # potentially sensitive content from File fields). This way, it cannot
        # be stored in the browser cache.
        # ~~~
        browserDate = handler.headers.get('If-Modified-Since')
        modified = fileInfo.modified if fileInfo else modified
        smodified = email.utils.formatdate(modified, usegmt=True) # RFC 822
        if not browserDate or (smodified > browserDate):
            resp = handler.resp
            resp.code = HTTPStatus.OK
            # Identify MIME type
            set = resp.setHeader
            mimeType, encoding = mimetypes.guess_type(path)
            mimeType = mimeType or 'application/octet-stream'
            set('Content-Type', mimeType)
            # Define content disposition
            if fileInfo or downloadName:
                niceName = downloadName or fileInfo.uploadName
                disp = '%s;filename="%s"' % (disposition, niceName)
                set('Content-Disposition', disp)
            # ~~~ Manage caching ~~~
            if enableCache:
                set('Last-Modified', smodified)
                # Ensure there is no the cache-related header
                resp.removeHeader('Cache-Control')
                resp.removeHeader('Expires')
            else:
                set('Cache-Control', 'no-cache, no-store, must-revalidate')
                set('Expires', '0')
            # Write the file content to the socket
            path = None if content else path
            resp.build(content, path)
        else:
            class_.writeUnchanged(handler)

    @classmethod
    def writeFromDisk(class_, handler, path,
                      disposition='attachment', downloadName=None):
        '''Serve a static file from disk, whose path is p_path'''
        # The string version of p_path
        spath = str(path)
        class_.write(handler, spath, os.path.getmtime(spath),
                     disposition=disposition, downloadName=downloadName)

    @classmethod
    def writeFromRam(class_, handler, config):
        '''Serve a static file loaded in RAM, from dict Static.ram'''
        # p_handler.parts contains something starting with ['ram', ...]
        if len(handler.parts) == 1:
            class_.notFound(handler, config)
            return
        # Re-join the splitted path to produce the key allowing to get the file
        # content in Static.ram.
        key = '/'.join(handler.parts[1:])
        # Indeed, Static.ram is a simple (ordered) dict, not a hierachical dict
        # of dicts. Standard Appy resources (like appy.css) stored in Static.ram
        # have keys whose names are simple filename-like keys ("appy.css"). But
        # if you want to reproduce a complete "file hierarchy" in Static.ram by
        # adding path-like information in the key, you can do it. By computing
        # keys like we did hereabove, a URL like:
        #               <host>/static/ram/a/b/c/some.css
        # can be served by defining, in Static.ram, an entry with key
        #                      "a/b/c/some.css"
        content = class_.ram.get(key)
        if content is None:
            class_.notFound(handler, config)
            return
        class_.write(handler, key, config.created, content=content)

    @classmethod
    def get(class_, handler):
        '''Returns the content of the static file whose splitted path is defined
           in p_handler.parts.'''
        # Unwrap the static config
        config = handler.server.config.server.static
        # The currently walked path
        path = None
        # Walk parts
        for part in handler.parts:
            if path is None:
                # We are at the root of the search: "part" must correspond to
                # the RAM root or to a key from config.map.
                if part == config.ramRoot:
                    class_.writeFromRam(handler, config)
                    return
                elif part in config.map:
                    path = config.map[part]
                else:
                    class_.notFound(handler, config)
                    return
            else:
                path = path / part
                if not path.exists():
                    class_.notFound(handler, config)
                    return
        # We have walked the complete path: ensure it is a file
        if not path or not path.is_file():
            return class_.notFound(handler, config)
        # Read the file content and write it in the HTTP response
        class_.writeFromDisk(handler, path)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
