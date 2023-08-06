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
import time
from appy.utils import Traceback

# Some POD-specific constants  - - - - - - - - - - - - - - - - - - - - - - - - -
XHTML_HEADINGS = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6')
XHTML_LISTS = ('ol', 'ul')
# "para" is a meta-tag representing p, div, blockquote or address
XHTML_PARA_TAGS = XHTML_HEADINGS + ('p', 'div', 'blockquote', 'address', 'para')
XHTML_INNER_TAGS = ('b', 'i', 'u', 'em', 'span')
XHTML_UNSTYLABLE_TAGS = ('li', 'a')
XHTML_META_TAGS = {'p': 'para', 'div': 'para',
                   'blockquote': 'para', 'address': 'para'}
# Cell-like tags (including "li")
XHTML_CELL_TAGS = ('th', 'td', 'li')

# Default output formats for POD templates, by template type
formatsByTemplate = {'.odt': ('pdf', 'doc', 'docx', 'odt'),
                     '.ods': ('xls', 'xlsx', 'ods')}

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Evaluator:
    '''Wrapper around the built-in Python function "eval"'''
    # When evaluating a Python expression, pod will use the built-in "eval"
    # function, like this:
    #             eval(expression, emptyContext, podContext)
    # "emptyContext" is the following variable: an empty dict.
    emptyContext = {}
    # "podContext" is the current pod context.

    @classmethod
    def run(class_, expression, context):
        '''Evaluates p_expression in this p_context'''
        # p_context may be a dict or an instance of appy.model.utils.Object. In
        # this latter case, although it implements dict-like methods, it cannot
        # be used as-is as local context. Indeed, it does not raise a KeyError
        # when a key lookup produces no result, but returns None instead. So,
        # for any non-local name, the "eval" function believes it has been found
        # in the local mapping, with value being None. This is why we unwrap the
        # __dict__ behind a context being an instance of
        # appy.model.utils.Object.
        context = context if isinstance(context, dict) else context.__dict__
        # Evaluate p_expression
        return eval(expression, class_.emptyContext, context)
        # Note that, after the first execution of function "eval", the function
        # adds, within "emptyDict", a key '__builtins__' containing all the
        # Python built-ins, similarly to the homonym entry in dict globals().

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class PodError(Exception):
    @staticmethod
    def dumpTraceback(buffer, tb, removeFirstLine):
        # If this error came from an exception raised by pod (p_removeFirstLine
        # is True), the text of the error may be very long, so we avoid having
        # it as error cause + in the first line of the traceback.
        linesToRemove = removeFirstLine and 3 or 2
        i = 0
        for tLine in tb.splitlines():
            i += 1
            if i > linesToRemove:
                buffer.write('<text:p>')
                try:
                    buffer.dumpContent(tLine)
                except UnicodeDecodeError:
                    buffer.dumpContent(tLine.decode('utf-8'))
                buffer.write('</text:p>')

    @staticmethod
    def dump(buffer, message, withinElement=None, removeFirstLine=False,
             dumpTb=True, escapeMessage=True):
        '''Dumps the error p_message in p_buffer or in r_ if p_buffer is None'''
        if withinElement:
            buffer.write('<%s>' % withinElement.OD.nsName)
            for subTag in withinElement.subTags:
                buffer.write('<%s>' % subTag.nsName)
        buffer.write('<office:annotation><dc:creator>POD</dc:creator>' \
          '<dc:date>%s</dc:date><text:p>' % time.strftime('%Y-%m-%dT%H:%M:%S'))
        if escapeMessage:
            buffer.dumpContent(message)
        else:
            buffer.write(message)
        buffer.write('</text:p>')
        if dumpTb:
            # We don't dump the traceback if it is an expression error (it is
            # already included in the error message).
            PodError.dumpTraceback(buffer, Traceback.get(), removeFirstLine)
        buffer.write('</office:annotation>')
        if withinElement:
            subTags = withinElement.subTags[:]
            subTags.reverse()
            for subTag in subTags:
                buffer.write('</%s>' % subTag.nsName)
            buffer.write('</%s>' % withinElement.OD.nsName)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
