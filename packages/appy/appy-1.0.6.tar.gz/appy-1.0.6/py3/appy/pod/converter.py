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
import sys, os, os.path, re, time
from optparse import OptionParser

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
htmlFilters = {'odt': 'HTML (StarWriter)',
               'ods': 'HTML (StarCalc)',
               'odp': 'impress_html_Export'}

FILE_TYPES = {'odt': 'writer8',
              'ods': 'calc8',
              'odp': 'impress8',
              'htm': htmlFilters, 'html': htmlFilters,
              'rtf': 'Rich Text Format',
              'txt': 'Text',
              'csv': 'Text - txt - csv (StarCalc)',
              'pdf': {'odt': 'writer_pdf_Export',  'ods': 'calc_pdf_Export',
                      'odp': 'impress_pdf_Export', 'htm': 'writer_pdf_Export',
                      'html': 'writer_pdf_Export', 'rtf': 'writer_pdf_Export',
                      'txt': 'writer_pdf_Export', 'csv': 'calc_pdf_Export',
                      'swf': 'draw_pdf_Export', 'doc': 'writer_pdf_Export',
                      'xls': 'calc_pdf_Export', 'ppt': 'impress_pdf_Export',
                      'docx': 'writer_pdf_Export', 'xlsx': 'calc_pdf_Export'
                      },
              'swf': 'impress_flash_Export',
              'doc': 'MS Word 97',
              'xls': 'MS Excel 97',
              'ppt': 'MS PowerPoint 97',
              'docx': 'MS Word 2007 XML',
              'xlsx': 'Calc MS Excel 2007 XML',
}
# Conversion from odt to odt does not make any conversion, but updates indexes
# and linked documents.

# Fields of these types are never replaced with their values
unresolvableFieldTypes = ['com.sun.star.text.TextField.PageNumber']
# Complete names for UNO fields that can be "resolved"
resolvableFieldTypes = {'PageCount': 'com.sun.star.text.TextField.PageCount'}
# Table column modifiers
columnModifiers = ('optimalColumnWidths', 'distributeColumns')
# Constants allowing to access LO's stored configuration
configProvider = 'com.sun.star.configuration.ConfigurationProvider'
configAccess = 'com.sun.star.configuration.ConfigurationAccess'
configUpdateAccess = 'com.sun.star.configuration.ConfigurationUpdateAccess'

# Default options when exporting to CSV
defaultCsvOptions = '59,34,76,1'
# Defaut options when reading a CSV file
defaultCsvLoadOptions = defaultCsvOptions

# Constants and messages - - - - - - - - - - - - - - - - - - - - - - - - - - - -
DOC_NOT_FOUND = '"%s" not found.'
URL_NOT_FOUND = 'Doc URL "%s" is wrong. %s'
INPUT_TYPE_ERROR = 'Wrong input type "%s".'
BAD_RESULT_TYPE = 'Bad result type "%s". Available types are %s.'
CANNOT_WRITE_RESULT = 'I cannot write result "%s". %s'
CONNECT_ERROR = "Couldn't not connect to LibreOffice on port %d. %s"
DEFAULT_SERVER = 'localhost'
DEFAULT_PORT = 2002

HELP_SERVER = 'The server IP or hostname that runs LibreOffice ' \
  '(defaults to "%s").' % DEFAULT_SERVER
HELP_PORT = "The port on which LibreOffice runs (default is %d)." % DEFAULT_PORT
HELP_TEMPLATE = 'The path to a LibreOffice template from which you may ' \
  'import styles.'
MANAGE_COLUMNS = 'Set this option to "True" if you want LibreOffice to %s ' \
  'for all tables included in the document. Alternately, specify a regular ' \
  'expression: only tables whose name match will be processed. And if the ' \
  'expression starts with char "~", only tables not matching it will be ' \
  'processed. WARNING - If, for some table, columns are both required to be ' \
  'optimized (parameter "optimalColumnWidths") and distributed (parameter ' \
  '"distributeColumns", only optimization will take place.'
