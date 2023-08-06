'''Parsing of CSS properties'''

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
from appy.utils import formatNumber
from appy.utils.string import sadd, sremove

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
htmlColorNames = {
  'aliceblue': '#f0f8ff', 'antiquewhite': '#faebd7', 'aqua': '#00ffff',
  'aquamarine': '#7fffd4','azure': '#f0ffff', 'beige': '#f5f5dc',
  'bisque': '#ffe4c4', 'black': '#000000', 'blanchedalmond': '#ffebcd',
  'blue': '#0000ff', 'blueviolet': '#8a2be2', 'brown': '#a52a2a',
  'burlywood': '#deb887', 'cadetblue': '#5f9ea0', 'chartreuse': '#7fff00',
  'chocolate': '#d2691e', 'coral': '#ff7f50', 'cornflowerblue': '#6495ed',
  'cornsilk': '#fff8dc', 'crimson': '#dc143c', 'cyan': '#00ffff',
  'darkblue': '#00008b', 'darkcyan': '#008b8b', 'darkgoldenrod': '#b8860b',
  'darkgray': '#a9a9a9', 'darkgrey': '#a9a9a9', 'darkgreen': '#006400',
  'darkkhaki': '#bdb76b', 'darkmagenta': '#8b008b', 'darkolivegreen': '#556b2f',
  'darkorange': '#ff8c00', 'darkorchid': '#9932cc', 'darkred': '#8b0000',
  'darksalmon': '#e9967a', 'darkseagreen': '#8fbc8f', 'darkslateblue':'#483d8b',
  'darkslategray': '#2f4f4f', 'darkslategrey': '#2f4f4f',
  'darkturquoise': '#00ced1', 'darkviolet': '#9400d3', 'deeppink': '#ff1493',
  'deepskyblue': '#00bfff', 'dimgray': '#696969', 'dimgrey': '#696969',
  'dodgerblue': '#1e90ff', 'firebrick': '#b22222', 'floralwhite': '#fffaf0',
  'forestgreen': '#228b22', 'fuchsia': '#ff00ff', 'gainsboro': '#dcdcdc',
  'ghostwhite': '#f8f8ff', 'gold': '#ffd700', 'goldenrod': '#daa520',
  'gray': '#808080', 'grey': '#808080', 'green': '#008000',
  'greenyellow': '#adff2f', 'honeydew': '#f0fff0', 'hotpink': '#ff69b4',
  'indianred ': '#cd5c5c', 'indigo ': '#4b0082', 'ivory': '#fffff0',
  'khaki': '#f0e68c', 'lavender': '#e6e6fa', 'lavenderblush': '#fff0f5',
  'lawngreen': '#7cfc00', 'lemonchiffon': '#fffacd', 'lightblue': '#add8e6',
  'lightcoral': '#f08080', 'lightcyan': '#e0ffff',
  'lightgoldenrodyellow': '#fafad2', 'lightgray': '#d3d3d3',
  'lightgrey': '#d3d3d3', 'lightgreen': '#90ee90', 'lightpink': '#ffb6c1',
  'lightsalmon': '#ffa07a', 'lightseagreen': '#20b2aa',
  'lightskyblue': '#87cefa', 'lightslategray': '#778899',
  'lightslategrey': '#778899', 'lightsteelblue': '#b0c4de',
  'lightyellow': '#ffffe0', 'lime': '#00ff00', 'limegreen': '#32cd32',
  'linen': '#faf0e6', 'magenta': '#ff00ff', 'maroon': '#800000',
  'mediumaquamarine': '#66cdaa', 'mediumblue': '#0000cd',
  'mediumorchid': '#ba55d3', 'mediumpurple': '#9370db',
  'mediumseagreen': '#3cb371', 'mediumslateblue': '#7b68ee',
  'mediumspringgreen': '#00fa9a', 'mediumturquoise': '#48d1cc',
  'mediumvioletred': '#c71585', 'midnightblue': '#191970',
  'mintcream': '#f5fffa', 'mistyrose': '#ffe4e1', 'moccasin': '#ffe4b5',
  'navajowhite': '#ffdead', 'navy': '#000080', 'oldlace': '#fdf5e6',
  'olive': '#808000', 'olivedrab': '#6b8e23', 'orange': '#ffa500',
  'orangered': '#ff4500', 'orchid': '#da70d6', 'palegoldenrod': '#eee8aa',
  'palegreen': '#98fb98', 'paleturquoise': '#afeeee','palevioletred': '#db7093',
  'papayawhip': '#ffefd5', 'peachpuff': '#ffdab9', 'peru': '#cd853f',
  'pink': '#ffc0cb', 'plum': '#dda0dd', 'powderblue': '#b0e0e6',
  'purple': '#800080', 'rebeccapurple': '#663399', 'red': '#ff0000',
  'rosybrown': '#bc8f8f', 'royalblue': '#4169e1', 'saddlebrown': '#8b4513',
  'salmon': '#fa8072', 'sandybrown': '#f4a460', 'seagreen': '#2e8b57',
  'seashell': '#fff5ee', 'sienna': '#a0522d', 'silver': '#c0c0c0',
  'skyblue': '#87ceeb', 'slateblue': '#6a5acd', 'slategray': '#708090',
  'slategrey': '#708090', 'snow': '#fffafa', 'springgreen': '#00ff7f',
  'steelblue': '#4682b4', 'tan': '#d2b48c', 'teal': '#008080',
  'thistle': '#d8bfd8', 'tomato': '#ff6347', 'turquoise': '#40e0d0',
  'violet': '#ee82ee', 'wheat': '#f5deb3', 'white': '#ffffff',
  'whitesmoke': '#f5f5f5', 'yellow': '#ffff00', 'yellowgreen': '#9acd32'}

