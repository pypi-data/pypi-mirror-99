# -*- coding: utf-8 -*-
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
# ------------------------------------------------------------------------------
from DateTime import DateTime
from cStringIO import StringIO
import time, os.path, mimetypes, shutil, base64

from appy.px import Px
from appy import Object
from appy.fields import Field, Layouts
from appy.shared import utils as sutils
from appy.shared import UnmarshalledFile, mimeTypesExts

# ------------------------------------------------------------------------------
WRONG_FILE_TUPLE = 'This is not the way to set a file. You can specify a ' \
    '2-tuple (fileName, fileContent) or a 3-tuple (fileName, fileContent, ' \
    'mimeType).'
CONVERSION_ERROR = 'An error occurred. %s'
RESIZED = '%s resized to %spx.'

def guessMimeType(fileName):
    '''Try to find the MIME type of file p_fileName'''
    return mimetypes.guess_type(fileName)[0] or File.defaultMimeType

def osPathJoin(*pathElems):
    '''Version of os.path.elems that takes care of path elems being empty
       strings.'''
    return os.path.join(*pathElems).rstrip(os.sep)

def getShownSize(size):
    '''Express p_size (a file size in bytes) in a human-readable way'''
    # Display the size in bytes if smaller than 1024 bytes
    if size < 1024: return '%d byte(s)' % size
    size = size / 1024.0 # This is the size, in Kb
    if size < 1024: return '%s Kb' % sutils.formatNumber(size, precision=1)
    size = size / 1024.0 # This is the size, in Mb
    return '%s Mb' % sutils.formatNumber(size, precision=1)