HELP_OPTIMAL_COLUMN_WIDTHS = MANAGE_COLUMNS % 'optimize column widths'
HELP_DISTRIBUTE_COLUMNS = MANAGE_COLUMNS % 'distribute columns evenly'
HELP_SCRIPT = 'You can specify here (the absolute path to) a Python script ' \
  'containing functions that the converter will call in order to customize ' \
  'the process of manipulating the document via the LibreOffice UNO ' \
  'interface. The following functions can be defined in your script and must ' \
  'all accept a single parameter: the Converter instance. ' \
  '***updateTableOfContents***, if defined, will be called for producing a ' \
  'custom table of contents. At the time this function is called by the ' \
  'converter, converter.toc will contain the table of contents, already ' \
  'updated by LibreOffice. ***finalize*** will be called at the end of the '\
  'process, just before saving the result.'
HELP_VERBOSE = 'Writes more information on stdout.'
HELP_PPP = 'Enable the POD post-processor (PPP). The PPP is a series of UNO ' \
  'commands that react to PPP instructions encoded within object names and ' \
  'must be executed at the end of the process, when all other tasks have ' \
  'been performed on the document, just before converting it to another ' \
  'format or saving it to disk or as a stream.'
HELP_STREAM = 'By default (stream = "auto"), if you specify "localhost" as ' \
  'server running LibreOffice, the converter and LibreOffice will exchange ' \
  'the input and result files via the disk. If you specify anything else, ' \
  'the converter will consider that LibreOffice runs on a distant server: ' \
  'input and result files will be carried as streams via the network. If you ' \
  'want to bypass this logic and force exchange as streams or files on disk, ' \
  'set this option to "True" for stream or "False" for disk. You may also ' \
  'specify "in" (the input file is streamed and the result is written on ' \
  'disk) or "out" (the input file is read on disk and the result is streamed).'
HELP_PAGE_START = "Specify an integer number different from 1 and the " \
  "produced document's page numbering will start at this number."
HELP_RESOLVE_FIELDS = 'Set this option to "True" if you want LibreOffice to ' \
  'replace the content of fields by their values. It can be useful, for ' \
  'instance, if the POD result must be included in another document, but the ' \
  'total number of pages must be kept as is. Set this option to "PageCount" ' \
  'instead of "True" to update this field only. Note that field "PageNumber" ' \
  'is never resolved, whatever the value of the option, because its value is ' \
  'different from one page to another.'
HELP_PDF_URL = 'https://wiki.openoffice.org/wiki/API/Tutorials/PDF_export'
HELP_PDF = 'If the output format is PDF, you can define here conversion ' \
  'options, as a series of comma-separated key=value pairs, as in ' \
  '"ExportNotes=True,PageRange=1-20". Available options are documented in ' \
  '%s.' % HELP_PDF_URL
HELP_CSV_URL = 'https://wiki.openoffice.org/wiki/Documentation/DevGuide/' \
  'Spreadsheets/Filter_Options#Filter_Options_for_the_CSV_Filter'
HELP_CSV = 'If the ouput format is CSV, you can define here conversion ' \
  'options, as a comma-separated list of values. Default options are: %s.' \
  'Values correspond to ASCII codes. The first one represents the field ' \
  'separator. The most frequent values are: 59 (the semi-colon ;), 44 (the ' \
  'comma ,) and 9 (a tab). The second value represents the text delimiter. ' \
  'The most frequent values are: 34 (double quotes), 39 (single quotes) or ' \
  'no value at all (as in 59,,76,1). The third one is the file encoding. The ' \
  'most frequent values are 76 (UTF-8) and 12 (ISO-8859-1). Complete ' \
  'documentation about CSV options can be found at %s.' % \
  (defaultCsvOptions, HELP_CSV_URL)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Classes defined here are used to contact LibreOffice via input/output streams
# instead of via the file system. In use when Libreoffice runs on a distant
# server (converter.server is not "localhost").
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
try: # UNO may not be there
    import uno
    from unohelper import Base
    from com.sun.star.io import XInputStream, XOutputStream, XSeekable

    class InputStream(Base, XInputStream, XSeekable):
        def __init__(self, path):
            self.stream = open(path, 'rb')
            self.stream.seek(0, os.SEEK_END)
            self.size = self.stream.tell()
        def readBytes(self, retSeq, nByteCount):
            retSeq = self.stream.read(nByteCount)
            return (len(retSeq), uno.ByteSequence(retSeq))
        def readSomeBytes(self, foo, n):
            return self.readBytes(foo, n)
        def skipBytes(self, n):
            self.stream.seek(n, 1)
        def available(self):
            return self.size - self.stream.tell()
        def closeInput(self):
            self.stream.close()
        def seek(self, posn):
            self.stream.seek(int(posn))
        def getPosition(self):
            return self.stream.tell()
        def getLength(self):
            return self.size

    class OutputStream(Base, XOutputStream):
        def __init__(self, path):
            self.closed = 0
            self.stream = open(path, 'wb')
        def closeOutput(self):
            self.closed = 1
            self.stream.close()
        def writeBytes(self, seq):
            self.stream.write(seq.value)
        def flush(self):
            pass
