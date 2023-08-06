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
from pathlib import Path
import os, os.path, sys, zipfile, re, shutil

from appy.xml.escape import Escape
from appy.pod.renderer import Renderer
from appy.pod import styles_manager as sm
from appy.test.integration import Test as BaseTest
from appy.pod.odf_parser import OdfEnvironment, OdfParser
from appy.test.integration import Tester, TestFactory, TesterError

# TesterError-related constants  - - - - - - - - - - - - - - - - - - - - - - - -
TEMPLATE_NOT_FOUND = 'Template file "%s" was not found.'
CONTEXT_NOT_FOUND = 'Context file "%s" was not found.'
EXPECTED_RESULT_NOT_FOUND = 'Expected result "%s" was not found.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class AnnotationsRemover(OdfParser):
    '''This parser is used to remove from content.xml and styles.xml the
       Python tracebacks that may be dumped into OpenDocument annotations by
       pod when generating errors. Indeed, those tracebacks contain lot of
       machine-specific info, like absolute paths to the python files, etc.'''

    def __init__(self, env, caller):
        OdfParser.__init__(self, env, caller)
        self.r = ''
        # Are we parsing an annotation ?
        self.inAnnotation = False
        # Within an annotation, have we already met a text ?
        self.textEncountered = False
        # Must we avoid dumping the current tag/content into the result ?
        self.ignore = False

    def startElement(self, tag, attrs):
        e = OdfParser.startElement(self, tag, attrs)
        # Do we enter into an annotation ?
        if tag == '%s:annotation' % e.ns(e.NS_OFFICE):
            self.inAnnotation = True
            self.textEncountered = False
        elif tag == '%s:p' % e.ns(e.NS_TEXT):
            if self.inAnnotation:
                if not self.textEncountered:
                    self.textEncountered = True
                else:
                    self.ignore = True
        if not self.ignore:
            self.r += '<%s' % tag
            for name, value in attrs.items():
                self.r += ' %s="%s"' % (name, Escape.xml(value,escapeApos=True))
            self.r += '>'

    def endElement(self, tag):
        e = self.env
        if tag == '%s:annotation' % e.ns(e.NS_OFFICE):
            self.inAnnotation = False
            self.ignore = False
        if not self.ignore:
            self.r += '</%s>' % tag
        OdfParser.endElement(self, tag)

    def characters(self, content):
        e = OdfParser.characters(self, content)
        if not self.ignore: self.r += Escape.xml(content)

    def getResult(self):
        return self.r.encode()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Test(BaseTest):
    '''Abstract test class'''
    interestingOdtContent = ('content.xml', 'styles.xml')

    # "list-style"s can be generated in random order
    ignoreTags = ((OdfEnvironment.NS_DC, 'date'),
                  (OdfEnvironment.NS_STYLE, 'style'),
                  (OdfEnvironment.NS_STYLE, 'font-face'),
                  (OdfEnvironment.NS_TEXT, 'list-style'))

    # Tags "text:style-name" can contain generated names based on time.time
    ignoreAttrs = ('draw:name', 'text:name', 'text:bullet-char', 'table:name',
                  'table:style-name', 'text:style-name', 'xlink:href', 'xml:id')

    def __init__(self, testData, testDescription, testFolder,
                 config, flavour, rendererParams):
        BaseTest.__init__(self, testData, testDescription, testFolder, config,
                          flavour, rendererParams)
        self.templatesPath = Path(self.testFolder) / 'templates'
        self.contextsPath = Path(self.testFolder) / 'contexts'
        self.resultsPath = Path(self.testFolder) / 'results'
        self.result = None
        self.rendererParams = rendererParams

    def getContext(self, contextName):
        '''Gets the objects that are in the context'''
        contextPy = self.contextsPath / (contextName + '.py')
        if not contextPy.is_file():
            raise TesterError(CONTEXT_NOT_FOUND % str(contextPy))
        exec('from appy.pod.test.contexts import %s' % contextName)
        module = eval(contextName)
        r = {}
        for elem in dir(module):
            if not elem.startswith('__'):
                r[elem] = getattr(module, elem)
        return r

    def do(self):
        '''Runs the test'''
        tempFileName = '%s.%s' % (self.data['Name'], self.data['Result'])
        self.result = self.tempFolder / tempFileName
        # Get the path to the template to use for this test. For ODT, which is
        # the most frequent case, the file extension is not specified (so, add
        # it).
        suffix = '' if self.data['Template'].endswith('.ods') else '.odt'
        template = self.templatesPath / (self.data['Template'] + suffix)
        if not template.is_file():
            raise TesterError(TEMPLATE_NOT_FOUND % template)
        # Get the context
        context = self.getContext(self.data['Context'])
        # Get the LibreOffice port
        ooPort = self.data['LibreOfficePort']
        pythonWithUno = self.config['pythonWithUnoPath']
        # Get the styles mapping. Dicts are not yet managed by the TablesParser
        stylesMapping = eval('{' + self.data['StylesMapping'] + '}')
        # Call the renderer
        params = {'ooPort': ooPort, 'pythonWithUnoPath': pythonWithUno,
                  'stylesMapping': stylesMapping, 'protection': True}
        params.update(self.rendererParams)
        Renderer(str(template), context, str(self.result), **params).run()

    def getOdtContent(self, odtPath):
        '''Creates in the temp folder content.xml and styles.xml extracted
           from p_odtFile.'''
        contentXml = None
        stylesXml = None
        version = 'actual' if odtPath == self.result else 'expected'
        zipFile = zipfile.ZipFile(str(odtPath))
        for zippedFile in zipFile.namelist():
            if zippedFile in self.interestingOdtContent:
                path = self.tempFolder / ('%s.%s' % (version, zippedFile))
                f = open(path, 'wb')
                fileContent = zipFile.read(zippedFile)
                # Python tracebacks that are in annotations include the full
                # path to the Python files, which of course may be different
                # from one machine to the other. So we remove those paths.
                remover = AnnotationsRemover(OdfEnvironment(), self)
                remover.parse(fileContent)
                fileContent = remover.getResult()
                f.write(fileContent)
                f.close()
        zipFile.close()

    def checkResult(self):
        '''r_ is False if the test succeeded'''
        # Get styles.xml and content.xml from the actual result
        r = False
        self.getOdtContent(self.result)
        # Get styles.xml and content.xml from the expected result
        expectedName = self.data['Name'] + '.' + self.data['Result']
        expectedResult = self.resultsPath / expectedName
        if not expectedResult.is_file():
            raise TesterError(EXPECTED_RESULT_NOT_FOUND % str(expectedResult))
        self.getOdtContent(expectedResult)
        for fileName in self.interestingOdtContent:
            diffOccurred = self.compareFiles(
                os.path.join(self.tempFolder, 'actual.%s' % fileName),
                os.path.join(self.tempFolder, 'expected.%s' % fileName),
                areXml=True, xmlTagsToIgnore=Test.ignoreTags,
                xmlAttrsToIgnore=Test.ignoreAttrs)
            if diffOccurred:
                r = True
                break
        return r

# Concrete test classes  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class NominalTest(Test): pass
class ErrorTest(Test):
    def onError(self):
        '''Compares the error that occurred with the expected error'''
        Test.onError(self)
        return not self.isExpectedError(self.data['Message'])

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class PodTestFactory(TestFactory):
    @staticmethod
    def createTest(testData, testDescription, testFolder, config, flavour,
                   rendererParams):
        isErrorTest = testData.table.instanceOf('ErrorTest')
        testClass = isErrorTest and ErrorTest or NominalTest
        return testClass(testData, testDescription, testFolder,
                         config, flavour, rendererParams)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class PodTester(Tester):
    def __init__(self, testPlan):
        Tester.__init__(self, testPlan, [], PodTestFactory)

# ------------------------------------------------------------------------------
if __name__ == '__main__': PodTester('Tests.odt').run()
# ------------------------------------------------------------------------------
