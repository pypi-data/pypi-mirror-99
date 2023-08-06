# -*- coding: utf-8 -*-

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
# Contributors: Gauthier Bastien, Fabio Marcuzzi, IMIO
# ------------------------------------------------------------------------------
import re, xml.sax, math

from appy.pod import *
from appy.pod.doc_importers import getUuid
from appy.pod.odf_parser import OdfEnvironment
from appy.shared.css import CssStyles, CssValue, px2cm
from appy.shared.xml_parser import XmlEnvironment, XmlParser, Escape
from appy.shared.utils import WhitespaceCruncher, formatNumber, addPair
from appy.pod.styles_manager import Style, BulletedProperties,NumberedProperties

# Tags for which there is a direct correspondance between HTML and ODF
h = 'text:h'
p = 'text:p'
span = 'text:span'
tlist = 'text:list'
table = 'table:table'
cell = table + '-cell'
HTML_2_ODF = {
  'h1':h, 'h2':h, 'h3':h, 'h4':h, 'h5':h, 'h6':h, 'p':p, 'div':p,
  'blockquote':p, 'address':p, 'sub': span, 'sup': span, 'br':'text:line-break',
  'table': table, 'thead': table + '-header-rows',
  'tr': table + '-row', 'td': cell, 'th': cell, 'a': 'text:a',
  'ol': tlist, 'ul': tlist, 'li': 'text:list-item'}

# Inner tags whose presence is only useful for specifying style information
STYLE_ONLY_TAGS = ('b', 'strong', 'i', 'em', 'strike', 's', 'u', 'span', 'q',
                   'code', 'font', 'samp', 'kbd', 'var', 'label', 'abbr')
for tag in STYLE_ONLY_TAGS: HTML_2_ODF[tag] = 'text:span'

# Styles whose translation to ODF is simple
SIMPLE_TAGS = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'blockquote',
               'address', 'sub', 'sup', 'br', 'th', 'td')

INNER_TAGS_NO_BR = STYLE_ONLY_TAGS + ('sub','sup','a','acronym','abbr','img')
INNER_TAGS = INNER_TAGS_NO_BR + ('br',)
TABLE_CELL_TAGS = ('td', 'th')
TABLE_COL_TAGS = TABLE_CELL_TAGS + ('col',)
TABLE_ROW_TAGS = ('tr', 'colgroup')
OUTER_TAGS = TABLE_CELL_TAGS + ('li',)
PARA_TAGS = ('p', 'div', 'blockquote', 'address')
# The following elements can't be rendered inside paragraphs
NOT_INSIDE_P = XHTML_HEADINGS + XHTML_LISTS + ('table',)
NOT_INSIDE_P_OR_P = NOT_INSIDE_P + PARA_TAGS
NOT_INSIDE_LI =  XHTML_HEADINGS + ('table',) + PARA_TAGS
NOT_INSIDE_LIST = ('table',)
IGNORABLE_TAGS = ('meta', 'title', 'style', 'script')

# ------------------------------------------------------------------------------
class Element:
    '''Abstract base class representing any HTML element encountered during the
       SAX parsing.'''

    # An instance of one of its concrete classes (see below) will be pushed on
    # the stack of currently parsed elements every time such element is
    # encountered.

    def getClass(self, last=False):
        '''Returns the name of the CSS class(es) defined on p_self'''
        styles = self.cssStyles
        if not styles: return
        return styles.getClass(last=last)

    def hasClass(self, css):
        '''Has p_self a CSS class named p_css ?'''
        styles = self.cssStyles
        return styles and styles.hasClass(css) or False

    def noClass(self):
        '''Returns True if no CSS class is defined on p_self'''
        return not self.getClass()

