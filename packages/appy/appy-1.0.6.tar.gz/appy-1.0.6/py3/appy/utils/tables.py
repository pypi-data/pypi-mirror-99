'''Parser allowing to retrieve Python objects from data defined in tabled within
    a LbreOffice Writer document (ODT).'''

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
# The ODT document must follow these conventions.
# - Each table must have a first row with only one cell: the table name.
# - The other rows must all have the same number of columns. This number must
#   be strictly greater than 1.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import os, os.path, re
from collections import UserList, UserDict

from appy.xml import Parser
from appy.utils.zip import unzip
from appy.utils import path as putils

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class ParserError(Exception): pass
class TypeError(Exception): pass

# ParserError-related constants  - - - - - - - - - - - - - - - - - - - - - - - -
BAD_PARENT_ROW = 'For table "%s", you specified "%s" as parent table, but ' \
  'you referred to row number "%s" within the parent. This value must be a ' \
  'positive integer or zero (we start counting rows at 0).'
PARENT_NOT_FOUND = 'I cannot find table "%s" that you defined as being ' \
  'parent of "%s".'
TABLE_KEY_ERROR = 'Within a row of table "%s", you mention a column named ' \
  '"%s" which does not exist neither in "%s" itself, neither in its parent ' \
  'row(s). '
PARENT_ROW_NOT_FOUND = 'You specified table "%s" as inheriting from table ' \
  '"%s", row "%d", but this row does not exist (table "%s" as a length = %d). '\
  ' Note that we start counting rows at 0.'
PARENT_COLUMN_NOT_FOUND = 'You specified table "%s" as inheriting from table ' \
  '"%s", column "%s", but this column does not exist in table "%s" or parents.'
PARENT_ROW_COL_NOT_FOUND = 'You specified table "%s" as inheriting from ' \
  'table "%s", column "%s", value "%s", but it does not correspond to any ' \
  'row in table "%s".'
NO_ROWS_IN_TABLE_YET = 'In first row of table "%s", you use value \' " \' ' \
  'for referencing the cell value in previous row, which does not exist.'
VALUE_ERROR = 'Value error for column "%s" of table "%s". %s'
TYPE_ERROR = 'Type error for column "%s" of table "%s". %s'

# TypeError-related constants  - - - - - - - - - - - - - - - - - - - - - - - - -
LIST_TYPE_ERROR = 'Maximum number of nested lists is 4.'
BASIC_TYPE_ERROR = 'Letter "%s" does not correspond to any valid type. ' \
  'Valid types are f (float), i (int), g (long) and b (bool).'
