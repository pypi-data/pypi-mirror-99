'''Includes external static files (CSS, JS) into HTML pages'''

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
class Includer:
    '''Produces chunks of XHTML for including external files like CSS and
       Javascript files.'''

    @classmethod
    def css(class_, url):
        '''Produces a chunk of XHTML for including CSS file with this p_url'''
        return '<link rel="stylesheet" type="text/css" href="%s"/>' % url

    @classmethod
    def js(class_, url):
        '''Produces a chunk of XHTML for including JS file with this p_url'''
        return '<script src="%s"></script>' % url

    @classmethod
    def getGlobal(class_, handler, config, dir):
        '''Returns a chunk of XHTML code for including, within the main page
           template, CSS and Javascript files.'''
        r = []
        tool = handler.tool
        # Get CSS files
        ltr = dir == 'ltr'
        # Get global CSS files from dict Static.ram. Indeed, every CSS file is
        # patched from a template and stored in it.
        for name in handler.Static.ram.keys():
            if name.endswith('.css'):
                # Do not include appyrtl.css, the stylesheet specific to
                # right-to-left (rtl) languages, if the language is
                # left-to-right.
                if ltr and (name == 'appyrtl.css'):
                    continue
                r.append(class_.css(tool.buildUrl(name, ram=True)))
        # Get CSS include for Google Fonts, when some of them are in use
        if config.ui.googleFonts:
            r.append(class_.css(config.ui.getFontsInclude()))
        # Get Javascript files
        for base, path in config.server.static.map.items():
            for jsFile in path.glob('*.js'):
                r.append(class_.js(tool.buildUrl(jsFile.name, base=base)))
        # Initialise a JS variable containing the site URL. It will be used by
        # JS code, ie, the one that loads waiting icons for Ajax requests.
        r.append('<script>var siteUrl="%s"</script>' % tool.siteUrl)
        return '\n'.join(r)

    @classmethod
    def getUrl(class_, url, tool):
        '''Gets an absolute URL based on p_url, that can already be absolute or
           not.'''
        if url.startswith('http'): return url
        return tool.buildUrl(url)

    @classmethod
    def getSpecific(class_, tool, css, js):
        '''Returns a chunk of XHTML code for including p_css and p_js files
           specifically required by some fields.'''
        r = []
        if css:
            for url in css: r.append(class_.css(class_.getUrl(url, tool)))
        if js:
            for url in js:  r.append(class_.js(class_.getUrl(url, tool)))
        return '\n'.join(r)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