# ------------------------------------------------------------------------------
class HtmlElement(Element):
    '''Represents any HTML element'''

    # Moreover, if the element is a table, it will be wrapped in a HtmlTable
    # element (see below).

    elemTypes = {'p':'para', 'div':'para', 'blockquote': 'para',
                 'li':'para', 'ol':'list', 'ul':'list'}

    # Prototypical instances
    protos = {}

    def __init__(self, elem, attrs=None, parent=None):
        self.elem = elem
        # Store a reference to the parent element if known
        self.parent = parent
        # Extract style information from p_elem and p_attrs
        self.cssStyles = CssStyles(elem, attrs)
        # When merging styles, "cssStyles" may temporarily hold a set of merged
        # styles. In this case, the original CssStyles instance is stored in the
        # following attribute.
        self.originalStyles = None
        # Extract other attributes depending on p_elem
        self.attrs = self.extractAttributes(elem, attrs)
        # When the HTML element corresponding to p_self is completely dumped,
        # if there was a problem related to tags inclusion, we may need to dump
        # start tags corresponding to tags that we had to close before dumping
        # this element.
        self.tagsToReopen = None # ~[HtmlElement]~
        # Before dumping the closing tag corresponding to p_self, we may need to
        # close other tags (ie closing a paragraph before closing a cell).
        self.tagsToClose = None # ~[HtmlElement]~
        # This tag's type
        if self.elemTypes.has_key(elem):
            self.elemType = self.elemTypes[elem]
        else:
            self.elemType = elem
        # If a conflict occurs on this element, we will note it
        self.isConflictual = False
        # Sometimes we must remember the ODT style that has been computed and
        # applied to this HTML element (for lists).
        self.odStyle = None
        # For cells, the style to apply to their inner paragraphs (set later)
        self.innerStyle = None
        # We must know if a style must be applied on inner paragraphs within
        # "li" tags.
        if (elem == 'li') and attrs.has_key('class'):
            self.paraStyle = attrs['class']
        else:
            self.paraStyle = None # Will also be set on "ol" and "ul" tags.
        # Must we only keep tag content and remove the tag itself ?
        self.removeTag = False
        # Must we dump a line-break just before encountering a tag from
        # INNER_TAGS within this tag ?
        self.dumpLineBreakOnInner = False
        # Was content already dumped from this tag (or any of its sub-tags) into
        # the result ?
        self.contentDumped = False
        # "Dump status" can have 3 values:
        # - None       in the majority of cases;
        # - "waiting"  we don't know yet if we must dump this tag or not: it
        #              will depend if content will be found or not;
        # - "dumped"   a tag previously "waiting" has effectively be dumped.
        self.dumpStatus = None
        # Inner CSS styles are those from a removed inner tag, or from this tag,
        # being an outer tag whose CSS styles must be dumped to an inner tag
        # that will be added.
        self.innerCssStyles = None
        if elem == 'li': self.addInnerCssStyles(self)
        # The number (starting at 1) of p_self's currently walked sub-tag. If we
        # are not walking a sub-tag, this number is set to 0.
        self.subNumber = 0

    def extractAttributes(self, elem, attrs):
        '''Extracts useful attributes from p_attrs'''
        if not attrs: return
        if elem == 'ol':
            if attrs.has_key('start'):
                return {'start': int(attrs['start'])}
        elif elem in TABLE_COL_TAGS:
            return attrs

    def getOdfTag(self):
        '''Gets the raw ODF tag that corresponds to me'''
        return HTML_2_ODF.get(self.elem, '')

    def getOdfTags(self):
        '''Gets the start and end tags corresponding to p_self'''
        tag = self.getOdfTag()
        if not tag: return (None, None)
        return ('<%s>' % tag, '</%s>' % tag)

    def setConflictual(self):
        '''Note p_self as conflictual'''
        self.isConflictual = True
        return self

    def getPath(self):
        '''Return this element's "absolute path" within the XHTML tree'''
        res = self.elem
        if self.parent:
            res = '%s>%s' % (self.parent.getPath(), res)
        return res

    def getConflictualElements(self, env):
        '''p_self was just parsed. In some cases, this element can't be dumped
           in the result because there are conflictual elements among previously
           parsed opening elements (p_env.currentElements). For example, if we
           just dumped a "p", we can't dump a table within the "p". Such
           constraints do not hold in XHTML code but hold in ODF code.'''
        if not env.currentElements: return ()
        parent = env.getCurrentElement()
        # Special case: check elements that can't be found within a "li".
        # Instead of being noted as "conflictual", note that we must keep
        # these element's contents but remove the surrounding tags.
        if (parent.elem == 'li') and (self.elem in PARA_TAGS):
            self.removeTag = True
            parent.addInnerCssStyles(self)
            return ()
        # Check elements that can't be found within a paragraph / li. The list
        # of such elements is different for a "li", but "li" has elemType
        # "para", so we must explicitly check the "li" case before checking
        # "elemType" being "para" or not.
        if parent.elem == 'li':
            if self.elem in NOT_INSIDE_LI:
                return (parent.parent.setConflictual(),parent.setConflictual(),)
        elif (parent.elemType == 'para') and (self.elem in NOT_INSIDE_P_OR_P):
            return (parent.setConflictual(),)
        # Check inner paragraphs
        elif (parent.elem in INNER_TAGS) and (self.elemType == 'para'):
            res = [parent.setConflictual()]
            if len(env.currentElements) > 1:
                i = 2
                visitParents = True
                while visitParents:
                    try:
                        nextParent = env.currentElements[-i]
                        i += 1
                        res.insert(0, nextParent.setConflictual())
                        if nextParent.elemType == 'para':
                            visitParents = False
                    except IndexError:
                        visitParents = False
            return res
        if parent.tagsToClose and \
            (parent.tagsToClose[-1].elemType == 'para') and \
            (self.elem in NOT_INSIDE_P_OR_P):
            return (parent.tagsToClose[-1].setConflictual(),)
        # Check elements that can't be found within a list
        if (parent.elemType == 'list') and (self.elem in NOT_INSIDE_LIST):
            return (parent.setConflictual(),)
        return ()

    def addInnerParagraph(self, env):
        '''Dump an inner paragraph inside self (if not already done)'''
        if self.tagsToClose: return # We already did it
        dump = env.dumpString
        p = HtmlElement('p', parent=self)
        dump('<text:p')
        if self.elem == 'li':
            listElem = env.getCurrentElement(isList=True)
            itemStyle = listElem.elem # ul or ol
            # Which 'li'-related style must I use ?
            css = self.cssStyles.classes
            if css:
                odtStyle = env.findStyle(self)
                styleName = None
                if odtStyle:
                    if odtStyle.name == 'podItemKeepWithNext':
                        itemStyle += '_kwn'
                    else:
                        if css == 'podItemKeepWithNext':
                            # We ignore the odtStyle. To improve: merge
                            # keep-with-next functionality with this style.
                            styleName = env.itemStyles[itemStyle + '_kwn']
                        else:
                            styleName = css
                styleName = styleName or env.itemStyles[itemStyle]
                dump(' text:style-name="%s"' % styleName)
            else:
                # Check if a style must be applied on 'p' tags
                if self.innerCssStyles:
                    p.cssStyles.merge(self.innerCssStyles)
                innerStyle = listElem.paraStyle or env.itemStyles[itemStyle]
                if innerStyle:
                    p.cssStyles.addClass(innerStyle)
                dump(env.getOdfAttributes(p))
        else:
            dump(env.getOdfAttributes(p))
        dump('>')
        if not self.tagsToClose: self.tagsToClose = []
        self.tagsToClose.append(p)
        # Note that an inner paragraph has been added
        self.show(env, prefix='!')

    def addInnerCssStyles(self, xhtmlElem):
        '''Remember on p_self the cssStyles defined on p_xhtmlElem'''
        # Do nothing if inner styles are already there or if p_xhtmlElem has no
        # CSS styles.
        if self.innerCssStyles or not xhtmlElem.cssStyles: return
        self.innerCssStyles = xhtmlElem.cssStyles

    def dump(self, start, env):
        '''Dumps the start or end (depending on p_start) tag of this HTML
           element. We must take care of potential innerTags.'''
        # Compute the tag in itself
        tag = ''
        prefix = '<'
        if not start: prefix += '/'
        # Compute tag attributes
        attrs = ''
        if start:
            if self.elemType == 'list':
                # I must specify the list style
                attrs += ' text:style-name="%s"' % self.odStyle
                if self.elem == 'ol':
                    # I have interrupted a numbered list. I need to continue
                    # the numbering.
                    attrs += ' text:continue-numbering="true"'
            else:
                attrs = env.getOdfAttributes(self)
        tag = prefix + self.getOdfTag() + attrs + '>'
        # Close/open subTags if any
        toClose = self.tagsToClose
        if toClose:
            for subElem in toClose:
                subTag = subElem.dump(start, env)
                if start: tag += subTag
                else: tag = subTag + tag
        return tag

    def getLevel(self):
        '''Gets the "depth" of this tag among the currently walked tags'''
        if not self.parent: return 0
        return self.parent.getLevel() + 1

    def getName(self):
        '''Get the name of this tag, potentially augmented wit sub-tags from
           self.tagsToClose.'''
        res = self.elem
        if self.tagsToClose:
            for tag in self.tagsToClose:
                res += '+' + tag.getName()
        return res

    def inInnerTag(self):
        '''Is this tag in an inner tag ?'''
        parent = self.parent
        if not parent: return
        return (parent.elem in INNER_TAGS) or parent.inInnerTag()

    def __repr__(self, prefix='<'):
        res = self.getName()
        if self.removeTag:
            # We do not dump the prefix, used for indicating the fact that the
            # tag is opened or closed.
            res += '-'
            prefix = ''
        if self.isConflictual: res += '*'
        return '%s%s' % (prefix, res)

    def show(self, env, indented=True, prefix='<', content=None):
        '''Returns a (possibly) p_indented representation of this HTML element
           (or of some other p_content at this indentation level), for debugging
           purposes.'''
        if not env.verbose: return
        if content:
            res = '%s%s' % (prefix, content)
        else:
            res = self.__repr__(prefix=prefix)
        if indented:
            res = (' ' * 2 * self.getLevel()) + res
        print res

# Create prototypical instances
for tag in ('p', 'ul', 'ol'): HtmlElement.protos[tag] = HtmlElement(tag)