except ImportError:
    pass

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class LoIter:
    '''Iterates over a collection of LibreOffice-UNO objects'''
    def __init__(self, collection, log=None, reverse=False):
        self.collection = collection
        self.count = collection.getCount()
        # Log the number of walked elements when relevant
        if log: log(self.count, cr=False)
        self.reverse = reverse
        if reverse:
            self.i = self.count - 1
        else:
            self.i = 0
        from com.sun.star.lang import IndexOutOfBoundsException
        self.error = IndexOutOfBoundsException

    def __iter__(self): return self

    def __next__(self):
        try:
            elem = self.collection.getByIndex(self.i)
            if self.reverse: self.i -= 1
            else: self.i += 1
            return elem
        except self.error:
            # IndexOutOfBoundsException can be raised because sometimes UNO
            # returns a number higher than the real number of elements. This is
            # because, in documents including sub-documents, it also counts the
            # sections that are present within these sub-documents.
            raise StopIteration

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class PPP:
    '''This class represents the POD post-processor (=PPP), a series of UNO
       commands that execute instructions inlaid within element names.'''

    def __init__(self, doc):
        # The document currently opened within LO
        self.doc = doc

    def updateTables(self):
        '''When a table name has a suffix between brackets, it means that some
           rows must be removed. This method performs these removals.'''
        for table in LoIter(self.doc.getTextTables()):
            name = table.Name
            # Ignore irrelevant tables
            if '(' not in name: continue
            rows = table.getRows()
            count = rows.getCount()
            # Extract the "slice"
            slice = name[name.index('(')+1 : name.index(')')]
            if slice.startswith(':'):
                # Keep the starting rows, until "i" (delete ending rows)
                i = int(slice[1:])
                rows.removeByIndex(i, count - i)
            else:
                # Keep the ending rows, from "i" (delete starting rows)
                i = int(slice[:-1])
                rows.removeByIndex(0, i)

    def run(self):
        '''Find and execute all post-processing commands'''
        self.updateTables()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class PdfOptions:
    # Some PDF options' values must be converted
    values = {'true': True, 'True': True, 'false': False, 'False': False}

    @classmethod
    def get(class_, options):
        '''Get and convert PDF options to a dict'''
        if not options: return
        r = {}
        for option in options.split(','):
            if not option: continue
            elems = option.split('=')
            if len(elems) != 2: continue
            key, value = elems
            if not key or not value: continue
            # Convert value when relevant
            if value in class_.values:
                value = class_.values[value]
            elif value.isdigit():
                value = int(value)
            # Add the final value to the result
            r[key] = value
        return r

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Converter:
    '''Converts a document readable by LibreOffice into pdf, doc, txt, rtf...'''

    # Converter-specific error class
    class Error(Exception): pass

    def __init__(self, docPath, result, server=DEFAULT_SERVER,
                 port=DEFAULT_PORT, templatePath=None, optimalColumnWidths=None,
                 distributeColumns=None, script=None, resolveFields=False,
                 pdfOptions=None, csvOptions=defaultCsvOptions, ppp=False,
                 stream='auto', pageStart=1, verbose=False):
        # The server and port where LibreOffice listens
        self.server = server
        self.port = port
        # The path to the document to convert
        self.docUrl, self.docPath = self.getFilePath(docPath)
        self.inputType = self.getInputType(docPath)
        # "resultType" determines the type of the converted file (=a file
        # extension among FILE_TYPES keys). "resultMultiple" is True if several
        # result files will be produced (like when producing one CSV file for
        # every sheet from an Excel file).
        self.resultType, self.resultMultiple = self.getResultType(result)
        self.resultFilter = self.getResultFilter()
        self.resultUrl = self.getResultUrl(result)
        # LibreOffice (LO) run-time objects
        self.context = None # The LO context
        self.oo = None # The LO application object
        self.doc = None # The document that will be loaded in LO
        self.toc = None # The table of contents, if existing
        # LO version, as a string
        self.version = None
        # The path to a LO template (ie, a ".ott" file) from which styles can be
        # imported.
        self.templateUrl = self.templatePath = None
        if templatePath:
            self.templateUrl, self.templatePath = self.getFilePath(templatePath)
        # Actions to perform on table columns
        # ~~~ Optimal column widths ~~~
        self.optimalColumnWidths = optimalColumnWidths
        # ~~~ Distribute columns evenly ~~~
        self.distributeColumns = distributeColumns
        # ~~~ Must we perform one of the above actions on table columns ? ~~~
        self.processColumns = optimalColumnWidths or distributeColumns
        # Must we replace fields with their values ?
        self.resolveFields = resolveFields
        # Functions extracted from the custom Python script that will be called
        # by the Converter for customizing the result.
        if script:
            self.functions = self.getCustomFunctions(script)
        else:
            self.functions = {}
        # Options for conversion to PDF
        self.pdfOptions = PdfOptions().get(pdfOptions)
        # Options for conversion to CSV
        self.csvOptions = csvOptions
        # Verbosity
        self.verbose = verbose
        # Enable the PPP (POD post-processor) ?
        self.ppp = ppp
        # Exchange template and result with LibreOffice via streams or files
        # on disk ?
        self.stream = stream
        # At what page number must the produced document start ?
        self.pageStart = pageStart

    def log(self, msg, cr=True):
        '''Logs some p_msg if we are in verbose mode'''
        if not self.verbose: return
        if not isinstance(msg, str): msg = str(msg)
        sys.stdout.write(msg)
        if cr:
            sys.stdout.write('\n')

    def getInputType(self, docPath):
        '''Extracts the input type from the p_docPath'''
        res = os.path.splitext(docPath)[1][1:].lower()
        if res not in FILE_TYPES: raise self.Error(INPUT_TYPE_ERROR % res)
        return res

    def getResultType(self, result):
        '''p_result can be the aobsolute path to the result to produce or only a
           file extension indicating the format of the file to produce. This
           method returns this format.'''
        if '.' in result:
            # We have a complete path
            r = os.path.splitext(result)[-1][1:]
        else:
            r = result
        # If result type ends with char '*', it means that several output files
        # will be produced, ie for getting a CSV file from every Excel or Calc
        # sheet.
        if r.endswith('*'): return r[:-1], True
        return r, False

    def getCustomFunctions(self, script):
        '''Compiles and executes the Python p_script and returns a dict
           containing its namespace.'''
        f = open(script)
        content = f.read()
        f.close()
        names = {}
        exec(compile(content, script, 'exec'), names)
        return names

    def getFilePath(self, filePath):
        '''Returns the absolute path of p_filePath. In fact, it returns a
           tuple with some URL version of the path for LO as the first element
           and the absolute path as the second element.''' 
        import unohelper
        if not os.path.exists(filePath) and not os.path.isfile(filePath):
            raise self.Error(DOC_NOT_FOUND % filePath)
        docAbsPath = os.path.abspath(filePath)
        # Return one path for OO, one path for me
        return unohelper.systemPathToFileUrl(docAbsPath), docAbsPath

    def getResultFilter(self):
        '''Based on the result type, identifies which OO filter to use for the
           document conversion.'''
        if self.resultType in FILE_TYPES:
            res = FILE_TYPES[self.resultType]
            if isinstance(res, dict):
                res = res[self.inputType]
        else:
            raise self.Error(BAD_RESULT_TYPE % (self.resultType,
                                                FILE_TYPES.keys()))
        return res

    def getResultUrl(self, result):
        '''Returns the path of the result file in the format needed by LO. If
           p_result is a file path, it will be used as base. Else, it is a file
           extension (=the "result type"): computing the complete path will be
           done as follows.

           If the result type and the input type are the same (ie the user wants
           to refresh indexes or some other action and not perform a real
           conversion), the result file will be named
                           <inputFileName>.res.<resultType>

           Else, the result file will be named like the input file but with a
           different extension:
                           <inputFileName>.<resultType>
        '''
        import unohelper
        if '.' in result:
            # It is a full path
            r = result
        else:
            # Name the result based on the input file
            baseName = os.path.splitext(self.docPath)[0]
            if self.resultType != self.inputType:
                r = '%s.%s' % (baseName, self.resultType)
            else:
                r = '%s.res.%s' % (baseName, self.resultType)
        try:
            f = open(r, 'w')
            f.write('Hello')
            f.close()
            os.remove(r)
            return unohelper.systemPathToFileUrl(r)
        except (OSError, IOError) as e:
            raise self.Error(CANNOT_WRITE_RESULT % (r, e))

    def props(self, properties):
        '''Create a UNO-compliant tuple of properties, from tuple p_properties
           containing sub-tuples (s_propertyName, value).'''
        from com.sun.star.beans import PropertyValue
        res = []
        for name, value in properties:
            prop = PropertyValue()
            prop.Name = name
            prop.Value = value
            res.append(prop)
        return tuple(res)

    def getConfig(self, path, update=False):
        '''Returns a node within the LO configuration, stored at p_path. If the
           objective is to update it, set p_update to True.'''
        provider = self.context.ServiceManager.createInstance(configProvider)
        prop = self.props((('nodepath', path),))
        access = update and configUpdateAccess or configAccess
        return provider.createInstanceWithArguments(access, prop)

    def getVersion(self):
        '''Returns the LO version'''
        try:
            path = '/org.openoffice.Setup/Product'
            return self.getConfig(path).getByName('ooSetupVersion')
        except Exception:
            # LibreOffice 3 raises an exception here
            return '3.0'

    def connect(self):
        '''Connects to LibreOffice'''
        if os.name == 'nt':
            import socket
        import uno
        from com.sun.star.connection import NoConnectException
        try:
            # Get the uno component context from the PyUNO runtime
            self.context = ctx = uno.getComponentContext()
            # Get the LO version
            self.version = self.getVersion()
            # Create the UnoUrlResolver
            create = ctx.ServiceManager.createInstanceWithContext
            resolver = create('com.sun.star.bridge.UnoUrlResolver', ctx)
            # Connect to LO running on self.port
            docContext = resolver.resolve(
              'uno:socket,host=%s,port=%d;urp;StarOffice.ComponentContext' % \
              (self.server, self.port))
            # Is seems that we can't define a timeout for this method. This
            # would be useful because when a non-LO server already listens
            # to self.port, this method blocks.
            self.log('Getting the UNO-LO instance...', cr=False)
            self.oo = docContext.ServiceManager.createInstanceWithContext(
                'com.sun.star.frame.Desktop', docContext)
            # If we must process table column widths, create a dispatch helper
            if self.processColumns:
                helper = create('com.sun.star.frame.DispatchHelper', ctx)
                self.dispatchHelper = helper
            self.log(' done.')
        except NoConnectException as e:
            raise self.Error(CONNECT_ERROR % (self.port, e))

    def getColumnModifiers(self):
        '''Returns the elements allowing to know if we must optimize or
           distribute table columns.'''
        r = []
        add = r.append
        for name in columnModifiers:
            value = getattr(self, name)
            if isinstance(value, bool):
                # Action must be performed on all tables or no table at all
                add(value); add(None)
            elif value:
                # Action must be performed on tables whose name match or not
                # some regular expression
                if value.startswith('~'):
                    value = value[1:]
                    vNot = True
                else:
                    vNot = False
                add(re.compile(value)); add(vNot)
            else:
                add(False); add(None)
        return r

    def processTableColumns(self, table, viewCursor, frame,
                            optimize, distribute):
        '''Process column widths for this p_table: either p_optimize them or
           p_distribute them evenly (one of these 2 params must be True). Note
           that:
           * the "optimize" algorithm dos not work properly in all cases, unless
             algorithm "distribute" is executed beforehand. So, in short:
                      optimize = distribute + optimize
           * if both p_optimize and p_distribute are specified, the p_optimize
             operation will be performed and will produce the final result.
             Indeed, even if a "distribute" preamble operation is performed, it
             will not be the final result.
        '''
        cursor = table.getCellByName('A1').createTextCursor()
        viewCursor.gotoRange(cursor, False)
        viewCursor.gotoEnd(True)
        viewCursor.gotoEnd(True)
        do = self.dispatchHelper.executeDispatch
        # Perform the "distribute" operation in all cases
        do(frame, '.uno:DistributeColumns', '', 0, ())
        # Perform the "optimize" operation when relevant
        if optimize:
            # With LibreOffice < 5, range selection must be done again
            if self.version < '5.0':
                viewCursor.gotoRange(cursor, False)
                viewCursor.gotoEnd(True)
                viewCursor.gotoEnd(True)
            do(frame, '.uno:SetOptimalColumnWidth', '', 0, ())

    def updateToc(self):
        '''Update the table of contents within the ODT document (if any)'''
        if self.toc is None: return
        self.toc.update()
        # Call custom code to update the TOC when relevant
        fun = self.functions.get('updateTableOfContents')
        if fun: fun(self)

    def mustStream(self, direction):
        '''Must the template and result files be exchanged between the converter
           and LibreOffice as streams over the network or files on disk ?'''
        stream = self.stream
        if stream == 'auto':
            # By default, use streams when LibreOffice runs on a distant
            # server = when the server is not "localhost".
            return self.server != 'localhost'
        elif stream in ('in', 'out'):
            # Stream only in the indicated direction
            return direction == stream
        else:
            # Streaming or not has been forced
            return stream

    def mustBeResolved(self, field):
        '''Must this p_field be replaced with its content ?'''
        # Check that this field is not among unresolvable field types
        for name in unresolvableFieldTypes:
            if field.supportsService(name):
                return
        resolve = self.resolveFields
        if isinstance(resolve, str):
            # We must resolve only fields of a given type
            name = resolvableFieldTypes.get(resolve)
            if not name: return
            return field.supportsService(name)
        else:
            return resolve

    def setPageStart(self):
        '''Sets, for the produced document, a page start different from 1, as
           specified in self.pageStart.'''
        text = self.doc.getText()
        textCursor = text.createTextCursor()
        textCursor.gotoEndOfParagraph(False)
        textCursor.BreakType = 'PAGE_BEFORE'
        textCursor.PageDescName = 'Standard'
        textCursor.PageNumberOffset = self.pageStart

    def updateOdtDocument(self):
        '''If the input file is an ODT document, we will perform those tasks:
           1) update all indexes;
           2) update sections (if sections refer to external content, we try to
              include the content within the result file);
           3) update table column's widths when relevant;
           4) load styles from an external template if given;
           5) execute PPP commands when relevant.
        '''
        log = self.log
        # The produced document may start at a page number which is not 1
        if self.pageStart != 1: self.setPageStart()
        # Getting some base LO objects is required
        controller = self.doc.getCurrentController()
        viewCursor = controller.getViewCursor()
        # The following lines of code were a trial to force LO to load big
        # documents in their entirery: because, with some early LO 6.x versions,
        # it could happen that resulting PDF results were truncated. But in some
        # rare cases, those lines caused LO to run 100% CPU in an infinite loop.
        # ~~~
        # viewCursor.jumpToLastPage()
        # viewCursor.jumpToEndOfPage()
        # ~~~
        # 1) Update indexes
        for index in LoIter(self.doc.getDocumentIndexes(), log):
            if index.ServiceName == 'com.sun.star.text.ContentIndex':
                # Update the TOC later, after any other action that may still
                # produce changes in page numbers.
                self.toc = index
            else:
                index.update()
        log(' index(es) updated.')
        # 2) Resolve (some) text fields when relevant
        if self.resolveFields:
            for field in self.doc.TextFields:
                # Ignore fields that must not be resolved
                if not self.mustBeResolved(field): continue
                anchor = field.getAnchor()
                cursor = anchor.getText().createTextCursorByRange(anchor)
                cursor.setString(cursor.getString())
            log(' field(s) updated.')
        # 3) Update sections
        self.doc.updateLinks()
        for section in LoIter(self.doc.getTextSections(), log, reverse=True):
            # I must walk into the section from last one to the first one. Else,
            # when "disposing" sections, I remove sections and the remaining
            # ones get another index.
            if section.FileLink and section.FileLink.FileURL:
                # This call removes the <section></section> tags without
                # removing the content of the section. Else, it won't appear.
                section.dispose()
        log(' section(s) updated.')
        # 4) Update tables
        count = 0
        if self.processColumns:
            optimize, oNot, distribute, dNot = self.getColumnModifiers()
            # Browse tables
            frame = controller.getFrame()
            for table in LoIter(self.doc.getTextTables()):
                # Must columns be optimized or distributed for this table ?
                opt = optimize
                if not isinstance(opt, bool):
                    opt = opt.match(table.Name)
                    if oNot: opt = not opt
                dis = distribute
                if not isinstance(dis, bool):
                    dis = dis.match(table.Name)
                    if dNot: dis = not dis
                if opt or dis:
                    self.processTableColumns(table, viewCursor, frame, opt, dis)
                    count += 1
        log('%d table(s) with optimized widths.' % count)
        # 5) Import styles from an external file when required
        if self.templateUrl:
            params = self.props((('OverwriteStyles', True),
                                 ('LoadPageStyles', False)))
            self.doc.StyleFamilies.loadStylesFromURL(self.templateUrl, params)
            log('Styles loaded from %s.' % self.templateUrl)
        # 6) Execute PPP commands when relevant
        if self.ppp:
            PPP(self.doc).run()

    def loadDocument(self, fileUrl, props):
        '''Loads the document in LO, either as a file or as a stream and returns
           a pointer to it.'''
        if self.mustStream('in'):
            # Create an input stream
            stream = InputStream(fileUrl[7:]) # Remove the leading "file://"
            # Add, among p_props, a new property with the input stream
            props = self.props((('InputStream', stream),)) + props
            # Specify that the stream must be read instead of p_fileUrl
            fileUrl = 'private:stream'
        return self.oo.loadComponentFromURL(fileUrl, "_blank", 0, props)

    def storeDocument(self, resultUrl, doc, props):
        '''Saves the result, either by dumping the result on disk or by
           receiving it from LO as a stream from the network.'''
        if self.mustStream('out'):
            # Create an output stream
            output = OutputStream(resultUrl[7:]) # Remove the leading "file://"
            # Add, among p_props, a new property with the output stream
            props = self.props((('OutputStream', output),)) + props
            # Specify that the stream must be written instead of p_resultUrl
            resultUrl = 'private:stream'
        doc.storeToURL(resultUrl, props)

    def openDocument(self):
        from com.sun.star.lang import IllegalArgumentException
        try:
            # Loads the document to convert in a new hidden frame
            self.log('Loading in LO file %s...' % self.docUrl, cr=False)
            props = [('Hidden', True)]
            if self.inputType == 'csv':
                # Give some additional params if we need to open a CSV file
                props.append(('FilterFlags', defaultCsvLoadOptions))
            self.doc = self.loadDocument(self.docUrl, self.props(props))
            self.log(' done.')
            # [ODT] Perform additional tasks
            isOdt = self.inputType == 'odt'
            if isOdt: self.updateOdtDocument()
            try:
                self.doc.refresh()
            except AttributeError:
                pass
            # [ODT] After every change has been applied, refresh the TOC
            if isOdt: self.updateToc()
        except IllegalArgumentException as e:
            raise self.Error(URL_NOT_FOUND % (self.docPath, e))

    def setPdfOptions(self):
        '''If p_self.doc must be converted to PDF, and PDF options need to be
           applied, a data structure containing these options is r_eturned.'''
        if not self.pdfOptions: return
        import uno
        # Available PDF options are documented @HELP_PDF_URL (see above)
        r = self.props(self.pdfOptions.items())
        return uno.Any("[]com.sun.star.beans.PropertyValue", r)
        # Getting the LO's PDF configuration to update it does not work (tested
        # with LO 5.3).
        #path = '/org.openoffice.Office.Common/Filter/PDF/Export/'
        #config = self.getConfig(path, update=True)
        #config.setPropertyValue('ExportNotes', True)
        # Or: config.ExportNotes = True
        #config.commitChanges()

    def convertDocument(self):
        '''Calls LO to perform a document conversion. Note that the conversion
           is not really done if the source and target documents have the same
           type.'''
        self.log('Saving the result in %s...' % self.resultUrl, cr=False)
        props = [('FilterName', self.resultFilter), ('UpdateDocMode', 3)]
        if self.resultType == 'csv':
            # Add options for CSV export
            props.append(('FilterOptions', self.csvOptions))
        elif self.resultType == 'pdf':
            # Get optional PDF options
            options = self.setPdfOptions()
            if options:
                props.append(('FilterData', options))
        if not self.resultMultiple:
            self.storeDocument(self.resultUrl, self.doc, self.props(props))
            self.log(' done.')
        else:
            # Dump one CSV file for every sheet in the input document
            import unicodedata
            doc = self.doc
            sheets = self.doc.getSheets()
            sheetsCount = sheets.getCount()
            controller = doc.getCurrentController()
            props = self.props(props)
            for i in range(sheetsCount):
                sheet = sheets.getByIndex(i)
                # Compute the csv output file name
                name = unicodedata.normalize('NFKD', sheet.getName())
                splitted = os.path.splitext(self.resultUrl)
                resultUrl = '%s.%s%s' % (splitted[0], name, splitted[1])
                controller.setActiveSheet(sheet)
                self.storeDocument(resultUrl, doc, props)

    def run(self):
        '''Connects to LO, does the job and disconnects'''
        if self.verbose: start = time.time()
        self.connect()
        self.openDocument()
        # Call custom code to modify the document when relevant
        fun = self.functions.get('finalize')
        if fun: fun(self)
        # Store the (converted) result
        self.convertDocument()
        self.doc.close(True)
        if self.verbose:
            self.log('Done in %.2f second(s).' % (time.time() - start))

