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
from appy import ui, utils

# Error messages - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
TB_COLS_ERR = 'A tabs-style group must have a single column.'
G_COLS_ERR  = 'For a grid-style group, you must specify an even number of ' \
              'columns, in order to produce couples of label/field columns. ' \
              'For every couple, the first columns holds a field label and ' \
              'the second one holds the field content.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Group:
    '''Used for describing a group of fields within a page'''
    def __init__(self, name, columns=None, wide=True, style='section2',
      hasLabel=True, hasDescr=False, hasHelp=False, hasHeaders=False,
      group=None, colspan=1, align='center', valign='top', css_class='',
      labelCss=None, master=None, masterValue=None, cellpadding=1,
      cellspacing=1, cellgap='0.6em', label=None, translated=None):
        self.name = name
        # In its simpler form, field "columns" below can hold a list or tuple
        # of column widths expressed as strings, that will be given as is in
        # the "width" attributes of the corresponding "td" tags. Instead of
        # strings, within this list or tuple, you may give Column instances
        # (see below).
        self.columns = columns
        self._setColumns(style)
        # If field "wide" below is True, the HTML table corresponding to this
        # group will have width 100%. You can also specify some string value,
        # which will be used for HTML param "width".
        if wide == True:
            self.wide = '100%'
        elif isinstance(wide, str):
            self.wide = wide
        else:
            self.wide = ''
        # Groups of various styles can be rendered. If "style" is:
        # - 'sectionX'  (X can be 1, 2, 3...) 
        #               the group will be rendered as a "section": the group
        #               title will be rendered in some style (depending on X)
        #               before the widgets;
        # - 'fieldset'  all widgets within the group will be rendered within an
        #               HTML fieldset;
        # - 'tabs'      the group will be rendered as tabs. One tab will be
        #               rendered for every inner widget. If you want some tab to
        #               contain several widgets, specify a group as sub-group of
        #               the group having style 'tabs';
        # - 'grid'      the widgets will be rendered in some standardized,
        #               tabular way.
        self.style = style
        # If hasLabel is True, the group will have a name and the corresponding
        # i18n label will be generated.
        self.hasLabel = hasLabel
        # If hasDescr is True, the group will have a description and the
        # corresponding i18n label will be generated.
        self.hasDescr = hasDescr
        # If hasHelp is True, the group will have a help text associated and the
        # corresponding i18n label will be generated.
        self.hasHelp = hasHelp
        # If hasheaders is True, group content will begin with a row of headers,
        # and a i18n label will be generated for every header.
        self.hasHeaders = hasHeaders
        self.nbOfHeaders = len(self.columns)
        # If this group is himself contained in another group, the following
        # attribute is filled.
        self.group = Group.get(group)
        # If the group is rendered into another group, we can specify the number
        # of columns that this group will span.
        self.colspan = colspan
        self.align = align
        self.valign = valign
        self.cellpadding = cellpadding
        self.cellspacing = cellspacing
        # Beyond standard cellpadding and cellspacing, cellgap can define an
        # additional horizontal gap between cells in a row. So this value does
        # not add space before the first cell or after the last one.
        self.cellgap = cellgap
        if style == 'tabs':
            # Group content will be rendered as tabs. In this case, some
            # param combinations have no sense.
            self.hasLabel = self.hasDescr = self.hasHelp = False
            # Inner field/group labels will be used as tab labels
        # "css_class", if specified, will be applied to the whole group
        self.css_class = css_class
        # "labelCss" is the CSS class that will be applied to the group label
        self._setLabelCss(labelCss, style)
        self.master = master
        self.masterValue = utils.initMasterValue(masterValue)
        if master: master.slaves.append(self)
        self.label = label # See similar attr of Type class
        # If a translated name is already given here, we will use it instead of
        # trying to translate the group label.
        self.translated = translated

    def __repr__(self):
        '''p_self's string representation'''
        parent = ',parent=%s' % self.group.name if self.group else ''
        return '<group %s%s>' % (self.name, parent)

    def _setColumns(self, style):
        '''Standardizes field "columns" as a list of Column instances. Indeed,
           the initial value for field "columns" may be a list or tuple of
           Column instances or strings.'''
        # Start with a default value, if self.columns is None
        if not self.columns:
            if style == 'grid':
                # One column for the labels, another for the remaining elements
                self.columns = ['150em', '']
            else:
                self.columns = ['100%']
        # Standardize columns as a list of Column instances
        for i in range(len(self.columns)):
            columnData = self.columns[i]
            if not isinstance(columnData, Column):
                self.columns[i] = Column(self.columns[i])
        # Standardize or check columns depending on group style
        if style == 'tabs':
            # There must be a unique column
            if len(self.columns) > 1: raise Exception(TB_COLS_ERR)
        elif style == 'grid':   
            # grid has always an even number of columns (couples of label/field
            # columns)
            if len(self.columns) % 2: raise Exception(G_COLS_ERR)

    def _setLabelCss(self, labelCss, style):
        '''For "sectionX"-style groups, the applied CSS class is by default the
           p_style itself. For the other styles of groups (tabs, grids,...) it
           is not the case.'''
        if labelCss:
            self.labelCss = labelCss
        else:
            # Set a default value for the label CSS
            if style.startswith('section'):
                self.labelCss = style
            else:
                self.labelCss = 'section3'

    @staticmethod
    def get(groupData):
        '''Produces a Group instance from p_groupData. User-defined p_groupData
           can be a string or a Group instance; this method returns always a
           Group instance.'''
        res = groupData
        if res and isinstance(res, str):
            # Group data is given as a string. 2 more possibilities:
            # (a) groupData is simply the name of the group;
            # (b) groupData is of the form <groupName>_<numberOfColumns>.
            groupElems = groupData.rsplit('_', 1)
            if len(groupElems) == 1:
                res = Group(groupElems[0])
            else:
                try:
                    nbOfColumns = int(groupElems[1])
                except ValueError:
                    nbOfColumns = 1
                width = 100.0 / nbOfColumns
                res = Group(groupElems[0], ['%.2f%%' % width] * nbOfColumns)
        return res

    def getMasterData(self):
        '''Gets the master of this group (and masterValue) or, recursively, of
           containing groups when relevant.'''
        if self.master: return self.master, self.masterValue
        if self.group: return self.group.getMasterData()

    def insertInto(self, r, groups, page, className, content='fields'):
        '''Insert the UiGroup instance corresponding to this Group instance
           into p_r, the recursive structure used for displaying elements in a
           given p_page (fields, searches, transitions...) and return this
           UiGroup instance.'''
        # First, create the corresponding UiGroup if not already in p_groups
        if self.name not in groups:
            uiGroup= groups[self.name] = UiGroup(self, page, className, content)
            # Insert the group at the higher level (ie, directly in p_r) if the
            # group is not itself in a group.
            if not self.group:
                r.append(uiGroup)
            else:
                outerGroup = self.group.insertInto(r, groups, page,
                                                   className, content)
                outerGroup.addElement(uiGroup)
        else:
            uiGroup = groups[self.name]
        return uiGroup

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Column:
    '''Used for describing a column within a Group like defined above'''
    def __init__(self, width, align="left"):
        self.width = width
        self.align = align

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class UiGroup:
    '''On-the-fly-generated data structure that groups all elements
       (fields, searches, transitions...) sharing the same Group instance, that
       the currently logged user can see.'''

    # Render a help icon for a group
    pxHelp = Px(lambda c: '<abbr title="%s"><img class="iconS" src="%s"/>' \
                    '</abbr>' % (c._('help', field=c.field), c.url('help.svg')))

    # Render the group title, description and help
    pxHeader = Px('''
     <!-- Title -->
     <tr if="field.hasLabel">
      <td colspan=":len(field.columnsWidths)" class=":field.labelCss"
          align=":dleft">
       <x>::_(field.labelId)</x><x if="field.hasHelp">:field.pxHelp</x>
      </td>
     </tr>
     <tr if="field.hasDescr">
      <td colspan=":len(field.columnsWidths)"
          class="discreet">::_(field.descrId)</td>
     </tr>''')

    # Render the fields within a group in the most frequent cases:
    # style = "sectionX" or "fieldset". The group is referred as var "field".
    pxFields = Px('''
     <table var="cellgap=field.cellgap" width=":field.wide"
            align=":ui.Language.flip(field.align, dir)"
            id=":tagId" name=":tagName" class=":groupCss"
            cellspacing=":field.cellspacing" cellpadding=":field.cellpadding">
      <!-- Title, description and help -->
      <x if="field.showHeader()">:field.pxHeader</x>
      <!-- The column headers -->
      <tr>
       <th for="colNb in range(len(field.columnsWidths))"
           align=":ui.Language.flip(field.columnsAligns[colNb], dir)"
           width=":field.columnsWidths[colNb]">::field.hasHeaders and \
            _('%s_col%d' % (field.labelId, (colNb+1))) or ''</th>
      </tr>
      <!-- The rows of widgets -->
      <tr valign=":field.valign" for="row in field.elements">
       <td for="field in row" colspan=":field.colspan|1"
           style=":not loop.field.last and ('padding-right:%s'% cellgap) or ''">
        <x if="field">:field.pxRender</x>
       </td>
      </tr>
     </table>''')

    # Render a group with style = 'fieldset'
    pxFieldset = Px('''
     <fieldset>
      <legend if="field.hasLabel">
       <i>::_(field.labelId)></i><x if="field.hasHelp">:field.pxHelp</x>
      </legend>
      <div if="field.hasDescr" class="discreet">::_(field.descrId)</div>
      <x>:field.pxFields</x>
     </fieldset>''')

    # Render a group with style = 'tabs'
    pxTabs = Px('''
     <table width=":field.wide" class=":groupCss" id=":tagId" name=":tagName">
      <!-- First row: the tabs -->
      <tr valign="middle"><td class="tabSep tabBottom">
       <table class="tabs" id=":'tabs_%s' % field.name">
        <tr valign="middle">
         <x for="sub in field.elements"
            var2="suffix='%s_%s' % (field.name, sub.name);
                  tabId='tab_%s' % suffix">
          <td class="tab" id=":tabId">
           <a onclick=":'showTab(%s)' % q(suffix)"
              class="clickable">:_(sub.labelId)</a>
          </td>
         </x>
        </tr>
       </table>
      </td></tr>

      <!-- Other rows: the fields -->
      <tr for="sub in field.elements"
          id=":'tabcontent_%s_%s' % (field.name, sub.name)"
          style=":(loop.sub.nb==0) and 'display:table-row' or 'display:none'">
       <td var="field=sub">:field.pxRender</td>
      </tr>
     </table>
     <script>:'initTab(%s,%s,%s)' % \
      (q('tab_%s'%field.name), q('%s_%s'%(field.name, field.elements[0].name)),\
       'true' if o.isTemp() else 'false')</script>''')

    # Render a group with style = 'grid'
    pxGrid = Px('''
     <table cellpadding="0" cellspacing="0" width=":field.wide"
            class=":groupCss" id=":tagId" name=":tagName" align=":field.align">
      <!-- Title, description and help -->
      <x if="field.showHeader()">:field.pxHeader</x>
      <tr><th for="col in field.columns" width=":col.width"></th></tr>
      <tr for="row in field.elements" valign="top"
          class=":loop.row.odd and 'odd' or 'even'">
       <x for="sub in row">
        <td id="summaryCell">
         <label if="sub.hasLabel and \
                    (sub.type != 'Action')">::_('label', field=sub)</label></td>
        <td var="field=sub" id="summaryCell">:field.pxRender</td>
       </x>
       <!-- Complete the last row when relevant -->
       <x if="loop.row.last"
          for="i in range(int((len(field.columns)/2))-len(row))">
         <td></td><td></td>
       </x>
      </tr>
     </table>''')

    # PX that renders a group of fields (the group is referred as var "field")
    pxRender = Px('''
     <x var="tagCss=field.master and ('slave*%s*%s' % \
                    (field.master.getMasterTag(layout), \
                    '*'.join(field.masterValue))) or '';
             widgetCss=field.css_class;
             groupCss=tagCss and ('%s %s' % (tagCss, widgetCss)) or widgetCss;
             tagName=field.master and 'slave' or '';
             tagId='%d_%s' % (o.iid, field.name)">:field.pxFromStyle()</x>''')

    # PX that renders a group of searches
    pxViewSearches = Px('''
     <x var="collapse=field.getCollapseInfo(field.labelId, req)">
      <!-- Group name, prefixed by the expand/collapse icon -->
      <div class="portletGroup"><x>:collapse.px</x>
       <x>:field.translated or _(field.labelId)</x>
      </div>
      <!-- Group content -->
      <div id=":collapse.id" style=":'padding-left: 10px; %s' % collapse.style">
       <x for="searches in field.elements">
        <x for="elem in searches">
         <!-- An inner group within this group -->
         <x if="elem.type== 'group'" var2="field=elem">:field.pxViewSearches</x>
         <!-- A search -->
         <x if="elem.type != 'group'" var2="search=elem">:search.view</x>
        </x>
       </x>
      </div></x>''')

    # PX that renders a group of transitions
    pxViewTransitions = Px('''
     <!-- Render a group of transitions, as a one-column table -->
     <table>
      <x for="row in trGroup.elements">
       <x for="transition in row"><tr><td>:transition.px</td></tr></x>
      </x>
     </table>''')

    # What PX to use, depending on group content?
    pxByContent = {'fields': pxRender, 'searches': pxViewSearches,
                   'transitions': pxViewTransitions}

    def __init__(self, group, page, className, content='fields'):
        '''A UiGroup can group various kinds of elements: fields, searches,
           transitions... The type of content that one may find in this group
           is given in p_content.
           * p_group      is the Group instance corresponding to this UiGroup;
           * p_page       is the Page instance where the group is rendered (for
                          transitions, it corresponds to a virtual page
                          "workflow");
           * p_className  is the name of the class that holds the elements to
                          group.'''
        self.type = 'group'
        # All p_group attributes become self attributes. This is required
        # because a UiGroup, in some PXs, must behave like a Field (ie, have
        # the same attributes, like "master".
        for name, value in group.__dict__.items():
            if not name.startswith('_'):
                setattr(self, name, value)
        self.group = group
        self.columnsWidths = [col.width for col in group.columns]
        self.columnsAligns = [col.align for col in group.columns]
        # The name of the page where the group lies
        self.page = page.name
        # The elements (fields or sub-groups) contained in the group, that the
        # current user may see. They will be inserted by m_addElement below.
        self.flatElements = self.style == 'tabs'
        if self.flatElements:
            # Elements will be stored as a simple list
            self.elements = []
        else:
            # In most cases, "elements" will be a list of lists for rendering
            # them as a table.
            self.elements = [[]]
        # PX to use for rendering this group
        self.px = self.pxByContent[content]
        # Names of i18n labels for this group
        if not self.hasLabel and not self.hasDescr and not self.hasHelp: return
        labelName = self.name
        prefix = None
        if group.label:
            if isinstance(group.label, str): prefix = group.label
            else: # It is a tuple (className, name)
                if group.label[1]: labelName = group.label[1]
                if group.label[0]: prefix = group.label[0]
        if not prefix:
            prefix = '%s_group' % className
        self.labelId = '%s_%s' % (prefix, labelName)
        self.descrId = self.labelId + '_descr'
        self.helpId  = self.labelId + '_help'

    def addElement(self, element):
        '''Adds p_element into self.elements. We try first to add p_element into
           the last row. If it is not possible, we create a new row.'''
        if self.flatElements:
            self.elements.append(element)
            return
        # Get the last row
        lastRow = self.elements[-1]
        numberOfColumns = len(self.columnsWidths)
        # Grid groups span a single field on 2 columns
        if self.style == 'grid': numberOfColumns = numberOfColumns / 2
        # Compute the number of columns already filled in the last row
        filledColumns = 0
        for rowElem in lastRow: filledColumns += rowElem.colspan
        freeColumns = numberOfColumns - filledColumns
        if freeColumns >= element.colspan:
            # We can add the element in the last row
            lastRow.append(element)
        else:
            if freeColumns:
                # Terminate the current row by appending empty cells
                for i in range(freeColumns): lastRow.append('')
            # Create a new row
            self.elements.append([element])

    def getCollapseInfo(self, id, request):
        '''Returns a Collapsible instance, that determines if this group,
           represented as an expandable menu item, is collapsed or expanded.'''
        return ui.Collapsible(id, request)

    def pxFromStyle(self):
        '''Get the PX to use for rendering a group, depending on its style'''
        style = self.style
        if style[-1].isdigit(): return self.pxFields # sectionX
        px = 'px%s' % style.capitalize()
        return getattr(self, px)

    def showHeader(self):
        '''The block "title, description, help" must not be rendered even if it
           exists, because it is rendered elsewhere.'''
        if self.style == 'fieldset': return
        parent = self.group.group
        if parent and (parent.style in ('tabs', 'grid')): return
        return self.hasLabel or self.hasDescr
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
