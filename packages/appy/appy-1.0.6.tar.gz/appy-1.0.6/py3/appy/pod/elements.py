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
from xml.sax.saxutils import quoteattr

from appy.xml import Tag
from appy.pod import PodError, Evaluator
from appy.pod.odf_parser import OdfEnvironment as ns

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class PodElement:
    OD_TO_POD = {'p': 'Text', 'h': 'Title', 'list-item': 'Item',
                 'section': 'Section', 'table': 'Table', 'table-row': 'Row',
                 'table-cell': 'Cell', None: 'Expression', 'frame': 'Frame'}
    POD_ELEMS = ('text', 'title', 'item', 'section', 'table', 'row', 'cell',
                 'frame')
    subTags = []

    # Elements for which the '-' operator can be applied
    MINUS_ELEMS = ('section', 'table')

    @staticmethod
    def create(elem):
        '''Used to create any POD elem that has an equivalent OD element. Not
           for creating expressions, for example.'''
        return eval(PodElement.OD_TO_POD[elem])()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Text(PodElement):
    OD = Tag('p', nsUri=ns.NS_TEXT)
    # When generating an error we may need to surround it with a given tag and
    # sub-tags.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Title(PodElement):
    OD = Tag('h', nsUri=ns.NS_TEXT)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Item(PodElement):
    OD = Tag('list-item', nsUri=ns.NS_TEXT)
    subTags = [Text.OD]

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Section(PodElement):
    OD = Tag('section', nsUri=ns.NS_TEXT)
    subTags = [Text.OD]
    # When we must remove the Section element from a buffer, the deepest element
    # to remove is the Section element itself.
    DEEPEST_TO_REMOVE = OD

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Cell(PodElement):
    OD = Tag('table-cell', nsUri=ns.NS_TABLE)
    subTags = [Text.OD]
    def __init__(self):
        self.tableInfo = None # ~OdTable~
        self.colIndex = None # The column index for this cell, within its table.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Row(PodElement):
    OD = Tag('table-row', nsUri=ns.NS_TABLE)
    subTags = [Cell.OD, Text.OD]

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Table(PodElement):
    OD = Tag('table', nsUri=ns.NS_TABLE)
    subTags = [Row.OD, Cell.OD, Text.OD]
    # When we must remove the Table element from a buffer, the deepest element
    # to remove is the Cell (it can only be done for one-row, one-cell tables).
    DEEPEST_TO_REMOVE = Cell.OD
    def __init__(self):
        self.tableInfo = None # ~OdTable~

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Frame(PodElement):
    OD = Tag('frame', nsUri=ns.NS_DRAW)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Expression(PodElement):
    '''Represents a Python expression that is found in a pod or px.'''
    OD = None
    metaWraps = {'"': '&quot;', "'": '&apos;'}

    def extractInfo(self, py):
        '''Within p_py, several elements can be included:
           - the fact that XML chars must be escaped or not (leading ":")
           - the "normal" Python expression,
           - an optional "error" expression, that is evaluated when the normal
             expression raises an exception.
           This method return a tuple (escapeXml, normaExpr, errorExpr).'''
        # Determine if we must escape XML chars or not.
        escapeXml = True
        if py.startswith(':'):
            py = py[1:]
            escapeXml = False
        # Extract normal and error expression
        if '|' not in py:
            expr = py
            errorExpr = None
        else:
            expr, errorExpr = py.rsplit('|', 1)
            expr = expr.strip()
            errorExpr = errorExpr.strip()
        return escapeXml, expr, errorExpr

    def __init__(self, py, pod):
        # Extract parts from expression p_py
        self.escapeXml, self.expr, self.errorExpr = self.extractInfo(py.strip())
        self.pod = pod # True if I work for pod, False if I work for px
        if self.pod:
            # pod-only: store here the expression's true result (before being
            # converted to a string).
            self.result = None
            # pod-only: the following bool indicates if this Expression instance
            # has already been evaluated or not. Expressions which are tied to
            # attribute hooks are already evaluated when the tied hook is
            # evaluated: this boolean prevents the expression from being
            # evaluated twice.
            self.evaluated = False
            # self.result and self.evaluated are not used by PX, because they
            # are not thread-safe.
        # The "meta-condition" is a Python expression. If it evaluates to True,
        # the expression will really be evaluated and its result will be dumped
        # in the result. Else, the expression will be left untouched and go
        # unevaluated in the result.
        self.metaCondition = None
        # Te meta-condition is "wrapped" around single or double quotes
        self.metaWrap = None

    def getUnevaluatedExpression(self):
        '''Gets the expression in its unevaluated form'''
        if not self.pod: return '' # Works just for pod
        wrap = self.metaWraps[self.metaWrap]
        res = '<text:conditional-text text:condition="ooow:%s%s%s" ' \
               'text:string-value-if-true="%s" ' \
               'text:string-value-if-false="">%s</text:conditional-text>' % \
               (wrap, self.metaCondition, wrap, self.expr, self.expr)
        return res

    def _eval(self, context):
        '''Evaluates self.expr with p_context. If self.errorExpr is defined,
           evaluate it if self.expr raises an error.'''
        if self.errorExpr:
            try:
                r = Evaluator.run(self.expr, context)
            except Exception:
                r = Evaluator.run(self.errorExpr, context)
        else:
            r = Evaluator.run(self.expr, context)
        return r

    def _evalMetaCondition(self, context):
        '''Checks whether the expression really needs to be evaluated'''
        # If no meta-condition is present, the expression must be evaluated
        expr = self.metaCondition
        if expr is None: return True
        # Evaluate the meta-condition
        return Evaluator.run(expr, context)

    def evaluate(self, context):
        '''Evaluates the Python expression (self.expr) with a given
           p_context, and returns the result. More precisely, it returns a
           tuple (result, escapeXml). Boolean escapeXml indicates if XML chars
           must be escaped or not.'''
        # Preamble: evaluate the meta-condition
        if not self._evalMetaCondition(context):
            # We must dump the expression unevaluated
            return self.getUnevaluatedExpression(), False
        escapeXml = self.escapeXml
        # Evaluate the expression, or get it from self.result if it has already
        # been computed.
        if self.pod and self.evaluated:
            res = self.result
            # It can happen only once, to ask to evaluate an expression that
            # was already evaluated (from the tied hook). We reset here the
            # boolean "evaluated" to allow for the next evaluation, probably
            # with another context.
            self.evaluated = False
        else:
            res = self._eval(context)
            # pod-only: cache the expression result
            if self.pod: self.result = res
        # Converts the expr result to a string that can be inserted in the
        # pod/px result.
        resultType = res.__class__.__name__
        if resultType == 'NoneType':
            res = ''
        elif resultType == 'Px':
            # A PX that must be called within the current PX. Call it with the
            # current context.
            res = res(context, applyTemplate=False)
            # Force escapeXml to False
            escapeXml = False
        elif resultType != 'str':
            # "str" is the target type
            res = str(res)
        return res, escapeXml

    def __repr__(self):
        '''String representation for an expression'''
        res = self.expr
        if self.errorExpr: res += '|%s' % self.errorExpr
        if self.escapeXml: res = ':' + res
        if self.metaCondition: res += '[MC=%s]' % self.metaCondition
        name = self.pod and 'Pod' or 'Px'
        return '<%sExpr %s>' % (name, res)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Attributes(PodElement):
    '''Represents a bunch of XML attributes that will be dumped for a given tag
       in the result. pod-only.'''
    OD = None
    floatTypes = ('int', 'long', 'float')
    dateTypes = ('DateTime', 'datetime')
    dateFormats = {True: '%Y-%m-%dT%H:%M:%S', False: '%Y-%m-%d'}

    def __init__(self, env):
        self.attrs = {}
        # Depending on the result of a tied expression, we will dump, for
        # another tag, the series of attrs that this instance represents.
        self.tiedExpression = None
        # We will need the env to get the full names of attributes to dump.
        self.env = env

    def computeAttributes(self, expr):
        '''p_expr has been evaluated: its result is in expr.result. Depending
           on its type, we will dump the corresponding attributes in
           self.attrs.'''
        exprType = expr.result.__class__.__name__
        attrs = self.attrs
        if exprType in self.floatTypes:
            attrs['office:value-type'] = 'float'
            attrs['office:value'] = str(expr.result)
        elif exprType in self.dateTypes:
            attrs['office:value-type'] = 'date'
            # Apply a different formatting if the date has a "time" part
            d = expr.result
            noTime = d._second == d._minute == d._hour == 0
            fmt = Attributes.dateFormats[not noTime]
            attrs['office:date-value'] = d.strftime(fmt)
        else:
            attrs['office:value-type'] = 'string'

    def evaluate(self, context):
        # Evaluate first the tied expression, in order to determine its type.
        try:
            self.tiedExpression.evaluate(context)
            self.tiedExpression.evaluated = True
        except Exception as e:
            # Don't set "evaluated" to True. This way, when the buffer will
            # evaluate the expression directly, we will really evaluate it, so
            # the error will be dumped into the pod result.
            pass
        # Analyse the return type of the expression.
        self.computeAttributes(self.tiedExpression)
        # Now, self.attrs has been populated. Transform it into a string.
        res = ''
        for name, value in self.attrs.items():
            res += ' %s=%s' % (name, quoteattr(value))
        return res

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Attribute(PodElement):
    '''Represents an HTML special attribute like "selected" or "checked".
       px-only.'''
    OD = None

    def __init__(self, name, expr):
        # The name of the attribute
        self.name = name
        # The expression that will compute the attribute value
        self.expr = expr.strip()

    def evaluate(self, context):
        # If the expr evaluates to False, we do not dump the attribute at all.
        if Evaluator.run(self.expr, context):
            return ' %s="%s"' % (self.name, self.name)
        return ''
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