# Valid CSS values for font-weight and font-style attributes
fontWeigths = ('normal', 'bold', 'lighter', 'bolder')
fontStyles = ('normal', 'italic', 'oblique')

# ------------------------------------------------------------------------------
# Default ratio for converting pixels to cm
px2cm = 44.173513561

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
ADD_CLASS_ERROR = 'Use method addClass to add CSS classes to this instance'
MERGE_VALUE_ERROR = 'Non-string CSS values cannot be merged or unmixed.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def parseStyleAttribute(value, asDict=False):
    '''Returns a list of CSS (name, value) pairs (or a dict if p_asDict is
       True), parsed from p_value, which holds the content of a HTML "style"
       tag.'''
    r = {} if asDict else []
    for attr in value.split(';'):
        if not attr.strip(): continue
        name, value = attr.split(':', 1)
        if asDict: r[name.strip()] = value.strip()
        else: r.append( (name.strip(), value.strip()) )
    return r

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class CssValue:
    '''Represents a CSS value'''
    # CSS properties having a unit, with their default unit
    unitProperties = {'width': 'px', 'height': 'px', 'margin-left': 'px',
      'margin-right': 'px', 'margin-top': 'px', 'margin-bottom': 'px',
      'text-indent': 'px', 'font-size': None, 'border-spacing': 'px',
      'line-height': ''} # line-height can be "normal" or a value with a unit
    # CSS properties defining colors
    colorProperties = ('color', 'background-color')
    # Regular expressions for parsing (parts of) CSS values
    valueRex = re.compile('(-?\d*(?:\.\d+)?)(%|px|cm|pt|em|ex)?')
    rgbVal = '\s*([\d.]+)\s*'
    rgbRex = re.compile('rgba?\(%s,%s,%s(?:,%s)?\)' % ((rgbVal,)*4))

    def __init__(self, name, value):
        # p_value can be another CssValue instance
        if isinstance(value, CssValue):
            self.value = value.value
            self.unit = value.unit
            return
        # If we are here, p_value is a string
        self.unit = None
        value = value.strip().lower()
        if name in CssValue.unitProperties:
            val, unit = CssValue.valueRex.match(value).groups()
            if not val:
                # Could not parse it. Maybe a enum value or a not-supported-yet
                # unit.
                self.value = value
            else:
                self.value = float(val)
            self.unit = unit or CssValue.unitProperties[name]
        elif name in CssValue.colorProperties:
            if value.startswith('#'):
                self.value = value # Hexadecimal, keep it as is
            elif value.startswith('rgb'):
                # Convert the RGB value to hexadecimal
                self.value = self.rgb2hex(value)
            else:
                # Probably a color name. Convert it to hexadecimal.
                self.value = htmlColorNames.get(value, value)
        else:
            self.value = value

    def rgb2hex(self, value):
        '''Converts a color expressed in RGB to hexadecimal'''
        match = CssValue.rgbRex.match(value)
        # If we couldn't parse the value, left it untouched
        if not match: return value
        res = '#'
        i = -1
        for val in match.groups():
            i += 1
            # Ignore the optional alpha channel
            if i > 2: continue
            # Convert the integer value to hexadecimal
            hexa = hex(int(val))[2:].upper().zfill(2) # Remove prefix "0x"
            res += hexa
        return res

    def __bool__(self):
        # This value is considered empty when self.value is an empty string
        return not isinstance(self.value, str) or bool(self.value)

    def merge(self, value):
        '''Add a new p_value among self.value, that can be a space-separated
           list of values.'''
        if not isinstance(self.value, str):
            raise Exception(MERGE_VALUE_ERROR)
        self.value = sadd(self.value, value)

    def unmix(self, value):
        '''Removes p_value from self.value, that can be a space-separated list
           of values.'''
        if not isinstance(self.value, str):
            raise Exception(MERGE_VALUE_ERROR)
        self.value = sremove(self.value, value)

    def isMultiple(self):
        '''Returns True if self.value contains several sub-values'''
        val = self.value
        return isinstance(val, str) and (' ' in val)

    def __str__(self):
        res = str(self.value)
        if self.unit: res += self.unit
        return res

    def __repr__(self): return self.__str__()

    def cm(self, formatted=True, value=None, ratio=px2cm):
        '''Returns p_self.value (or the given p_value) expressed in cm'''
        unit = self.unit
        if not unit: return
        if value is None:
            r = self.value
        else:
            r = value
        if unit == 'px': # Convert pixels to cm
            r = r / ratio
        elif unit in ('em', 'ex'):
            # For "ex", the ratio must be adapted
            if unit == 'ex': ratio = ratio * 1.6
            r = (r / ratio) * 10
        elif unit == 'pt':
            # Use a specific ratio
            r *= 0.0352778
        elif unit != 'cm':
            r = None
        if formatted and (r is not None):
            r = formatNumber(r, sep='.', precision=3)
        return r

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class CssStyles:
    '''This class represents a set of styles collected from:
       * an HTML "style" attribute;
       * other attributes like "width";
       * an HTML tag itself (ie, <b>, <i>...).
       Moreover, it can refer to externally defined CSS classes (mentioned in a
       "class" attribute) in its attribute "classes".
    '''
    # The correspondance between XHTML attributes and CSS properties. Within
    # CSS property names, dashes have been removed because they are used as
    # names for Python instance attributes.
    xhtml2css = {'width': 'width', 'height': 'height', 'align': 'text-align',
                 'cellspacing': 'border-spacing', 'border': 'border'}
    # CSS properties whose values can be combined
    combinable = ('textdecoration',)
    # CSS combined properties (= that can be split into individual properties)
    combined = ('margin',)
    # Directions in use in combined CSS properties (padding, margin, etc),
    # defined in the standard order.
    directions = ('top', 'right', 'bottom', 'left')
    # Values, on combined attributes, that prevent splitting
    unsplittable = ('auto',)
    # Values that must be ignored
    ignore = {'*': {'auto':None, 'initial':None, 'inherit':None}}
    # Values specified in ignore['*'] must not be ignored for these attributes
    ignoreExcept = {'auto': {'table-layout':None}}
    # The '!important' CSS rule
    importantRule = '!important'

    def __init__(self, elem=None, attrs=None, other=None, **kwargs):
        '''Analyses styles as found in p_attrs and/or deduced from XHTML element
           p_elem, and sets, for every found style, an attribute on self. This
           constructor can also be used to build a CssStyles instance from
           another CssStyles instance, given in p_other. A CssStyles instance
           can also be initialised from p_kwargs representing CSS attributes.
           CSS styles defined in p_kwargs override those in p_other, that, in
           turn,override any existing value. Within p_kwargs, CSS attribute
           names must not contain any dash (it would produce illegal Python
           code).'''
        # The content of a potential "class" attribute in p_attrs
        self.classes = ''
        # Parse first the "style" attribute if present
        if attrs and ('style' in attrs):
            value = attrs['style']
            if value:
                styles = parseStyleAttribute(attrs['style'], asDict=True)
                for name, value in styles.items():
                    self.add(name, value)
        # Parse obsolete XHTML style-related attributes if present. But they
        # will not override corresponding attributes from the "styles"
        # attributes if found.
        if attrs:
            for name, value in attrs.items():
                if value and (name in self.xhtml2css):
                    self.add(self.xhtml2css[name], value, override=False)
        # If a "class" attribute is defined, store, in attribute "classes", the
        # "external" class(es) defined in it.
        if attrs and ('class' in attrs):
            css = attrs['class']
            if css: self.addClass(css)
        # Add the style(s) corresponding to p_elem when relevant, excepted if
        # the corresponding CssValue is already defined.
        if elem and (elem in self.tag2css):
            self.merge(self.tag2css[elem], override=False)
        # Get the styles from p_other and/or p_kwargs. Those styles will
        # override any exsting one.
        if other: self.merge(other)
        for k, v in kwargs.items(): self.add(k, v)
        # Split combined CSS properties
        self.split()

    def __repr__(self):
        res = '<CSS'
        for name, value in self.__dict__.items():
            if name == 'classes':
                if value: res += ' %s::%s' % (name, value)
            else:
                res += ' %s:%s' % (name, value)
        return res + '>'

    def __bool__(self):
        # Count all attributes but "classes" that is always present
        return (len(self.__dict__) > 1) or bool(self.classes)

    def get(self, name=None):
        '''Gets the value (as a CssValue instance) corresponding to the CSS
           attribute p_name. If p_name is ommitted, it returns all CSS
           attributes as a dict. This method allows to use the original CSS
           attribute names (possibly containing dashes). If this CssStyles
           instance does not store such an attribute, no error is raised:
           None is returned.'''
        if not name: return self.__dict__
        if '-' in name: name = name.replace('-', '')
        return getattr(self, name, None)

    def addClass(self, value, append=True):
        '''Add CSS class(es) p_value (as a string) to self.classes. p_value can
           hold several CSS space-separated classes.'''
        # If p_append is True, CSS classes in p_value are appended to
        # p_self.classes. Else, they are inserted at the start of
        # p_self.classes.
        self.classes = sadd(self.classes, value, append=append)

    def deleteClass(self, value):
        '''Remove CSS class(es) in p_value from self.classes'''
        self.classes = sremove(self.classes, value)

    def getClass(self, last=False):
        '''Returns the name of the CSS class(es) defined in p_self.classes, or
           None if no class is defined. If p_last is True, and several classes
           are defined, only the last one is returned.'''
        # Is a CSS class defined ?
        classes = self.classes
        if not classes: return
        # Yes. Keep only the last one if requested.
        if last and (' ' in classes):
            classes = classes.split()[-1]
        return classes

    def hasClass(self, css):
        '''Is CSS class p_css defined ?'''
        classes = self.classes
        if not classes: return
        if ' ' in classes:
            r = css in classes.split()
        else:
            r = css == classes
        return r

    def add(self, name, value, override=True):
        '''Adds a CSS attribute to this instance as a CssValue instance, and
           also return it. p_name can be the original name of the CSS attribute
           (possibly containing dashes).'''
        if name == 'classes': raise Exception(ADD_CLASS_ERROR)
        # Ignore potential "!important" suffix
        if isinstance(value, str) and value.endswith(self.importantRule):
            value = value[:-len(self.importantRule)].strip()
        # Do not add anything if the value must be ignored
        ignore = self.ignore
        if (value in ignore['*']) or \
           ((name in ignore) and (value in ignore[name])):
               # Ignore it, excepted if there is a match in "ignoreExcept"
               if (value not in self.ignoreExcept) or \
                  (name not in self.ignoreExcept[value]):
                   return
        attrName = name.replace('-', '')
        if not override and hasattr(self, attrName): return
        # Define the new value or combine it with the existing value when
        # relevant.
        res = getattr(self, attrName, None)
        if res and (attrName in CssStyles.combinable):
            res.merge(value.value)
        else:
            res = CssValue(name, value)
            setattr(self, attrName, res)
        return res

    def delete(self, name, value=None):
        '''Removes CSS attribute p_name from self, or only p_value for
           combinable CSS properties.'''
        attrName = name.replace('-', '')
        # Nothing to do if the corresponding attribute is not defined
        if not hasattr(self, attrName): return
        # Manage value removal from a combinable CSS property
        existing = getattr(self, attrName)
        if existing and value and (name in CssStyles.combinable):
            existing.unmix(value.value)
            if not existing:
                delattr(self, attrName)
        else:
            delattr(self, attrName)

    def merge(self, other, override=True):
        '''Merges other's styles within self's styles'''
        for name, value in other.get().items():
            if name == 'classes':
                if value:
                    self.addClass(value)
            else:
                self.add(name, value, override=override)

    def unmix(self, other):
        '''Ensures styles defined in p_other are not in p_self'''
        for name, value in other.get().items():
            if name == 'classes':
                self.deleteClass(value)
            else:
                self.delete(name, value)

    def split(self):
        '''Splits combined properties found on p_self into individual
           properties.'''
        # For every combined CSS property found on p_self:
        #  - if it refers to an "unsplittable" value (like "margin:auto"), the
        #    property is removed from p_self and no other property is added;
        #  - if it refers to a "splittable" value, the property is removed from
        #    p_self and the corresponding individual values (one for each
        #    direction as specified in CssStyles.directions) is added to p_self.
        for prop in CssStyles.combined:
            if not hasattr(self, prop): continue
            value = getattr(self, prop)
            if not value or (value.value in CssStyles.unsplittable):
                delattr(self, prop)
                continue
            value = value.value.split()
            length = len(value)
            if length == 1:
                value = value * 4
            elif length == 2:
                value = (value[0], value[1], value[0], value[1])
            elif length == 3:
                value = (value[0], value[1], value[2], value[1])
            elif length != 4:
                # This will be ignored
                delattr(self, prop)
                continue
            # Replace the combined property with individual ones
            i = -1
            for direction in CssStyles.directions:
                i += 1
                self.add('%s-%s' % (prop, direction), value[i])
            delattr(self, prop)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# For some XHTML tags, we define CssStyle instances containing one or several
# styles that correspond to them.
bold = CssStyles(fontweight='bold')
italic = CssStyles(fontstyle='italic')
strike = CssStyles(textdecoration='line-through')

CssStyles.tag2css = {'b': bold, 'strong': bold, 'i': italic, 'em': italic,
  'strike': strike, 's': strike, 'u': CssStyles(textdecoration='underline'),
  'sup': CssStyles(verticalalign='super'), 'sub': CssStyles(verticalalign='sub')
}
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