# ------------------------------------------------------------------------------
class HtmlTable(Element):
    '''Represents an HTML table, and also a sub-buffer. When parsing elements
       corresponding to an HTML table (<table>, <tr>, <td>, etc), we can't dump
       corresponding ODF elements directly into the global result buffer
       (XhtmlEnvironment.res). Indeed, when dumping an ODF table, we must
       dump columns declarations at the beginning of the table. So before
       dumping rows and cells, we must know how much columns will be present
       in the table. It means that we must first parse the first <tr> entirely
       in order to know how much columns are present in the HTML table before
       dumping the ODF table. So we use this class as a sub-buffer that will
       be constructed as we parse the HTML table; when encountering the end
       of the HTML table, we will dump the result of this sub-buffer into
       the parent buffer, which may be the global buffer or another table
       buffer.'''

    def __init__(self, env, xhtmlElem, attrs):
        self.env = env
        # p_xhtmlElem is the HtmlElement representing this table
        self.parent = xhtmlElem.parent
        self.elem = 'table'
        self.cssStyles = CssStyles(self.elem, attrs)
        self.originalStyles = None
        self.removeTag = False
        self.contentDumped = False
        self.name = env.getUniqueStyleName('table')
        # Suffix the table name with a post-processor command when needed
        if attrs and attrs.has_key('keeprows'):
            # This command tells the post-processor to remove some rows from
            # the table.
            self.name += '(%s)' % attrs['keeprows']
            # So ensure the post-processor is enabled
            env.enablePpp()
        self.styleNs = env.ns[OdfEnvironment.NS_STYLE]
        self.tableNs = env.ns[OdfEnvironment.NS_TABLE]
        # Must be set a border for this table ?
        self.border = self.hasBorder()
        # If a CSS property "border-spacing" is defined on this table,
        # m_setTableStyle will parse it and store it here.
        self.borderSpacing = None
        # Get the TableProperties instance. There is always one.
        self.props = props = env.findStyle(self)
        self.style, self.widthInPx, self.originalWidthInPx =self.setTableStyle()
        # Patch the table name when columns must be modified by LO
        modifier = props.columnModifier
        if modifier:
            prefix = props.columnModifiersPrefixes[modifier]
            self.name = '%s_%s' % (prefix, self.name)
        self.res = u'' # The sub-buffer
        # The temporary sub-buffer, into which we will dump all table
        # sub-elements, until we encounter the end of the first row. Then, we
        # will know how much columns are defined in the table; we will dump
        # columns declarations into self.res and dump self.tempRes into
        # self.res.
        self.tempRes = u''
        # Was the first table row completely parsed ?
        self.firstRowParsed = False
        # The number of columns in the table
        self.nbOfColumns = 0
        # Are we currently within a table cell? Instead of a boolean, the field
        # stores an integer. The integer is > 1 if the cell spans more than one
        # column.
        self.inCell = 0
        # The index, within the current row, of the current cell
        self.cellIndex = -1
        # The size of the content of the currently parsed table cell
        self.cellContentSize = 0
        # The size of the longest word of the currently parsed table cell
        self.cellLongestWord = 0
        # The following lists store, for every column: the size of (a) the
        # longest content and (b) the longest words of all its cells.
        self.columnContentSizes = []
        self.columnLongestWords = [] # Computed but currently not used
        # The following list stores, for every column, its width, if specified.
        # If widths are found, self.columnContentSizes will not be used:
        # self.columnWidths will be used instead.
        self.columnWidths = []

    def hasBorder(self):
        '''Support for table borders is currently limited. We have 2 cases:
           either we set a border to the table, either we do not. This method
           r_eturns a boolean value reflecting this, based on the CSS or HTML
           attribute "border". By default, we set a border.'''
        prop = getattr(self.cssStyles, 'border', None)
        if prop is None: return True # By default we set a border
        val = prop.value
        if (val == '0') or ('none' in val) or ('undefined' in val): return
        return True

    def setTableStyle(self):
        '''The default ODT style "podTable" will apply to the table, excepted if
           specific style elements are specified. In this case, we will create a
           dynamic style whose parent will be "podTable". This method returns a
           tuple (styleName, tableWidthPx). The table width in pixels is
           sometimes needed to convert column widths, expressed in pixels, to
           percentages.'''
        tableProps = self.props
        cssStyles = self.cssStyles
        if hasattr(cssStyles, 'borderspacing'):
            # This attribute will be used at the cell level. Extract it and
            # delete it.
            self.borderSpacing = cssStyles.borderspacing
            del cssStyles.borderspacing
        # Get the table width and alignment
        hasWidth = hasattr(cssStyles, 'width')
        width = tableProps.getWidth(cssStyles)
        originalWidth = tableProps.getWidth(cssStyles, original=True)
        align = getattr(cssStyles, 'textalign', 'left')
        # Get the page width, in cm, and the ratio "px2cm"
        pageWidth, px2cmRatio = tableProps.pageWidth, tableProps.px2cm
        pageWidth = pageWidth or self.env.pageWidth
        px2cmRatio = px2cmRatio or px2cm
        # Compute the table attributes for setting its width
        s = self.styleNs
        if width.unit == '%':
            tableWidth = pageWidth * (width.value / 100.0)
            percentage = str(width.value)
        else: # cm or px
            ratio = (width.unit == 'cm') and 1.0 or px2cmRatio
            tableWidth = min(width.value / ratio, pageWidth)
            percentage = formatNumber(float(tableWidth/pageWidth)*100, sep='.')
        # Compute the table size in PX: it will be needed to convert column
        # widths in px to percentages.
        tableWidthPx = int(tableWidth * px2cmRatio)
        # Get the original table size in PX, that can be different from the real
        # one as computed above (see styles_manager::TableProperties.wideAbove).
        if originalWidth.unit == 'px':
            originalTableWidthPx = int(originalWidth.value)
        else:
            originalTableWidthPx = None
        # Get margins if defined
        margins = tableProps.getMargins(cssStyles)
        # Apply attribute "keep-with-next" ?
        kwn = cssStyles.hasClass('TableKWN') and \
              ' fo:keep-with-next="always"' or ''
        # Is the table "unbreakable" ?
        unbreak = tableProps.unbreakable and \
                  ' style:may-break-between-rows="false"' or ''
        # Do not define a specific table style if not necessary
        if not hasWidth and not margins and not kwn and not unbreak and \
           (align == 'left'):
            return 'podTable', tableWidthPx, originalTableWidthPx
        # Define a specific style for this table and return its name
        decl = '<%s:style %s:name="%s" %s:family="table" ' \
               '%s:parent-style-name="podTable"><%s:table-properties ' \
               '%s:width="%scm" %s:rel-width="%s%%" %s:table-align="%s" ' \
               '%s:align="%s"%s%s%s/></%s:style>' % \
               (s, s, self.name, s, s, s, s, formatNumber(tableWidth, sep='.'),
                s, percentage, self.tableNs, align, self.tableNs, align,
                margins, kwn, unbreak, s)
        self.env.stylesManager.dynamicStyles.add('content', decl)
        return self.name, tableWidthPx, originalTableWidthPx

    def setColumnWidth(self, width):
        '''A p_width is defined for the current cell. Store it in
           self.columnWidths'''
        # But first, ensure self.columnWidths is long enough
        widths = self.columnWidths
        while (len(widths)-1) < self.cellIndex: widths.append(None)
        # The first encountered value will be kept
        if widths[self.cellIndex] == None:
            widths[self.cellIndex] = width

    def softenWidths(self):
        '''Reduce columns widths being proportionnaly too large'''
        sizes = self.columnContentSizes
        i = len(sizes) - 1
        while i >= 0:
            # Calibrate the value in order to soften differences between small
            # and large column widths.
            value = sizes[i]
            if not value:
                i -= 1
                continue
            elif value < 5: value = 10
            elif value < 50: value = value * 2.5
            else:
                value = min(value, 1000)
            sizes[i] = int(math.pow(math.log(value), 3))
            i -= 1
        return sizes

    def computeColumnStyles(self):
        '''Once the table has been completely parsed, self.columnContentSizes
           should be correctly filled. Based on this, we can deduce the width
           of every column and create the corresponding style declarations, in
           p_self.env.stylesManager.dynamicStyles.'''
        # The objective is to compute, in "widths", relative column widths,
        # as percentages, from 0 to 1.0.
        widths = []
        i = 0
        # Compute the min and max column sizes, as percentages
        minCellWidth = min(1.0/(self.nbOfColumns*2), self.props.minColumnWidth)
        maxCellWidth = 1 - minCellWidth
        # 1st step: collect or compute widths for columns for which a width has
        # been specified.
        remainingPc = 1.0 # What global percentage will remain after this step ?
        noWidth = 0 # Count the number of columns with no specified width
        tableWidth = self.originalWidthInPx or self.widthInPx
        while i < self.nbOfColumns:
            if (i < len(self.columnWidths)) and self.columnWidths[i]:
                width = self.columnWidths[i]
                if width.unit == 'px':
                    widthAsPc = width.value / tableWidth
                elif width.unit == '%':
                    widthAsPc = width.value / 100
                else:
                    # "cm" or "pt". Ignore this for the moment.
                    widthAsPc = None
                # Ignore the computed width if wrong
                if (widthAsPc <= minCellWidth) or (widthAsPc >= maxCellWidth):
                    # A cell width of 1.0 (=100%) must be ignored: if there is a
                    # single cell, it is implicit; if there are more cells, it
                    # means that others cells will have a width of 0% and will
                    # be invisible.
                    widthAsPc = None
                widths.append(widthAsPc)
                if widthAsPc:
                    remainingPc -= widthAsPc
                else:
                    noWidth += 1
            else:
                widths.append(None)
                noWidth += 1
            i += 1
        # We must guarantee that at least 5% are available for every column
        # having no percentage yet. Else, they could be invisible. If it is not
        # the case, reset all column widths.
        if noWidth:
            required = minCellWidth * noWidth
            if remainingPc < required:
                widths = [None] * len(widths)
                remainingPc = 1.0
        # 2nd step: compute widths of columns for which no width has been
        # specified, by using self.columnContentSizes and
        # self.columnLongestWords. As a preamble, compute the total size of
        # content from all columns.
        contentTotal = 0
        i = 0
        contentSizes = self.softenWidths()
        longestWords = self.columnLongestWords
        while i < self.nbOfColumns:
            # Ignore columns for which a width has already been computed
            if widths[i] is None:
                if (i < len(contentSizes)) and contentSizes[i]:
                    contentTotal += contentSizes[i]
            i += 1
        # We will first store, in "widths", a tuple (f_width, b_minForced)
        # instead of a f_width directly. Indeed, we must ensure that every such
        # width is >= minCellWidth. All cells with a width below it will be
        # flagged with p_minForced=True. And in a second step, the surplus
        # granted to those cells will be deduced from the others.
        i = 0
        surplus = 0.0 # The total surplus granted to too narrow cells
        remainingCount = 0 # The number of cells with no surplus
        while i < self.nbOfColumns:
            if widths[i] is None:
                # Get the content size and longest word for this column
                if (i < len(contentSizes)) and contentSizes[i]:
                    contentSize = contentSizes[i]
                    longest = longestWords[i]
                else:
                    contentSize = longest = 0
                # Compute the column width
                if contentSize == 0:
                    val = 0
                else:
                    width = (float(contentSize) / contentTotal) * remainingPc
                    if width < minCellWidth:
                        surplus += minCellWidth - width
                        val = (minCellWidth, True)
                    else:
                        remainingCount += 1
                        val = (width, False)
                widths[i] = val
            i += 1
        # "Convert" stored tuples into final values
        i = 0
        while i < self.nbOfColumns:
            if isinstance(widths[i], tuple):
                if not surplus:
                    # Simply store the value without changing it
                    widths[i] = widths[i][0]
                else:
                    if widths[i][1]:
                        # Simply store the forced minimum
                        widths[i] = widths[i][0]
                    else:
                        # Reduce this value by a part of the surplus
                        widths[i] = widths[i][0] - (surplus / remainingCount)
            i += 1
        # Multiply widths (as percentages) by a predefined number, in order to
        # get a LibreOffice-compliant column width.
        i = 0
        total = 65534.0
        while i < self.nbOfColumns:
            # Compute the width of this column, relative to "total"
            widths[i] = int(widths[i] * total)
            i += 1
        # Compute style declaration corresponding to every column
        s = self.styleNs
        i = 0
        dynamic = self.env.stylesManager.dynamicStyles
        for width in widths:
            i += 1
            decl = '<%s:style %s:name="%s.%d" %s:family="table-column">' \
                   '<%s:table-column-properties %s:rel-column-width="%d*"' \
                   '/></%s:style>' % (s, s, self.name, i, s, s, s, width, s)
            dynamic.add('content', decl)

