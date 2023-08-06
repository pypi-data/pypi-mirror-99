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
import re, sys
from xml.sax.saxutils import quoteattr

from appy.pod import actions
from appy.pod import PodError
from appy.pod.elements import *
from appy.utils import Traceback
from appy.xml import xmlPrologue
from appy.xml.escape import Escape

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class ParsingError(Exception): pass

# ParsingError-related constants - - - - - - - - - - - - - - - - - - - - - - - -
ELEMENT = 'identifies the part of the document that will be impacted ' \
  'by the command. It must be one of %s.' % str(PodElement.POD_ELEMS)
FOR_EXPRESSION = 'must be of the form: {name} in {expression}. {name} must be '\
  'a Python variable name. It is the name of the iteration variable. ' \
  '{expression} is a Python expression that, when evaluated, produces a ' \
  'Python sequence (tuple, string, list, etc).'
POD_STATEMENT = 'A Pod statement has the form: do {element} ' \
  '[{command} {expression}]. {element} ' + ELEMENT + ' Optional {command} ' \
  'can be "if" (conditional inclusion of the element) or "for" (multiple ' \
  'inclusion of the element). For an "if" command, {expression} is any ' \
  'Python expression. For a "for" command, {expression} '+ FOR_EXPRESSION
FROM_CLAUSE = 'A "from" clause has the form: from[+] {expression}, where ' \
  '{expression} is a Python expression that, when evaluated, produces a valid '\
  'chunk of odt content that will be inserted instead of the element that is ' \
  'the target of the note. If the "+" is specified, the root target element ' \
  'will be kept and its content will be replaced with the expression result.'
EMPTY_NOTE = 'This note is empty. It must at least contain a Pod statement. '+ \
  POD_STATEMENT
BAD_STATEMENT = 'Syntax error for statement "%s". ' + POD_STATEMENT
BAD_SUB_STATEMENT = 'Wrong sub-statement "%s".'
BAD_ELEMENT = 'Bad element "%s". An element ' + ELEMENT
BAD_MINUS = "The '-' operator can't be used with element '%s'. It can only be "\
  "specified for elements among %s."
ELEMENT_NOT_FOUND = 'Action specified element "%s" but available elements ' \
  'in this part of the document are %s.'
BAD_FROM_CLAUSE = 'Syntax error in "from" clause "%s". ' + FROM_CLAUSE
DUPLICATE_NAMED_IF = 'An "if" statement with the same name already exists.'
ELSE_NOT_MAIN = 'An "else" clause can only be defined as a main statement.'
ELSE_WITHOUT_IF = 'No previous "if" statement could be found for this "else" ' \
  'statement.'
ELSE_WITHOUT_NAMED_IF = 'I could not find an "if" statement named "%s".'
BAD_FOR_EXPRESSION = 'Bad "for" expression "%s". A "for" expression ' + \
  FOR_EXPRESSION
BAD_VAR_EXPRESSION = 'Bad variable definition "%s". A variable definition ' \
  'must have the form: {name[,name2,...} = {expression}, or * = {expression}. '\
  'Every name must be a Python-compliant variable name. {expression} is a ' \
  'Python expression. When encountering such a statement, pod will define, ' \
  'in the specified part of the document, variables {name}, {name2}, etc, ' \
  'whose values will be initialized by evaluating {expression}.'