# ------------------------------------------------------------------------------
class FileInfo:
    '''A FileInfo instance holds metadata about a file on the filesystem.

       For every File field, we will store a FileInfo instance in the dabatase;
       the real file will be stored in the Appy/ZODB database-managed
       filesystem.

       This is the primary usage of FileInfo instances. FileInfo instances can
       also be used every time we need to manipulate a file. For example, when
       getting the content of a Pod field, a temporary file may be generated and
       you will get a FileInfo that represents it.
    '''
    BYTES = 50000
    NOT_FOUND = 'File "%s" was not found.'

    def __init__(self, fsPath, inDb=True, uploadName=None):
        '''p_fsPath is the path of the file on disk.
           - If p_inDb is True, this FileInfo will be stored in the database and
             will hold metadata about a File field whose content will lie in the
             database-controlled filesystem. In this case, p_fsPath is the path
             of the file *relative* to the root DB folder. We avoid storing
             absolute paths in order to ease the transfer of databases from one
             place to the other. Moreover, p_fsPath does not include the
             filename, that will be computed later, from the field name.

           - If p_inDb is False, this FileInfo is a simple temporary object
             representing any file on the filesystem (not necessarily in the
             db-controlled filesystem). For instance, it could represent a temp
             file generated from a Pod field in the OS temp folder. In this
             case, p_fsPath is the absolute path to the file, including the
             filename. If you manipulate such a FileInfo instance, please avoid
             using methods that are used by Appy to manipulate
             database-controlled files (like methods getFilePath, removeFile,
             writeFile or copyFile).'''
        self.fsPath = fsPath
        self.fsName = None # The name of the file in fsPath
        self.uploadName = uploadName # The name of the uploaded file
        self.size = 0 # Its size, in bytes
        self.mimeType = None # Its MIME type
        self.modified = None # The last modification date for this file
        # Complete metadata if p_inDb is False. p_inDb is not stored as is:
        # checking if self.fsName is the empty string is equivalent.
        if not inDb:
            self.fsName = '' # Already included in self.fsPath
            self.setAttributes(self.fsPath)

    def setAttributes(self, path):
        '''Compute file attributes (size, MIME type and last modification date)
           for a file whose absolute p_path is passed and store these attributes
           on p_self.'''
        info = os.stat(path)
        self.size = info.st_size
        self.mimeType = guessMimeType(path)
        self.modified = DateTime(info.st_mtime)

    def getFilePath(self, obj):
        '''Returns the absolute file name of the file on disk that corresponds
           to this FileInfo instance.'''
        dbFolder, folder = obj.o.getFsFolder()
        r = osPathJoin(dbFolder, folder, self.fsName)
        if not os.path.exists(r):
            # It may already have been deleted by a failed transaction. Try to
            # get a copy we may have made in the OS temp folder.
            folder = os.path.basename(folder)
            r = osPathJoin(sutils.getOsTempFolder(), folder, self.fsName)
        return r

    def removeFile(self, dbFolder='', removeEmptyFolders=False):
        '''Removes the file from the filesystem.'''
        try:
            os.remove(osPathJoin(dbFolder, self.fsPath, self.fsName))
        except Exception, e:
            # If the current ZODB transaction is re-triggered, the file may
            # already have been deleted.
            pass
        # Don't leave empty folders on disk. So delete folder and parent folders
        # if this removal leaves them empty (unless p_removeEmptyFolders is
        # False).
        if removeEmptyFolders:
            sutils.FolderDeleter.deleteEmpty(osPathJoin(dbFolder,self.fsPath))

    def normalizeFileName(self, name):
        '''Normalizes file p_name.'''
        return name[max(name.rfind('/'), name.rfind('\\'), name.rfind(':'))+1:]

    def getShownSize(self): return getShownSize(self.size)

    def replicateFile(self, src, dest):
        '''p_src and p_dest are open file handlers. This method copies content
           of p_src to p_dest and returns the file size. Note that p_src can
           also be binary data in a string.'''
        size = 0
        if isinstance(src, str): src = StringIO(src)
        while True:
            chunk = src.read(self.BYTES)
            if not chunk: break
            size += len(chunk)
            dest.write(chunk)
        return size

    def getBase64(self, obj=None):
        '''Returns the file content, as a base64-encoded string'''
        if obj:
            filePath = self.getFilePath(obj)
        else:
            filePath = self.fsPath
        f = file(filePath, 'rb')
        res = base64.b64encode(f.read())
        f.close()
        return res

    def getExtension(self):
        '''Get the file extension from the MIME type or from the upload name'''
        if self.mimeType in mimeTypesExts:
            return mimeTypesExts[self.mimeType]
        elif self.uploadName:
            parts = os.path.splitext(self.uploadName)
            if len(parts) > 1:
                return parts[-1][1:]

    def getMimeTypeFromFileUpload(self, fileObj):
        '''Under some unknown circumstances, the MIME type received from Zope
           FileUpload instances is wrong:
           * MIME type of docx and xlsx documents may be wrongly initialised to
             "application/zip";
           * MIME type of some Excel (.xls) files have MIME type
             "application/msword".
           This method corrects it.'''
        mimeType = fileObj.headers.get('content-type')
        ext = os.path.splitext(fileObj.filename)[1]
        # If no extension is there, I cannot correct the MIME type
        if not ext: return mimeType
        # Correct xls files having MIME type "application/msword"
        if (ext == '.xls') and (mimeType == 'application/msword'):
            return 'application/vnd.ms-excel'
        # No error: return the MIME type as computed by Zope
        if not ext or (mimeType != 'application/zip') or (ext == '.zip'):
            return mimeType
        # Correct the wrong MIME type
        ext = ext[1:].lower()
        for mime, extension in mimeTypesExts.iteritems():
            if extension == ext: return mime
        # If we are here, we haven't found the correct MIME type
        return mimeType

    def writeFile(self, fieldName, fileObj, dbFolder):
        '''Writes to the filesystem the p_fileObj file, that can be:
           - a Zope FileUpload (coming from a HTTP post);
           - a OFS.Image.File object (legacy within-ZODB file object);
           - another ("not-in-DB") FileInfo instance;
           - a tuple (fileName, fileContent, mimeType)
             (see doc in method File.store below).'''
        # Determine p_fileObj's type
        fileType = fileObj.__class__.__name__
        # Determine the MIME type and the base name of the file to store
        if fileType == 'FileUpload':
            mimeType = self.getMimeTypeFromFileUpload(fileObj)
            fileName = fileObj.filename
        elif fileType == 'File':
            mimeType = fileObj.content_type
            fileName = fileObj.filename
        elif fileType == 'FileInfo':
            mimeType = fileObj.mimeType
            fileName = fileObj.uploadName
        else:
            mimeType = fileObj[2]
            fileName = fileObj[0]
        self.mimeType = mimeType or File.defaultMimeType
        if not fileName:
            # Name it according to field name. Deduce file extension from the
            # MIME type.
            ext = (self.mimeType in mimeTypesExts) and \
                  mimeTypesExts[self.mimeType] or 'bin'
            fileName = '%s.%s' % (fieldName, ext)
        # As a preamble, extract file metadata from p_fileObj and store it in
        # this FileInfo instance.
        name = self.normalizeFileName(fileName)
        self.uploadName = name
        self.fsName = '%s%s' % (fieldName, os.path.splitext(name)[1].lower())
        # Write the file on disk (and compute/get its size in bytes)
        fsName = osPathJoin(dbFolder, self.fsPath, self.fsName)
        f = file(fsName, 'wb')
        if fileType == 'FileUpload':
            # Write the FileUpload instance on disk
            self.size = self.replicateFile(fileObj, f)
        elif fileType == 'File':
            # Write the File instance on disk
            if fileObj.data.__class__.__name__ == 'Pdata':
                # The file content is splitted in several chunks
                f.write(fileObj.data.data)
                nextPart = fileObj.data.next
                while nextPart:
                    f.write(nextPart.data)
                    nextPart = nextPart.next
            else:
                # Only one chunk
                f.write(fileObj.data)
            self.size = fileObj.size
        elif fileType == 'FileInfo':
            src = file(fileObj.fsPath, 'rb')
            self.size = self.replicateFile(src, f)
            src.close()
        else:
            # Write fileObj[1] on disk
            if fileObj[1].__class__.__name__ == 'file':
                # It is an open file handler
                self.size = self.replicateFile(fileObj[1], f)
            else:
                # We have file content directly in fileObj[1]
                self.size = len(fileObj[1])
                f.write(fileObj[1])
        f.close()
        from DateTime import DateTime
        self.modified = DateTime()

    def copyFile(self, fieldName, filePath, dbFolder):
        '''Copies the "external" file stored at p_filePath in the db-controlled
           file system, for storing a value for p_fieldName.'''
        # Set names for the file
        name = self.normalizeFileName(filePath)
        self.uploadName = name
        self.fsName = '%s%s' % (fieldName, os.path.splitext(name)[1])
        # Set mimeType
        self.mimeType = guessMimeType(filePath)
        # Copy the file
        fsName = osPathJoin(dbFolder, self.fsPath, self.fsName)
        shutil.copyfile(filePath, fsName)
        from DateTime import DateTime
        self.modified = DateTime()
        self.size = os.stat(fsName).st_size

    def writeResponse(self, response, dbFolder='',
                      disposition='attachment', enableCache=False):
        '''Writes this file in the HTTP p_response object.

           For privacy reasons, p_enableCache is disabled by default. This way,
           it cannot be stored in the browser cache. For non-privacy-sensitive
           information (ie, icons), you can enable caching. When enabled, the
           last modification date is returned in the HTTP header: this way, the
           browser will only download it if the cached version is older than the
           last version, according to this date.
        '''
        set = response.setHeader
        # The file may not exist on disk
        fsName = osPathJoin(dbFolder, self.fsPath, self.fsName)
        if not os.path.isfile(fsName):
            # Return a dummy file containing an error message
            msg = self.NOT_FOUND % sutils.normalizeString(self.uploadName)
            set('Content-Type', 'text/plain')
            set('Content-Length', len(msg))
            response.write(msg)
            return
        # Initialise response headers
        set('Content-Type', self.mimeType)
        set('Content-Length', self.size)
        set('Content-Disposition',
            '%s;filename="%s"' % (disposition, self.uploadName))
        # For now, disable byte serving (value "bytes" instead of "none")
        set('Accept-Ranges', 'none')
        if enableCache:
            set('Last-Modified', self.modified.rfc822())
        else:
            set('Cache-Control', 'no-cache, no-store, must-revalidate')
            set('Expires', '0')
        # Write the file in the response
        f = file(fsName, 'rb')
        while True:
            chunk = f.read(self.BYTES)
            if not chunk: break
            response.write(chunk)
        f.close()

    def dump(self, obj, filePath=None, format=None):
        '''Exports this file to disk (outside the db-controlled filesystem).
           The tied Appy p_obj(ect) is required. If p_filePath is specified, it
           is the path name where the file will be dumped; folders mentioned in
           it must exist. If not, the file will be dumped in the OS temp folder.
           The absolute path name of the dumped file is returned. If an error
           occurs, the method returns None. If p_format is specified,
           LibreOffice will be called for converting the dumped file to the
           desired format.'''
        if not filePath:
            filePath = '%s/file%f.%s' % (sutils.getOsTempFolder(), time.time(),
                                         self.fsName)
        # Copies the file to disk
        shutil.copyfile(self.getFilePath(obj), filePath)
        if format:
            # Convert the dumped file using LibreOffice
            out, err = obj.tool.convert(filePath, format)
            # Even if we have an "error" message, it could be a simple warning.
            # So we will continue here and, as a subsequent check for knowing if
            # an error occurred or not, we will test the existence of the
            # converted file (see below).
            os.remove(filePath)
            # Get the name of the converted file
            baseName, ext = os.path.splitext(filePath)
            if (ext == '.%s' % format):
                filePath = '%s.res.%s' % (baseName, format)
            else:
                filePath = '%s.%s' % (baseName, format)
            if not os.path.exists(filePath):
                obj.log(CONVERSION_ERROR % err, type='error')
                return
        return filePath

    def resize(self, folder, width, obj):
        '''Resize this image if it is a resizable image'''
        if self.mimeType not in File.resizableImages: return
        # Get the absolute path to the file on disk
        path = self.getFilePath(obj)
        # Get the width, in pixels, that will be used to resize it
        width = sutils.keepDigits(str(width))
        sutils.convert(path, '-resize %sx%s>' % (width, width))
        obj.log(RESIZED % (path, width))
        # (re)compute p_self's attributes, after resizing
        self.setAttributes(path)