# ------------------------------------------------------------------------------
class XhtmlEnvironment(XmlEnvironment):
    itemStyles = {'ul': 'podBulletItem', 'ol': 'podNumberItem',
                  'ul_kwn': 'podBulletItemKeepWithNext',
                  'ol_kwn': 'podNumberItemKeepWithNext'}
    defaultListStyles = {'ul': 'podBulletedList', 'ol': 'podNumberedList'}
    # For list styles, this dict maps values of HTML attrbute "type" to CSS
    # property values for attribute "list-style-type".
    typeToListStyleType = {'1': 'decimal', 'a': 'lower-alpha',
      'A': 'upper-alpha', 'i': 'lower-roman', 'I': 'upper-roman',
      'disc': 'disc', 'circle': 'circle', 'square': 'square'}
    # Mapping between HTML list styles and ODT list styles
    listClasses = {'ol': NumberedProperties, 'ul': BulletedProperties}
    # "list-style-type" values supported by OpenDocument
    listFormats = {
      # Number formats
      'lower-alpha': ('a',), 'upper-alpha': ('A',), 'lower-latin': ('a',),
      'upper-latin': ('A',), 'lower-roman': ('i',), 'upper-roman': ('I',),
      'decimal': ('1',),
      # Bullet formats
      'disc': (u'•'), 'circle': (u'◦'), 'square': (u'▪'), 'none': ''}

    def __init__(self, renderer):
        XmlEnvironment.__init__(self)
        self.renderer = renderer
        self.stylesManager = renderer.stylesManager
        self.ns = renderer.currentParser.env.namespaces
        self.res = u''
        self.currentContent = u''
        self.currentElements = [] # Stack of currently walked elements
        self.currentLists = [] # Stack of currently walked lists (ul or ol)
        self.currentTables = [] # Stack of currently walked tables
        self.lastElem = None # Last walked element before the current one
        self.textNs = self.ns[OdfEnvironment.NS_TEXT]
        self.linkNs = self.ns[OdfEnvironment.NS_XLINK]
        self.tableNs = self.ns[OdfEnvironment.NS_TABLE]
        self.styleNs = self.ns[OdfEnvironment.NS_STYLE]
        # The following attr will be True when parsing parts of the XHTML that
        # must be ignored.
        self.ignore = False
        # Maintain a dict of collected [Bulleted|Numbered]Properties instances,
        # to avoid generating the corresponding list styles several times.
        self.listProperties = {}
        # The fusion of currently encountered styles corresponding to XHTML
        # "style-only" tags (STYLE_ONLY_TAGS).
        self.mergedInnerStyles = CssStyles()
        # How much STYLE_ONLY_TAGS are currently walked (whose fusion is in
        # self.mergedInnerStyles) ?
        self.mergedCount = 0
        # The width (in cm, as a float) of pages (margins excluded) within the
        # current document.
        self.pageWidth = renderer.stylesManager.pageLayout.getWidth()
        # It may be required to enable the POD post-processor (=PPP). But did we
        # already do it ?
        self.pppEnabled = False

    def enablePpp(self):
        '''Enable the POD post-processor (if not already done yet)'''
        if self.pppEnabled: return
        self.renderer.enablePpp()
        self.pppEnabled = True

    def getUniqueStyleName(self, type):
        '''Gets a unique name for an element of some p_type (a table, a
           list).'''
        return '%s%s' % (type.capitalize(), getUuid(removeDots=True))

    def getCurrentElement(self, isList=False):
        '''Gets the element that is on the top of self.currentElements or
           self.currentLists.'''
        res = None
        if isList:
            elements = self.currentLists # Stack of list elements only
        else:
            elements = self.currentElements # Stack of all elements (including
            # elements also pushed on other stacks, like lists and tables).
        if elements:
            res = elements[-1]
            if res.removeTag:
                # This tag will not be dumped: the real current one is the
                # parent.
                res = res.parent
        return res

    def anElementIsMissing(self, previous, current):
        return previous and (previous.elem in OUTER_TAGS) and \
               ((not current) or (current.elem in INNER_TAGS))

    def dumpCurrentContent(self, place, elem):
        '''Dumps content that was temporarily stored in self.currentContent
           into the result.'''
        current = self.getCurrentElement()
        # Remove the trailing whitespace if needed
        if place == 'start':
            if self.currentContent.endswith(' ') and \
               ((elem not in INNER_TAGS_NO_BR) or (elem == 'img')):
                self.currentContent = self.currentContent[:-1]
        # Remove the leading whitespace if needed
        if self.currentContent.startswith(' '):
            last = self.lastElem
            if (place == 'end') and (elem in INNER_TAGS):
                parent = current.parent
                if not parent or \
                   ((parent.elem not in INNER_TAGS) and \
                     not parent.contentDumped) or \
                   (last and (last.elem == 'br')):
                    self.currentContent = self.currentContent[1:]
            else:
                if not last or (last.elem not in INNER_TAGS_NO_BR):
                    self.currentContent = self.currentContent[1:]
        if self.currentContent:
            # Manage missing elements
            if self.anElementIsMissing(current, None):
                current.addInnerParagraph(self)
            # Dump the current content
            self.dumpString(Escape.xml(self.currentContent))
            current.show(self, content='...', prefix='')
            for e in self.currentElements:
                e.contentDumped = True
        # Reinitialise the current content
        if self.currentContent:
            # If we are within a table cell, update the total size of cell
            # content and the longest found word.
            if self.currentTables and self.currentTables[-1].inCell:
                contentSize = len(self.currentContent)
                longest = 0 # Longest word's size
                # "longest" is currently not used. We do not compute it to save
                # processing.
                # for word in self.currentContent.split():
                #    longest = max(longest, len(word))
                for table in self.currentTables:
                    table.cellContentSize += contentSize
                    table.cellLongestWord = max(table.cellLongestWord, longest)
            self.currentContent = u''

    def getOdfAttributes(self, xhtmlElem):
        '''Gets the ODF attributes to dump for p_xhtmlElem'''
        # Complete attributes if inherited from a parent tag
        if xhtmlElem.elem in ('td', 'th'):
            table = self.currentTables[-1]
            # Manage cells' borders
            border = table.props.border
            if border is None:
                border = table.border and '0.05pt solid #000000' or '0'
            xhtmlElem.cssStyles.add('border', border)
            # Manage cells' spacing
            spacing = table.borderSpacing
            if spacing:
                # A minimum cell padding may be applicable
                value = table.props.getCellPadding(spacing)
                xhtmlElem.cssStyles.add('border-spacing', '%.2fcm' % value)
        else:
            parent = xhtmlElem.parent
            if parent and (parent.elem in ('td', 'th')) and \
               (xhtmlElem.elem in PARA_TAGS):
                # The enclosed "p" must get the td's inner styles
                if parent.innerStyle:
                    xhtmlElem.cssStyles.addClass(parent.innerStyle,
                                                 append=False)
                if parent.innerCssStyles:
                    xhtmlElem.cssStyles.merge(parent.innerCssStyles)
        # Get the base ODF style for this p_xhtmlElem
        style = self.findStyle(xhtmlElem)
        if style: return style.getOdfAttributes(xhtmlElem.attrs)
        return ''

    def addListProperties(self, elem, listProps):
        '''Ensures the ListProperties instance p_listProps is among
           self.listProperties.'''
        for name, value in self.listProperties.iteritems():
            if value == listProps:
                return name
        # If we are here, p_listProps wat not found. Add it.
        name = self.getUniqueStyleName('list')
        self.listProperties[name] = listProps
        return name

    def addListPropertiesByName(self, elem, name):
        '''A specific list style must be used, based on HTML attribute "type" or
           CSS property "list-style-type". Add the corresponding
           BulletedProperties or NumberedProperties instance in
           self.listProperties if not present yet.'''
        if name in self.listProperties: return
        # Determine the ListProperties class to use
        klass = self.listClasses[elem]
        # Determine the format of bullets/numbers
        formats = (name in self.listFormats) and self.listFormats[name] or \
                  klass.defaultFormats
        # Create the Properties instance
        styleName = 'L-%s' % name
        self.listProperties[styleName] = klass(formats=formats)
        return styleName

    def getListStyle(self, xhtmlElem, attrs):
        '''Gets the list style to apply to p_xhtmlElem (a "ol" or "ul"). If no
           specific style information is found in p_attrs, a default style is
           applied, from XhtmlEnvironment.defaultListStyles. Else, a specific
           list style is created and added to dynamic styles.'''
        # Check if a specific style must be created
        res = None
        # Check first in the styles mappings
        listProps = self.findStyle(xhtmlElem)
        elem = xhtmlElem.elem
        if listProps:
            # I have a ListProperties instance from a styles mapping. Get a name
            # for the corresponding style.
            xhtmlElem.paraStyle = listProps.paraStyle
            return self.addListProperties(elem, listProps)
        # Check CSS attribute "list-style-type"
        styles = xhtmlElem.cssStyles
        if hasattr(styles, 'liststyletype'):
            typeValue = styles.liststyletype.value
            if typeValue not in ('initial', 'inherit'):
                res = typeValue
        # Check HTML attribute "type"
        if not res and attrs.has_key('type'):
            res = self.typeToListStyleType.get(attrs['type'])
        if res:
            # A specific style has been found. Ensure it will be added among
            # dynamic styles.
            res = self.addListPropertiesByName(elem, res)
        else:
            # Apply a default style, added by default among dynamic styles
            res = self.defaultListStyles[elem]
        return res

    def getTags(self, elems, start=True,
                ignoreToRemove=False, ignoreWaiting=False):
        '''This method returns a series of start or end tags (depending on
           p_start) that correspond to HtmlElement instances in p_elems.'''
        res = ''
        for elem in elems:
            # Ignore tags flagged "to remove" when relevant
            if ignoreToRemove and elem.removeTag: continue
            # Ignore not-yet-dumped elements when relevant
            if ignoreWaiting and (elem.dumpStatus == 'waiting'): continue
            # Get the tag
            tag = elem.dump(start, self)
            if start: res += tag
            else: res = tag + res
        return res

    def closeConflictualElements(self, conflictElems):
        '''This method dumps end tags for p_conflictElems, excepted if those
           tags would be empty. In this latter case, tags are purely removed
           from the result.'''
        startTags = self.getTags(conflictElems, start=True,
                                 ignoreToRemove=True, ignoreWaiting=True)
        if startTags and self.res.endswith(startTags):
            # In this case I would dump an empty (series of) tag(s). Instead, I
            # will remove those tags.
            self.res = self.res[:-len(startTags)]
        else:
            tags = self.getTags(conflictElems, start=False,
                                ignoreToRemove=True, ignoreWaiting=True)
            self.dumpString(tags)
        return conflictElems

    def dumpString(self, s):
        '''Dumps arbitrary content p_s.
           If the table stack is not empty, we must dump p_s into the buffer
           corresponding to the last parsed table. Else, we must dump p_s
           into the global buffer (self.res).'''
        if self.currentTables:
            currentTable = self.currentTables[-1]
            if (not currentTable.res) or currentTable.firstRowParsed:
                currentTable.res += s
            else:
                currentTable.tempRes += s
        else:
            self.res += s

    def getTagsToReopen(self, conflictElems):
        '''Normally, tags to reopen are equal to p_conflictElems. But we have a
           special case. Indeed, if a conflict elem has itself tagsToClose,
           the last tag to close may not be needed anymore on the tag to
           reopen, so we remove it.'''
        conflictElems[-1].tagsToClose = None
        return conflictElems

    def onElementStart(self, elem, attrs):
        '''Returns an HtmlElement instance representing the currently walked
           p_elem.'''
        self.dumpCurrentContent('start', elem)
        parent = self.getCurrentElement()
        current = HtmlElement(elem, attrs, parent=parent)
        # Insert a line-break when relevant
        if parent and parent.dumpLineBreakOnInner:
            if elem in INNER_TAGS:
                self.dumpString('<text:line-break/>')
                current.show(self, content='br', prefix='')
            parent.dumpLineBreakOnInner = False
        # Manage conflictual elements
        conflictElems = current.getConflictualElements(self)
        if conflictElems:
            # We must close the conflictual elements, and once the currentElem
            # will be dumped, we will re-open the conflictual elements.
            toReopen = self.closeConflictualElements(conflictElems)
            current.tagsToReopen = self.getTagsToReopen(toReopen)
        # Manage missing elements
        if self.anElementIsMissing(parent, current):
            parent.addInnerParagraph(self)
        # Add the current element to the stack of walked elements
        self.currentElements.append(current)
        if elem in XHTML_LISTS:
            # Update stack of current lists
            self.currentLists.append(current)
        elif elem == 'table':
            # Update stack of current tables
            self.currentTables.append(HtmlTable(self, current, attrs))
        elif elem in TABLE_COL_TAGS:
            # Determine colspan
            colspan = 1
            if attrs.has_key('colspan'): colspan = int(attrs['colspan'])
            table = self.currentTables[-1]
            table.inCell = colspan
            table.cellIndex += colspan
            # If we are in the first row of a table, update columns count
            if not table.firstRowParsed:
                table.nbOfColumns += colspan
            styles = current.cssStyles
            if hasattr(styles, 'width') and (colspan == 1):
                table.setColumnWidth(styles.width)
            # Determine the styles to apply to inner-cell paragraphs
            if elem == 'td':
                current.innerStyle = table.props.cellContentStyle
            elif elem == 'th':
                current.innerStyle = table.props.headerContentStyle
        return current

    def onElementEnd(self, elem):
        res = None
        self.dumpCurrentContent('end', elem)
        current = self.currentElements.pop()
        if elem in XHTML_LISTS:
            self.currentLists.pop()
        elif elem == 'table':
            table = self.currentTables.pop()
            if table.nbOfColumns:
                # Computes the column styles required by the table
                table.computeColumnStyles()
            # Dumps the content of the last parsed table into the parent buffer
            self.dumpString(table.res)
        elif elem in TABLE_ROW_TAGS:
            table = self.currentTables[-1]
            table.cellIndex = -1
            if not table.firstRowParsed and table.nbOfColumns:
                # If no cell has been parsed yet, we have an empty row that must
                # be ignored.
                table.firstRowParsed = True
                # First row is parsed. The number of columns in the table is
                # known: columns declarations can be dumped.
                for i in range(1, table.nbOfColumns + 1):
                    table.res+= '<%s:table-column %s:style-name="%s.%d"/>' % \
                                (self.tableNs, self.tableNs, table.name, i)
                table.res += table.tempRes
                table.tempRes = u''
        elif elem in TABLE_COL_TAGS:
            table = self.currentTables[-1]
            # If we are walking a td or th, update "columnContentSizes" and
            # "columnLongestWords" for the currently parsed table, excepted if
            # the cell spans several columns.
            if elem != 'col':
                # Divide the content size if cell colspan > 1
                cellContentSize = table.cellContentSize / table.inCell
                cellLongestWord = table.cellLongestWord / table.inCell
                i = table.cellIndex
                sizes = table.columnContentSizes
                wordSizes = table.columnLongestWords
                # Insert None values if the lists are too small
                while (len(sizes)-1) < i:
                    sizes.append(None)
                    wordSizes.append(None)
                longest = max(sizes[i], cellContentSize, 5)
                wordLongest = max(wordSizes[i], cellLongestWord, 5)
                sizes[i] = longest
                wordSizes[i] = min(wordLongest, 25)
            table.inCell = table.cellContentSize = table.cellLongestWord = 0
        if current.tagsToClose:
            self.closeConflictualElements(current.tagsToClose)
        if current.tagsToReopen:
            res = current.tagsToReopen
        if current.removeTag:
            current.parent.dumpLineBreakOnInner = True
        self.lastElem = current
        return current, res

    def findStyle(self, elem):
        converter = self.parser.caller
        localStylesMapping = converter.localStylesMapping
        return converter.stylesManager.findStyle(elem, localStylesMapping)

    def updateMergedStyles(self, action, xhtmlElem):
        '''Updates the current set of applicable inner styles after inner tag
           p_xhtmlElem has been encountered.'''
        styles = self.mergedInnerStyles
        if action == 'add':
            # Add the CSS styles related to the encountered p_xhtmlElem to
            # self.mergedInnerStyles.
            originalStyles = xhtmlElem.cssStyles
            self.mergedInnerStyles.merge(originalStyles)
            xhtmlElem.cssStyles = self.mergedInnerStyles
            xhtmlElem.originalStyles = originalStyles
            self.mergedCount += 1
        elif action == 'delete':
            # Remove the CSS styles related to p_xhtmlElem from
            # self.mergedInnerStyles.
            originalStyles = xhtmlElem.originalStyles
            self.mergedInnerStyles.unmix(originalStyles)
            xhtmlElem.cssStyles = originalStyles
            xhtmlElem.originalStyles = None
            self.mergedCount -= 1

