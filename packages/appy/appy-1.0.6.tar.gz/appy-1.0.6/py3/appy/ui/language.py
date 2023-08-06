'''Manages the user interface language'''

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
from appy.px import Px
from appy.data import Languages
from appy.utils import noSwitchLayouts

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Language:
    '''Manages the language for the user interface'''
    traverse = {}

    # This static attribute will store the unique appy.data.Languages instance
    languages = None

    @classmethod
    def getIsoLanguages(class_):
        '''Returns p_class_.languages or create it if it does not exist yet'''
        r = class_.languages
        if r: return r
        class_.languages = Languages()
        return class_.languages

    @classmethod
    def showSelector(class_, config, layout):
        '''We must show the language selector if the p_config requires it and if
           there is more than 2 supported languages. Moreover, on some layouts,
           switching the language is not allowed.'''
        if not config.languageSelector or config.forcedLanguage: return
        if len(config.languages) < 2: return
        return layout not in noSwitchLayouts

    @classmethod
    def getName(class_, code, lowerize=False):
        '''Gets the language name (in this language) from a 2-chars language
           p_code.'''
        r = class_.getIsoLanguages().get(code)[2]
        if not lowerize: return r
        return r.lower()

    traverse['switch'] = True
    @classmethod
    def switch(class_, o):
        '''Switch the user interface to the language as specified in the
           request.'''
        # Set the language cookie with the new language and go back to the
        # referer or to the app's home page.
        H = o.H()
        resp = H.resp
        resp.setCookie('AppyLanguage', H.req.language)
        resp.goto(H.headers['Referer'] or H.config.server.getUrl(H))

    @classmethod
    def flip(class_, align, dir):
        '''Flip p_align(ment) if p_dir indicates a right-to-left language'''
        if dir == 'ltr': return align
        if align == 'left': return 'right'
        if align == 'right': return 'left'
        return align

    # PX for selecting the language in the ui
    pxSelector = Px('''
      <select var="languages=config.ui.selectableLanguages or \
                     config.ui.languages;
                   defaultLanguage=languages[0]"
              onchange=":'switchLanguage(this,%s)' % q(siteUrl)">
       <option for="lg in languages" value=":lg"
               selected=":lang == lg">:ui.Language.getName(lg)</option>
      </select>''',

      js='''
       function switchLanguage(select, siteUrl) {
         goto(siteUrl + '/tool/ui/Language/switch?language=' + select.value);}
      ''')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
