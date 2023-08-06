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
from appy.xml import Parser
from appy.utils.string import Normalize

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
EXTRACTOR_WRONG_PARAMS = "You can't have both 'keepCRs' and 'normalize' " \
  "being True. Normalizing implies CRs to be removed."

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Extractor(Parser):
    '''Produces a text version of XML/XHTML content'''
    # There are 2 main usages to this parser. It can extract text:
    # - to produce a complete but textual version of some XHTML chunk, keeping
    #   accented chars and carriage returns;
    # - to extract text for search purposes, converting any accented char to its
    #   non-accented counterpart and removing any other element.

    paraTags = ('p', 'li', 'center', 'div', 'blockquote')

    def __init__(self, keepCRs=True, normalize=False, lower=True,
                       keepDashes=False, raiseOnError=False):
        Parser.__init__(self, raiseOnError=raiseOnError)
        # Must we keep carriage returns (and thus keep the global splitting of
        # the text into paragraphs) ?
        self.keepCRs = keepCRs
        # Must text be normalized ? When True, every accented char is converted
        # to its non-accented counterpart.
        self.normalize = normalize
        # Is is not possible to have both p_keepCRs and p_normalize being True
        if keepCRs and normalize: raise Exception(EXTRACTOR_WRONG_PARAMS)
        # Must be lowerise text ? (only if p_normalize is True)
        self.lower = lower
        # Must we keep dashes ? (only if p_normalize is True)
        self.keepDashes = keepDashes

    def startDocument(self):
        Parser.startDocument(self)
        self.r = []

    def endDocument(self):
        sep = '' if self.keepCRs else ' '
        self.r = sep.join(self.r)
        return Parser.endDocument(self)

    def characters(self, content):
        if self.normalize:
            content = Normalize.text(content, lower=self.lower,
                                     keepDash=self.keepDashes)
            if len(content) <= 1: return
        else:
            # Even if we must keep CRs, those encountered here are not
            # significant.
            content = content.replace('\n', ' ')
        self.r.append(content)

    def startElement(self, name, attrs):
        '''In "non-normalizing" mode, dumps a carriage return every time a "br"
           tag is encountered'''
        if self.keepCRs and (name == 'br'): self.r.append('\n')

    def endElement(self, name):
        '''In "non-normalizing" mode, dumps a carriage return every time a
           paragraph is encountered.'''
        if self.keepCRs and (name in Extractor.paraTags): self.r.append('\n')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
