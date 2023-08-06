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
import difflib, xml.sax
from xml.sax.handler import ContentHandler

from appy.xml import xmlPrologue

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
DIFFS_DETECTED = 'Difference(s) detected between files %s and %s:'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class XmlHandler(ContentHandler):
    '''Handler is used for producing, in self.r, a readable XML (with carriage
       returns) and for removing some tags that always change (like dates) from
       a file that need to be compared to another file.'''

    def __init__(self, xmlTagsToIgnore, xmlAttrsToIgnore):
        ContentHandler.__init__(self)
        self.r = xmlPrologue
        self.namespaces = {} # ~{s_namespaceUri: s_namespaceName}~
        self.indentLevel = -1
        self.tabWidth = 3
        self.tagsToIgnore = xmlTagsToIgnore
        self.attrsToIgnore = xmlAttrsToIgnore
        # Some content must be ignored, and not dumped into the result
        self.ignoring = False

    def isIgnorable(self, tag):
        '''Is p_tag an ignorable tag ?'''
        r = False
        for tagName in self.tagsToIgnore:
            if isinstance(tagName, list) or isinstance(tagName, tuple):
                # We have a namespace
                nsUri, name = tagName
                try:
                    nsName = self.ns(nsUri)
                    tagFullName = '%s:%s' % (nsName, name)
                except KeyError:
                    tagFullName = ''
            else:
                # No namespace
                tagFullName = tagName
            if tagFullName == tag:
                r = True
                break
        return r

    def setDocumentLocator(self, locator):
        self.locator = locator

    def endDocument(self): pass

    def dumpSpaces(self):
        self.r += '\n' + (' ' * self.indentLevel * self.tabWidth)

    def manageNamespaces(self, attrs):
        '''Manage namespaces definitions encountered in p_attrs'''
        for name, value in attrs.items():
            if name.startswith('xmlns:'):
                self.namespaces[value] = name[6:]

    def ns(self, nsUri):
        return self.namespaces[nsUri]

    def startElement(self, tag, attrs):
        self.manageNamespaces(attrs)
        # Do we enter into a ignorable element ?
        if self.isIgnorable(tag):
            self.ignoring = True
        else:
            if not self.ignoring:
                self.indentLevel += 1
                self.dumpSpaces()
                self.r += '<%s' % tag
                attrsNames = attrs.keys()
                attrsNames.sort()
                for attrToIgnore in self.attrsToIgnore:
                    if attrToIgnore in attrsNames:
                        attrsNames.remove(attrToIgnore)
                for attrName in attrsNames:
                    self.r += ' %s="%s"' % (attrName, attrs[attrName])
                self.r += '>'

    def endElement(self, tag):
        if self.isIgnorable(tag):
            self.ignoring = False
        else:
            if not self.ignoring:
                self.dumpSpaces()
                self.indentLevel -= 1
                self.r += '</%s>' % tag

    def characters(self, content):
        if not self.ignoring:
            self.r += content.replace('\n', '')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Diff:
    '''Compares 2 XML files and produces a diff'''

    def __init__(self, fileNameA, fileNameB, areXml=True,
                 xmlTagsToIgnore=(), xmlAttrsToIgnore=()):
        self.fileNameA = fileNameA
        self.fileNameB = fileNameB
        self.areXml = areXml # Can also diff non-XML files
        self.xmlTagsToIgnore = xmlTagsToIgnore
        self.xmlAttrsToIgnore = xmlAttrsToIgnore

    def say(self, message, report=None):
        '''Outputs a message, either into the p_report or on stdout'''
        if report:
            report.say(message)
        else:
            print(message)

    def filesAreIdentical(self, report=None):
        '''Compares the 2 files and returns True if they are identical (if we
           ignore xmlTagsToIgnore and xmlAttrsToIgnore). If p_report is
           specified, it must be an instance of appy.test.report.TestReport;
           the diffs will be dumped in it.'''
        # Perform the comparison
        differ = difflib.Differ()
        if self.areXml:
            f = open(self.fileNameA)
            contentA = f.read()
            f.close()
            f = open(self.fileNameB)
            contentB = f.read()
            f.close()
            xmlHandler = XmlHandler(self.xmlTagsToIgnore, self.xmlAttrsToIgnore)
            xml.sax.parseString(contentA, xmlHandler)
            contentA = xmlHandler.r.split('\n')
            xmlHandler = XmlHandler(self.xmlTagsToIgnore, self.xmlAttrsToIgnore)
            xml.sax.parseString(contentB, xmlHandler)
            contentB = xmlHandler.r.split('\n')
        else:
            f = open(self.fileNameA)
            contentA = f.readlines()
            f.close()
            f = open(self.fileNameB)
            contentB = f.readlines()
            f.close()
        diffResult = list(differ.compare(contentA, contentB))
        # Analyse, format and report the result
        atLeastOneDiff = False
        lastLinePrinted = False
        i = -1
        for line in diffResult:
            i += 1
            if line and (line[0] != ' '):
                if not atLeastOneDiff:
                    msg = DIFFS_DETECTED % (self.fileNameA, self.fileNameB)
                    self.say(msg, report)
                    atLeastOneDiff = True
                if not lastLinePrinted:
                    self.say('...', report)
                if self.areXml:
                    self.say(line, report)
                else:
                    self.say(line[:-1], report)
                lastLinePrinted = True
            else:
                lastLinePrinted = False
        return not atLeastOneDiff
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
