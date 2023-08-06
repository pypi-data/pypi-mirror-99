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
import re

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Escape:
    '''Escapes XML chars within strings'''

    # Escaping consists in replacing special chars used by the XML language by
    # replacement entities that can be used in the content of XML tags and
    # attributes. This class does it for various XML flavours:
    # --------------------------------------------------------------------------
    #   "odf"    | Open Document Format - The XML format for LibreOffice files
    #  "xhtml"   | The XML-compliant version of HTML
    #   "xml"    | Any other XML flavour
    # --------------------------------------------------------------------------
    # Base chars to escape
    chars = '<>&"'
    # For some XML flavours we escape "blanks" as well
    blanks = '\n\t\r'
    # Base regular expression matching these chars
    rex = re.compile('[%s]' % chars)
    # Regular expression also matching the single quote (less used)
    rexApos = re.compile("[%s']" % chars)
    # Regular expression also matching carriage returns and tabs (= "blanks")
    rexBlanks = re.compile('[%s%s]' % (chars, blanks))
    rexBlanksApos = re.compile("[%s'%s]" % (chars, blanks))
    # All regular expressions, grouped by flavour and 'apos' escaping or not
    nonXmlRex = { False: rexBlanks, True: rexBlanksApos }
    rexAll = {'xml': { False: rex, True: rexApos },
              'odf': nonXmlRex,
              'odf*': nonXmlRex,
              'xhtml': nonXmlRex }
    # Entities to use to escape base chars
    entities = {'<':'&lt;', '>':'&gt;', '&':'&amp;', '"':'&quot;', "'":'&apos;'}
    # For "odf" and "xhtml" flavours, we replace "blank" chars with their
    # counterparts in these flavours as well.
    values = {
     # While using an additional "text:tab" when replacing "\n" chars for
     # conversion to ODF solves problems with justified text, it causes problems
     # when converting the result to Microsoft Word. This is why there are 2
     # possibilities for ODF.
     'odf': {'\n':'<text:line-break/>', '\t':'<text:tab/>', '\r':''},
     'odf*':{'\n':'<text:tab/><text:line-break/>', '\t':'<text:tab/>', '\r':''},
     'xhtml': {'\n':'<br/>', '\t':'', '\r':''},
     'xml': {} # We do not escape blanks by default
    }
    # Complete "values" with entities
    for value in values.values(): value.update(entities)

    @staticmethod
    def xml(s, flavour='xml', escapeApos=False):
        '''Returns p_s, whose XML special chars have been replaced with XML
           entities. You can perform escaping for a specific XML flavour: "odf"
           or "xhtml" (see doc in class Escape) or use the default flavour
           "xml".

           Most of the time, we do not escape 'apos' (there is no particular
           need for that), excepted if p_escapeApos is True.'''
        # Choose the regular expression to use depending on parameters
        rex = Escape.rexAll[flavour][escapeApos]
        # Define the function to use to choose the replacement value depending
        # on the matched char.
        fun = lambda match: Escape.values[flavour][match.group(0)]
        # Apply it
        return rex.sub(fun, s)

    @staticmethod
    def xhtml(s):
        '''Shorthand for escaping XHTML content'''
        return Escape.xml(s, flavour='xhtml')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
