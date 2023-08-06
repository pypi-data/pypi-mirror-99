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
from appy.pod.buffers import MemoryBuffer
from appy.pod.xhtml.tags import SELF_CLOSING
from appy.shared.xml_parser import XmlEnvironment, XmlParser

# ------------------------------------------------------------------------------
class PxEnvironment(XmlEnvironment):
    '''Environment for the PX parser'''

    def __init__(self):
        # In the following buffer, we will create a single memory sub-buffer
        # that will hold the result of parsing the PX = a hierarchy of memory
        # buffers = PX's AST (Abstract Syntax Tree).
        # A major difference between POD and PX: POD creates the AST and
        # generates the result in the same step: one AST is generated, and then
        # directly produces a single evaluation, in the root file buffer. PX
        # works in 2 steps: the AST is initially created in self.ast. Then,
        # several (concurrent) evaluations can occur, without re-generating the
        # AST.
        self.ast = MemoryBuffer(self, None)
        # Buffer where we must dump the content we are currently reading
        self.currentBuffer = self.ast
        # Tag content we are currently reading. We will put something in this
        # attribute only if we encounter content that is Python code.
        # Else, we will directly dump the parsed content into the current
        # buffer.
        self.currentContent = ''
        # The currently walked element. We redefine it here. This attribute is
        # normally managed by the parent XmlEnvironment, but we do not use the
        # standard machinery from this environmment and from the default
        # XmlParser for better performance. Indeed, the base parser and env
        # process namespaces, and we do not need this for the PX parser.
        self.currentElem = None
        # Exceptions are always raised (for pod, it is not the case)
        self.raiseOnError = True

    def addSubBuffer(self):
        subBuffer = self.currentBuffer.addSubBuffer()
        self.currentBuffer = subBuffer

    def isActionElem(self, elem):
        '''Returns True if the currently walked p_elem is the same elem as the
           main buffer elem.'''
        action = self.currentBuffer.action
        return action and (action.elem == elem)

# ------------------------------------------------------------------------------
class PxParser(XmlParser):
    '''PX parser that is specific for parsing PX data'''
    pxAttributes = ('var', 'for', 'if', 'var2')
    noDumpTags = ('selected', 'checked', 'disabled', 'multiple', 'readonly')
    # The following dict allows to convert attrs "lfor" to "for". Indeed,
    # because tags "label" can have an attribute named "for", it clashes with
    # the "for" attribute added by PX. The solution is to force users to write,
    # in their PX, the HTML attr for" as "lfor".
    renamedAttributes = {'lfor': 'for'}

    def __init__(self, env, caller=None):
        XmlParser.__init__(self, env, caller)

    def startElement(self, elem, attrs):
        '''A start p_elem with p_attrs is encountered in the PX.'''
        e = self.env
        self.currentElem = elem
        # See if we have a PX attribute among p_attrs
        found = False
        for name in self.pxAttributes:
            if attrs.has_key(name):
                if not found:
                    # This is the first PX attr we find.
                    # Create a sub-buffer with an action.
                    e.addSubBuffer()
                    found = True
                # Add the action
                e.currentBuffer.createPxAction(elem, name, attrs[name])
        if e.isActionElem(elem):
            # Add a temp element in the buffer (that will be unreferenced
            # later). This way, when encountering the corresponding end element,
            # we will be able to check whether the end element corresponds to
            # the main element or to a sub-element.
            e.currentBuffer.addElement(elem, elemType='px')
        if elem != 'x':
            # Dump the start element and its attributes. But as a preamble,
            # manage special attributes that could not be dumped at all, like
            # "selected" or "checked".
            hook = None
            ignorableAttrs = self.pxAttributes
            for name in self.noDumpTags:
                if attrs.has_key(name) and attrs[name].startswith(':'):
                    hook = (name, attrs[name][1:])
                    ignorableAttrs += (name,)
                    break
            e.currentBuffer.dumpStartElement(elem, attrs,
                ignoreAttrs=ignorableAttrs, noEndTag=elem in SELF_CLOSING,
                hook=hook, renamedAttrs=self.renamedAttributes)

    def endElement(self, elem):
        e = self.env
        # Manage the potentially collected Python expression in
        # e.currentContent.
        if e.currentContent:
            e.currentBuffer.addExpression(e.currentContent)
            e.currentContent = ''
        # Dump the end element into the current buffer
        if (elem != 'x') and (elem not in SELF_CLOSING):
            e.currentBuffer.dumpEndElement(elem)
        # If this element is the main element of the current buffer, we must
        # pop it and continue to work in the parent buffer.
        if e.isActionElem(elem):
            # Is it the buffer main element?
            isMainElement = e.currentBuffer.isMainElement(elem)
            # Unreference the element among buffer.elements
            e.currentBuffer.unreferenceElement(elem)
            if isMainElement:
                # Continue to work in the parent buffer
                e.currentBuffer = e.currentBuffer.parent

    def characters(self, content):
        e = self.env
        if not e.currentContent and content.startswith(':'):
            # This content is not static content to dump as-is into the result:
            # it is a Python expression.
            e.currentContent += content[1:]
        elif e.currentContent:
            # We continue to dump the Python expression
            e.currentContent += content
        else:
            # Remove blanks which are there only for improving PX's readability
            if content == ' ':
                pass # Keep individual spaces
            elif content.isspace():
                return
            e.currentBuffer.dumpContent(content)
# ------------------------------------------------------------------------------