# ------------------------------------------------------------------------------
class File(Field):

    # MIME types for images
    imageMimeTypes = ('image/png', 'image/jpeg', 'image/gif')
    # MIME types for resizable images
    resizableImages = imageMimeTypes

    pxView = pxCell = Px('''
      <x>::field.getDownloadLink(name, zobj, layoutType)</x>''')

    pxEdit = Px('''
     <x var="fName='%s_file' % name">
      <x if="value">:field.pxView</x><br if="value"/>
      <x if="value">
       <!-- Keep the file unchanged -->
       <input type="radio" value="nochange"
              checked=":value and 'checked' or None"
              name=":'%s_delete' % name" id=":'%s_nochange' % name"
              onclick=":'document.getElementById(%s).disabled=true'% q(fName)"/>
       <label lfor=":'%s_nochange' % name">:_('keep_file')</label><br/>
       <!-- Delete the file -->
       <x if="not field.required">
        <input type="radio" value="delete"
               name=":'%s_delete' % name" id=":'%s_delete' % name"
               onclick=":'document.getElementById(%s).disabled=true'%q(fName)"/>
        <label lfor=":'%s_delete' % name">:_('delete_file')</label><br/>
       </x>
       <!-- Replace with a new file -->
       <input type="radio" value=""
              checked=":not value and 'checked' or None"
              name=":'%s_delete' % name" id=":'%s_upload' % name"
              onclick=":'document.getElementById(%s).disabled=false'%q(fName)"/>
       <label lfor=":'%s_upload' % name">:_('replace_file')</label><br/>
      </x>
      <!-- The upload field -->
      <input type="file" name=":fName" id=":fName" style=":field.getStyle()"
             onChange=":field.getJsOnChange()"/>
      <script var="isDisabled=not value and 'false' or 'true'"
             type="text/javascript">:'document.getElementById(%s).disabled=%s'%\
                                     (q(fName), isDisabled)</script></x>''')

    pxSearch = ''

    def __init__(self, validator=None, multiplicity=(0,1), default=None,
      defaultOnEdit=None, show=True, page='main', group=None, layouts=None,
      move=0, specificReadPermission=False, specificWritePermission=False,
      width=None, height=None, inputWidth=None, maxChars=None, colspan=1,
      master=None, masterValue=None, focus=False, historized=False,
      mapping=None, generateLabel=None, label=None, isImage=False,
      downloadAction=None, sdefault='', scolspan=1, swidth=None, sheight=None,
      view=None, cell=None, edit=None, xml=None, translations=None, render=None,
      icon='paperclip', nameStorer=None, resize=False):
        # This boolean is True if the file is an image
        self.isImage = isImage
        # "downloadAction" can be a method called every time the file is
        # downloaded. The method gets, as single arg, the FileInfo instance
        # representing the downloaded file.
        self.downloadAction = downloadAction
        # If "render" is "icon", the file will be rendered as an icon
        # (self.icon) on "buttons" and "result" layouts.
        self.render = render
        # Icon to use when this file is rendered as an icon
        self.icon = icon
        # In "nameStorer", you can specify another field that will store the
        # file name. This field must be a String belonging to the same class as
        # p_self. As soon as, in the UI, a file is selected in p_self's widget,
        # its name will be copied into the nameStorer field, without the
        # extension, only if this latter is not empty.
        self.nameStorer = nameStorer
        # Attribute "width" is used to specify the width of the image or
        # document. The width of the input field allowing to upload the file can
        # be defined in attribute "inputWidth".
        self.inputWidth = inputWidth
        # If attribute "resize" is False (the default), the image will be
        # previewed in the UI with dimensions as defined in attributes "width"
        # and "height", but without being effectively resized. If "resize" is
        # True, when uploading the file, it will be resized to self.width,
        # keeping the width / height ratio.
        self.resize = resize
        # Call the base constructor
        Field.__init__(self, validator, multiplicity, default, defaultOnEdit,
          show, page, group, layouts, move, False, True, None, False,
          specificReadPermission, specificWritePermission, width, height, None,
          colspan, master, masterValue, focus, historized, mapping,
          generateLabel, label, sdefault, scolspan, swidth, sheight, True,
          False, view, cell, edit, xml, translations)

    def getRequestValue(self, obj, requestName=None):
        name = requestName or self.name
        return obj.REQUEST.get('%s_file' % name)

    def getRequestSuffix(self): return '_file'

    def getCopyValue(self, obj):
        '''Create a copy of the FileInfo instance stored for p_obj for this
           field. This copy will contain the absolute path to the file on the
           filesystem. This way, the file may be read independently from p_obj
           (and copied somewhere else).'''
        info = self.getValue(obj)
        if not info: return
        # Create a "not-in-DB", temporary FileInfo
        return FileInfo(info.getFilePath(obj), inDb=False,
                        uploadName=info.uploadName)

    def getDefaultLayouts(self):
        '''Default layouts depend on the field being in a grid or not'''
        return self.inGrid() and Layouts.File.bg or Layouts.File.b

    def isEmptyValue(self, obj, value):
        '''Must p_value be considered as empty?'''
        if value: return
        # If "nochange", the value must not be considered as empty
        if hasattr(obj, 'REQUEST'):
            return obj.REQUEST.get('%s_delete' % self.name) != 'nochange'
        return True

    def getJsOnChange(self):
        '''Gets the JS code for updaing the name storer when defined'''
        storer = self.nameStorer
        if not storer: return ''
        return 'updateFileNameStorer(this, "%s")' % storer.name

    def getStyle(self):
        '''Get the content of the "style" attribute of the "input" tag on the
           "edit" layout for this field.'''
        if self.inputWidth:
            return 'width: %s' % self.inputWidth
        return ''

    def isRenderable(self, layoutType):
        '''A file with 'icon' rendering is potentially renderable everywhere'''
        if self.render == 'icon': return True
        return layoutType != 'buttons'

    def getDownloadLink(self, name, obj, layoutType):
        '''Gets the HTML code for downloading the file p_value as stored in
           field p_name on p_obj.'''
        value = self.getValueIf(obj, name, layoutType)
        # Display an empty value
        if not value: return (layoutType != 'cell') and '-' or ''
        # Get the "file title", derived from the upload name and size
        size = value.getShownSize()
        title = "%s - %s" % (value.uploadName, size)
        # On "edit", simply repeat the file title
        if layoutType == 'edit': return value.uploadName
        # Build the URL for downloading or displaying the file
        url = '%s/download?name=%s' % (obj.absolute_url(), name)
        # For images, display them directly
        if self.isImage:
            # Define a max width when relevant
            if self.width:
                css = ' style="max-width: %s"' % self.width
            else:
                css = ''
            return '<img src="%s" title="%s"%s/>' % (url, title, css)
        # For non-images, display a link for downloading it, as an icon when
        # relevant.
        if self.render == 'icon':
            content = '<img src="%s" title="%s"/>' % \
                      (obj.getTool().getIncludeUrl(self.icon), title)
            # On "view", we have place, so display "title" besides the icon
            suffix = (layoutType == 'view') and title or ''
        else:
            # Display textual information only
            content = title
            suffix = ''
        # Style the suffix
        if suffix: suffix = '<span class="refLink">%s</span>' % suffix
        return '<a href="%s">%s%s</a>' % (url, content, suffix)

    imageExts = ('.jpg', '.jpeg', '.png', '.gif')
    def validateValue(self, obj, value):
        form = obj.REQUEST.form
        action = '%s_delete' % self.name
        if (not value or not value.filename) and form.has_key(action) and \
            not form[action]:
            # If this key is present but empty, it means that the user selected
            # "replace the file with a new one". So in this case he must provide
            # a new file to upload.
            return obj.translate('file_required')
        # Check that, if self.isImage, the uploaded file is really an image
        if value and value.filename and self.isImage:
            ext = os.path.splitext(value.filename)[1].lower()
            if ext not in File.imageExts:
                return obj.translate('image_required')

    defaultMimeType = 'application/octet-stream'
    def store(self, obj, value):
        '''Stores the p_value that represents some file. p_value can be:
           a. an instance of Zope class ZPublisher.HTTPRequest.FileUpload. In
              this case, it is file content coming from a HTTP POST;
           b. an instance of Zope class OFS.Image.File (legacy within-ZODB file
              object);
           c. an instance of appy.shared.UnmarshalledFile. In this case, the
              file comes from a peer Appy site, unmarshalled from XML content
              sent via an HTTP request;
           d. a string. In this case, the string represents the path of a file
              on disk;
           e. a 2-tuple (fileName, fileContent) where:
              - fileName is the name of the file (ie "myFile.odt")
              - fileContent is the binary or textual content of the file or an
                open file handler.
           f. a 3-tuple (fileName, fileContent, mimeType) where
              - fileName and fileContent have the same meaning than above;
              - mimeType is the MIME type of the file.
           g. a FileInfo instance, that must be "not-in-DB", ie, with an
              absolute path in attribute fsPath.
        '''
        zobj = obj.o
        if value:
            # There is a new value to store. Get the folder on disk where to
            # store the new file.
            dbFolder, folder = zobj.getFsFolder(create=True)
            # Remove the previous file if it existed
            info = getattr(obj.aq_base, self.name, None)
            if info:
                # The previous file can be a legacy File object in an old
                # database we are migrating.
                if isinstance(info, FileInfo): info.removeFile(dbFolder)
                else: delattr(obj, self.name)
            # Store the new file. As a preamble, create a FileInfo instance.
            info = FileInfo(folder)
            cfg = zobj.getProductConfig()
            if isinstance(value, cfg.FileUpload) or isinstance(value, cfg.File):
                # Cases a, b
                value.filename = value.filename.replace('/', '-')
                info.writeFile(self.name, value, dbFolder)
            elif isinstance(value, UnmarshalledFile):
                # Case c
                fileInfo = (value.name, value.content, value.mimeType)
                info.writeFile(self.name, fileInfo, dbFolder)
            elif isinstance(value, basestring):
                # Case d
                info.copyFile(self.name, value, dbFolder)
            elif isinstance(value, FileInfo):
                # Case g
                info.writeFile(self.name, value, dbFolder)
            else:
                # Cases e, f. Extract file name, content and MIME type.
                fileName = mimeType = None
                if len(value) == 2:
                    fileName, fileContent = value
                elif len(value) == 3:
                    fileName, fileContent, mimeType = value
                if not fileName:
                    raise Exception(WRONG_FILE_TUPLE)
                mimeType = mimeType or guessMimeType(fileName)
                info.writeFile(self.name, (fileName, fileContent, mimeType),
                               dbFolder)
            # Resize the image when relevant
            if self.resize and self.width: info.resize(folder, self.width, obj)
            # Store the FileInfo instance in the database
            setattr(obj, self.name, info)
        else:
            # I store value "None", excepted if I find in the request the desire
            # to keep the file unchanged.
            action = None
            rq = getattr(zobj, 'REQUEST', None)
            if rq: action = rq.get('%s_delete' % self.name, None)
            if action != 'nochange':
                # Delete the file on disk
                info = getattr(zobj.aq_base, self.name, None)
                if info:
                    info.removeFile(zobj.getDbFolder(), removeEmptyFolders=True)
                # Delete the FileInfo in the DB
                setattr(zobj, self.name, None)

    def onDownload(self, obj, rq):
        '''Triggered when a file download is requested from the ui'''
        # Security check
        obj.mayView(self.readPermission, raiseError=True)
        # Write the file in the HTTP response
        info = getattr(obj.aq_base, self.name, None)
        if info:
            # Content disposition may be given in the request
            disposition = rq.get('disposition', 'attachment')
            if disposition not in ('inline', 'attachment'):
                disposition = 'attachment'
            # Is caching enabled or not ?
            cache = rq.get('cache', '0') == '1'
            info.writeResponse(rq.RESPONSE, obj.getDbFolder(), disposition,
                               enableCache=cache)
            # Call the "download action" if specified
            if self.downloadAction: self.downloadAction(obj.appy(), info)
# ------------------------------------------------------------------------------