# ConverterScript constants  - - - - - - - - - - - - - - - - - - - - - - - - - -
WRONG_NB_OF_ARGS = 'Wrong number of arguments.'
ERROR_CODE = 1
usage = '''usage: python3 converter.py fileToConvert output [options]

   "fileToConvert" is the absolute or relative pathname of the file you
   want to convert (or whose content like indexes need to be refreshed)
   
   "output" can be the output format, that must be one of: %s
            or can be the absolute path to the result file, whose extension must
            correspond to a valid output format.

   "python" should be a UNO-enabled Python interpreter (ie the one which is
   included in the LibreOffice distribution).''' % str(FILE_TYPES.keys())

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class ConverterScript:
    '''The command-line program'''

    def run(self):
        optParser = OptionParser(usage=usage)
        add = optParser.add_option
        add('-e', '--server', dest='server', default=DEFAULT_SERVER,
            metavar='SERVER', type='string', help=HELP_SERVER)
        add('-p', '--port', dest='port', default=DEFAULT_PORT,
            metavar='PORT', type='int', help=HELP_PORT)
        add('-t', '--template', dest='template', default=None,
            metavar='TEMPLATE', type='string', help=HELP_TEMPLATE)
        add('-o', '--optimalColumnWidths', dest='optimalColumnWidths',
            default=None, metavar='OPTIMAL_COL_WIDTHS', type='string',
            help=HELP_OPTIMAL_COLUMN_WIDTHS)
        add('-d', '--distributeColumns', dest='distributeColumns',
            default=None, metavar='DISTRIBUTE_COLUMNS', type='string',
            help=HELP_DISTRIBUTE_COLUMNS)
        add('-r', '--resolveFields', dest='resolveFields', default=None,
            metavar='RESOLVE_FIELDS', type='string', help=HELP_RESOLVE_FIELDS)
        add('-s', '--script', dest='script', default=None, metavar='SCRIPT',
            type='string', help=HELP_SCRIPT)
        add('-v', '--verbose', action='store_true', help=HELP_VERBOSE)
        add('-f', '--pdf', dest='pdf', default=None, metavar='PDF_OPTIONS',
            type='string', help=HELP_PDF)
        add('-i', '--csv', dest='csv', default=defaultCsvOptions,
            metavar='CSV_OPTIONS', type='string', help=HELP_CSV)
        add('-c', '--ppp', action='store_true', help=HELP_PPP)
        add('-a', '--stream', dest='stream', default='auto',
            metavar='STREAM', type='string', help=HELP_STREAM)
        add('-g', '--pageStart', dest='pageStart', default=1,
            metavar='PAGESTART', type='int', help=HELP_PAGE_START)
        options, args = optParser.parse_args()
        if len(args) != 2:
            sys.stderr.write(WRONG_NB_OF_ARGS)
            sys.stderr.write('\n')
            optParser.print_help()
            sys.exit(ERROR_CODE)
        # Apply relevant type conversions to options
        optimize = options.optimalColumnWidths
        if optimize in ('True', 'False'): optimize = eval(optimize)
        distribute = options.distributeColumns
        if distribute in ('True', 'False'): distribute = eval(distribute)
        resolveFields = options.resolveFields
        if resolveFields == 'True': resolveFields = True
        stream = options.stream
        if stream in ('True', 'False'): stream = eval(stream)
        converter = Converter(args[0], args[1], options.server, options.port,
          options.template, optimize, distribute, options.script, resolveFields,
          options.pdf, options.csv, options.ppp, stream, options.pageStart,
          options.verbose)
        try:
            converter.run()
        except Converter.Error as err:
            sys.stderr.write(str(err))
            sys.stderr.write('\n')
            optParser.print_help()
            sys.exit(ERROR_CODE)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    ConverterScript().run()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