# ------------------------------------------------------------------------------
class XhtmlParser(XmlParser):
    def lowerizeInput(self, elem, attrs=None):
        '''Because (X)HTML is case insensitive, we may receive input p_elem and
           p_attrs in lower-, upper- or mixed-case. So here we produce lowercase
           versions that will be used throughout our parser.'''
        resElem = elem.lower()
        resAttrs = attrs
        if attrs:
            resAttrs = {}
            for attrName in attrs.keys():
                resAttrs[attrName.lower()] = attrs[attrName]
        if attrs == None:
            return resElem
        else:
            return resElem, resAttrs

    def startElement(self, elem, attrs):
        elem, attrs = self.lowerizeInput(elem, attrs)
        e = self.env
        dump = e.dumpString
        current = e.onElementStart(elem, attrs)
        parent = current.parent
        current.show(e)
        if current.removeTag: # Do not dump this tag
            if parent.contentDumped:
                # Dump a line break instead, only if content was already dumped
                # into the parent.
                dump('<text:line-break/>')
                current.show(self, content='br', prefix='')
            return
        odfTag = current.getOdfTag()
        if elem in SIMPLE_TAGS:
            dump('<' + odfTag)
            dump(e.getOdfAttributes(current))
            dump('>')
        elif elem in STYLE_ONLY_TAGS:
            # Dump an end tag if we are already dumping styled content
            if e.mergedCount and (parent.dumpStatus == 'dumped'):
                dump('</%s>' % odfTag)
            e.updateMergedStyles('add', current)
            # We will dump this tag only if subsequent content is found
            current.dumpStatus = 'waiting'
        elif elem == 'a':
            dump('<%s %s:type="simple"' % (odfTag, e.linkNs))
            if attrs.has_key('href'):
                dump(' %s:href="%s"' % (e.linkNs, Escape.xml(attrs['href'])))
            dump('>')
        elif elem in XHTML_LISTS:
            prologue = ''
            if parent and (parent.elem in XHTML_LISTS):
                # It is a list into another list. In this case the inner list
                # must be surrounded by a list-item element.
                prologue = '<text:list-item>'
            numbering = ''
            if elem == 'ol':
                # By default, LO seems to continue numbering or previous lists
                numbering = ' text:continue-numbering="false"'
            current.odStyle = e.getListStyle(current, attrs)
            dump('%s<%s text:style-name="%s"%s>' % (
                 prologue, odfTag, current.odStyle, numbering))
        elif elem == 'li':
            # Must numbering restart at this "li" ?
            current = e.currentLists[-1]
            current.subNumber += 1
            numbered = current.elem == 'ol'
            start = None
            if numbered:
                attrs = current.attrs
                start = None
                if attrs and ('start' in attrs):
                    start = attrs['start']
                    del attrs['start']
                elif current.subNumber == 1:
                    start = 1
            if start is None:
                restart = ''
            else:
                restart = ' text:start-value="%d"' % start
            dump('<%s%s>' % (odfTag, restart))
        elif elem == 'thead':
            dump('<%s>' % odfTag)
        elif elem == 'tr':
            attr = e.currentTables[-1].props.unbreakableRows and \
                   ' table:style-name="podUnbreakableRow"' or ''
            dump('<%s%s>' % (odfTag, attr))
        elif elem == 'table':
            # Here we must call "dumpString" only once
            table = e.currentTables[-1]
            dump('<%s %s:name="%s" %s:style-name="%s">' % \
                 (odfTag, e.tableNs, table.name, e.tableNs, table.style))
        elif elem == 'img':
            conv = self.caller
            src = attrs.get('src', '').strip()
            if src: 
                imgCode = e.renderer.importDocument(at=attrs['src'],
                  format='image', wrapInPara=False, style=current.cssStyles,
                  maxWidth=conv.imagesMaxWidth, keepRatio=conv.keepImagesRatio)
                dump(imgCode)
        elif elem == 'footnote':
            # An inexistent tag in HTML, nervertheless usable to produce ODF
            # footnotes.
            nb = attrs['nb']
            dump('<text:note text:id="ftn%s" text:note-class="footnote">' \
                 '<text:note-citation>%s</text:note-citation><text:note-body>'%\
                 (nb, nb))
        elif elem == 'tab':
            # Another inexistent tag in HTML, useful for managing tabs
            dump('<text:tab/>')
        elif elem in IGNORABLE_TAGS:
            e.ignore = True

    def endElement(self, elem):
        elem = self.lowerizeInput(elem)
        e = self.env
        dump = e.dumpString
        current, elemsToReopen = e.onElementEnd(elem)
        # Determine the tag to dump
        startTag, endTag = current.getOdfTags()
        if current.isConflictual:
            # Compute the start tag, with potential styles applied
            startTag = e.getTags((current,), start=True)
        if current.isConflictual and e.res.endswith(startTag):
            # We will not dump it, it would constitute a silly empty tag
            e.res = e.res[:-len(startTag)]
            if current.elem in STYLE_ONLY_TAGS:
                e.mergedCount -= 1
        else:
            # Dump the end tag, but dump some additional stuff if required
            if elem == 'footnote':
                dump('</text:note-body></text:note>')
            elif elem in XHTML_LISTS:
                if current.parent and (current.parent.elem in XHTML_LISTS):
                    # We were in an inner list. So we must close the list-item
                    # tag that surrounds it.
                    endTag = '%s</text:list-item>' % endTag
            if endTag and not current.removeTag and \
               (current.dumpStatus != 'waiting'):
                dump(endTag)
                current.show(e, prefix='>')
            # Manage the end of a styled inner tag
            if elem in STYLE_ONLY_TAGS:
                # Unmix styles corresponding to this end tag
                e.updateMergedStyles('delete', current)
                parent = current.parent
                if e.mergedCount and (parent.elem in STYLE_ONLY_TAGS):
                    # Possibly reopen a tag. The parent is already loaded with
                    # merged styles.
                    parent.dumpStatus = 'waiting'
            elif (elem not in INNER_TAGS) and not current.inInnerTag():
                # We are not in an "inner" zone anymore
                e.mergedCount = 0
        if elem in IGNORABLE_TAGS:
            e.ignore = False
        if elemsToReopen:
            dump(e.getTags(elemsToReopen, start=True, ignoreWaiting=True))

    def characters(self, content):
        e = XmlParser.characters(self, content)
        if e.ignore: return
        # Dump a tag waiting for content
        current = e.getCurrentElement()
        if current.dumpStatus == 'waiting':
            dump = e.dumpString
            dump('<' + current.getOdfTag())
            dump(e.getOdfAttributes(current))
            dump('>')
            current.dumpStatus = 'dumped'
        e.currentContent += WhitespaceCruncher.crunch(content, e.currentContent)

    def endDocument(self):
        '''Dump all collected list styles'''
        styles = self.caller.stylesManager.dynamicStyles.styles_base
        for name, props in self.env.listProperties.iteritems():
            styles.append(props.dumpStyle(name))

