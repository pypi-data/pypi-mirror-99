# -*- coding: utf-8 -*-

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
import os.path, io
from base64 import encodebytes
from xml.sax.saxutils import quoteattr

from appy.xml import xmlPrologue
from appy.xml.escape import Escape

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Marshaller:
    '''Allows to produce the XML version of a Python object. The XML result
       respects conventions as described in appy.xml.unmarshaller.py.'''

    # Names of object attributes to exclude from the result, by class name
    fieldsToExclude = {'History': 'o'}

    # The correspondence between classes and their equivalent base class
    typesMap = {'list': 'list', 'PersistentList': 'list', 'UserList': 'list',
                'dict': 'dict', 'PersistentMapping': 'dict', 'UserDict': 'dict',
                'FileInfo': 'file', 'bool': 'bool', 'int': 'int',
                'float': 'float', 'bytes': 'bytes', 'tuple': 'tuple',
                'DateTime': 'DateTime'}

    def __init__(self, cdata=False, conversionFunctions={}, rootTag='appyData',
                 dumpXmlPrologue=True, namespaces={}, namespacedTags={}):
        # If p_cdata is True, all string values will be dumped as XML CDATA
        self.cdata = cdata
        # The following dict stores specific conversion (=Python to XML)
        # functions. Such functions are useful when you are not happy with the
        # way built-in converters work, or if you want to define a specific way
        # to represent, in XML, some particular Python object or value. In this
        # dict, every key represents a given type (it must correspond to the
        # class name as retrieved by someObject.__class__.__name__); every value
        # is a function accepting 2 args: the first one is the StringIO where
        # the result is being dumped, while the second one is the Python object
        # to dump.
        self.conversionFunctions = conversionFunctions
        # If dumpXmlPrologue is True, the XML prologue will be dumped
        self.dumpXmlPrologue = dumpXmlPrologue
        # The name of the root tag
        self.rootTagName = rootTag
        # The namespaces that will be defined at the root of the XML message.
        # It is a dict whose keys are namespace prefixes and whose values are
        # namespace URLs. If you want to specify a default namespace, specify an
        # entry whose key is an empty string.
        self.namespaces = namespaces
        # The following dict will tell which XML tags will get which namespace
        # prefix ({s_tagName: s_prefix}). Special optional dict entry
        # '*':s_prefix will indicate a default prefix that will be applied to
        # any tag that does not have it own key in this dict.
        self.namespacedTags = namespacedTags
        # The following attribute will hold the object to marshall (will be set
        # by m_parshall).
        self.o = None

    def getTagName(self, name):
        '''Returns the name of tag p_name as will be dumped. It can be p_name,
           or p_name prefixed with a namespace prefix (will depend on
           self.prefixedTags).'''
        # Determine the prefix
        prefix = ''
        if name in self.namespacedTags: prefix = self.namespacedTags[name]
        elif '*' in self.namespacedTags: prefix = self.namespacedTags['*']
        return '%s:%s' % (prefix, name) if prefix else name

    def isAppy(self, o):
        '''Returns True if p_o is an Appy object'''
        return hasattr(o, 'class_')

    def isObject(self, o):
        '''Returns True if p_o is an instance of a custom class, False if it is
           a basic type, or tuple, sequence, etc.'''
        return hasattr(o, '__dict__')

    def dumpRootTag(self, r, o):
        '''Dumps the root tag'''
        # Dumps the name of the tag
        tagName = self.getTagName(self.rootTagName)
        r.write('<%s type="object"' % tagName)
        # Dumps namespace definitions if any
        for prefix, url in self.namespaces.items():
            if not prefix:
                pre = 'xmlns' # The default namespace
            else:
                pre = 'xmlns:%s' % prefix
            r.write(' %s="%s"' % (pre, url))
        # Dumps Appy-specific attributes
        if self.isAppy(o):
            r.write(' id="%s" iid="%d" className="%s"' % \
                    (o.id, o.iid, o.class_.name))
        r.write('>')
        return tagName

    def dumpString(self, r, s):
        '''Dumps a string into the result'''
        # Surround it with a CDATA when appropriate
        if self.cdata: r.write('<![CDATA[')
        # Escape XML chars
        r.write(Escape.xml(s))
        if self.cdata: r.write(']]>')

    def dumpFile(self, r, v):
        '''Dumps a file into the result'''
        if not v: return
        w = r.write
        # p_value contains an instance of class appy.model.fields.file.FileInfo.
        # Encode it in Base64, in one or several parts.
        partTag = self.getTagName('part')
        r.write('<%s type="base64" number="1">' % partTag)
        if v.inDb():
            path = v.getFilePath(self.o)
        else:
            path = v.fsPath
        if not os.path.isfile(path):
            w('</%s>' % partTag) # Close the (empty) tag
            return
        f = open(path, 'rb')
        partNb = 1
        while True:
            chunk = f.read(v.BYTES)
            if not chunk: break
            # We have one more chunk. Dump the start tag (excepted if it is
            # the first chunk: the start tag has already been dumped, see
            # above).
            if partNb > 1:
                w('<%s type="base64" number="%d">' % (partTag, partNb))
            w(encodebytes(chunk).decode())
            w('</%s>' % partTag) # Close the tag
            partNb += 1
        f.close()

    def dumpDict(self, r, value):
        '''Dumps in p_r the XML version of dict p_value'''
        for k, v in value.items():
            r.write('<entry type="object">')
            self.dumpField(r, 'k', k)
            self.dumpField(r, 'v', v)
            r.write('</entry>')

    def dumpList(self, r, value):
        '''Dumps the XML version of list p_value'''
        for v in value: self.dumpField(r, 'e', v)

    # Dumping a tuple is similar to dumping a list
    dumpTuple = dumpList

    def dumpBool(self, r, value):
        '''Dumps in p_r this p_boolean value'''
        r.write(str(bool(value)))

    def dumpBytes(self, r, value):
        '''Dumps p_value, which is a bytes value'''
        r.write(value.decode())

    def dumpValue(self, r, value, type, className):
        '''Dumps in p_r the XML version of p_value'''
        # Use a custom function if one is defined for this type of value
        if className in self.conversionFunctions:
            self.conversionFunctions[className](r, value)
            return
        # Find the specific method for dumping this p_value
        if not type:
            r.write(value or '')
        else:
            method = 'dump%s' % type.capitalize()
            if hasattr(self, method):
                exec('self.%s(r, value)' % method)
            else:
                r.write(str(value))

    def dumpField(self, r, name, value):
        '''Dumps in p_r, the p_value of field named p_name'''
        # As a preamble, manage special case of p_name being "_any". In that
        # case, p_value corresponds to a previously marshalled string that must
        # be included as is here, without dumping the tag name.
        if name == '_any':
            r.write(value)
            return
        # Dump the start tag
        tagName = self.getTagName(name)
        r.write('<%s' % tagName)
        # Dump value's type as an XML attribute
        className = value.__class__.__name__
        if className in self.typesMap:
            type = self.typesMap[className]
        elif self.isObject(value):
            type = 'object'
        else:
            # For any other type, attribute "type" will not be dumped
            type = None
        if type: r.write(' type="%s"' % type)
        # Dump the value's length if multi-valued
        if type in ('list', 'tuple'):
            length = len(value) if value else 0
            r.write(' count="%d"' % length)
        # Dump file-related attributes
        if value and (type == 'file'):
            # Dump the MIME type
            r.write(' mimeType="%s"' % value.mimeType)
            # Dump the file name
            r.write(' name=%s' % quoteattr(value.uploadName))
        r.write('>')
        # Dump the field value
        self.dumpValue(r, value, type, className)
        # Dump the end tag
        r.write('</%s>' % tagName)

    def mustDump(self, name, className):
        '''Must attribute named p_name on the class named p_className be part of
           the result ?'''
        exclude = self.fieldsToExclude.get(className)
        return not exclude or (name not in exclude)

    def dumpObject(self, r, o, complete=False, fieldNames=None):
        '''Dumps this p_o(bject) in p_r'''
        # Is p_o an Appy object ?
        # ----------------------------------------------------------------------
        #  yes | if p_complete is True, the entire object is dumped, with all
        #      | its fields being visible on the "xml" layout (p_fieldNames is
        #      | ignored). If p_complete is False, only its URL is dumped.
        # ----------------------------------------------------------------------
        #  no  | p_complete is ignored and the entire object is dumped, based on
        #      | its __dict__ or using names from p_fieldNames.
        # ----------------------------------------------------------------------
        if self.isAppy(o):
            # It is a Appy object
            if complete:
                className = o.class_.name
                # Browse p_o's fields that must appear on the XML layout
                for field in o.getFields('xml'):
                    # Dump only needed fields
                    if not self.mustDump(field.name, className): continue
                    val = field.getValue(o, single=False)
                    v = field.getXmlValue(o, val)
                    self.dumpField(r, field.name, v)
                # Dump the object history
                self.dumpField(r, 'history', o.history)
            else:
                # Dump its URL
                r.write('%s/xml' % o.url)
        else:
            # A non-Appy object: dump it in its entirety
            className = o.__class__.__name__
            if fieldNames:
                # The fields are specified in a list, in order to dump them in
                # that specific order.
                for name in fieldNames:
                    if self.mustDump(name, className):
                        value = getattr(o, name, None)
                        self.dumpField(r, name, value)
            else:
                # Get the field by browsing p_o's dict
                for name, value in o.__dict__.items():
                    if self.mustDump(name, className):
                        self.dumpField(r, name, value)

    def marshall(self, o, appy=False, conversionFunctions=None,
                 fieldNames=None):
        '''Returns, as a string, the XML version of this p_o(bject)'''
        self.o = o
        if conversionFunctions:
            self.conversionFunctions.update(conversionFunctions)
        # Create the buffer where the XML result will be dumped
        r = io.StringIO()
        # Dump the XML prologue if required
        if self.dumpXmlPrologue:
            r.write(xmlPrologue)
        if self.isObject(o):
            # Dump the root tag
            rootTagName = self.dumpRootTag(r, o)
            # Dump the fields of this root object
            self.dumpObject(r, o, complete=True, fieldNames=fieldNames)
            self.marshallSpecificElements(o, r)
            r.write('</%s>' % rootTagName)
        else:
            self.dumpField(r, self.rootTagName, o)
        # Return the result
        return r.getvalue()

    def marshallSpecificElements(self, o, r):
        '''You can use this marshaller as a base class for creating your own.
           In this case, this method will be called by m_marshall to allow your
           concrete marshaller to insert more things in the result. p_r is the
           StringIO buffer where the result of the marshalling process is
           currently dumped; p_o is the object being currently marshalled.'''
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
