# -*- coding: utf-8 -*-

'''This folder contains copies of external, "authentic" data, stored as text
   files, like ISO 3166-1 country codes. In this package, corresponding Python
   classes are available for accessing the data in the text files.'''

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

# Languages names in their own language  - - - - - - - - - - - - - - - - - - - - 
nativeNames = {
  'aa' : 'магIарул мацI',
  'ab' : 'бызшәа',
  'af' : 'Afrikaans',
  'am' : 'አማርኛ',
  'ar' : 'العربية',
  'as' : 'অসমিয়া',
  'ay' : 'Aymara',
  'az' : 'Azəri Türkçəsi',
  'ba' : 'Bashkir',
  'be' : 'Беларускі',
  'bg' : 'Български',
  'bh' : 'Bihari',
  'bi' : 'Bislama',
  'bn' : 'বাংলা',
  'bo' : 'བོད་སྐད་',
  'bs' : 'Bosanski',
  'br' : 'Brezhoneg',
  'ca' : 'Català',
  'ch' : 'Chamoru',
  'co' : 'Corsu',
  'cs' : 'Čeština',
  'cy' : 'Cymraeg',
  'da' : 'Dansk',
  'de' : 'Deutsch',
  'dz' : 'རྫོང་ཁ',
  'el' : 'Ελληνικά',
  'en' : 'English',
  'eo' : 'Esperanto',
  'es' : 'Español',
  'et' : 'Eesti',
  'eu' : 'Euskara',
  'fa' : 'فارسی',
  'fi' : 'Suomi',
  'fj' : 'Fiji',
  'fo' : 'Føroyska',
  'fr' : 'Français',
  'fy' : 'Frysk',
  'ga' : 'Gaeilge',
  'gd' : 'Gàidhlig',
  'gl' : 'Galego',
  'gn' : 'Guarani',
  'gu' : 'ગુજરાતી',
  'gv' : 'Gaelg',
  'ha' : 'هَوُس',
  'he' : 'עברית',
  'hi' : 'हिंदी',
  'hr' : 'Hrvatski',
  'hu' : 'Magyar',
  'hy' : 'Հայերէն',
  'ia' : 'Interlingua',
  'id' : 'Bahasa Indonesia',
  'ie' : 'Interlingue',
  'ik' : 'Inupiak',
  'is' : 'Íslenska',
  'it' : 'Italiano',
  'iu' : 'ᐃᓄᒃᑎᑐᑦ',
  'ja' : '日本語',
  'jbo': 'lojban',
  'jw' : 'Basa Jawi',
  'ka' : 'ქართული',
  'kk' : 'ﻗﺎﺯﺍﻗﺸﺎ',
  'kl' : 'Greenlandic',
  'km' : 'ខ្មែរ',
  'kn' : 'ಕನ್ನಡ',
  'ko' : '한국어',
  'ks' : 'काऽशुर',
  'ku' : 'Kurdí',
  'kw' : 'Kernewek',
  'ky' : 'Кыргыз',
  'la' : 'Latin',
  'lb' : 'Lëtzebuergesch',
  'li' : 'Limburgs',
  'ln' : 'Lingala',
  'lo' : 'ພາສາລາວ',
  'lt' : 'Lietuviskai',
  'lv' : 'Latviešu',
  'mg' : 'Malagasy',
  'mi' : 'Maori',
  'mk' : 'Македонски',
  'ml' : 'മലയാളം',
  'mn' : 'Монгол',
  'mo' : 'Moldavian',
  'mr' : 'मराठी',
  'ms' : 'Bahasa Melayu',
  'mt' : 'Malti',
  'my' : 'Burmese',
  'na' : 'Nauru',
  'ne' : 'नेपाली',
  'nl' : 'Nederlands',
  'no' : 'Norsk',
  'nn' : 'Nynorsk',
  'oc' : 'Languedoc',
  'om' : 'Oromo',
  'or' : 'ଓଡ଼ିଆ',
  'pa' : 'ਪੰਜਾਬੀ',
  'pl' : 'Polski',
  'ps' : 'پښتو',
  'pt' : 'Português',
  'qu' : 'Quechua',
  'rm' : 'Rumantsch',
  'rn' : 'Kirundi',
  'ro' : 'Română',
  'ru' : 'Русский',
  'rw' : 'Kiyarwanda',
  'sa' : 'संस्कृत',
  'sd' : 'Sindhi',
  'se' : 'Northern Sámi',
  'sg' : 'Sangho',
  'sh' : 'Serbo-Croatian',
  'si' : 'Singhalese',
  'sk' : 'Slovenčina',
  'sl' : 'Slovenščina',
  'sm' : 'Samoan',
  'sn' : 'Shona',
  'so' : 'Somali',
  'sq' : 'Shqip',
  'sr' : 'српски',
  'ss' : 'Siswati',
  'st' : 'Sesotho',
  'su' : 'Sudanese',
  'sv' : 'Svenska',
  'sw' : 'Kiswahili',
  'ta' : 'தமிழ',
  'te' : 'తెలుగు',
  'tg' : 'Тоҷики',
  'th' : 'ไทย',
  'ti' : 'ትግርኛ',
  'tk' : 'түркmенче',
  'tl' : 'Tagalog',
  'tn' : 'Setswana',
  'to' : 'Lea faka-Tonga',
  'tr' : 'Türkçe',
  'ts' : 'Tsonga',
  'tt' : 'татарча',
  'tw' : 'Twi',
  'ug' : 'Uigur',
  'uk' : 'Українська',
  'ur' : 'اردو',
  'uz' : 'Ўзбекча',
  'vi' : 'Tiếng Việt',
  'vo' : 'Volapük',
  'wa' : 'Walon',
  'wo' : 'Wolof',
  'xh' : 'isiXhosa',
  'yi' : 'ײִדיש',
  'yo' : 'Yorùbá',
  'za' : 'Zhuang',
  'zh' : '中文',
  'zu' : 'isiZulu'
}
# List of languages having direction right-to-left (RTL) - - - - - - - - - - - -
rtlLanguages = ('ar', 'he', 'fa')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Languages:
    '''This class gives access to the language codes and names as standardized
       by ISO-639. The file has been downloaded in July 2009 from
       http://www.loc.gov/standards/iso639-2/ascii_8bits.html (UTF-8 version)'''

    def __init__(self):
        self.path = Path(__file__).parent / 'Languages.Iso639-2'
        self.languageCodes = []
        # Names of languages in English
        self.languageNames = []
        # Names of languages in their language. It is not part of ISO 639.2 and
        # is taken from dict languageNames above.
        self.nativeNames = []
        self.parseFile()

    def parseFile(self):
        '''Parses the language codes and names in the ISO file and puts them in
           self.languageCodes, self.languageNames and self.nativeNames.'''
        with self.path.open(encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    lineElems = line.split('|')
                    if lineElems[2].strip():
                        # I take only those that have a 2-chars ISO-639-1 code
                        self.languageCodes.append(lineElems[2])
                        self.languageNames.append(lineElems[3])
                        if lineElems[2] in nativeNames:
                            self.nativeNames.append(nativeNames[lineElems[2]])
                        else:
                            # Put the english name nevertheless.
                            self.nativeNames.append(lineElems[3])

    def exists(self, code):
        '''Is p_code a valid 2-digits language code ?'''
        return code in self.languageCodes

    def get(self, code):
        '''Returns information about the language whose code is p_code'''
        try:
            iCode = self.languageCodes.index(code)
            return self.languageCodes[iCode], self.languageNames[iCode], \
                   self.nativeNames[iCode]
        except ValueError:
            return None, None, None

    def __repr__(self):
        i = -1
        res = ''
        for languageCode in self.languageCodes:
            i += 1
            res += 'Language: ' + languageCode + ' - ' + self.languageNames[i]
            res += '\n'
        return res

# Country codes ISO 3166-1 - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Countries:
    '''This class gives access to the country codes and names as standardized by
       ISO 3166-1. The file has been downloaded in March 2011 from
       http://www.iso.org/iso/country_codes/iso_3166_code_lists.htm
       (first line has been removed).'''
    # The single Countries instance will be stored here
    instance = None

    @classmethod
    def get(class_):
        '''Returns the single existing instance of this class in
           p_class_.instance. If it does noe exist yet, it is created.'''
        r = class_.instance
        if not r:
            class_.instance = r = class_()
        return r

    def __init__(self):
        # This file has been downloaded from
        # http://www.iso.org/iso/country_codes.htm and converted to utf-8.
        self.path = Path(__file__).parent / 'Countries.Iso3166-1'
        self.countryCodes = []
        # Names of countries in English
        self.countryNames = []
        self.parseFile()

    def parseFile(self):
        with self.path.open() as f:
            for line in f:
                if line.strip():
                    name, code = line.split(';')
                    self.countryCodes.append(code.strip())
                    self.countryNames.append(name.strip())

    def exists(self, code):
        '''Is p_code a valid 2-digits country code?'''
        return code in self.countryCodes
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