# ------------------------------------------------------------------------------
class XhtmlPreprocessor:
    '''The Xhtml2OdtConverter (see below) requires valid XHTML as input, because
       it uses a SAX parser to do its job. This preprocessor ensures it is the
       case, by applying some modifications to this input.'''
    # Regular expression representing a HTML void tag
    voidTags = ('area', 'base', 'br', 'col', 'hr', 'img', 'input', 'link',
                'meta', 'param', 'command', 'keygen', 'source')
    voidTag = re.compile('<(%s)([^>]*?)(/)?\s*>' % '|'.join(voidTags), re.S)

    @staticmethod
    def patchTag(match):
        '''Add the trailing slash if absent'''
        # If char "/" is already here, do not change anything
        if match.group(3): return match.group(0)
        return '<%s%s/>' % (match.group(1), match.group(2))

    @staticmethod
    def html2xhtml(s):
        '''Converts valid HTML p_s to valid XHTML'''
        return re.sub(XhtmlPreprocessor.voidTag, XhtmlPreprocessor.patchTag, s)

    @staticmethod
    def preprocess(s, html=False):
        '''Converts string p_s to valid XHTML and r_eturns it. If p_html is
           True, p_s is supposed to be valid HTML: void tags must be converted
           to XHTML's self-closing start tags.'''
        if s == None: s = ''
        # Manage encoding
        if isinstance(s, unicode): s = s.encode('utf-8')
        # Surround p_s with a tag in order to get a XML-compliant file (we need
        # a root tag). We also remove special blank chars that produce SAX
        # parsing errors.
        s = '<p>%s</p>' % s.replace('\f', '').replace('\v', '')
        # Convert, when required, conversion of HTML's void tags to XHTML's
        # self-closing start tags.
        if html:
            s = XhtmlPreprocessor.html2xhtml(s)
        return s

