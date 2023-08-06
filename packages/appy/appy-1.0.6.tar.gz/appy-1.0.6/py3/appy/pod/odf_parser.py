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
from appy.xml import Environment, Parser

class OdfEnvironment(Environment):
    '''This environment is specific for parsing ODF files.'''
    # URIs of namespaces found in ODF files
    NS_OFFICE = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'
    NS_STYLE = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'
    NS_TEXT = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
    NS_TABLE = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
    NS_DRAW = 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0'
    NS_FO = 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'
    NS_XLINK = 'http://www.w3.org/1999/xlink'
    NS_DC = 'http://purl.org/dc/elements/1.1/'
    NS_META = 'urn:oasis:names:tc:opendocument:xmlns:meta:1.0'
    NS_NUMBER = 'urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0'
    NS_SVG = 'urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0'
    NS_CHART = 'urn:oasis:names:tc:opendocument:xmlns:chart:1.0'
    NS_DR3D = 'urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0'
    NS_MATH = 'http://www.w3.org/1998/Math/MathML'
    NS_FORM = 'urn:oasis:names:tc:opendocument:xmlns:form:1.0'
    NS_SCRIPT = 'urn:oasis:names:tc:opendocument:xmlns:script:1.0'
    NS_OOO = 'http://openoffice.org/2004/office'
    NS_OOOW = 'http://openoffice.org/2004/writer'
    NS_OOOC = 'http://openoffice.org/2004/calc'
    NS_DOM = 'http://www.w3.org/2001/xml-events'
    NS_XFORMS = 'http://www.w3.org/2002/xforms'
    NS_XSD = 'http://www.w3.org/2001/XMLSchema'
    NS_XSI = 'http://www.w3.org/2001/XMLSchema-instance'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class OdfParser(Parser):
    '''XML parser that is specific for parsing ODF files'''
    def __init__(self, env=None, caller=None):
        env = env or OdfEnvironment()
        Parser.__init__(self, env, caller)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