BAD_VAR_STAR = 'A multi-variable definition must be of the form: * = {expr}'
BAD_VAR_NAME = 'Bad variable name "%s".'
EVAL_EXPR_ERROR = 'Error while evaluating expression "%s". %s'
BAD_META_CONDITION = 'Wrong meta-condition "%s". A meta-condition must be a ' \
  'Python expression surrounded by single or double quotes.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class BufferIterator:
    def __init__(self, buffer):
        self.buffer = buffer
        self.remainingSubBufferIndexes = list(buffer.subBuffers.keys())
        self.remainingElemIndexes = list(buffer.elements.keys())
        self.remainingSubBufferIndexes.sort()
        self.remainingElemIndexes.sort()

    def __iter__(self): return self
    def __next__(self):
        # Stop if there is no more elem nor sub-buffer
        if not self.remainingSubBufferIndexes and not self.remainingElemIndexes:
            raise StopIteration
        nextSubBufferIndex = None
        if self.remainingSubBufferIndexes:
            nextSubBufferIndex = self.remainingSubBufferIndexes[0]
        nextExprIndex = None
        if self.remainingElemIndexes:
            nextExprIndex = self.remainingElemIndexes[0]
        # Compute min between nextSubBufferIndex and nextExprIndex
        if (nextSubBufferIndex is not None) and (nextExprIndex is not None):
            res = min(nextSubBufferIndex, nextExprIndex)
        elif (nextSubBufferIndex is None) and (nextExprIndex is not None):
            res = nextExprIndex
        elif (nextSubBufferIndex is not None) and (nextExprIndex is None):
            res = nextSubBufferIndex
        # Update "remaining" lists
        if res == nextSubBufferIndex:
            self.remainingSubBufferIndexes = self.remainingSubBufferIndexes[1:]
            resDict = self.buffer.subBuffers
        elif res == nextExprIndex:
            self.remainingElemIndexes = self.remainingElemIndexes[1:]
            resDict = self.buffer.elements
        return res, resDict[res]
    next = __next__ # Python2-3 compliance

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Buffer:
    '''Abstract class representing any buffer used during rendering'''
    elementRex = re.compile('([\w-]+:[\w-]+)\s*(.*?)>', re.S)

    def __init__(self, env, parent):
        self.parent = parent
        self.subBuffers = {} # ~{i_bufferIndex: Buffer}~
        self.env = env
        # Are we computing for pod (True) or px (False)
        self.pod = env.__class__.__name__ != 'PxEnvironment'

    def addSubBuffer(self, subBuffer=None):
        if not subBuffer:
            subBuffer = MemoryBuffer(self.env, self)
        self.subBuffers[self.getLength()] = subBuffer
        subBuffer.parent = self
        return subBuffer

    def removeLastSubBuffer(self):
        subBufferIndexes = list(self.subBuffers.keys())
        subBufferIndexes.sort()
        lastIndex = subBufferIndexes.pop()
        del self.subBuffers[lastIndex]

    def write(self, something): pass # To be overridden

    def getLength(self): pass # To be overridden

    def patchProtected(self, elem, attrs):
        '''Add or patch the attribute allowing to protect this p_elem (a cell or
           section), by evaluating variable "cellProtected" or
           "sectionProtected".'''
        type = elem[:elem.index(':')]
        name = '%s:protected' % type
        var = 'cell' if type == 'table' else 'section'
        value = attrs.get(name, "false").strip() or "false"
        attrs[name] = ':str(%sProtected).lower()|"%s"' % (var, value)

    def patchElement(self, elem, attrs):
        '''Modifies p_elem's attributes when relevant and make them dependent of
           some variable definitions.'''
        if elem == 'table:table':
            # If a variable "tableName" is defined in the context, the current
            # table will get this name instead of its predefined name. Useful,
            # ie, for naming calc sheets (which are implemented as tables).
            attrs = attrs._attrs
            name = 'table:name'
            attrs[name] = ':tableName|"%s"' % attrs[name]
        elif elem == 'table:table-column':
            # Convert attribute "number-columns-repeated" of every table column
            # (or add it if it does not exist) to let the user define how he
            # will repeat table columns via variable "columnsRepeated".
            attrs = attrs._attrs
            key = 'table:number-columns-repeated'
            columnNumber = self.env.getTable().nbOfColumns -1
            nb = (key in attrs) and attrs[key] or '1'
            attrs[key] = ':columnsRepeated[%d]|%s' % (columnNumber, nb)
        elif elem == 'table:table-cell':
            attrs = attrs._attrs
            key = 'table:style-name'
            style = attrs.get(key)
            if style and style.startswith('S'):
                # By convention, if a style name starts with letter "S", POD
                # will allow to replace the name of the cell style with another
                # one, via function "styleFor" if found in the context. The
                # function will be passed 2 args: the name of the style that
                # should normally have been applied, and the context itself. It
                # must return the name of the style to apply. This mechanism is
                # restricted to styles starting with "S" for performance
                # reasons.
                attrs[key] = ':styleFor("%s",_ctx_)|"%s"' % (style, style)
            elif self.env.parser.caller.protection:
                self.patchProtected(elem, attrs)
        elif elem == 'text:section' and self.env.parser.caller.protection:
            self.patchProtected(elem, attrs._attrs)
        elif elem == 'text:list-item' and 'text:start-value' in attrs:
            attrs = attrs._attrs
            val = int(attrs['text:start-value'])
            attrs['text:start-value'] = ':loop._all_[-1].nb+%d|%d' % (val, val)

    def dumpStartElement(self, elem, attrs={}, ignoreAttrs=(), hook=False,
                         noEndTag=False, renamedAttrs=None):
        '''Inserts into this buffer the start tag p_elem, with its p_attrs,
           excepted those listed in p_ignoreAttrs. Attrs can be dumped with an
           alternative name if specified in dict p_renamedAttrs. If p_hook is
           not None (works only for MemoryBuffers), we will insert, at the end
           of the list of dumped attributes:
           * [pod] an Attributes instance, in order to be able, when evaluating
                   the buffer, to dump additional attributes, not known at this
                   dump time;
           * [px]  an Attribute instance, representing a special HTML attribute
                   like "checked" or "selected", that, if the tied expression
                   returns False, must not be dumped at all. In this case,
                   p_hook must be a tuple (s_attrName, s_expr).
        '''
        self.write('<%s' % elem)
        # Some table elements must be patched (pod only)
        if self.pod: self.patchElement(elem, attrs)
        for name, value in attrs.items():
            if ignoreAttrs and (name in ignoreAttrs): continue
            if renamedAttrs and (name in renamedAttrs): name=renamedAttrs[name]
            # If the value begins with ':', it is a Python expression. Else,
            # it is a static value.
            if not value.startswith(':'):
                self.write(' %s=%s' % (name, quoteattr(value)))
            else:
                self.write(' %s="' % name)
                self.addExpression(value[1:])
                self.write('"')
        res = None
        if hook:
            if self.pod:
                res = self.addAttributes()
            else:
                self.addAttribute(*hook)
        # Close the tag
        self.write(noEndTag and '/>' or '>')
        return res

    def dumpEndElement(self, elem):
        self.write('</%s>' % elem)

    def dumpElement(self, elem, content=None, attrs={}):
        '''For dumping a whole element at once'''
        self.dumpStartElement(elem, attrs)
        if content:
            self.dumpContent(content)
        self.dumpEndElement(elem)

    def dumpContent(self, content):
        '''Dumps string p_content into the buffer'''
        # For POD, take care of converting line breaks and tabs
        if self.pod:
            flavour = self.env.parser.caller.tabbedCR and 'odf*' or 'odf'
        else:
            flavour = 'xml'
        content = Escape.xml(content, flavour=flavour)
        self.write(content)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class FileBuffer(Buffer):
    def __init__(self, env, result):
        Buffer.__init__(self, env, None)
        self.result = result
        self.content = open(result, 'w', encoding='utf-8')
        self.content.write(xmlPrologue)

    # getLength is used to manage insertions into sub-buffers. But in the case
    # of a FileBuffer, we will only have 1 sub-buffer at a time, and we don't
    # care about where it will be inserted into the FileBuffer.
    def getLength(self): return 0

    def write(self, something):
        self.content.write(something)

    def pushSubBuffer(self, subBuffer): pass
    def getRootBuffer(self): return self

    def addExpression(self, expression, elem=None, tiedHook=None):
        try:
            expr = Expression(expression, self.pod)
            if tiedHook: tiedHook.tiedExpression = expr
            res, escape = expr.evaluate(self.env.context)
            if escape: self.dumpContent(res)
            else: self.write(res)
        except Exception as e:
            if not self.env.raiseOnError:
                PodError.dump(self, EVAL_EXPR_ERROR % (expression, e),
                              dumpTb=False)
            else:
                raise Exception(EVAL_EXPR_ERROR % (expression, e))

    def addAttributes(self):
        # Into a FileBuffer, it is not possible to insert Attributes. Every
        # Attributes instance is tied to an Expression; because dumping
        # expressions directly into FileBuffer instances seems to be rare, it
        # should not be a severe problem.
        pass

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class MemoryBuffer(Buffer):
    class Rex:
        '''Regular expressions in use for a memory buffer'''
        part = '(for|if|else|with|meta-if)\s*(.*)'
        action = re.compile('(?:(\w+)\s*\:\s*)?do\s+(\w+)(-)?(?:\s+%s)?' % part)
        subAction = re.compile(part)
        for_ = re.compile('\s*([\w\-_,\s]+)\s+in\s+(.*)')
        vars_ = re.compile('\s*([\w\-_*,\s@]+)\s*=\s*(.*)')
        var_ = re.compile('@?[\w\-_]+')
        from_ = re.compile('from(\+)?\s+(.*)')

    def __init__(self, env, parent):
        Buffer.__init__(self, env, parent)
        self.content = ''
        self.elements = {}
        self.action = None

    def clone(self):
        '''Produces an empty buffer that is a clone of this one'''
        return MemoryBuffer(self.env, self.parent)

    def addSubBuffer(self, subBuffer=None):
        sub = Buffer.addSubBuffer(self, subBuffer)
        # Dump a whitespace to avoid having several subbuffers referenced at the
        # same place within this buffer.
        self.content += ' '
        return sub

    def getInsertIndex(self, tag, opening):
        '''Return, within this buffer or any of its sub-buffers, the index that
           immediately follows the first occurrence of p_tag, which is an
           opening or ending tag, depending on p_opening.'''
        # More precisely, it returns a tuple (buffer, i), "buffer" being the
        # precise buffer where p_tag is found (can be p_self or one of its
        # sub-buffers at any level).
        buf = None
        i = self.content.find(tag)
        if i != -1:
            # The tag has been found directly in p_self
            if opening:
                # Find the end of the opening tag
                i = self.content.index('>', i) + 1
            else:
                # Get the index of the char following the closing tag
                i += len(tag)
            buf = self
        if self.subBuffers:
            # Browse sub-buffers
            subs = list(self.subBuffers.items())
            subs.sort()
            for j, sub in subs:
                buffer, k = sub.getInsertIndex(tag, opening)
                if buffer is None: continue
                # We have found the tag in this buffer
                if (buf is None) or (k < i):
                    # If the tag was also found in the main buffer, the tag
                    # from the sub-buffer must be chose because it comes first.
                    buf = buffer
                    i = k
                    break
        return buf, i

    def insertSubBuffer(self, subBuffer, after=None, afterClosing=None):
        '''Inserts p_subBuffer just after the main opening tag, in p_self that
           is already complete.'''
        # If p_after is given, it is a tag, and the p_subBuffer is inserted
        # immediately after this tag's start tag. If p_afterClosing is given, it
        # is a tag, and the p_subBuffer is inserted immediately after this tags'
        # closing tag. If p_both p_afterClosing and p_after are specified, the
        # method tries first to insert the subBuffer via p_afterClosing, and, if
        # this tag is not found, tries to insert it via p_after.
        buf = i = None
        if afterClosing:
            buf, i = self.getInsertIndex('</%s>' % afterClosing, opening=False)
        if after and (buf is None):
            buf, i = self.getInsertIndex('<%s' % after, opening=True)
        if buf is None:
            # Insert p_subBuffer after the main element
            buf = self
            i = buf.content.index('>') + 1
        # Insert sub-buffer's content info buf.content
        size = len(subBuffer.content)
        buf.content = buf.content[:i] + subBuffer.content + buf.content[i:]
        # Increment by 1 all subsequent elements and sub-buffers
        for subType in ('elements', 'subBuffers'):
            subElements = getattr(buf, subType)
            if not subElements: continue
            indexes = list(subElements.keys())
            indexes.sort(reverse=True)
            for j in indexes:
                if j >= i:
                    elem = subElements[j]
                    del subElements[j]
                    subElements[j+size] = elem

    def getRootBuffer(self):
        '''Returns the root buffer. For POD it is always a FileBuffer. For PX,
           it is a MemoryBuffer.'''
        if self.parent: return self.parent.getRootBuffer()
        return self

    def getLength(self): return len(self.content)

    def write(self, thing): self.content += thing

    def getIndex(self, podElemName):
        res = -1
        for index, podElem in self.elements.items():
            if podElem.__class__.__name__.lower() == podElemName:
                if index > res:
                    res = index
        return res

    def getMainElement(self):
        res = None
        if 0 in self.elements:
            res = self.elements[0]
        return res

    def isMainElement(self, elem):
        '''Is p_elem the main element within this buffer?'''
        mainElem = self.getMainElement()
        if not mainElem: return
        if hasattr(mainElem, 'OD'): mainElem = mainElem.OD.nsName
        if elem != mainElem: return
        # elem is the same as the main elem. But is it really the main elem, or
        # the same elem, found deeper in the buffer?
        for index, iElem in self.elements.items():
            foundElem = None
            if hasattr(iElem, 'OD'):
                if iElem.OD:
                    foundElem = iElem.OD.nsName
            else:
                foundElem = iElem
            if (foundElem == mainElem) and (index != 0):
                return
        return True

    def unreferenceElement(self, elem):
        # Find last occurrence of this element
        elemIndex = -1
        for index, iElem in self.elements.items():
            foundElem = None
            if hasattr(iElem, 'OD'):
                # A POD element
                if iElem.OD:
                    foundElem = iElem.OD.nsName
            else:
                # A PX elem
                foundElem = iElem
            if (foundElem == elem) and (index > elemIndex):
                elemIndex = index
        del self.elements[elemIndex]

    def pushSubBuffer(self, subBuffer):
        '''Sets p_subBuffer at the very end of the buffer.'''
        subIndex = None
        for index, aSubBuffer in self.subBuffers.items():
            if aSubBuffer == subBuffer:
                subIndex = index
                break
        if subIndex is not None:
            # Indeed, it is possible that this buffer is not referenced
            # in the parent (if it is a temp buffer generated from a cut)
            del self.subBuffers[subIndex]
            self.subBuffers[self.getLength()] = subBuffer
            self.content += ' '

    def transferAllContent(self):
        '''Transfer all content to parent'''
        if isinstance(self.parent, FileBuffer):
            # First unreference all elements
            for index in self.getElementIndexes(expressions=False):
                del self.elements[index]
            self.evaluate(self.parent, self.env.context)
        else:
            # Transfer content in itself
            oldParentLength = self.parent.getLength()
            self.parent.write(self.content)
            # Transfer elements
            for index, podElem in self.elements.items():
                self.parent.elements[oldParentLength + index] = podElem
            # Transfer sub-buffers
            for index, buf in self.subBuffers.items():
                self.parent.subBuffers[oldParentLength + index] = buf
        # Empty the buffer
        MemoryBuffer.__init__(self, self.env, self.parent)
        # Change buffer position wrt parent
        self.parent.pushSubBuffer(self)

    def addElement(self, elem, elemType='pod'):
        if elemType == 'pod':
            elem = PodElement.create(elem)
        self.elements[self.getLength()] = elem
        if isinstance(elem, Cell) or isinstance(elem, Table):
            elem.tableInfo = self.env.getTable()
            if isinstance(elem, Cell):
                # Remember where this cell is in the table
                elem.colIndex = elem.tableInfo.curColIndex
        if elem == 'x':
            # See comment on similar statement in the method below.
            self.content += ' '

    def addExpression(self, expression, elem=None, tiedHook=None):
        '''Creates an Expression instance and add it in the buffer'''
        # Create the POD expression
        expr = Expression(expression, self.pod)
        # Get the meta-condition if found
        if elem and elem.attrs:
            metaCondition = elem.attrs.get('text:condition')
            if metaCondition and (metaCondition.lower() != 'ooow:true'):
                metaCondition = metaCondition.split(':', 1)[1]
                metaWrap = metaCondition[0]
                if (metaWrap != metaCondition[-1]) or \
                   (metaWrap not in expr.metaWraps):
                    raise ParsingError(BAD_META_CONDITION % metaCondition)
                expr.metaWrap = metaWrap
                expr.metaCondition = metaCondition.strip('"\'"')
        if tiedHook: tiedHook.tiedExpression = expr
        self.elements[self.getLength()] = expr
        # To be sure that an expr and an elem can't be found at the same index
        # in the buffer.
        self.content += ' '

    def addAttributes(self):
        '''pod-only: adds an Attributes instance into this buffer'''
        attrs = Attributes(self.env)
        self.elements[self.getLength()] = attrs
        self.content += ' '
        return attrs

    def addAttribute(self, name, expr):
        '''px-only: adds an Attribute instance into this buffer'''
        attr = Attribute(name, expr)
        self.elements[self.getLength()] = attr
        self.content += ' '
        return attr

    def _getVariables(self, expr):
        '''Returns variable definitions in p_expr as a list
           ~[(s_varName|[s_varName], s_expr)]~.'''
        r = []
        for sub in expr.strip().split(';'):
            # If the last variable definition ends with a semi-colon, it
            # produces an empty element.
            if not sub: continue
            # Do we have valid variable definitions ?
            match = self.Rex.vars_.match(sub)
            if not match:
                raise ParsingError(BAD_VAR_EXPRESSION % sub)
            # Extract individual variable definitions
            names = match.group(1).strip()
            if '*' in names:
                if len(names) > 1:
                    raise ParsingError(BAD_VAR_STAR % name)
            elif ',' in names:
                # Several variable names
                names = names.split(',')
                # Strip these names and ensure they are valid variable names
                i = 0
                while i < len(names):
                    name = names[i].strip()
                    if not self.Rex.var_.match(name):
                        raise ParsingError(BAD_VAR_NAME % name)
                    names[i] = name
                    i += 1
            r.append((names, match.group(2).strip()))
        return r

    def _getForIterators(self, iters):
        '''Gets the variables used as iterators in a "for" statement, from
           comma-separated string p_iters.'''
        r = iters.split(',')
        i = len(r) - 1
        while i >= 0:
            r[i] = r[i].strip()
            i -= 1
        return r

    def createPodAction(self, actionType, statements, statementName, subExpr,
                        podElem, minus, main=True):
        '''Creates an Action instance, depending on p_actionType'''
        if actionType == 'if':
            r = actions.If(statementName, self, subExpr, podElem, minus)
            if main:
                self.env.ifActions.append(r)
                if r.name:
                    # We must register this action as a named action
                    if r.name in self.env.namedIfActions:
                        raise ParsingError(DUPLICATE_NAMED_IF)
                    self.env.namedIfActions[r.name] = r
        elif actionType == 'else':
            if not main: raise ParsingError(ELSE_NOT_MAIN)
            if not self.env.ifActions: raise ParsingError(ELSE_WITHOUT_IF)
            # Does the "else" action reference a named "if" action?
            ifReference = subExpr.strip()
            if ifReference:
                if ifReference not in self.env.namedIfActions:
                    raise ParsingError(ELSE_WITHOUT_NAMED_IF % ifReference)
                linkedIfAction = self.env.namedIfActions[ifReference]
                # This "else" action "consumes" the "if" action: this way,
                # it is not possible to define two "else" actions related to
                # the same "if".
                del self.env.namedIfActions[ifReference]
                self.env.ifActions.remove(linkedIfAction)
            else:
                linkedIfAction = self.env.ifActions.pop()
            r = actions.Else(statementName, self, None, podElem, minus,
                             linkedIfAction)
        elif actionType == 'for':
            forRes = self.Rex.for_.match(subExpr.strip())
            if not forRes:
                raise ParsingError(BAD_FOR_EXPRESSION % subExpr)
            iters, subExpr = forRes.groups()
            iters = self._getForIterators(iters)
            r = actions.For(statementName, self, subExpr, podElem, minus, iters)
        elif actionType == 'with':
            variables = self._getVariables(subExpr)
            r = actions.Variables(statementName, self, podElem, minus,variables)
        elif actionType == 'meta-if':
            r = actions.MetaIf(self, subExpr, podElem, minus, statements)
        else:
            r = actions.Null(self, podElem)
        return r

    def createPodActions(self, statements):
        '''Tries to create action(s) based on p_statements. If the statement is
           not correct, r_ is -1. Else, r_ is the index of the element within
           the buffer that is the object of the action(s).'''
        r = -1
        try:
            # Check that the statement group is not empty
            if not statements: raise ParsingError(EMPTY_NOTE)
            # Get the main statement (starting with "do...") and check it
            main = statements[0]
            aRes = self.Rex.action.match(main)
            if not aRes:
                raise ParsingError(BAD_STATEMENT % main)
            statementName, podElem, minus, actionType, subExpr = aRes.groups()
            if not (podElem in PodElement.POD_ELEMS):
                raise ParsingError(BAD_ELEMENT % podElem)
            if minus and (not podElem in PodElement.MINUS_ELEMS):
                raise ParsingError(BAD_MINUS % (podElem,PodElement.MINUS_ELEMS))
            # Find the target element in the buffer
            i = self.getIndex(podElem)
            if i == -1:
                raise ParsingError(ELEMENT_NOT_FOUND % (podElem, str([
                        e.__class__.__name__.lower() \
                        for e in self.elements.values()])))
            podElem = self.elements[i]
            # Create the main action
            self.action = self.createPodAction(actionType, statements,
              statementName, subExpr, podElem, minus)
            # Parse the remaining statements, that can contain any number of
            # secondary actions and a from clause.
            fromClause = last = None
            for statement in statements[1:]:
                # Get the "from" clause
                if statement.startswith('from') or \
                   statement.startswith('from+'):
                    fromInfo = self.Rex.from_.match(statement)
                    if not fromInfo:
                        raise ParsingError(BAD_FROM_CLAUSE % fromClause)
                    fromClause = fromInfo.groups()
                # Get any secondary statement
                else:
                    info = self.Rex.subAction.match(statement)
                    if not info:
                        raise ParsingError(BAD_SUB_STATEMENT % statement)
                    actionType, subExpr = info.groups()
                    last = self.createPodAction(actionType, statements, '',
                                             subExpr, podElem, None, main=False)
                    self.action.addSubAction(last)
            # Link the "from" clause
            if fromClause:
                target = last or self.action
                target.setFrom(*fromClause)
            success, msg = self.action.check()
            if not success: raise ParsingError(msg)
            r = i
        except ParsingError as ppe:
            PodError.dump(self, str(ppe), removeFirstLine=True)
        return r

    def createPxAction(self, elem, actionType, statement):
        '''Creates a PX action and link it to this buffer. If an action is
           already linked to this buffer (in self.action), this action is
           chained behind the last action via self.action.subAction.'''
        res = 0
        statement = statement.strip()
        if actionType == 'for':
            forRes = self.Rex.for_.match(statement)
            if not forRes:
                raise ParsingError(BAD_FOR_EXPRESSION % statement)
            iters, subExpr = forRes.groups()
            iters = self._getForIterators(iters)
            action = actions.For('for', self, subExpr, elem, False, iters)
        elif actionType == 'if':
            action = actions.If('if', self, statement, elem, False)
        elif actionType in ('var', 'var2'):
            variables = self._getVariables(statement)
            action = actions.Variables('var', self, elem, False, variables)
        # Is it the first action for this buffer or not?
        if not self.action:
            self.action = action
        else:
            self.action.addSubAction(action)
        return res

    def cut(self, index, keepFirstPart):
        '''Cuts this buffer into 2 parts. Depending on p_keepFirstPart, the 1st
        (from 0 to index-1) or the second (from index to the end) part of the
        buffer is returned as a MemoryBuffer instance without parent; the other
        part is self.'''
        res = MemoryBuffer(self.env, None)
        # Manage buffer meta-info (elements, expressions, subbuffers)
        subBuffersToDelete = []
        elementsToDelete = []
        mustShift = False
        for itemIndex, item in BufferIterator(self):
            if keepFirstPart:
                if itemIndex >= index:
                    newIndex = itemIndex-index
                    if isinstance(item, MemoryBuffer):
                        res.subBuffers[newIndex] = item
                        subBuffersToDelete.append(itemIndex)
                    else:
                        res.elements[newIndex] = item
                        elementsToDelete.append(itemIndex)
            else:
                if itemIndex < index:
                    if isinstance(item, MemoryBuffer):
                        res.subBuffers[itemIndex] = item
                        subBuffersToDelete.append(itemIndex)
                    else:
                        res.elements[itemIndex] = item
                        elementsToDelete.append(itemIndex)
                else:
                    mustShift = True
        if elementsToDelete:
            for elemIndex in elementsToDelete:
                del self.elements[elemIndex]
        if subBuffersToDelete:
            for subIndex in subBuffersToDelete:
                del self.subBuffers[subIndex]
        if mustShift:
            elements = {}
            for elemIndex, elem in self.elements.items():
                elements[elemIndex-index] = elem
            self.elements = elements
            subBuffers = {}
            for subIndex, buf in self.subBuffers.items():
                subBuffers[subIndex-index] = buf
            self.subBuffers = subBuffers
        # Manage content
        if keepFirstPart:
            res.write(self.content[index:])
            self.content = self.content[:index]
        else:
            res.write(self.content[:index])
            self.content = self.content[index:]
        return res

    def getElementIndexes(self, expressions=True):
        res = []
        for index, elem in self.elements.items():
            condition = isinstance(elem, Expression) or \
                        isinstance(elem, Attributes)
            if not expressions:
                condition = not condition
            if condition:
                res.append(index)
        return res

    def transferActionIndependentContent(self, actionElemIndex):
        # Manage content to transfer to parent buffer
        if actionElemIndex != 0:
            actionIndependentBuffer = self.cut(actionElemIndex,
                                               keepFirstPart=False)
            actionIndependentBuffer.parent = self.parent
            actionIndependentBuffer.transferAllContent()
            self.parent.pushSubBuffer(self)
        # Manage content to transfer to a child buffer
        actionElemIndex = self.getIndex(
            self.action.elem.__class__.__name__.lower())
        # We recompute actionElemIndex because after cut it may have changed
        elemIndexes = self.getElementIndexes(expressions=False)
        elemIndexes.sort()
        if elemIndexes.index(actionElemIndex) != (len(elemIndexes)-1):
            # I must create a sub-buffer with the impactable elements after
            # the action-related element
            childBuffer = self.cut(elemIndexes[elemIndexes.index(
                actionElemIndex)+1], keepFirstPart=True)
            self.addSubBuffer(childBuffer)
            res = childBuffer
        else:
            res = self
        return res

    def getStartIndex(self, removeMainElems):
        '''When I must dump the buffer, sometimes (if p_removeMainElems is
        True), I must dump only a subset of it. This method returns the start
        index of the buffer part I must dump.'''
        if not removeMainElems: return 0
        # Find the start position of the deepest element to remove
        deepestElem = self.action.elem.DEEPEST_TO_REMOVE
        pos = self.content.find('<%s' % deepestElem.nsName)
        pos = pos + len(deepestElem.nsName)
        # Now we must find the position of the end of this start tag,
        # skipping potential attributes.
        inAttrValue = False # Are we parsing an attribute value ?
        endTagFound = False # Have we found the end of this tag ?
        while not endTagFound:
            pos += 1
            nextChar = self.content[pos]
            if (nextChar == '>') and not inAttrValue:
                # Yes we have it
                endTagFound = True
            elif nextChar == '"':
                inAttrValue = not inAttrValue
        return pos + 1

    def getStopIndex(self, removeMainElems):
        '''This method returns the stop index of the buffer part I must dump.'''
        if removeMainElems:
            ns = self.env.namespaces
            deepestElem = self.action.elem.DEEPEST_TO_REMOVE
            pos = self.content.rfind('</%s>' % deepestElem.getFullName(ns))
            res = pos
        else:
            res = self.getLength()
        return res

    def removeAutomaticExpressions(self):
        '''When a buffer has an action with minus=True, we must remove the
           expressions automatically inserted by pod ("columnsRepeat"
           "cellProtected"...) . Else, we will have problems when computing the
           index of the part to keep (m_getStartIndex).'''
        # Find the position of the end of the starting element of the deepest
        # element to remove.
        deepestElem = self.action.elem.DEEPEST_TO_REMOVE
        pos = self.content.find('<%s' % deepestElem.nsName)
        pos = self.content.find('>', pos)
        for index in list(self.elements.keys()):
            if index < pos: del(self.elements[index])

    reTagContent = re.compile('<(?P<p>[\w-]+):(?P<f>[\w-]+)(.*?)>.*</(?P=p):' \
                              '(?P=f)>', re.S)
    def evaluate(self, result, context, subElements=True,
                 removeMainElems=False):
        '''Evaluates this buffer given the current p_context and add the result
           into p_result. With pod, p_result is the root file buffer; with px
           it is a memory buffer.'''
        if not subElements:
            # Dump the root tag in this buffer, but not its content
            res = self.reTagContent.match(self.content.strip())
            if not res: result.write(self.content)
            else:
                g = res.group
                g1, g2, g3 = g(1), g(2), g(3)
                if self.env.parser.caller.protection and (g2 == 'table-cell'):
                    # Attribute "protected" must be removed
                    g3 = g3.replace('table:protected=" "', '')
                r = '<%s:%s%s></%s:%s>' % (g1, g2, g3, g1, g2)
                result.write(r)
        else:
            if removeMainElems: self.removeAutomaticExpressions()
            currentIndex = self.getStartIndex(removeMainElems)
            for index, evalEntry in BufferIterator(self):
                result.write(self.content[currentIndex:index])
                currentIndex = index + 1
                if isinstance(evalEntry, Expression):
                    try:
                        res, escape = evalEntry.evaluate(context)
                        if escape: result.dumpContent(res)
                        else: result.write(res)
                    except actions.EvaluationError as e:
                        # This exception has already been treated (see the 
                        # "except" block below). Simply re-raise it when needed.
                        if self.env.raiseOnError: raise e
                    except Exception as e:
                        if not self.env.raiseOnError:
                            PodError.dump(result, EVAL_EXPR_ERROR % (
                                          evalEntry.expr, e))
                        else:
                            raise actions.EvaluationError(e, EVAL_EXPR_ERROR % \
                                        (evalEntry.expr, '\n'+Traceback.get(5)))
                elif isinstance(evalEntry, Attributes) or \
                     isinstance(evalEntry, Attribute):
                    result.write(evalEntry.evaluate(context))
                else: # It is a subBuffer
                    if evalEntry.action:
                        evalEntry.action.execute(result, context)
                    else:
                        result.write(evalEntry.content)
            stopIndex = self.getStopIndex(removeMainElems)
            if currentIndex < (stopIndex-1):
                result.write(self.content[currentIndex:stopIndex])

    def clean(self):
        '''Cleans the buffer content'''
        self.content = ''
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
