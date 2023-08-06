'''Pretty-prints chunks of Python code'''

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
import re, keyword

from appy.xml.escape import Escape
from appy.utils.client import Resource

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NO_DATA  = 'No data as been returned.'
URL_KO   = 'Error getting %s. %s.'
PART_KO  = 'Invalid part specifier "%s".'
PT_KO    = 'Invalid part type "%s". Valid ones are: %s.'
METH_KO  = 'Wrong name "%s" for "%s". Expected <className>.<methodName>.'
NAME_KO  = '%s "%s" was not found.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class PrettyPrinter:
    '''Transforms a chunk of Python code into a pretty-printed XHTML version'''

    # Pretty-printer-specific error class
    class Error(Exception): pass

    # Regular expressions and their components, for extracting parts of code
    # (classes, methods...)
    # ~~~
    # A group representing blanks at the start of the found class or method.
    # Counting blanks is important to find the place where the method or class
    # will end.
    blanks = '(?P<blanks> *)'
    blanksR = '(?P=blanks)' # A reference to this group
    # The regex part allowing to detect "detentation" at the end of the class or
    # method definition.
    dedent = '(?:^%s[\w#]|^[\w#]|\Z)' % blanksR
    # A template regular expression matching a class declaration
    classDecl = 'class +%s *(?:\(|\:).*?'
    # A template regular expression matching a complete method definition
    methodDef = '%s^%s(def +%%s *\(.*?)%s' % (classDecl, blanks, dedent)
    # A template regular expression matching a complete class definition
    classDef = '^%s(%s)%s' % (blanks, classDecl, dedent)

    # Types of code parts that can be used in a part specifier, with their
    # corresponding regular expressions.
    partTypes = {
      'c': classDef,  # The signature of a class (name and docstring)
      's': methodDef, # The signature of a method (name and docstring)
      'm': methodDef  # A complete method (signature and body)
    }
    # Names of part types, used in messages
    partNames = {'c': 'class', 's': 'method', 'm': 'method'}

    # States, while parsing a Python object (method or class) definition
    IN_DEF  = 0 # Within the object definition ("def m1(self):", "class C1:")
    IN_BODY = 1 # Within the method body (after the "def" or "class" line)
    IN_DOC  = 2 # Within the object's docstring

    # Docstring delimiters
    docDelimiters = ('"""', "'''")

    # Regular expression identifying, in Python comments, Appy names: p_param1,
    # m_method2...
    commentNames = re.compile('(?<=\W)(p|m|r|c)_(\w+)')

    # Styles to apply to names matched by regular expression "commentNames"
    commentStyles = {'p': 'u', 'm': 'i', 'r': 'ui', 'c': 'bi'}

    # Regular expression matching Python keywords
    pythonKeywords = re.compile('(?<=\W)(%s)(?![\w-])'%'|'.join(keyword.kwlist))
    
    def __init__(self, code, part, url=None, o=None):
        # The content of the Python file to pretty-print
        self.code = code
        # A specifier indicating which portion of the file must be kept
        self.partType, self.partName = self.getPartElements(part)
        # If the p_code file came from a given URL, p_url is present and the
        # source object whose Rich field referenced this URL, as p_o.
        self.url = url
        self.o = o

    def prettifyKeywords(self, match):
        '''Formats a Python keyword in bold'''
        return '<b>%s</b>' % match.group(1)

    def prettifyCommentName(self, match):
        '''Formats a comment name identified in this m_match'''
        # Get the HTML tags to use to surround the name
        tags = self.commentStyles.get(match.group(1))
        if not tags:
            # An unknown type of name
            return match.group(0)
        start = end = ''
        for tag in tags:
            start = '%s<%s>' % (start, tag)
            end = '</%s>%s' % (tag, end)
        return '%s%s%s' % (start, match.group(2), end)

    def prettifyLoc(self, r, loc, inComment=False, css=None):
        '''Compute p_loc's pretty version and add it to p_r'''
        ploc = Escape.xml(loc)
        if inComment:
            # Format Appy-specific comment names
            ploc = self.commentNames.sub(self.prettifyCommentName, ploc)
            if css: ploc = '<span class="%s">%s</span>' % (css, ploc)
        else:
            # Format Python keywords
            ploc = self.pythonKeywords.sub(self.prettifyKeywords, ploc)
        r.append(ploc)

    def prettify(self, odef, blanks, signOnly):
        '''Returns the prettified version of p_odef, which is a class or method
           definition. If p_signOnly is True, from p_odef, we only keep the
           object's signature, and starting comments.'''
        first = True
        r = []
        state = self.IN_DEF
        add = self.prettifyLoc
        for loc in odef.split('\n'): # loc = line of code
            if state == self.IN_DEF:
                # We are still in the object definition
                if first:
                    add(r, '%s%s' % (blanks, loc))
                    first = False
                else:
                    add(r, loc)
                if loc.rstrip().endswith(':'):
                    # The end of the definition has been reached
                    state = self.IN_BODY
            elif state == self.IN_BODY:
                # We are in the method body
                stripped = loc.strip()
                prefix = stripped[:3]
                if prefix == '# ~':
                    # A special comment indicating that, if p_signOnly mode, we
                    # have to stop now.
                    if signOnly:
                        break
                    else:
                        add(r, loc)
                elif not stripped or (stripped[0] == '#'):
                    # Add this blank or comment line into the result
                    add(r, loc, inComment=True, css='comment')
                elif prefix in self.docDelimiters:
                    # We enter into a docstring
                    add(r, loc, inComment=True, css='docstring')
                    if (len(stripped) > 3) and \
                       (stripped[-3:] in self.docDelimiters):
                        # We are already out of it
                        pass
                    else:
                        state = self.IN_DOC
                else:
                    # This is a not-commented line of code. Stop here if we are
                    # in p_signOnly mode.
                    if signOnly:
                        break
                    else:
                        add(r, loc)
            elif state == self.IN_DOC:
                add(r, loc, inComment=True, css='docstring')
                stripped = loc.strip()
                if stripped[-3:] in self.docDelimiters:
                    # We are out of the docstring
                    state = self.IN_BODY
        r = '\n'.join(r)
        if self.url and self.o:
            r = '<a href="%s" target="appyIFrame" ' \
                'onclick="openPopup(\'iframePopup\',null,750,600)"/>' \
                '<img src="%s" class="picto"/></a>%s' % \
                (self.url, self.o.buildUrl('page.svg'), r)
        return r

    def run(self):
        '''Returns, as a string, a chunk of XHTML code representing the
           pretty-printed version of some p_self.part of this p_self.code.'''
        # Create the regular expression allowing to search p_self.part
        template = self.partTypes[self.partType]
        if self.partNames[self.partType] == 'method':
            template = template % tuple(self.partName.split('.'))
        else:
            template = template % self.partName
        rex = re.compile(template, re.S|re.M)
        # Extracts the part of p_self.code corresponding to p_self.part
        match = rex.search(self.code)
        if match is None:
            # The part was not found, return an error message
            isError = True
            content = NAME_KO % (self.partNames[self.partType].capitalize(),
                                 self.partName)
        else:
            # The part was found, return it
            blanks = match.group(1) # Leading blanks preceding the definition
            content = match.group(2)
            isError = False
            # Keep only the object "signature" (=declaration + starting
            # comments) or keep the entire definition ?
            signOnly = self.partType != 'm'
            # Prettify the code
            content = self.prettify(content, blanks, signOnly=signOnly)
        return self.wrap(content, isError=isError, escape=isError)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Class methods
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @classmethod
    def wrap(class_, content, isError=True, escape=True):
        '''Wraps and xml-escape (if p_escape is True) the final pretty p_content
           (or error message if p_isError is True) in a "pre" tag.'''
        prefix = '<i>' if isError else ''
        suffix = '</i>' if isError else ''
        if escape: content = Escape.xml(content)
        return '<pre>%s%s%s</pre>' % (prefix, content, suffix)

    @classmethod
    def getPartElements(class_, part):
        '''If p_part specifier is valid, this method returns the p_part,
           splitted into its elemens: (type, name). Else, it raises an
           exception.'''
        # The part must contain a type and a name
        try:
            type, name = part.split('_', 1)
        except ValueError:
            raise class_.Error(PART_KO % part)
        # The type must be among valid ones
        if type not in class_.partTypes:
            validTypes = ', '.join(class_.partTypes.keys())
            raise class_.Error(PT_KO % (type, validTypes))
        # For types "s" and "m", name must be of the form
        #                  <className>.<methodName>
        if (class_.partNames[type] == 'method') and (name.count('.') != 1):
            raise class_.Error(METH_KO % (name, type))
        return type, name

    @classmethod
    def cache(class_, url, data, o):
        '''Cache file content p_data downloaded at this p_url on the cache
           accessible via p_o.'''
        if o is None: return
        mainCache = o.H().cache
        if mainCache._pretty_:
            mainCache._pretty_[url] = data
        else:
            mainCache._pretty_ = {url: data}

    @classmethod
    def getFromCache(class_, url, o):
        '''Several parts of the same file at this p_url may be requested. So
           once a file has been downloaded once, cache its content. Get the
           p_url content from the cache if present.'''
        if o is None: return
        cache = o.H().cache._pretty_
        if cache is None: return
        return cache.get(url)

    @classmethod
    def getFromUrl(class_, url, part, o=None):
        '''Retrieve the code file present at this p_url and return its pretty-
           printed p_part.'''
        wrap = class_.wrap
        # Check p_part specifier before performing the HTTP request. If it is
        # invalid, we save a useless request.
        try:
            class_.getPartElements(part)
        except class_.Error as err:
            return wrap(str(err))
        # Get the code file and returns it wrapped in a "pre" tag. Get the file
        # content from the cache if present.
        try:
            data = class_.getFromCache(url, o)
            if data is None:
                content = Resource(url).get()
                data = getattr(content, 'body', None)
                class_.cache(url, data, o)
            if not data:
                r = wrap(URL_KO % (url, NO_DATA))
            else:
                r = class_(data, part, url=url, o=o).run()
        except Resource.Error as err:
            r = wrap(URL_KO % (url, str(err)))
        return r
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
