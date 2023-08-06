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
from appy.data import rtlLanguages

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Languages:
    '''Manages user language-related elements'''

    @classmethod
    def getDirection(self, lang):
        '''Determines if p_lang is a LTR (left-to-right) or RTL (right-to-left)
           language.'''
        # It returns a 3-tuple  (dir, dleft, dright)
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # dir    | String "ltr" for a left-to-right language, "rtl" for a
        #        | right-to-left language;
        # dleft  | String "left" for a LTR and "right" for a RTL language
        # dright | String "right" for a LTR and "left" for a RTL language
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        isRtl = lang in rtlLanguages
        return ('rtl', 'right', 'left') if isRtl else ('ltr', 'left', 'right')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