# ------------------------------------------------------------------------------
class Xhtml2OdtConverter:
    '''Converts a chunk of XHTML into a chunk of ODT'''
    verbose = False

    def __init__(self, s, encoding, stylesManager, localStylesMapping,
                 keepWithNext, keepImagesRatio, imagesMaxWidth, renderer,
                 html, unwrap):
        self.renderer = renderer
        self.xhtmlString = XhtmlPreprocessor.preprocess(s, html=html)
        self.encoding = encoding # Todo: manage encoding that is not utf-8
        self.stylesManager = stylesManager
        self.localStylesMapping = localStylesMapping
        self.odtChunk = None
        self.xhtmlParser = XhtmlParser(XhtmlEnvironment(renderer), self)
        if keepWithNext:
            if (keepWithNext is True) or (keepWithNext > 1):
                # Apply "keep-with-next" functionality by using a sub-SAX parser
                from appy.pod.xhtml import parser as xparser
                parser = xparser.XhtmlParser(xparser.XhtmlEnvironment(), self,
                                             keepWithNext=keepWithNext)
                self.xhtmlString= parser.parse(self.xhtmlString).encode('utf-8')
            else:
                self.xhtmlString = self.applyKeepWithNext()
        self.keepImagesRatio = keepImagesRatio
        self.imagesMaxWidth = imagesMaxWidth
        self.unwrap = unwrap
        # In verbose mode, we dump a trace of the xhtml2odt algorithm
        self.xhtmlParser.verbose = self.xhtmlParser.env.verbose = self.verbose
        # Some components within the styles manager may require the XHTML parser
        # for generating some styles.
        self.stylesManager.setXhtmlParser(self.xhtmlParser)

    def run(self):
        '''Parses the input XHTML string and returns the resulting ODF chunk'''
        self.xhtmlParser.parse(self.xhtmlString)
        r = self.xhtmlParser.env.res
        if self.unwrap and r.startswith('<text:p>'):
            r = r[8:-9]
        return r

    def applyKeepWithNext(self):
        '''This method is called prior to parsing self.xhtmlString in order to
           add specific CSS classes to some XHTML tags, implementing the
           "keep-with-next" functionality. If the last tag is:
           * a paragraph (tag "p"), class "ParaKWN" will be set;
           * a bullet (tag "li"), class "podItemKeepWithNext" will be set.

           Note that this latter class will then be converted by the XHTML
           parser into "real" style "podBulletItemKeepWithNext" or
           "podNumberItemKeepWithNext", if the "li" is, respectively, in a "ul"
           or "ol" tag.
        '''
        res = self.xhtmlString
        lastParaIndex = res.rfind('<p')
        lastItemIndex = res.rfind('<li')
        if (lastParaIndex != -1) or (lastItemIndex != -1):
            # Is the last one a paragraph or an item ?
            if lastParaIndex > lastItemIndex:
                # A paragraph
                styleName = 'ParaKWN'
                elemLenght = 2
            else:
                # An item
                styleName = 'podItemKeepWithNext'
                elemLenght = 3
            maxIndex = max(lastParaIndex, lastItemIndex)
            # Does this element already have a "class" attribute ?
            if res.find('class="', maxIndex) == -1:
                # No: I add the style
                res = res[:maxIndex+elemLenght] + (' class="%s" ' % styleName) \
                      + res[maxIndex+elemLenght:]
        return res
# ------------------------------------------------------------------------------