BASIC_VALUE_ERROR = 'Value "%s" can\'t be converted to type "%s".'
LIST_VALUE_ERROR = 'Value "%s" is malformed: within it, %s. You should check ' \
  'the use of separators ( , : ; - ) to obtain a schema conform to the type ' \
  '"%s".'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Type:
    basicTypes = {'f': float, 'i':int, 'b':bool}
    separators = ['-', ';', ',', ':']

    def __init__(self, typeDecl):
        self.basicType = None # The Python basic type
        self.listNumber = 0
        # If = 1 : it is a list. If = 2: it is a list of lists. If = 3...
        self.analyseTypeDecl(typeDecl)
        if self.listNumber > 4:
            raise TypeError(LIST_TYPE_ERROR)
        self.name = self.computeName()

    def analyseTypeDecl(self, typeDecl):
        for char in typeDecl:
            if char == 'l':
                self.listNumber += 1
            else:
                # Get the basic type
                if char not in Type.basicTypes:
                    raise TypeError(BASIC_TYPE_ERROR % char)
                self.basicType = Type.basicTypes[char]
                break
        if not self.basicType:
            self.basicType = str

    def convertBasicValue(self, value):
        try:
            return self.basicType(value.strip())
        except ValueError:
            raise TypeError(BASIC_VALUE_ERROR % (value,
                                                 self.basicType.__name__))

    def convertValue(self, value):
        '''Converts a p_value which is a string into a value conform
        to self.'''
        if self.listNumber == 0:
            r = self.convertBasicValue(value)
        else:
            # Get separators in their order of appearance
            separators = []
            for char in value:
                if (char in Type.separators) and (char not in separators):
                    separators.append(char)            
            # Remove surplus separators
            if len(separators) > self.listNumber:
                nbOfSurplusSeps = len(separators) - self.listNumber
                separators = separators[nbOfSurplusSeps:]
            # If not enough separators, create corresponding empty lists.
            r = None
            innerList = None
            rIsComplete = False
            if len(separators) < self.listNumber:
                if not value:
                    r = []
                    rIsComplete = True
                else:
                    # Begin with empty list(s)
                    nbOfMissingSeps = self.listNumber - len(separators)
                    r = []
                    innerList = r
                    for i in range(nbOfMissingSeps-1):
                        newInnerList = []
                        innerList.append(newInnerList)
                        innerList = newInnerList
            # We can now convert the value
            separators.reverse()
            if innerList is not None:
                innerList.append(self.convertListItem(value, separators))
            elif not rIsComplete:
                try:
                    r = self.convertListItem(value, separators)
                except TypeError as te:
                    raise TypeError(LIST_VALUE_ERROR % (value, te, self.name))
        return r

    def convertListItem(self, stringItem, remainingSeps):
        if not remainingSeps:
            r = self.convertBasicValue(stringItem)
        else:
            curSep = remainingSeps[0]
            tempRes = stringItem.split(curSep)
            if (len(tempRes) == 1) and (not tempRes[0]):
                # There was no value within value, so we produce an empty list.
                r = []
            else:
                r = []
                for tempItem in tempRes:
                    r.append(self.convertListItem(tempItem, remainingSeps[1:]))
        return r

    def computeName(self):
        prefix = 'list of ' * self.listNumber
        return '<%s%s>' % (prefix, self.basicType.__name__)

    def __repr__(self): return self.name

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class TableRow(UserDict):
    def __init__(self, table):
        UserDict.__init__(self)
        self.table = table

    def __getitem__(self, key):
        '''This method "implements" row inheritance: if the current row does
           not have an element with p_key, it looks in the parent row of this
           row, via the parent table self.table.'''
        # Return the value from this dict if present
        if key in self: return UserDict.__getitem__(self, key)
        # Try to get the value from the parent row
        keyError = False
        t = self.table
        # Get the parent row
        if t.parent:
            if isinstance(t.parentRow, int):
                if t.parentRow < len(t.parent):
                    try:
                        r = t.parent[t.parentRow][key]
                    except KeyError:
                        keyError = True
                else:
                    raise ParserError(PARENT_ROW_NOT_FOUND % (t.name,
                      t.parent.name, t.parentRow, t.parent.name, len(t.parent)))
            else:
                tColumn, tValue = t.parentRow
                # Get the 1st row having tColumn = tValue
                rowFound = False
                for row in t.parent:
                    try:
                        curVal = row[tColumn]
                    except KeyError:
                        raise ParserError(PARENT_COLUMN_NOT_FOUND % (t.name,
                                         t.parent.name, tColumn, t.parent.name))
                    if curVal == tValue:
                        rowFound = True
                        try:
                            r = row[key]
                        except KeyError:
                            keyError = True
                        break
                if not rowFound:
                    raise ParserError(PARENT_ROW_COL_NOT_FOUND % (t.name,
                                 t.parent.name, tColumn, tValue, t.parent.name))
        else:
            keyError = True
        if keyError:
            raise KeyError(TABLE_KEY_ERROR % (t.name, key, t.name))
        return r

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Table(UserList):
    nameRex = re.compile('([^\(]+)(?:\((.*)\))?')

    def __init__(self):
        UserList.__init__(self)
        self.name = ''
        # Column names
        self.columns = []
        # Column types. If no type is defined for some column, value "None" will
        # be stored and wille correspond to default type "str".
        self.columnTypes = []
        # The parent table
        self.parent = None
        # The parent row, within the parent table
        self.parentRow = None

    def setName(self):
        '''Parses the table name and extracts from it the potential reference
           to a parent table.'''
        name = self.name.strip()
        elems = Table.nameRex.search(name)
        name, parentSpec = elems.groups()
        self.name = name
        if parentSpec:
            r = parentSpec.split(':')
            if len(r) == 1:
                self.parent = parentSpec.strip()
                self.parentRow = 0
            else:
                self.parent = r[0].strip()
                r = r[1].split('=')
                if len(r) == 1:
                    try:
                        self.parentRow = int(r[0])
                    except ValueError:
                        msg = BAD_PARENT_ROW % (self.name, self.parent, r[0])
                        raise ParserError(msg)
                    if self.parentRow < 0:
                        msg = BAD_PARENT_ROW % (self.name, self.parent, r[0])
                        raise ParserError(msg)
                else:
                    self.parentRow = (r[0].strip(), r[1].strip())

    def addRow(self):
        '''Adds a row of data into this table, as a TableRow instance. This
           consists in converting the list of row data we have already added
           into the table into a TableRow instance.'''
        data = self[-1]
        row = TableRow(self)
        for i in range(len(self.columns)):
            column = self.columns[i]
            value = data[i].strip()
            if value == '"':
                # Check if a previous row exists
                if len(self) == 1:
                    raise ParserError(NO_ROWS_IN_TABLE_YET % self.name)
                value = self[-2][column]
            else:
                # Get the column type and convert the value to this type
                type = self.columnTypes[i]
                if type:
                    try:
                        value = type.convertValue(value)
                    except TypeError as te:
                        raise ParserError(VALUE_ERROR % (column, self.name, te))
            row[self.columns[i]] = value
        self[-1] = row

    def addColumn(self):
        '''A new column has been added into self.columns. Extract its type if
           defined.'''
        # Extract the parsed column name
        name = self.columns[-1].strip()
        type = None
        if ':' in name:
            # We have a type declaration
            name, typeDecl = name.split(':')
            try:
                type = Type(typeDecl.strip())
            except TypeError as te:
                raise ParserError(TYPE_ERROR % (name, self.name, te))
        # Update the lists of header names and types
        self.columns[-1] = name
        self.columnTypes.append(type)
        # Create a new empty column for the next one
        self.columns.append('')

    def dump(self, withContent=True):
        r = 'Table "%s"' % self.name
        if self.parent:
            r += ' extends table "%s"' % self.parent.name
            if isinstance(self.parentRow, int):
                r += '(%d)' % self.parentRow
            else:
                r += '(%s=%s)' % self.parentRow
        if withContent:
            r += '\n'
            for line in self:
                r += str(line)
        return r

    def instanceOf(self, tableName):
        r = False
        if self.parent:
            if self.parent.name == tableName:
                r = True
            else:
                r = self.parent.instanceOf(tableName)
        return r

    def asDict(self):
        '''If this table as only 2 columns named "key" and "value", it can be
           represented as a Python dict. This method produces this dict.'''
        infoDict = {}
        if self.parent:
            for info in self.parent:
              infoDict[info["key"]] = info["value"]
        for info in self:
            infoDict[info["key"]] = info["value"]
        return infoDict

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class OdtTablesParser(Parser):
    PARSING = 0
    PARSING_TABLE_NAME = 1
    PARSING_TABLE_HEADERS = 2
    PARSING_DATA_ROW = 3

    def startDocument(self):
        Parser.startDocument(self)
        # Where to store the parsed tables, keyed by their names
        self.r = {}
        # The currently walked table
        self.currentTable = None
        # The currently walked data row, as list of strings (cell content)
        self.currentRow = None
        # The initial parsing state
        self.state = self.PARSING

    def startElement(self, tag, attrs):
        if tag == 'table:table':
            # A new table is encountered
            self.currentTable = Table()
        elif tag == 'table:table-row':
            if not self.currentTable.name:
                # This is the first row (table name)
                self.state = self.PARSING_TABLE_NAME
            elif not self.currentTable.columns:
                # This is the second row (column headers)
                self.state = self.PARSING_TABLE_HEADERS
                self.currentTable.columns.append('')
            else:
                # This is a data row
                self.state = self.PARSING_DATA_ROW
                self.currentTable.append([''])
        elif tag == 'table:table-cell':
            pass

    def endElement(self, tag):
        if tag == 'table:table':
            # Store the completelty parsed table in self.res
            table = self.currentTable
            self.r[table.name] = table
            self.currentTable = None
        elif tag == 'table:table-row':
            if self.state == self.PARSING_TABLE_NAME:
                # We have finished to parse the first row (table name)
                self.currentTable.setName()
                self.state = self.PARSING
            elif self.state == self.PARSING_TABLE_HEADERS:
                # We have finished to parse the second row
                del self.currentTable.columns[-1]
                self.state = self.PARSING
            elif self.state == self.PARSING_DATA_ROW:
                # We have finished parsing a data row
                del self.currentTable[-1][-1]
                self.currentTable.addRow()
                self.state = self.PARSING
        elif tag == 'table:table-cell':
            if self.state == self.PARSING_TABLE_HEADERS:
                # We have finished parsing a header value. Add a new one.
                self.currentTable.addColumn()
            elif self.state == self.PARSING_DATA_ROW:
                # We have finished parsing a cell value. Add a new one.
                self.currentTable[-1].append('')

    def characters(self, content):
        # Get the table name
        if self.state == self.PARSING_TABLE_NAME:
            self.currentTable.name += content
        elif self.state == self.PARSING_TABLE_HEADERS:
            self.currentTable.columns[-1] += content
        elif self.state == self.PARSING_DATA_ROW:
            self.currentTable[-1][-1] += content

    def endDocument(self):
        Parser.endDocument(self)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class TablesParser:
    def __init__(self, path):
        # The path to the ODT file containing the tables
        self.path = path
        # Parsed tables will be stored in this dict
        self.tables = None

    def linkTables(self):
        '''Resolve parend/child links between parsed tables'''
        for name, table in self.tables.items():
            if not table.parent: continue
            if table.parent not in self.tables:
                raise ParserError(PARENT_NOT_FOUND % (table.parent, table.name))
            table.parent = self.tables[table.parent]

    def run(self):
        '''Unzip the ODT file and parse tables within content.xml'''
        # Create a folder in the OS temp folder
        folder = putils.getOsTempFolder(sub=True)
        # Unzip the file in the OS temp folder
        unzip(str(self.path), folder)
        # Parse content.xml
        contentXml = os.path.join(folder, 'content.xml')
        self.tables = OdtTablesParser().parse(contentXml, source='file')
        # Revolve parent/child table links
        self.linkTables()
        # Delete the folder
        putils.FolderDeleter.delete(folder)
        return self.tables
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
