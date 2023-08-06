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
import sys, re, os.path
from urllib.parse import urlparse, parse_qsl

from persistent.list import PersistentList

from appy.px import Px
from appy import ui, utils
from appy.ui import LinkTarget
from appy.model.batch import Batch
from appy.model.searches import Search
from appy.utils import string as sutils
from appy.model.utils import Object as O
from appy.ui.layout import Layout, Layouts
from appy.model.fields.colset import ColSet
from appy.database.operators import Operator
from appy.model.fields import Field, Initiator

# Errors - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
ATTR_EXISTS = 'Attribute "%s" already exists on class "%s". Note that ' \
              'several back Refs pointing to the same class must have ' \
              'different names, ie: back=Ref(attribute="every_time_a_' \
              'distinct_name",...).'
ADD_LK_KO   = 'Parameters "add" and "link" can\'t both be used.'
BACK_COMP   = 'Only forward Refs may be composite.'
BACK_1_COMP = 'The backward Ref of a composite Ref must have an upper ' \
              'multiplicity of 1. Indeed, a component can not be contained ' \
              'in more than one composite object.'
LK_POP_ERR  = 'When "link" is "popup", "select" must be a instance of ' \
              'appy.fields.search.Search instance or a method that returns ' \
              'such an instance.'
WRITE_KO    = "User can't write Ref field %s::%s. %s."
UNLINK_KO   = 'field.unlinkElement prevents you to unlink this object.'
SEARCH_KO   = 'Ref "%s": attribute "searches" contains at least one unnamed ' \
              'Search instance.'
RADIOS_KO   = "This field can't be rendered as radio buttons because it may " \
              "contain several values (max multiplicity is higher than 1)."
CBS_KO      = "This field can't be rendered as checkboxes because it can " \
              "only contain a single value (max multiplicity is 1)."
DDOWN_KO    = 'A Ref with link="dropdown" must have a max multiplicity being 1.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def setAttribute(class_, name, value):
    '''Sets on p_class_ attribute p_name having some p_value. If this attribute
       already exists, an exception is raised.'''
    if hasattr(class_, name):
        raise Exception(ATTR_EXISTS % (name, class_.__name__))
    setattr(class_, name, value)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Position:
    '''When inserting some object among a list of tied objects, this class gives
       information about where to insert it.'''
    def __init__(self, place, o):
        # p_o is an object (or among tied objects that will be the reference
        # point for the insertion.
        self.insertObject = o
        # p_place can be "before" or "after" and indicates where to insert the
        # new object relative to p_o.
        self.place = place

    def getInsertIndex(self, refs):
        '''Gets the index, within tied objects p_refs, where to insert the newly
           created object.'''
        r = refs.index(self.insertObject)
        if self.place == 'after':
            r += 1
        return r

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class RefInitiator(Initiator):
    '''When an object is added via a Ref field, this class gives information
       about the initiator Ref field and its object.'''

    def __init__(self, tool, req, info):
        Initiator.__init__(self, tool, req, info)
        # We may have information about the place to insert the newly created
        # object into the Ref.
        self.insertInfo = req.insert
        if self.insertInfo:
            place, objectId = self.insertInfo.split('.')
            o = tool.getObject(objectId)
            self.position = Position(place, o)
        else:
            self.position = None

    def checkAllowed(self, log=False):
        '''Checks that adding an object via self.field is allowed'''
        return self.field.checkAdd(self.o, log=log)

    def updateParameters(self, params):
        '''Add the relevant parameters to the object edition page, related to
           this initiator.'''
        # Get potential information about where to insert the object
        if self.insertInfo: params['insert'] = self.insertInfo

    def goBack(self):
        '''After the object has been created, go back to its "view" page or go
           back to the initiator.'''
        return 'view' if self.field.viewAdded else 'initiator'

    def getNavInfo(self, new):
        '''Compute the correct nav info at the newly inserted p_new object'''
        # At what position is p_new among tied objects ?
        o = self.o
        position = self.field.getIndexOf(o, new) + 1
        total = o.countRefs(self.field.name)
        return self.field.getNavInfo(o, position, total)

    def manage(self, new):
        '''The p_new object must be linked with the initiator object and the
           action must potentially be historized.'''
        o = self.o
        # Link the new object to the initiator
        self.field.linkObject(o, new, at=self.position, secure=True)
        # Record this change into the initiator's history when relevant
        if self.field.getAttribute(o, 'historized'):
            title = new.getValue('title', formatted='shown')
            msg = '%s: %s' % (new.translate(new.class_.name), title)
            o.history.add('Link', addition=True, comment=msg)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Separator:
    '''Withins lists of tied objects, one may need to insert one or several
       separator(s). If you need this, specify, in attribute Ref.separator, a
       method that will return an instance of this class.'''

    def __init__(self, label=None, translated=None, css=None):
        # If some text must be shown within the separator, you can specify an
        # i18n p_label for it, or a translated text in p_translated. If
        # p_translated is provided, p_label will be ignored.
        self.label = label
        self.translated = translated
        # The CSS class(es) to apply to the separator
        self.css = css

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Ref(Field):
    # Some elements will be traversable
    traverse = Field.traverse.copy()

    # Make sub-classes available here
    Position = Position
    Separator = Separator

    # Ref-specific layouts
    class Layouts(Layouts):
        '''Ref-specific layouts'''
        base = 'lrv-f'
        # The unique, static cell layout
        cell = Layout('f|', width='100%', css_class='no')
        # Layout for a Ref with link=True
        l = Layouts(edit=Layout(base, width=None), view=Layout('l-f'))
        # Wide layout for a Ref with add=True: it must be 100% wide
        a = Layouts(edit=Layout(base), view=Layout(base))
        # "d" stands for "description": a description label is added, on view
        wd = Layouts(view=Layout('l-d-f'))
        # Wide, but not on edit
        w_e = Layouts(edit=Layout(base, width=None), view=Layout(base))

        @classmethod
        def getDefault(class_, field):
            '''Default layouts for this List p_field'''
            if field.inGrid(): return class_.g
            return class_.l if field.link else class_.a

    # Getting a ref value is something special: disable the standard Appy
    # machinery for this.
    customGetValue = True

    # A Ref has a specific initiator class
    initiator = RefInitiator

    # Its is more practical if the empty value is iterable
    empty = ()

    # The name of the index class storing values of this field in the catalog
    indexType = 'RefIndex'

    # This PX displays the title of a referenced object, with a link on it to
    # reach the consult view for this object. If we are on a back reference, the
    # link allows to reach the correct page where the forward reference is
    # defined. If we are on a forward reference, the "nav" parameter is added to
    # the URL for allowing to navigate from one object to the next/previous one.
    pxObjectTitle = Px('''
     <x var="navInfo=ifield.getNavInfo(initiator.o, batch.start+currentNumber, \
                                      batch.total, inPickList, inMenu);
             pageName=ifield.back.pageName if ifield.isBack else 'main';
             titleMode=ifield.getTitleMode(selector);
             selectJs='onSelectObject(%s,%s,%s,%s)' % (q(cbId), \
                         q(selector.initiatorHook), q(selector.initiator.iid), \
                         q(selector.ckNum)) if selector else ''">
      <x if="not selectable">::ifield.getSupTitle(initiator.o, o, navInfo) \
                               or ''</x>
      <x>::ui.Title.get(o, mode=titleMode, nav=navInfo, target=target, \
             page=pageName, popup=popup, selectJs=selectJs)</x>
      <x if="not selectable">
       <span style=":showSubTitles and 'display:inline' or 'display:none'"
             name="subTitle" class=":tiedClass.getCssFor(o, 'subTitle')"
             var="sub=ifield.getSubTitle(initiator.o, o)" if="sub">::sub</span>
      </x></x>''')

    # This PX displays buttons for triggering global actions on several linked
    # objects (delete many, unlink many,...)
    pxGlobalActions = Px('''
     <div class="globalActions">

      <!-- Insert several objects (if in pick list) -->
      <input if="inPickList"
             var2="action='link'; label=_('object_link_many');
                   css=ui.Button.getCss(label)"
             type="button" class=":css" value=":label"
             onclick=":'onLinkMany(%s,%s,%s,%s)' % \
                        (q(action), q(o.url), q(hook), q(batch.start))"
             style=":url('linkMany.svg', bg='18px 18px')"/>

      <!-- Unlink several objects -->
      <input if="mayUnlink and not selector"
             var2="imgName=linkList and 'unlinkManyUp' or 'unlinkMany.svg';
                   action='unlink'; label=_('object_unlink_many');
                   css=ui.Button.getCss(label)"
             type="button" class=":css" value=":label"
             onclick=":'onLinkMany(%s,%s,%s,%s)' % \
                        (q(action), q(o.url), q(hook), q(batch.start))"
             style=":url(imgName, bg='18px 18px')"/>

      <!-- Delete several objects -->
      <input if="mayEdit and field.delete and not selector"
             var2="action='delete'; label=_('object_delete_many');
                   css=ui.Button.getCss(label)"
             type="button" class=":css" value=":label"
             onclick=":'onLinkMany(%s,%s,%s,%s)' % \
                        (q(action), q(o.url), q(hook), q(batch.start))"
             style=":url('deleteMany.svg', bg='18px 18px')"/>

      <!-- Select objects and close the popup -->
      <input if="selector and selector.cbShown" type="button"
             var="label=_('object_link_many'); css=ui.Button.getCss(label)"
             value=":label" class=":css"
             style=":url('linkMany.svg', bg='18px 18px')"
             onclick=":'onSelectObjects(%s,%s,%s,%s,%s)' % \
              (q('%d_%s' % (o.iid, field.name)), q(selector.initiatorHook), \
               q(selector.initiator.url), q(selector.initiatorMode), \
               q(selector.onav))"/>
     </div>''')

    # This PX displays icons for triggering actions on some tied object
    # (edit, delete, etc).
    pxObjectActions = Px('''
     <div if="ifield.showActions"
          class=":ui.getActionsCss(ifield.actionsDisplay)"
          var2="layout='buttons';
                editable=guard.mayEdit(o);
                io=initiator.o;
                locked=o.Lock.isSet(o, user, 'main')">

      <!-- Fields on layout "buttons" -->
      <x if="not popup and (ifield.showActions == 'all')"
         var2="fields=o.getFields('buttons', 'main'); layout='cell'">
       <!-- Call px "cell" and not "render" to avoid having a table -->
       <x for="field in fields"
          var2="name=field.name;
                value=field.getValueIf(o, name, layout)">:field.cell</x>
      </x>

      <!-- Workflow transitions -->
      <x if="tiedClass.showTransitions(o, 'result')"
         var2="workflow=o.getWorkflow()">:workflow.pxTransitions</x>

      <!-- Arrows for moving objects up or down -->
      <x if="(batch.total &gt;1) and changeOrder and not inPickList \
             and not inMenu"
         var2="js='askBunchMove(%s,%s,%s,%%s)' % \
                   (q(batch.hook), q(batch.start), q(id))">

       <!-- Move to top -->
       <img if="objectIndex &gt; 1" class="clickable iconS"
            src=":url('arrows.svg')" title=":_('move_top')"
            style="transform: rotate(180deg)" onclick=":js % q('top')"/>

       <!-- Move to bottom -->
       <img if="objectIndex &lt; (batch.total-2)" class="clickable iconS"
            src=":url('arrows.svg')" title=":_('move_bottom')"
            onclick=":js % q('bottom')"/>

       <!-- Move up -->
       <img if="objectIndex &gt; 0" class="clickable iconS"
            src=":url('arrow.svg')" title=":_('move_up')"
            style="transform: rotate(180deg)" onclick=":js % q('up')"/>

       <!-- Move down -->
       <img if="objectIndex &lt; (batch.total-1)" class="clickable iconS"
            src=":url('arrow.svg')" title=":_('move_down')"
            onclick=":js % q('down')"/>
      </x>

      <!-- Edit -->
      <x if="editable and (create != 'noForm')">
       <a if="not locked"
          var2="navInfo=ifield.getNavInfo(io, batch.start + currentNumber, \
                                          batch.total);
                linkInPopup=popup or (target.target != '_self')"
          href=":o.getUrl(sub='edit', page='main', nav=navInfo, \
                          popup=linkInPopup)"
          target=":target.target" onclick=":target.onClick">
        <img src=":url('edit.svg')" class="iconS" title=":_('object_edit')"/>
       </a>
       <x if="locked" var2="lockStyle='iconS'; page='main'">::o.Lock.px</x>
      </x>

      <!-- Delete -->
      <img var="mayDeleteViaField=inPickList or ifield.delete;
                back=q(io.iid) if inMenu and (layout == 'buttons') else 'null'"
        if="not locked and mayEdit and mayDeleteViaField and \
            guard.mayDelete(o)"
        class="clickable iconS" title=":_('object_delete')"
        src=":url('deleteS.svg')"
        onclick=":'onDeleteObject(%s,%s)' % (q(o.url), back)"/>

      <!-- Unlink -->
      <img if="mayUnlink and ifield.mayUnlinkElement(io, o)"
           var2="imgName=linkList and 'unlinkUp' or 'unlink.svg'"
           class="clickable iconS" title=":_('object_unlink')"
           onClick=":ifield.getOnUnlink(q, _, io, id, batch)"
           src=":url(imgName)"/>

      <!-- Insert (if in pick list) -->
      <img if="inPickList" var2="action='link'" class="clickable"
           title=":_('object_link')" src=":url(action)"
           onclick=":'onLink(%s,%s,%s,%s)' % (q(action), q(io.url), \
                      q(field.name), q(id))"/>

      <!-- Insert another object before this one -->
      <x if="not inPickList and (mayAdd == 'anywhere')">
       <img if="not createFromSearch"
            src=":url('addAbove')" class="clickable"
            title=":_('object_add_above')"
            onclick=":'onAdd(%s,%s,%s)' % \
                      (q('before'), q(addFormName), q(id))"/>
       <a if="createFromSearch" target="appyIFrame"
          href=":tiedClass.getCreateLink(tool, create, addFormName, \
                  sourceField=prefixedName, insert='before.%s' % id)">
        <img src=":url('addAboveFrom')" class="clickable"
             title=":_('object_add_above_from')"
             onclick="openPopup('iframePopup')"/>
       </a>
      </x>
     </div>''')

    # Displays the button allowing to add a new object through a Ref field, if
    # it has been declared as addable and if multiplicities allow it.
    pxAdd = Px('''
     <x if="mayAdd and not inPickList">
      <form class=":inMenu and 'addFormMenu' or 'addForm'"
            name=":addFormName" id=":addFormName" target=":target.target"
            action=":'%s/new' % o.url">
       <input type="hidden" name="className" value=":tiedClass.name"/>
       <input type="hidden" name="template" value=""/>
       <input type="hidden" name="insert" value=""/>
       <input type="hidden" name="nav"
              value=":field.getNavInfo(o, 0, batch.total)"/>
       <input type="hidden" name="popup"
          value=":(popup or (target.target != '_self')) and 'True' or 'False'"/>
       <input if="not createFromSearch"
              type=":'button' if field.addConfirm or (create == 'noForm') \
                              else 'submit'"
        var="addLabel=_(field.addLabel);
             label=inMenu and tiedClassLabel or addLabel;
             css=ui.Button.getCss(label)" class=":css"
        style=":url('add.svg', bg='18px 18px') if addIcon else ''"
        value=":label" title=":addLabel"
        onclick=":field.getOnAdd(q, addFormName, addConfirmMsg, target, \
                                 hook, batch.start, create)"/>
      </form>
      <!-- Button for creating an object from a template when relevant -->
      <x if="createFromSearch"
         var2="fromRef=True; className=tiedClass.name;
               sourceField=prefixedName">:tool.pxAddFrom</x>
     </x>''')

    # Displays the button allowing to select from a popup objects to be linked
    # via the Ref field.
    pxLink = Px('''
     <a target="appyIFrame"
        href=":field.getPopupLink(o, popupMode, name)"
        onclick="openPopup('iframePopup')">
      <div var="repl=popupMode == 'repl';
                labelId='search_button' if repl else field.addLabel;
                icon='search.svg' if repl else 'add.svg';
                label=_(labelId);
                css=ui.Button.getCss(label)"
           class=":css"
           style=":field.getLinkStyle(icon, layout, url)">:label</div>
     </a>''')

    # This PX displays, in a cell header from a ref table, icons for sorting the
    # ref field according to the field that corresponds to this column.
    pxSortIcons = Px('''
     <x if="changeOrder and (len(objects) &gt; 1) and \
            refField.isSortable(inRefs=True)">
      <img src=":url('asc.svg')" class="clickable iconS"
           var="js='askBunchSortRef(%s, %s, %s, %s)' % \
                  (q(hook), q(batch.start), q(refField.name), q('False'))"
           onclick=":'askConfirm(%s,%s,%s)' % (q('script'), q(js,False), \
                                               q(sortConfirm))"/>
      <img src=":url('asc.svg')" class="clickable iconS"
           style="transform:rotate(180deg)"
           var="js='askBunchSortRef(%s, %s, %s, %s)' % \
                  (q(hook), q(batch.start), q(refField.name), q('True'))"
           onclick=":'askConfirm(%s,%s,%s)' % (q('script'), q(js,False), \
                                               q(sortConfirm))"/>
     </x>''')

    # Shows the object number in a numbered list of tied objects
    pxNumber = Px('''
     <x if="not changeNumber">:objectIndex+1</x>
     <div if="changeNumber" class="dropdownMenu"
          var2="id='%s_%d' % (hook, objectIndex);
                imgId='%s_img' % id;
                inputId='%s_v' % id"
          onmouseover="toggleDropdown(this)"
          onmouseout="toggleDropdown(this,'none')">
      <input type="text" size=":numberWidth" id=":inputId" class="nbref"
             value=":objectIndex+1" onclick="this.select()"
             onkeydown=":'if (event.keyCode==13) \
                              document.getElementById(%s).click()' % q(imgId)"/>
      <!-- The menu -->
      <div class="dropdown">
       <img class="clickable" src=":url('move')" id=":imgId"
            title=":_('move_number')"
            onclick=":'askBunchMove(%s,%s,%s,this)' % \
                       (q(batch.hook), q(batch.start), q(o.iid))"/>
      </div>
     </div>''')

    # Part of pxList displaying the list of tied objects
    pxSub = Px('''
     <!-- (Top) navigation -->
     <div align=":dright">:batch.pxNavigate</div>

     <!-- No object is present -->
     <p class="discreet" if="not objects">:_(field.noObjectLabel)</p>

     <!-- Linked objects -->
     <table if="objects" id=":collapse.id" style=":collapse.style"
            class=":tiedClass.getListCss(layout)"
            width=":field.width or field.layouts['view'].width"
            var2="columns=field.getCurrentColumns(colset, colsets);
                  initiator=field.initiator(tool, req, (o, field));
                  currentNumber=0">
      <tr if="field.showHeaders">
       <th for="column in columns" width=":column.width" align=":column.align"
           var2="refField=column.field; isCB=refField=='_checkboxes'"
           class=":selector.cbClass if isCB and selector else ''">
        <x if="column.header">
         <img if="isCB" src=":url('checkAll.svg')" title=":_('check_uncheck')"
              onclick=":'toggleAllCbs(%s)' % q(hook)" class="clickable iconM"/>
         <x if="not column.special">
          <span class="htitle">::_(refField.labelId)</span>
          <x if="not selector">:field.pxSortIcons</x>
          <x if="ui.Title.showSub(tiedClass, refField)">:ui.Title.pxSub</x>
         </x>
        </x>
       </th>
      </tr>
      <!-- Loop on every (tied or selectable) object -->
      <x for="o in objects"
         var2="@currentNumber=currentNumber + 1;
               rowCss=loop.o.odd and 'even' or 'odd'">
       <x if="field.separator">::field.dumpSeparator(initiator.o, \
                                 loop.o.previous, tied, columns)</x>
       <x>:o.pxTied</x></x>
     </table>

     <!-- Global actions -->
     <x if="mayEdit and checkboxes and field.getAttribute(o, \
             'showGlobalActions')">:field.pxGlobalActions</x>

     <!-- (Bottom) navigation -->
     <div align=":dright" class="bottomSpace">:batch.pxNavigate</div>

     <!-- Init checkboxes if present -->
     <script if="checkboxes">:'initCbs(%s)' % q(hook)</script>''')

    # PX displaying tied objects as a list, with controls
    pxList = Px('''
     <div id=":hook"
          var="colsets=field.getColSets(o, tool, tiedClass, dir, \
                addNumber=numbered and not inPickList and not selector, \
                addCheckboxes=checkboxes)">

      <!-- Top controls -->
      <div if="(layout == 'view') or mayAdd or mayLink" class="topSpaceS">
       <x if="field.collapsible and objects">:collapse.px</x>
       <span if="subLabel" class="discreet">:_(subLabel)</span>
       <x if="batch.length &gt; 1">
        (<span class="discreet">:batch.total</span>)</x>
       <x if="not selector">:field.pxAdd</x>

       <!-- Button: open a popup for linking additional objects -->
       <x if="mayLink and not inPickList and not selector and field.linkInPopup"
          var2="popupMode='add'">:field.pxLink</x>

       <!-- The search selector if searches are defined -->
       <select if="field.searches" class="refSel"
               id=":'%s_%s_ssel' % (o.iid, field.name)"
               var2="searches=field.getSearches(o);
                     sdef=field.getCurrentSearch(req, searches)"
               onchange=":'askBunchSwitchSearch(%s,%s,this.value)' % \
                          (q(hook), q(field.name))">
         <!-- The first option is used to select the default pxSub -->
         <option value="" selected=":sdef == ''">:_('standard_view')</option>
         <option for="name, rs in searches.items()"
                 selected=":name == sdef" value=":name">:rs.translated</option>
       </select>

       <!-- The search button if field is queryable -->
       <input if="objects and field.queryable" type="button"
              var2="label=_('search_button'); css=ui.Button.getCss(label)"
              value=":label" class=":css"
              style=":url('search.svg', bg='18px 18px')"
              onclick=":'goto(%s)' % \
               q('%s/Search/advanced?className=%s&amp;ref=%d:%s' % \
               (tool.url, tiedClass.name, o.iid, field.name))"/>

       <!-- The colset selector if multiple colsets are available -->
       <select if="len(colsets) &gt; 1" class="refSel"
               onchange=":'askBunchSwitchColset(%s,this.value)'% q(hook)">
        <option for="cset in colsets" value=":cset.identifier"
                selected=":cset.identifier==colset">:_(cset.label)</option>
       </select>
      </div>

     <script>:field.getAjaxData(hook, o, popup=popup, colset=colset, \
        start=batch.start, total=batch.total)</script>

      <!-- The tied objects -->
      <x>:field.getListPx(o)</x>
     </div>''')

    # PX that displays referred objects as dropdown menus
    pxMenu = Px('''
     <img if="menu.icon" src=":menu.icon" title=":menu.text"/><x
          if="not menu.icon">:menu.text</x>
     <!-- Nb of objects in the menu -->
     <b>:len(menu.objects)</b>''')

    pxViewMenus = Px('''
     <x var2="inMenu=True">
      <!-- One menu for every object type -->
      <div for="menu in field.getLinkedObjectsByMenu(obj, objects)"
           class="inline"
           style=":not loop.menu.last and 'padding-right:4px' or ''">
       <div class="dropdownMenu inline"
            var2="singleObject=len(menu.objects) == 1"
            onmouseover="toggleDropdown(this)"
            onmouseout="toggleDropdown(this,'none')">

        <!-- The menu name and/or icon, that is clickable if there is a single
             object in the menu. -->
        <x if="singleObject" var2="tied=menu.objects[0]">
         <x if="field.menuUrlMethod"
            var2="mUrl,mTarget=field.getMenuUrl(
                   o,tied,target)">::ui.Title.get(tied, target=mTarget,
                   baseUrl=mUrl, css='dropdownMenu',
                   linkTitle=tied.getShownValue('title'),title=field.pxMenu)</x>
         <x if="not field.menuUrlMethod"
            var2="linkInPopup=popup or (target.target != '_self');
                  baseUrl=tied.getUrl(nav='no',
                    popup=linkInPopup)">::ui.Title.get(tied, target=target,
                baseUrl=baseUrl, css='dropdownMenu', \
                linkTitle=tied.getShownValue(), title=field.pxMenu)</x>
        </x>
        <b if="not singleObject"
           class=":field.getMenuCss(obj, menu)">:field.pxMenu</b>

        <!-- The dropdown menu containing tied objects -->
        <div class="dropdown" style="width:150px">
         <div for="tied in menu.objects"
              var2="batch=field.getBatchFor(batch.hook, len(menu.objects));
                    tiedId=tied.iid"
              class=":not loop.tied.first and 'refMenuItem' or ''">
          <!-- A specific link may have to be computed from
               field.menuUrlMethod -->
          <x if="field.menuUrlMethod"
             var2="mUrl,mTarget=field.getMenuUrl(zobj,tied,\
                target)">::ui.Title.get(tied, target=mTarget, baseUrl=mUrl)</x>
          <!-- Show standard pxObjectTitle else -->
          <x if="not field.menuUrlMethod">:field.pxObjectTitle</x>
          <x if="tied.o.mayAct()">:field.pxObjectActions</x>
         </div>
        </div>
       </div>
      </div><x>:field.pxAdd</x></x> ''')

    # Simplified widget for fields with render="minimal"
    pxViewMinimal = Px('''
     <x><x>::field.renderMinimal(o, objects, popup)</x>
      <!-- If this field is a master field -->
      <input type="hidden" if="masterCss and (layout == 'view')"
             name=":name" id=":name" class=":masterCss"
             value=":[o.iid for o in objects]" /></x>''')

    # Simplified widget for fields with render="links"
    pxViewLinks = Px('''
     <x>::field.renderMinimal(o, objects, popup, links=True)</x>''')

    # PX that displays referred objects through this field.
    # In mode link="list", if request key "scope" is:
    # - not in the request, the whole field is shown (both available and already
    #   tied objects);
    # - "objs", only tied objects are rendered;
    # - "poss", only available objects are rendered (the pick list).
    # ! scope is forced to "objs" on non-view "inner" (cell, buttons) layouts.
    view = cell = Px('''
     <x var="*=field.initPx(o, req, _ctx_)">
      <!-- JS tables storing checkbox statuses if checkboxes are enabled -->
      <script if="checkboxesEnabled and (render == 'list') and \
                  (scope == 'all')">:field.getCbJsInit(o)</script>
      <!-- The list of possible values, when relevant -->
      <x if="linkList and (scope == 'all') and mayEdit"
         var2="scope='poss'; layout='view'">:field.view</x>
      <!-- The list of tied or possible values, depending on scope -->
      <x if="render == 'list'"
         var2="subLabel=field.getListLabel(inPickList)">:field.pxList</x>
      <x if="render in ('menus', 'minimal', 'links')">:getattr(field, \
         'pxView%s' % render.capitalize())</x>
     </x>''')

    # Edit widget, for Refs with links being True (select widget)
    pxEditSelect = Px('''
     <select var="objects=field.getPossibleValues(o);
             ids=[str(o.iid) for o in field.getValue(o, name, single=False, \
                                                     layout=layout)];
             charsWidth=field.getWidthInChars(False)"
        name=":name" id=":name" multiple=":isMultiple"
        size=":field.getSelectSize(False, isMultiple)"
        style=":field.getSelectStyle(False, isMultiple)"
        onchange=":field.getOnChange(o, layout)">
      <option value="" if="not isMultiple">:_(field.noValueLabel)</option>
      <option for="tied in objects"
       var2="id=str(tied.iid);
             title=field.getReferenceLabel(o, tied, unlimited=True)"
       selected=":field.valueIsSelected(id,inRequest,ids,requestValue)"
       value=":id" title=":title">:Px.truncateValue(title, charsWidth)</option>
     </select>''')

    # Edit widget, for Refs with links being 'radio' (R) or 'checkbox' (C)
    pxEditRC = Px('''
     <div var="objects=field.getPossibleValues(o);
               ids=[str(o.iid) for o in field.getValue(o, name, single=False, \
                                                       layout=layout)]"
          style=":field.getRadioStyle()">
      <div for="tied in objects"
           var2="id=str(tied.iid);
                 vid='%s_%s' % (name, id);
                 text=field.getReferenceLabel(o, tied, unlimited=True)">
       <input type=":field.link" name=":name" id=":vid" value=":id"
              class=":masterCss" onchange=":field.getOnChange(o, layout)"
              checked=":field.valueIsSelected(id,inRequest,ids,requestValue)"/>
       <label lfor=":vid" class="subLabel">:text</label>
      </div>
     </div>''')

    # Edit widget, for Refs with link starting with "popup" or "dropdown"
    pxEditPopup = Px('''
     <x var="objects=field.getPopupObjects(o, name, req, requestValue);
             onChangeJs=field.getOnChange(o, layout);
             charsWidth=field.getWidthInChars(False);
             dropdown=field.link == 'dropdown'">

      <!-- The button for opening the popup or field for typing keywords -->
      <x if="not dropdown" var="popupMode='repl'">:field.pxLink</x>
      <x if="dropdown"
         var2="pre='%d_%s' % (o.iid, field.name);
               className=field.class_.meta.name;
               liveCss='lsRef'">:tool.Search.live</x>

      <!-- The select field allowing to store the selected objects -->
      <select if="objects" name=":name" id=":name" multiple="multiple"
              size=":field.getSelectSize(False, isMultiple)"
              style=":field.getSelectStyle(False, isMultiple)"
              onchange=":onChangeJs">
       <option for="tied in objects" value=":tied.iid" selected="selected"
               var2="title=field.getReferenceLabel(o, tied, unlimited=True)"
               title=":title">:Px.truncateValue(title, charsWidth)</option>
      </select>
      <!-- Back from a popup, force executing onchange JS code above, for
           updating potential master/slave relationships. -->
      <script if="objects and \
         ('semantics' in req)">:'getNode(%s,true).onchange()' % q(name)</script>
      <span if="not objects">-</span>
     </x>''',

     css='''.inputRef { vertical-align: top; margin-left: 10px !important} ''')

    edit = Px('''<x>:field.editPx</x>''')

    search = Px('''
     <!-- The "and" / "or" radio buttons -->
     <x if="field.multiplicity[1] != 1"
        var2="operName='o_%s' % name;
              orName='%s_or' % operName;
              andName='%s_and' % operName">
      <input type="radio" name=":operName" id=":orName" checked="checked"
             value="or"/>
      <label lfor=":orName">:_('search_or')</label>
      <input type="radio" name=":operName" id=":andName" value="and"/>
      <label lfor=":andName">:_('search_and')</label><br/>
     </x>
     <!-- The list of values -->
     <select var="objects=field.getPossibleValues(tool, usage='search');
                  charsWidth=field.getWidthInChars(True)"
             name=":widgetName" multiple="multiple"
             size=":field.getSelectSize(True, True)"
             style=":field.getSelectStyle(True, True)"
             onchange=":field.getOnChange(tool, 'search', className)">
      <option if="field.emptyIndexValue"
              value=":field.emptyIndexValue">:_('no_object')</option>
      <option for="tied in objects" value=":tied.iid"
              var2="title=field.getReferenceLabel(o, tied, unlimited=True)"
              title=":title">:Px.truncateValue(title, charsWidth)</option>
     </select>''')

    # Widget for filtering object values on query results
    pxFilterSelect = Px('''
     <select var="name=field.name;
                  filterId='%s_%s' % (mode.hook, name);
                  charsWidth=field.getWidthInChars(True);
                  emptyVal=field.emptyIndexValue;
                  objects=field.getPossibleValues(tool, usage='filter')"
          if="objects" id=":filterId" name=":filterId" class="discreet"
          onchange=":'askBunchFiltered(%s,%s)' % (q(mode.hook), q(name))">
      <option value="">:_('everything')</option>
      <option if="emptyVal" value=":emptyVal"
              selected=":mode.inFilter(name, emptyVal)">:_('no_object')</option>
      <option for="tied in objects" value=":tied.iid"
       var2="title=field.getReferenceLabel(o, tied, unlimited=True, \
                                           usage='filter')"
       selected=":mode.inFilter(name, str(tied.iid))"
       title=":title">:Px.truncateValue(title, charsWidth)</option>
     </select>''')

    def __init__(self, class_=None, attribute=None, validator=None,
      composite=False, multiplicity=(0,1), default=None, defaultOnEdit=None,
      add=False, addConfirm=False, delete=None, create='form', viaPopup=None,
      creators=None, link=True, unlink=None, linkMethod=None,
      unlinkElement=None, unlinkConfirm=True, insert=None, beforeLink=None,
      afterLink=None, afterUnlink=None, back=None, backSecurity=True, show=True,
      page='main', group=None, layouts=None, showHeaders=False, shownInfo=None,
      fshownInfo=None, select=None, maxPerPage=30, move=0, indexed=False,
      mustIndex=True, indexValue=None, emptyIndexValue=0, searchable=False,
      filterField=None, readPermission='read', writePermission='write',
      width=None, height=5, maxChars=None, colspan=1, master=None,
      masterValue=None, focus=False, historized=False, mapping=None,
      generateLabel=None, label=None, queryable=False, queryFields=None,
      queryNbCols=1, searches=None, navigable=False, changeOrder=True,
      numbered=False, checkboxes=True,checkboxesDefault=False, sdefault='',
      scolspan=1, swidth=None, sheight=None, sselect=None, persist=True,
      render='list', renderMinimalSep=', ', menuIdMethod=None,
      menuInfoMethod=None, menuUrlMethod=None, menuCss=None, view=None,
      cell=None, edit=None, xml=None, translations=None, showActions='all',
      actionsDisplay='block', showGlobalActions=True, collapsible=False,
      links=True, viewAdded=True, noValueLabel='choose_a_value',
      noObjectLabel='no_ref', addLabel='object_add', filterable=True,
      supTitle=None, subTitle=None, separator=None, rowAlign='top'):
        # The class whose tied objects will be instances of
        self.class_ = class_
        # Specify "attribute" only for a back reference: it will be the name
        # (a string) of the attribute that will be defined on self's class and
        # will allow, from a linked object, to access the source object.
        self.attribute = attribute
        # If this Ref is "composite", it means that the source object will be
        # a composite object and tied object(s) will be its components.
        self.composite = composite

        # May the user add new objects through this ref ? "add" may hold the
        # following values:
        # ----------------------------------------------------------------------
        #  True      | (boolean value): the object will be created and inserted
        #            | at the place defined by parameter "insert" (see below);
        # ----------------------------------------------------------------------
        # "anywhere" | (string) the object can be inserted at any place in the
        #            | list of already linked objects ("insert" is bypassed);
        # ----------------------------------------------------------------------
        # <a method> | a method producing one of the hereabove values.
        # ----------------------------------------------------------------------
        self.add = add

        # When the user adds a new object, must a confirmation popup be shown?
        self.addConfirm = addConfirm
        # May the user delete objects via this Ref?
        self.delete = delete
        if delete is None:
            # By default, one may delete objects via a Ref for which one can
            # add objects.
            self.delete = bool(self.add)

        # ----------------------------------------------------------------------
        # If "create"   | when clicking the "add" button / icon to create an
        # is....        | object through this ref...
        # ----------------------------------------------------------------------
        #    "form"     | (the default) an empty form will be shown to the user
        #               | (p_self.klass' "edit" layout);
        # ----------------------------------------------------------------------
        #   "noForm"    | the object will be created automatically, and no
        #               | creation form will be presented to the user. Code
        #               | p_self.klass' m_onEdit to initialise the object
        #               | according to your needs;
        # ----------------------------------------------------------------------
        #   a Search    | the user will get a popup and will choose some object
        #   instance    | among search results; this object will be used as base
        #               | for filling the form for creating the new object.
        #               |
        #               | Note that when specifying a Search instance, value of
        #               | attribute "addConfirm" will be ignored.
        # ----------------------------------------------------------------------
        # "create" may also hold a method returning one of the above-mentioned
        # values.
        # ----------------------------------------------------------------------
        self.create = create

        # When a page related to a tied object must be shown, for creating,
        # editing or simply viewing it, its target (=where it is rendered, in
        # the current window or in the popup window) depends on attribute
        # "popup" as defined on the referenced p_self.class_. This attribute
        # also determines the popup dimensions. You can override this attribute
        # in the context of this Ref field by using attribute "viaPopup"
        # hereafter. Allowed values for this attribute are similar to those for
        # attribute p_self.class_.popup. Note that, if "viaPopup" is:
        # ----------------------------------------------------------------------
        # None  | it is ignored and p_self.class_.popup will be used instead;
        # ----------------------------------------------------------------------
        # False | it is taken into account and the form will not be opened in a
        #       | popup, even if p_self.class_.popup exists and is not empty.
        # ----------------------------------------------------------------------
        self.viaPopup = viaPopup

        # ----------------------------------------------------------------------
        # If "creators"  | people allowed to create instances of p_self.klass
        # is...          | in the context of this Ref, will be...
        # ----------------------------------------------------------------------
        #      None      | (the default) those having one of the global roles as
        #                | listed in p_self.klass.creators;
        # ----------------------------------------------------------------------
        #     a list     | those having, locally on the ref's source object, one
        #  of role names | of the roles from this list.
        # ----------------------------------------------------------------------
        self.creators = creators

        # May the user link existing objects through this Ref ? If "link" is:
        # ----------------------------------------------------------------------
        #    True    | the user will, on "edit", choose objects from an HTML
        #            | select widget, rendered as a dropdown list if max
        #            | multiplicity is 1 or as a selection box if several values
        #            | can be chosen ;
        # ----------------------------------------------------------------------
        #  "radio"   | the user will, on "edit", choose objects from radio
        #            | buttons. This mode is valid for fields with a max
        #            | multiplicity being 1 ;
        # ----------------------------------------------------------------------
        # "checkbox" | the user will, on "edit", choose objects from checkboxes.
        #            | This mode is valid for fields with a max multiplicity
        #            | being higher than 1.
        #            | ~~~
        #            | Note that choosing "radio"/"checkbox" instead of boolean
        #            | value "True" is appropriate if the number of objects from
        #            | which to choose is low ;
        # ----------------------------------------------------------------------
        #   "list"   | the user will, on "view", choose objects from a list of
        #            | objects which is similar to those rendered in pxViewList;
        # ----------------------------------------------------------------------
        #  "popup"   | the user will, on "edit", choose objects from a popup
        #            | window. In this case, parameter "select" can hold a
        #            | Search instance or a method ;
        # ----------------------------------------------------------------------
        # "dropdown" | the user will, on "edit", choose objects by typing some
        #            | chars in an input text field: in a dropdown, the first
        #            | matching objects will be shown and will be selectable.
        #            | The set of possible objects shown in the dropdown must be
        #            | defined by a Search instance in attribute "select".
        # ----------------------------------------------------------------------
        # "popupRef" | the user will choose objects from a popup window, that
        #            | will display objects tied via a Ref field. In this case,
        #            | parameter "select" must hold a method returning a tuple
        #            | (obj, name), "obj" being the source object of the Ref
        #            | field whose name is in "name".
        # ----------------------------------------------------------------------
        self.link = link
        self.linkInPopup = False
        # Determine the PX to use when editing a Ref, based on attribute "link"
        if link == True:
            px = Ref.pxEditSelect
        elif link in ('radio', 'checkbox'):
            px = Ref.pxEditRC
        elif link in ('popup', 'dropdown', 'popupRef'):
            px = Ref.pxEditPopup
            self.linkInPopup = True
        else: # link == 'list'
            px = None
        self.editPx = px

        # If you place a method in the following attribute, the user will be
        # able to link or unlink objects only if the method returns True.
        self.linkMethod = linkMethod
        # May the user unlink existing objects?
        self.unlink = unlink
        if unlink is None:
            # By default, one may unlink objects via a Ref for which one can
            # link objects.
            self.unlink = bool(self.link)
        # "unlink" above is a global flag. If it is True, you can go further and
        # determine, for every linked object, if it can be unlinked or not by
        # defining a method in parameter "unlinkElement" below. This method
        # accepts the linked object as unique arg.
        self.unlinkElement = unlinkElement
        # If "unlinkConfirm" is True (the default), when unlinking an object,
        # the user will get a confirm popup.
        self.unlinkConfirm = unlinkConfirm

        # When an object is inserted through this Ref field, at what position is
        # it inserted ? If "insert" is:
        # ----------------------------------------------------------------------
        #   None   | it will be inserted at the end;
        # ----------------------------------------------------------------------
        # "start"  | it will be inserted at the start of the tied objects;
        # ----------------------------------------------------------------------
        # a method | (called with the object to insert as single arg), its
        #          | return value (a number or a tuple of numbers) will be used
        #          | to insert the object at the corresponding position (this
        #          | method will also be applied to other objects to know where
        #          | to insert the new one);
        # ----------------------------------------------------------------------
        # a tuple  | ('sort', method), the given method (called with the object
        # ('sort', | to insert as single arg) will be used to sort tied objects
        #  method) | and will be given as param "key" of the standard Python
        #          | method "sort" applied on the list of tied objects.
        # ----------------------------------------------------------------------
        # With the ('sort', method) tuple, a full sort is performed and may
        # completely change the order of tied objects; with value "method"
        # alone, the tied object is inserted at some given place: tied other
        # tied objects are more maintained in the order of their insertion.
        self.insert = insert

        # Immediately before an object is going to be linked via this Ref field,
        # method potentially specified in "beforeLink" will be executed and will
        # take the object to link as single parameter.
        self.beforeLink = beforeLink
        # Immediately after an object has been linked via this Ref field, method
        # potentially specified in "afterLink" will be executed and will take
        # the linked object as single parameter.
        self.afterLink = afterLink
        # Immediately after an object as been unlinked from this Ref field,
        # method potentially specified in "afterUnlink" will be executed and
        # will take the unlinked object as single parameter.
        self.afterUnlink = afterUnlink
        self.back = None
        if not attribute:
            # It is a forward reference
            self.isBack = False
            # Initialise the backward reference (if found)
            if back:
                self.back = back
                back.back = self
            # class_ may be None in the case we are defining an auto-Ref to the
            # same class as the class where this field is defined. In this case,
            # when defining the field within the class, write
            # myField = Ref(None, ...)
            # and, at the end of the class definition (name it K), write:
            # K.myField.class_ = K
            # setattr(K, K.myField.back.attribute, K.myField.back)
            if class_ and back: setAttribute(class_, back.attribute, back)
            # A composite ref must have a back ref having an upper
            # multiplicity = 1
            if self.composite and back and (back.multiplicity[1] != 1):
                raise Exception(BACK_1_COMP)
        else:
            self.isBack = True
            if self.composite: raise Exception(BACK_COMP)
        # When (un)linking a tied object from the UI, by defaut, security is
        # checked. But it could be useful to disable it for back Refs. In this
        # case, set "backSecurity" to False. This parameter has only sense for
        # forward Refs and is ignored for back Refs.
        self.backSecurity = backSecurity
        # When displaying a tabular list of referenced objects, must we show
        # the table headers?
        self.showHeaders = showHeaders
        # "shownInfo" is a tuple or list (or a method producing it) containing
        # the names of the fields that will be shown when displaying tables of
        # tied objects. Field "title" should be present: by default it is a
        # clickable link to the "view" page of every tied object. "shownInfo"
        # can also hold a tuple or list (or a method producing it) containing
        # appy.model.utils.ColSet instances. In this case, several sets of
        # columns are available and the user can switch between those sets when
        # consulting the field.
        if shownInfo is None:
            self.shownInfo = ['title']
        elif isinstance(shownInfo, tuple):
            self.shownInfo = list(shownInfo)
        else:
            self.shownInfo = shownInfo
        # "fshownInfo" is the variant used in filters
        self.fshownInfo = fshownInfo or self.shownInfo
        # If a method is defined in this field "select", it will be used to
        # return the list of possible tied objects. Be careful: this method can
        # receive, in its first argument ("self"), the tool instead of an
        # instance of the class where this field is defined. This little cheat
        # is:
        #  - not really a problem: in this method you will mainly use methods
        #    that are available on a tool as well as on any object (like
        #    "search");
        #  - necessary because in some cases we do not have an instance at our
        #    disposal, ie, when we need to compute a list of objects on a
        #    search screen.
        # "select" can also hold a Search instance.
        # NOTE that when a method is defined in field "masterValue" (see parent
        # class "Field"), it will be used instead of select (or sselect below).
        self.select = select
        if not select and (self.link == 'popup'):
            # Create a query for getting all objects
            self.select = Search(sortBy='title', maxPerPage=20)
        # If you want to specify, for the search screen, a list of objects that
        # is different from the one produced by self.select, define an
        # alternative method in field "sselect" below.
        self.sselect = sselect or self.select
        # Maximum number of referenced objects shown at once
        self.maxPerPage = maxPerPage
        # If param p_queryable is True, the user will be able to perform
        # searches from the UI within referenced objects. A Ref being queryable
        # requires an index. Two possibilities exist:
        # - your queryable Ref is composite (p_composite=True). In that case,
        #   the index used to restrict searches to Ref elements will be the
        #   special container index "cid";
        # - your queryable Ref has a mirror Ref being indexed. The mirror Ref is
        #   a forward Ref's back Ref or a back Ref's forward Ref.
        # If none of these conditions is met, the performed searches will
        # produce wrong results or errors.
        self.queryable = queryable
        # Here is the list of fields that will appear on the search screen.
        # If None is specified, by default we take every indexed field
        # defined on referenced objects' class.
        self.queryFields = queryFields
        # The search screen will have this number of columns
        self.queryNbCols = queryNbCols
        # If this field is p_queryable, you may specify, in attribute
        # "searches" below, a dict of Search instances, or a method producing
        # it. Keys must be names (following Python variable naming conventions)
        # and values must be Search instances. On every such instance, it is
        # useless to specify a name or the attribute corresponding to the index
        # allowing to restrict the search to this Ref's tied objects (it will be
        # added automatically). On the other hand, you must define translations
        # for its name (and, optionally, for its longer description), in its
        # attributes named "translated" and "translatedDescr". When Ref
        # attribute "searches" is not None, when displaying the Ref on the
        # "view" layout, results of the first Search from the dict will be
        # shown, instead of the standard Ref rendering. A dropdown list will
        # allow to switch to the standard view or to results from other searches
        # in the list. This allows to produce alternate or partial views of
        # the referred objects, via searches and their related facilities, like
        # sorting and filtering.
        self.searches = searches
        # Within the portlet, will referred elements appear ?
        self.navigable = navigable
        # If "changeOrder" is or returns False, it even if the user has the
        # right to modify the field, it will not be possible to move objects or
        # sort them.
        self.changeOrder = changeOrder
        # If "numbered" is or returns True, a leading column will show the
        # number of every tied object. Moreover, if the user can change order of
        # tied objects, an input field will allow him to enter a new number for
        # the tied object. If "numbered" is or returns a string, it will be used
        # as width for the column containing the number. Else, a default width
        # will be used.
        self.numbered = numbered
        # If "checkboxes" is or returns True, every linked object will be
        # "selectable" via a checkbox. Global actions will be activated and will
        # act on the subset of selected objects: delete, unlink, etc.
        self.checkboxes = checkboxes
        # Default value for checkboxes, if enabled
        self.checkboxesDefault = checkboxesDefault

        # There are different ways to render a bunch of tied objects:
        # ----------------------------------------------------------------------
        #  "list"   | (the default) renders them as a list (=a XHTML table);
        # ----------------------------------------------------------------------
        #  "menus"  | renders them as a series of popup menus, grouped by type.
        #           | Note that render mode "menus" will only be applied in
        #           | "cell" and "buttons" layouts. Indeed, we need to keep the
        #           | "list" rendering in the "view" layout because the "menus"
        #           | rendering is minimalist and does not allow to perform all
        #           | operations on linked objects (add, move, delete, edit...);
        # ----------------------------------------------------------------------
        # "minimal" | renders a list not-even-clickable data about the tied
        #           | objects (according to shownInfo);
        # ----------------------------------------------------------------------
        #  "links"  | renders a list of clickable comma-separated data about the
        #           | tied objects (according to shownInfo).
        # ----------------------------------------------------------------------
        self.render = render

        # When render is "minimal" or "links", the separator used between linked
        # objects is defined here.
        self.renderMinimalSep = renderMinimalSep
        # If render is 'menus', 2 methods must be provided.
        # "menuIdMethod" will be called, with every linked object as single arg,
        # and must return an ID that identifies the menu into which the object
        # will be inserted.
        self.menuIdMethod = menuIdMethod
        # "menuInfoMethod" will be called with every collected menu ID (from
        # calls to the previous method) to get info about this menu. This info
        # must be a tuple (text, icon):
        # - "text" is the menu name;
        # - "icon" (can be None) gives the URL of an icon, if you want to render
        #   the menu as an icon instead of a text.
        self.menuInfoMethod = menuInfoMethod
        # "menuUrlMethod" is an optional method that allows to compute an
        # alternative URL for the tied object that is shown within the menu
        # (when render is "menus"). It can also be used with render being "list"
        # as well. The method can return a URL as a string, or, alternately, a
        # tuple (url, target), "target" being a string that will be used for
        # the "target" attribute of the corresponding XHTML "a" tag.
        self.menuUrlMethod = menuUrlMethod
        # "menuCss" is an optional CSS (list of) class(es) (or a method
        # producing it) that will be applied to menus (when render is "menus")
        # containing more than 1 object. If the menu contains a single object,
        # the applied CSS class will be the one applied to the tied object's
        # title.
        self.menuCss = menuCss

        # "showActions" determines if we must show or not actions on every tied
        # object. Values can be:
        # ----------------------------------------------------------------------
        #    'all'    | All actions are shown: standard ones (move up/down,
        #             | edit, delete... the precisely shown set of actions
        #             | depends on user's permissions and other settings
        #             | like p_changeOrder) and actions whose layout is
        #             | "buttons" and whose page is "main".
        # ----------------------------------------------------------------------
        #  'standard' | Only standard actions are shown (see above).
        # ----------------------------------------------------------------------
        #    False    | No action is shown.
        # ----------------------------------------------------------------------
        self.showActions = showActions

        # When actions are shown (see p_showActions hereabove), p_actionsDisplay
        # determines how they are rendered.
        # ----------------------------------------------------------------------
        #  'block'  | Actions are shown in a "div" tag with CSS attribute
        #           | "display:block", so it will appear below the item title.
        # ----------------------------------------------------------------------
        #  'inline' | The "div" tag has CSS attribute "display:inline": it
        #           | appears besides the item's title and not below it,
        #           | producing a more compact list of results.
        # ----------------------------------------------------------------------
        #  'right'  | Similar to 'inline', but actions are right-aligned. Nice
        #           | rendering when the column containing the title and its
        #           | actions is not too large.
        # ----------------------------------------------------------------------
        self.actionsDisplay = actionsDisplay

        # It may be inappropriate to show global actions. "showGlobalActions"
        # can be a boolean or a method computing and returning it.
        self.showGlobalActions = showGlobalActions
        # If "collapsible" is True, a "+/-" icon will allow to expand/collapse
        # the tied or available objects.
        self.collapsible = collapsible
        # Normally, tied objects' titles are clickable and lead to tied object's
        # view pages. If you want to deactivate it, set "links" to False.
        self.links = links
        # When creating a new tied object from this ref, we will redirect the
        # user to the initiator's view page, excepted if this parameter is True.
        self.viewAdded = viewAdded
        # When selecting a value from a "select" widget, the entry representing
        # no value is translated according to this label. The default one is
        # something like "[ choose ]", but if you prefer a less verbose version,
        # you can use "no_value" that simply displays a dash, or your own label.
        self.noValueLabel = noValueLabel
        # When displaying tied objects, if there is no object, the following
        # label is used to produce a message (which can be as short as a simple
        # dash or an empty string).
        self.noObjectLabel = noObjectLabel
        # Label for the "add" button
        self.addLabel = addLabel

        # When displaying column "title" within lists of tied objects, methods
        # m_getSupTitle and m_getSubTitle from the tied object's class are
        # called for producing custom zones before and after rendering the
        # object title. If you want to particularize these zones for this
        # specific ref, instead of using the defaults methods from the tied
        # object's class, specify alternate methods in attributes "supTitle" and
        # "subTitle".
        # ----------------------------------------------------------------------
        # supTitle | may hold a method accepting 2 args: the tied object and
        #          | the navigation string;
        # ----------------------------------------------------------------------
        # subTitle | may hold a method accepting the tied object as single arg.
        # ----------------------------------------------------------------------
        self.supTitle = supTitle
        self.subTitle = subTitle

        # "separator" can accept a method that will be called before rendering
        # every tied object, to render a separator when the method returns
        # a Separator instance (see class above). This method must accept 2
        # args: "previous" and "next", and must return a Separator instance if a
        # separator must be inserted between the "previous" and "next" tied
        # objects. When the first tied object is rendered, the method is called
        # with parameter "previous" being None. Specifying a separator has only
        # sense when p_render is "list".
        self.separator = separator

        # When tied objects are rendered as a list, this attribute specifies
        # each row's vertical alignment.
        self.rowAlign = rowAlign

        # Call the base constructor
        Field.__init__(self, validator, multiplicity, default, defaultOnEdit,
          show, page, group, layouts, move, indexed, mustIndex, indexValue,
          emptyIndexValue, searchable, filterField, readPermission,
          writePermission, width, height, None, colspan, master, masterValue,
          focus, historized, mapping, generateLabel, label, sdefault, scolspan,
          swidth, sheight, persist, False, view, cell, edit, xml, translations)
        self.validable = bool(self.link)
        # Initialise filterPx when relevant. If you want to disable filtering
        # although it could be proposed, set p_filterable to False. This can be
        # useful when there would be too many values to filter.
        if (self.link == True) and indexed and filterable:
            self.filterPx = 'pxFilterSelect'
        self.checkParameters()

    def init(self, class_, name):
        '''Ref-specific lazy initialisation'''
        Field.init(self, class_, name)
        if not self.isBack and self.back:
            # Set the class for the back reference
            self.back.class_ = class_.python

    def initPx(self, o, req, c):
        '''Create context variables in v_r for layout "view"'''
        r = O()
        r.iid = o.iid
        r.layout = c.layout or req.layout or 'view'
        r.colset = c.colset or 'main'
        r.render = self.getRenderMode(r.layout)
        r.name = c.name or self.name
        r.prefixedName = '%s:%s' % (r.iid, r.name)
        r.selector = self.getSelector(o, req)
        r.selectable = bool(r.selector) and c.popup
        r.linkList = self.link == 'list'
        r.scope = c.scope or ('objs' if r.layout != 'view' else 'all')
        r.inPickList = r.scope == 'poss'
        r.create = self.getAttribute(o, 'create')
        r.createFromSearch = not isinstance(r.create, str)
        r.ajaxSuffix = 'poss' if r.inPickList else 'objs'
        r.hook = '%s_%s_%s' % (r.iid, r.name, r.ajaxSuffix)
        r.inMenu = False
        batch = self.getBatch(r.render, req, r.hook)
        r.batch = batch if c.ajaxSingle else \
                  self.getViewValues(o, r.name, r.scope, batch, r.hook)
        r.objects = r.batch.objects
        r.numberWidth = len(str(r.batch.total))
        r.tiedClass = c.handler.server.model.classes.get(self.class_.__name__)
        r.tiedClassLabel = c._(r.tiedClass.name)
        r.backHook = str(r.iid) if r.layout == 'cell' else None
        r.target = c.ui.LinkTarget(self.class_, r.backHook, self.viaPopup)
        r.mayEdit = (r.layout != 'edit') and \
                    c.guard.mayEdit(o, self.writePermission)
        r.mayEd = not r.inPickList and r.mayEdit
        r.mayAdd = r.mayEd and self.mayAdd(o, checkMayEdit=False)
        r.addFormName = '%s_%s_add' % (r.iid, self.name) if r.mayAdd else ''
        r.mayLink = r.mayEd and self.mayAdd(o, mode='link', checkMayEdit=False)
        r.mayUnlink = r.mayLink and self.getAttribute(o, 'unlink')
        r.addConfirmMsg = self.addConfirm and \
                          c._('%s_addConfirm' % self.labelId) or ''
        r.addIcon = True # Set an icon on button "add"
        r.changeOrder = r.mayEd and self.getAttribute(o, 'changeOrder')
        r.sortConfirm = c._('sort_confirm') if r.changeOrder else ''
        r.numbered = not r.inPickList and self.isNumbered(o)
        r.gotoNumber = r.numbered and (batch.total > 1)
        r.changeNumber = not r.inPickList and r.numbered and r.changeOrder and \
                         (r.batch.total > 3)
        r.checkboxesEnabled = (r.layout != 'cell') and \
                              self.getAttribute(o, 'checkboxes')
        r.checkboxes = r.checkboxesEnabled and ((r.batch.total > 1) or c.popup)
        r.collapse = self.getCollapseInfo(o, r.inPickList)
        r.showSubTitles = req.showSubTitles == 'True'
        # Add more variables if we are in the context of a single object
        # retrieved via Ajax.
        if c.ajaxSingle:
            r.colsets = self.getColSets(o, o.tool, r.tiedClass, c.dir,
              addNumber=r.numbered and not r.inPickList and not r.selector, \
              addCheckboxes=r.checkboxes)
            r.columns = self.getCurrentColumns(r.colset, r.colsets)
        return r

    def getSearches(self, o):
        '''Gets the list of Search instances defined or computed via attributes
           "searches".'''
        r = self.getAttribute(o, 'searches')
        if not r: return
        # Define the Search container, being p_self.class_
        class_ = self.class_.meta
        for search in r.values():
            search.init(class_)
        return r

    def getSearch(self, o, name):
        '''Returns, among, p_self.searches, the one having this p_name'''
        all = self.getSearches(o)
        if name == '_default_':
            # Get the first one
            for search in all.values():
                r = search
                break
        else:
            r = all[name]
        return r

    def getCurrentSearch(self, req, searches):
        '''Returns the name of the currently selected search, from
           p_self.searches.'''
        key = '%s_view' % self.name
        if key not in req:
            # The absence of that key means: use the first search as default
            for name in searches:
                r = name
                break
        else:
            r = req[key]
            # "r" can be the empty string: in that case, the standard view must
            # be shown.
        return r

    def getListPx(self, o):
        '''Get the sub-PX to display inside pxList'''
        # In most cases, display the list of tied objects as is
        if not self.searches: return self.pxSub
        # If attribute "searches" is not None, we may have to show search
        # results from one of the searches defined in it, or the standard list
        # of tied objects, depending on some request key.
        key = '%s_view' % self.name
        req = o.req
        searchName = req[key] if key in req else '_default_'
        # If no search was found, show the standard list of tied objects
        if not searchName: return self.pxSub
        # If we are here, we must render the PX for rendering the found search.
        # Inject the appropriate keys in the request, simulating a call to a
        # search PX.
        req.className = self.class_.meta.name
        # Key "search" allows to find the Search from the request
        req.search = '%s,%s,search*%s' % (o.iid, self.name, searchName)
        # Key "ref" allows to restrict seach results to ref's tied objects
        req.ref = '%s:%s' % (o.iid, self.name)
        context = o.traversal.context
        Px.injectRequest(context, req, o.tool, specialOnly=True)
        context.className = req.className # Not automatically injected
        return context.uiSearch.search.results

    def checkParameters(self):
        '''Ensures this Ref is correctly defined'''
        # For forward Refs, "add" and "link" can't both be used
        if not self.isBack and (self.add and self.link):
            raise Exception(ADD_LK_KO)
        # If link is "popup", "select" must hold a Search instance
        if (self.link == 'popup') and \
           (not isinstance(self.select, Search) and not callable(self.select)):
            raise Exception(LK_POP_ERR)
        # Valid link modes depend on multiplicities
        multiple = self.isMultiValued()
        if multiple and (self.link == 'radio'):
            raise Exception(RADIOS_KO)
        if not multiple and (self.link == 'checkbox'):
            raise Exception(CBS_KO)
        # A Ref with link="dropdown" must have max multiplicity being 1
        if multiple and self.link == 'dropdown':
            raise Exception(DDOWN_KO)

    def isShowable(self, o, layout):
        '''Showability for a Ref adds more rules w.r.t base field rules'''
        r = Field.isShowable(self, o, layout)
        if not r: return r
        # We add here specific Ref rules for preventing to show the field under
        # some inappropriate circumstances.
        isEdit = layout == 'edit'
        if isEdit:
            if self.mayAdd(o): return
            if self.link in (False, 'list'): return
        if self.isBack:
            if isEdit: return
            else: return getattr(o, self.name, None)
        return r

    def isRenderable(self, layout):
        '''Only Ref fields with render = "menus" can be rendered on "button"
           layouts.'''
        if layout == 'buttons': return self.render == 'menus'
        return True

    def valueIsSelected(self, id, inRequest, dbValue, requestValue):
        '''In PX "Edit", is object whose ID is p_id selected ?'''
        if inRequest:
            # The request value can be a single or multiple value
            r = (id in requestValue) if isinstance(requestValue, list) \
                                     else (id == requestValue)
        else:
            r = id in dbValue
        return r

    def getValue(self, o, name=None, layout=None, single=True, start=None,
                 batch=False, maxPerPage=None):
        '''Returns the objects linked to p_o through this Ref field.

           * If p_start is None, it returns all referred objects;
           * if p_start is a number, it returns p_maxPerPage objects (or
             self.maxPerPage if p_maxPerPage is None), starting at p_start.

           If p_single is True, it returns the single reference as an object and
           not as a list.

           If p_batch is True, it returns an instance of appy.model.utils.Batch
           instead of a list of references. When single is True, p_batch is
           ignored.
        '''
        # Get the value from the database. It is more performant to try to get
        # first the value via o.values. Calling Field.getValue then retrieves a
        # potential default value.
        r = o.values.get(self.name) or Field.getValue(self, o, name, layout)
        # Return an empty tuple or Batch instance if there is no object
        if not r: return Ref.empty if not batch else Batch()
        # Manage p_single
        if single and (self.multiplicity[1] == 1): return r[0]
        total = len(r)
        # Manage p_start and p_maxPerPage
        if start is not None:
            maxPerPage = maxPerPage or self.maxPerPage
            # Create a sub-list containing only the relevant objects
            sub = []
            i = start
            total = len(r)
            while i < (start + maxPerPage):
                if i >= total: break
                sub.append(r[i])
                i += 1
            r = sub
        # Manage p_batch
        if batch:
            r = Batch(r, total, size=maxPerPage, start=start or 0)
        return r

    def getCopyValue(self, o):
        '''Here, as "value ready-to-copy", we return the list of tied object
           ids, because m_store on the destination object can store tied
           objects based on such a list.'''
        # Return a copy: it can be dangerous to give the real database value
        return self.getValue(o, single=False)[:]

    def getXmlValue(self, o, value):
        '''The default XML value for a Ref is the list of tied object URLs'''
        # Bypass the default behaviour if a custom method is given
        return self.xml(o, value) if self.xml \
                                  else ['%s/xml' % tied.url for tied in value]

    def getSearchValue(self, req, value=None):
        '''Values from a search form are tied object's IIDS encoded as strings.
           Convert them to integer IIDs and manage an and/or operator.'''
        r = Field.getSearchValue(self, req, value=value)
        if isinstance(r, list):
            # It is a list of values. Get the operator to use.
            oper = Operator.fromRequest(req, self.name)
            r = oper(*[int(v) for v in r])
        elif r:
            r = int(r)
        else:
            r = None
        return r
    
    def updateHistoryValue(self, o, values):
        '''Store, in p_values, tied object's titles instead of the objects
           themselves.'''
        objects = values[self.name]
        values[self.name] = [tied.getShownValue('title') for tied in objects]

    def getSelect(self, o, forSearch=False):
        '''p_self.select can hold a Search instance or a method. In this latter
           case, call the method and return its result, that can be a Search
           instance or a list of objects.'''
        method = self.sselect if forSearch else self.select
        # If no search is defined, get a custom search
        if method is None: method = Search('customSearch')
        r = method if isinstance(method, Search) else self.callMethod(o, method)
        if isinstance(r, Search) and not r.container:
            # Ensure the class is set for this search
            r.init(self.class_.meta)
        return r

    def getPossibleValues(self, o, start=None, batch=False, removeLinked=False,
                          maxPerPage=None, usage='edit'):
        '''This method returns the list of all objects that can be selected
           to be linked as references to p_o via p_self. It is applicable only
           for Ref fields with link!=False. If master values are present in the
           request, we use field.masterValues method instead of self.[s]select.

           If p_start is a number, it returns p_maxPerPage objects (or
           self.maxPerPage if p_maxPerPage is None), starting at p_start.
           If p_batch is True, it returns an instance of appy.model.utils.Batch
           instead of returning a list of objects.

           If p_removeLinked is True, we remove, from the result, objects which
           are already linked. For example, for Ref fields rendered as a
           dropdown menu or a multi-selection box (with link=True), on the edit
           page, we need to display all possible values: those that are already
           linked appear to be selected in the widget. But for Ref fields
           rendered as pick lists (link="list"), once an object is linked, it
           must disappear from the "pick list".

           p_usage can be:
           - "edit": we need possible values for selecting it on an edit form;
           - "search": we need it for selecting it on a search screen;
           - "filter": wee need it for getting it in a filter widget.
        '''
        req = o.req
        paginated = start is not None
        maxPerPage = maxPerPage or self.maxPerPage
        isSearch = False
        master = self.master
        if master and callable(self.masterValue):
            # This field is an ajax-updatable slave
            if usage == 'filter':
                # A filter will not get any master. We need to display all the
                # slave values from all the master values the user may see.
                objects = None
                for masterValue in master.getPossibleValues(o):
                    if objects is None:
                        objects = self.masterValue(o, masterValue)
                    else:
                        # Ensure there is no duplicate among collected objects
                        for mo in self.masterValue(o, masterValue):
                            if mo not in objects:
                                objects.append(mo)
                objects = objects or []
            else:
                # Usage is "edit" or "search". Get the master value...
                if master.valueIsInRequest(o, req):
                    # ... from the request if available
                    requestValue = master.getRequestValue(o)
                    masterValues = master.getStorableValue(o, requestValue,
                                                           complete=True)
                elif usage == 'edit':
                    # ... or from the database if we are editing an object
                    masterValues = master.getValue(o, layout=usage)
                else: # usage is "search" and we don't have any master value
                    masterValues = None
                # Get the possible values by calling self.masterValue
                if masterValues:
                    objects = self.masterValue(o, masterValues)
                else:
                    objects = []
        else:
            # Get the possible values from attributes "select" or "sselect"
            forSearch = usage != 'edit'
            selectMethod = forSearch and self.sselect or self.select
            if not selectMethod:
                # No select method or search has been defined: we must retrieve
                # all objects of the referred type that the user is allowed to
                # access.
                objects = o.search(self.class_.__name__)
            else:
                # "[s]select" can be/return a Search instance or return objects
                search = self.getSelect(o, forSearch)
                if isinstance(search, Search):
                    isSearch = True
                    start = start or 0
                    objects = search.run(o.H(), start=start, batch=paginated)
                else:
                    # "[s]select" has returned objects
                    objects = search
        # Remove already linked objects if required
        if removeLinked:
            linked = getattr(o, self.name, None)
            if linked:
                # Browse objects in reverse order and remove linked objects
                if isSearch: objs = objects.objects
                else: objs = objects
                i = len(objs) - 1
                while i >= 0:
                    if objs[i] in linked: del objs[i]
                    i -= 1
        # If possible values are not retrieved from a Search, restrict (if
        # required) the result to "maxPerPage" starting at p_start. Indeed, in
        # this case, unlike m_getValue, we already have all objects in
        # "objects": we can't limit objects "waking up" to at most "maxPerPage".
        if isSearch:
            total = objects.total
        else:
            total = len(objects)
        if paginated and not isSearch:
            objects = objects[start:start + maxPerPage]
        # Return the result, wrapped in a SomeObjects instance if required
        if not batch:
            if isSearch: return objects.objects
            return objects
        if isSearch: return objects
        return Batch(objects, total, maxPerPage, start)

    def getViewValues(self, o, name, scope, batch, hook):
        '''Gets the values as must be shown on px "view". If p_scope is "poss",
           it is the list of possible, not-yet-linked, values. Else, it is the
           list of linked values. In both cases, we take the sub-set starting at
           p_batch.start.'''
        if scope == 'poss':
            r = self.getPossibleValues(o, start=batch.start, batch=True,
                                       removeLinked=True, maxPerPage=batch.size)
        else:
            # Return the list of already linked values
            r = self.getValue(o, name=name, start=batch.start, batch=True,
                              maxPerPage=batch.size, single=False)
        r.hook = hook
        return r

    def getLinkedObjectsByMenu(self, o, objects):
        '''This method groups p_objects into sub-lists of objects, grouped by
           menu (happens when self.render == 'menus').'''
        if not objects: return ()
        r = []
        # We store in "menuIds" the already encountered menus:
        # ~{s_menuId : i_indexInRes}~
        menuIds = {}
        # Browse every object from p_objects and put them in their menu
        # (within "r").
        for tied in objects:
            menuId = self.menuIdMethod(o, tied)
            if menuId in menuIds:
                # We have already encountered this menu
                menuIndex = menuIds[menuId]
                r[menuIndex].objects.append(tied)
            else:
                # A new menu
                menu = O(id=menuId, objects=[tied])
                r.append(menu)
                menuIds[menuId] = len(r) - 1
        # Complete information about every menu by calling self.menuInfoMethod
        for menu in r:
            text, icon = self.menuInfoMethod(o, menu.id)
            menu.text = text
            menu.icon = icon
        return r

    def getLinkStyle(self, icon, layout, url):
        '''Gets the CSS styles to apply for rendering the "search" button that
           opens the popup for linking objects.'''
        # Get the value for CSS attribute "float". On the "edit" layout, always
        # put the button on the right.
        if layout == 'edit':
            align = 'right'
        else:
            align = 'right' if self.multiplicity[1] == 1 else 'left'
        return '%s; background-position: 10%% 50%%; float: %s' % \
               (url(icon, bg='18px 18px'), align)

    def getColSets(self, o, tool, tiedClass, dir, usage=None,
                   addNumber=False, addCheckboxes=False):
        '''Gets the ColSet instances corresponding to every showable set of
           columns.'''
        attr = (usage == 'filter') and 'fshownInfo' or 'shownInfo'
        r = self.getAttribute(o, attr)
        # We can have either a list of strings (a single set) or a list of
        # ColSet instances.
        specs = ColSet.getSpecs
        if isinstance(r[0], str):
            # A single set
            columns = specs(tiedClass, o, r, dir, addNumber, addCheckboxes)
            return [ColSet('main', '', columns, specs=True)]
        # Several sets
        for colset in r:
            colset.specs = specs(tiedClass, o, colset.columns, dir,
                                 addNumber, addCheckboxes)
        return r

    def getCurrentColumns(self, identifier, colsets):
        '''Gets the columns defined for the current colset, whose p_identifier
           is given. The list of available p_colsets is also given.'''
        for cset in colsets:
            if cset.identifier == identifier:
                return cset.specs
        # If no one is found, return the first one, considered the default
        return colsets[0].specs

    def isNumbered(self, o):
        '''Must we show the order number of every tied object?'''
        r = self.getAttribute(o, 'numbered')
        if not r: return r
        # Returns the column width
        return r if isinstance(r, str) else '15px'

    def getMenuUrl(self, o, tied, target):
        '''We must provide the URL of the p_tied object, when shown in a Ref
           field in render mode 'menus'. If self.menuUrlMethod is specified,
           use it. Else, returns the "normal" URL of the view page for the tied
           object, but without any navigation information, because in this
           render mode, tied object's order is lost and navigation is
           impossible.'''
        if self.menuUrlMethod:
            r = self.menuUrlMethod(o, tied)
            if r is None:
                # There is no specific link to build
                return None, target
            elif isinstance(r, str):
                # The method has just returned an URL
                return r, LinkTarget()
            else:
                # The method has returned a tuple (url, target)
                target = LinkTarget()
                target.target = r[1]
                return r[0], target
        return tied.getUrl(nav='no'), target

    def getMenuCss(self, o, menu):
        '''Gets the CSS class that will be applied to a menu'''
        if not self.menuCss: return ''
        if callable(self.menuCss): return self.menuCss(o, menu.objects) or ''
        return self.menuCss

    def getBatch(self, render, req, hook):
        '''This method returns a Batch instance in the single objective of
           collecting batch-related information that might be present in the
           request.'''
        r = Batch(hook=hook)
        # When using any render mode, "list" excepted, all objects must be shown
        if render != 'list': return r
        # Get the index of the first object to show
        r.start = int(req['%s_start' % hook] or req.start or 0)
        # Get batch size
        r.size = int(req.maxPerPage or self.maxPerPage)
        # The total nb of elements may be in the request (if we are ajax-called)
        total = req.total
        if total: r.total = int(total)
        return r

    def getBatchFor(self, hook, total):
        '''Return a Batch instance for a p_total number of objects'''
        return Batch(hook, total, length=total, size=None, start=0)
    
    def getFormattedValue(self, o, value, layout='view', showChanges=False,
                          language=None):
        return value

    def hasSortIndex(self):
        '''An indexed Ref field is of type "ListIndex", which is not sortable.
           So an additional FieldIndex is required.'''
        return True

    def validateValue(self, o, value):
        if not self.link: return
        # We only check "link" Refs because in edit views, "add" Refs are
        # not visible. So if we check "add" Refs, on an "edit" view we will
        # believe that there is no referred object even if there is.
        # Also ensure that multiplicities are enforced.
        if not value:
            nbOfRefs = 0
        elif isinstance(value, str):
            nbOfRefs = 1
        else:
            nbOfRefs = len(value)
        minRef = self.multiplicity[0]
        maxRef = self.multiplicity[1]
        if maxRef is None:
            maxRef = sys.maxsize
        if nbOfRefs < minRef:
            return o.translate('min_ref_violated')
        elif nbOfRefs > maxRef:
            return o.translate('max_ref_violated')

    def linkObject(self, o, p, back=False, secure=False,
                   executeMethods=True, at=None):
        '''This method links object p_p (which can be a list of objects) to
           object p_o through this Ref field. When linking 2 objects via a Ref,
           m_linkObject must be called twice: once on the forward Ref and once
           on the backward Ref. p_back indicates if we are calling it on the
           forward or backward Ref. If p_secure is False, we bypass security
           checks (has the logged user the right to modify this Ref field ?).
           If p_executeMethods is False, we do not execute methods that
           customize the object insertion (parameters insert, beforeLink,
           afterLink...). This can be useful while migrating data or duplicating
           an object. If p_at is specified, it is a Position instance indicating
           where to insert the object: it then overrides self.insert.

           The method returns the effective number of linked objects.'''
        # Security check
        if secure: o.guard.mayEdit(o, self.writePermission, raiseError=True)
        # p_value can be a list of objects
        if type(p) in utils.sequenceTypes:
            count = 0
            for q in p:
                count += self.linkObject(o, q, back, secure, executeMethods, at)
            return count
        # Get or create the list of tied objects
        if self.name in o.values:
            refs = o.values[self.name]
        else:
            refs = o.values[self.name] = PersistentList()
        # Stop here if the object is already there
        if p in refs: return 0
        # Execute self.beforeLink if present
        if executeMethods and self.beforeLink:
            r = self.beforeLink(o, p)
            # Abort object linking if required by p_self.beforeLink
            if r == False: return 0
        # Where must we insert the object ?
        if at and (at.insertId in refs):
            # Insertion logic is overridden by this Position instance, that
            # imposes obj's position within tied objects.
            refs.insert(at.getInsertIndex(refs), p)
        elif not self.insert or not executeMethods:
            refs.append(p)
        elif self.insert == 'start':
            refs.insert(0, p)
        elif callable(self.insert):
            # It is a method. Use it on every tied object until we find where to
            # insert the new object.
            insertOrder = self.insert(o, p)
            i = 0
            inserted = False
            while i < len(refs):
                if self.insert(o, refs[i]) > insertOrder:
                    refs.insert(i, p)
                    inserted = True
                    break
                i += 1
            if not inserted: refs.append(p)
        else:
            # It is a tuple ('sort', method). Perform a full sort.
            refs.append(p)
            refs.sort(key=lambda q: self.insert[1](o, q))
        # Update the back reference (if existing)
        if not back and self.back:
            # Disable security when required
            if secure and not self.backSecurity: secure = False
            self.back.linkObject(p, o, True, secure, executeMethods)
        # Execute self.afterLink if present
        if executeMethods and self.afterLink: self.afterLink(o, p)
        return 1

    def unlinkObject(self, o, p, back=False, secure=False, executeMethods=True):
        '''This method unlinks p_p (which can be a list of objects) from p_o
           through this Ref field. For an explanation about parameters p_back,
           p_secure and p_executeMethods, check m_linkObject above.'''
        # Security check
        if secure:
            o.guard.mayEdit(o, self.writePermission, raiseError=True)
            if executeMethods:
                self.mayUnlinkElement(o, p, raiseError=True)
        # p_p can be a list of objects
        if type(p) in utils.sequenceTypes:
            for q in p:
                self.unlinkObject(o, q, back, secure, executeMethods)
            return
        refs = o.values.get(self.name)
        if not refs or (p not in refs): return
        # Unlink p_p
        refs.remove(p)
        # Update the back reference (if existing)
        if not back and self.back:
            # Disable security when required
            if secure and not self.backSecurity: secure = False
            self.back.unlinkObject(p, o, True, secure, executeMethods)
        # Execute self.afterUnlink if present
        if executeMethods and self.afterUnlink: self.afterUnlink(o, p)

    def getStorableValue(self, o, value, complete=False):
        '''Even if multiplicity is (x,1), the storable value for a Ref (to be
           given to m_store, when p_complete is False) must always be a list.

           If we need to produce a p_complete version, this method returns an
           Appy object or a list of Appy objects.'''
        if not value: return value
        if not complete:
            # Ensure p_value is a list
            return [value] if isinstance(value, str) else value
        else:
            # Produce an Appy object or a list of Appy objects
            if isinstance(value, str):
                return o.getObject(value)
            else:
                return o.getObject(value[0]) if self.multiplicity[1] == 1 \
                       else [o.getObject(v) for v in value]

    def store(self, o, value, secure=True):
        '''Stores on p_o, the p_value, which can be:
           * None;
           * an object ID (as a string);
           * a list of object IDs (=list of strings). Generally, IDs or lists
             of IDs come from Ref fields with link:True edited through the web;
           * an Appy object;
           * a list of Appy objects.'''
        if not self.persist: return
        # Standardize p_value into a list of Appy objects
        objects = value or []
        if type(objects) not in utils.sequenceTypes: objects = [objects]
        for i in range(len(objects)):
            tied = objects[i]
            if isinstance(tied, str) or isinstance(tied, int):
                # We have an (I)ID here
                objects[i] = o.getObject(tied)
        # Unlink objects that are not referred anymore
        tiedObjects = o.values.get(self.name, ())
        if tiedObjects:
            i = len(tiedObjects) - 1
            while i >= 0:
                tied = tiedObjects[i]
                if tied not in objects:
                    self.unlinkObject(o, tied, secure=secure)
                i -= 1
        # Link new objects
        if objects: self.linkObject(o, objects, secure=secure)

    def mayLink(self, o):
        '''If p_self defines a link method, this method evaluates it and returns
           its result. Else, the method returns True.'''
        method = self.linkMethod
        return True if method is None else self.getAttribute(o, 'linkMethod')

    def mayAdd(self, o, mode='create', checkMayEdit=True):
        '''May the user create (if p_mode == "create") or link
           (if mode == "link") (a) new tied object(s) from p_o via this Ref ?
           If p_checkMayEdit is False, it means that the condition of being
           allowed to edit this Ref field has already been checked somewhere
           else (it is always required, we just want to avoid checking it
           twice).'''
        # We can't (yet) do that on back references
        if self.isBack: return utils.No('is_back')
        r = True
        # Check if this Ref is addable/linkable
        if mode == 'create':
            r = self.getAttribute(o, 'add')
            if not r: return utils.No('no_add')
        elif mode == 'link':
            if not self.link or not self.isMultiValued() or not self.mayLink(o):
                return
        # Have we reached the maximum number of referred elements ?
        if self.multiplicity[1] is not None:
            objects = o.values.get(self.name)
            count = len(objects) if objects else 0
            if count >= self.multiplicity[1]: return utils.No('max_reached')
        # May the user edit this Ref field ?
        if checkMayEdit:
            if not o.guard.mayEdit(o, self.writePermission):
                return utils.No('no_write_perm')
        # May the user create instances of the referred class ?
        if mode == 'create':
            if self.creators:
                checkInitiator = True
                initiator = RefInitiator(o.tool, o.req, (o, self))
            else:
                checkInitiator = False
                initiator = None
            if not o.guard.mayInstantiate(self.class_.meta, checkInitiator, \
                                          initiator):
                return utils.No('no_create_perm')
        return r

    def checkAdd(self, o, log=False):
        '''Compute m_mayAdd above, and raise an Unauthorized exception if
           m_mayAdd returns False.'''
        may = self.mayAdd(o)
        if not may:
            message = WRITE_KO % (self.container.name, self.name, may)
            if log: o.log(message, type='error')
            o.raiseUnauthorized(message)

    def getOnAdd(self, q, formName, addConfirmMsg, target, hookId, start,
                 create):
        '''Computes the JS code to execute when button "add" is clicked'''
        if create == 'noForm':
            # Ajax-refresh the Ref with a special param to link a newly created
            # object.
            res = "askAjax('%s', null, {'start':'%d', " \
                  "'action':'doCreateWithoutForm'})" % (hookId, start)
            if self.addConfirm:
                res = "askConfirm('script', %s, %s)" % \
                      (q(res, False), q(addConfirmMsg))
        else:
            # In the basic case, no JS code is executed: target.onClick is
            # empty and the button-related form is submitted in the main page.
            res = target.onClick
            if self.addConfirm and not target.onClick:
                res = "askConfirm('form','%s',%s)" % (formName,q(addConfirmMsg))
            elif self.addConfirm and target.onClick:
                res = "askConfirm('form+script',%s,%s)" % \
                      (q(formName + '+' + target.onClick, False), \
                       q(addConfirmMsg))
        return res

    def getOnUnlink(self, q, _, o, tiedId, batch):
        '''Computes the JS code to execute when button "unlink" is clicked'''
        js = "onLink('unlink','%s','%s','%s','%s','%s')" % \
             (o.url, self.name, tiedId, batch.hook, batch.start)
        if not self.unlinkConfirm: return js
        return "askConfirm('script', %s, %s)" % \
               (q(js, False), q(_('action_confirm')))

    def getAddLabel(self, o, addLabel, tiedClassLabel, inMenu):
        '''Gets the label of the button allowing to add a new tied object. If
           p_inMenu, the label must contain the name of the class whose instance
           will be created by clincking on the button.'''
        if not inMenu: return o.translate(self.addLabel)
        return tiedClassLabel

    def getListLabel(self, inPickList):
        '''If self.link == "list", a label must be shown in front of the list.
           Moreover, the label is different if the list is a pick list or the
           list of tied objects.'''
        if self.link != 'list': return
        return inPickList and 'selectable_objects' or 'selected_objects'

    def mayUnlinkElement(self, o, p, raiseError=False):
        '''May we unlink p_p from p_o via this Ref field ?'''
        if not self.unlinkElement: return True
        r = self.unlinkElement(o, p)
        if r: return True
        else:
            if not raiseError: return
            # Raise an exception
            o.raiseUnauthorized(UNLINK_KO)

    def getCbJsInit(self, o):
        '''When checkboxes are enabled, this method defines a JS associative
           array (named "_appy_objs_cbs") that will store checkboxes' statuses.
           This array is needed because all linked objects are not visible at
           the same time (pagination).

           Moreover, if self.link is "list", an additional array (named
           "_appy_poss_cbs") is defined for possible values.

           Semantics of this (those) array(s) can be as follows: if a key is
           present in it for a given linked object, it means that the
           checkbox is unchecked. In this case, all linked objects are selected
           by default. But the semantics can be inverted: presence of a key may
           mean that the checkbox is checked. The current array semantics is
           stored in a variable named "_appy_objs_sem" (or "_appy_poss_sem")
           and may hold "unchecked" (initial semantics) or "checked" (inverted
           semantics). Inverting semantics allows to keep the array small even
           when checking/unchecking all checkboxes.

           The mentioned JS arrays and variables are stored as attributes of the
           DOM node representing this field.'''
        # The initial semantics depends on the checkboxes default value.
        default = self.getAttribute(o, 'checkboxesDefault') and \
                  'unchecked' or 'checked'
        code = "\nnode['_appy_%%s_cbs']={};\nnode['_appy_%%s_sem']='%s';" % \
               default
        poss = (code % ('poss', 'poss')) if self.link == 'list' else ''
        return "var node=findNode(this, '%d_%s');%s%s" % \
               (o.iid, self.name, code % ('objs', 'objs'), poss)

    def getAjaxData(self, hook, o, **params):
        '''Initializes an AjaxData object on the DOM node corresponding to this
           Ref field.'''
        # Complete params with default parameters
        params['hook'] = hook;
        params['scope'] = hook.rsplit('_', 1)[-1]
        req = o.req
        selector = req.selector
        if selector: params['selector'] = selector
        # Carry ckeditor-specific parameters
        if req.CKEditor:
            params['CKEditor'] = req.CKEditor
            params['CKEditorFuncNum'] = req.CKEditorFuncNum
        params['onav'] = req.nav or ''
        params = sutils.getStringFrom(params)
        return "new AjaxData('%s/%s/view', 'GET', %s, '%s')" % \
               (o.url, self.name, params, hook)

    def getAjaxDataRow(self, o, parentHook, **params):
        '''Initializes an AjaxData object on the DOM node corresponding to
           p_parentHook = a row within the list of referred objects.'''
        return "new AjaxData('%s/pxTied', 'GET', %s, '%d', '%s')" % \
               (o.url, sutils.getStringFrom(params), o.iid, parentHook)

    traverse['moveObject'] = 'perm:write'
    def moveObject(self, o):
        '''Moves a tied object up/down/top/bottom'''
        req = o.req
        # How to move the item ?
        move = req.move
        # Get the object to move
        tied = o.getObject(req.tiedId)
        objects = getattr(o, self.name, ())
        i = objects.index(tied)
        if move == 'up':
            i -= 1
        elif move == 'down':
            i += 1
        elif move == 'top':
            i = 0
        elif move == 'bottom':
            i = len(objects) - 1
        elif move.startswith('index'):
            # New index starts at 1 (old index starts at 0)
            try:
                i = int(move.split('_')[1]) - 1
            except ValueError:
                i = -1
        # If the new index is negative, the move can't occur
        if i > -1:
            objects.remove(tied)
            objects.insert(i, tied)

    traverse['doCreateWithoutForm'] = 'perm:write'
    def doCreateWithoutForm(self, o):
        '''This method is called when a user wants to create a object from a
           reference field, automatically (without displaying a form).'''
        o.create(self.name)

    xhtmlToText = re.compile('<.*?>', re.S)
    def getReferenceLabel(self, o, tied, unlimited=False, dir='ltr',usage=None):
        '''Only works for a Ref with link=True. Displays, on an edit view, the
           p_tied object in the select field allowing the user to choose which
           object(s) to link through the Ref. The information to display may
           only be the object title or more if "shownInfo" is used.'''
        r = ''
        # p_obj may not be present, if we are on a search screen
        tool = o.tool
        for col in self.getColSets(o, tool, tied.class_, dir, \
                                   usage=usage)[0].specs:
            name = col.field.name
            refType = tied.getField(name)
            value = getattr(tied, name)
            value = refType.getShownValue(tied, value) or '-'
            if refType.type == 'Rich':
                value = self.xhtmlToText.sub(' ', value)
            elif type(value) in utils.sequenceTypes:
                value = ', '.join(value)
            prefix = r and ' | ' or ''
            r += prefix + value
        if unlimited: return r
        maxWidth = self.width or 30
        if len(r) > maxWidth:
            r = Px.truncateValue(r, maxWidth)
        return r

    def getIndexOf(self, o, tied, raiseError=True):
        '''Gets the position of p_tied object within this field on p_o'''
        try:
            return self.getValue(o, single=False).index(tied)
        except ValueError:
            if raiseError: raise IndexError()

    def getPageIndexOf(self, o, tied):
        '''Returns the index of the first object of the page where p_tied is'''
        index = self.getIndexOf(o, tied)
        return int(index/self.maxPerPage) * self.maxPerPage

    traverse['sort'] = 'perm:write'
    def sort(self, o):
        '''Called by the UI to sort the content of this field'''
        req = o.req
        o.sort(self.name, sortKey=req.sortKey, reverse=req.reverse == 'True')

    traverse['gotoTied'] = 'perm:read'
    def gotoTied(self, o):
        '''Redirect to the object tied to p_o via p_self whose position is given
           by request key "number".'''
        # Get the object tied to p_o via p_self, at the index given in the req
        tied = o.values[self.name][int(o.req.number)-1]
        return o.goto(tied.url)

    def getRenderMode(self, layout):
        '''Gets the render mode, determined by self.render and some
           exceptions.'''
        if (layout == 'view') and (self.render == 'menus'): return 'list'
        return self.render

    def getTitleMode(self, selector):
        '''How will we render the tied objects's titles ?'''
        if selector: return 'select'
        if self.links: return 'link'
        return 'text'

    def getPopupLink(self, o, popupMode, name):
        '''Gets the link leading to the page to show in the popup for selecting
           objects.'''
        # Transmit the original navigation when existing
        nav = o.req.nav
        suffix = '&onav=%s' % nav if nav else ''
        if self.link in ('popup', 'dropdown'):
            # Go to the page for querying objects
            r = '%s/Search/results?className=%s&search=%d,%s,%s&popup=1%s' % \
             (o.tool.url, self.class_.meta.name, o.iid, name, popupMode, suffix)
        elif self.link == 'popupRef':
            # Go to the page that displays a single field
            po, fieldName = self.select(o) # "po" = the *p*opup *o*bject
            r = '%s/pxField?name=%s&pageLayout=w-b&popup=True&maxPerPage=%d' \
                '&selector=%d,%s,%s%s' % (po.url, fieldName, self.maxPerPage,
                                          o.iid, name, popupMode, suffix)
        return r

    def getSelector(self, o, req):
        '''When this Ref field is shown in a popup for selecting objects to be
           included in an "originator" Ref field, this method gets info from the
           request about this originator.'''
        if 'selector' not in req: return
        id, name, mode = req.selector.split(',')
        initiator = o.getObject(id)
        initiatorField = o.getField(name)
        # If several objects can be selected, show their checkboxes
        cbShown = initiatorField.isMultiValued()
        cbClass = '' if cbShown else 'hide'
        return O(initiator=initiator, initiatorField=initiatorField,
                 initiatorMode=mode, onav=req.onav or '',
                 initiatorHook='%d_%s' % (initiator.iid, name),
                 cbShown=cbShown, cbClass=cbClass,
                 # The originator can also be a rich field for which images must
                 # be browsed. In that case, we transmit "ckNum", a number being
                 # internal to the originating ckeditor.
                 ckNum=req.CKEditorFuncNum or '')

    def getPopupObjects(self, o, name, req, requestValue):
        '''Gets the list of objects that were selected in the popup (for fields
           with link="popup" or "popupRef").'''
        if requestValue:
            # We are validating the form. Return the request value instead of
            # the popup value.
            return [o.getObject(requestValue)] if isinstance(requestValue,str) \
                   else [o.getObject(v) for v in requestValue]
        r = []
        # No object can be selected if the popup has not been opened yet
        if 'semantics' not in req:
            # In this case, display already linked objects if any
            return r if o.isEmpty(name) \
                     else self.getValue(o, name=name, single=False)
        ids = req.selected.split(',')
        tool = o.tool
        if req.semantics == 'checked':
            # Simply get the selected objects from their uid
            return [o.getObject(id) for id in ids]
        else:
            # If link=popup, replay the search in self.select to get the list of
            # ids that were shown in the popup. If link=popupRef, simply get
            # the list of tied object ids for this Ref.
            if self.link == 'popup':
                search = self.getSelect(o)
                r = search.run(o.H(), batch=False, sortBy=req.sortKey,
                               sortOrder=req.sortOrder,
                               filters=self.class_.meta.getFilters(req))
            elif self.link == 'popupRef':
                initiatorObj, fieldName = self.select(o)
                r = getattr(initiatorObj, fieldName)
        return r

    traverse['onSelectFromPopup'] = 'perm:write'
    def onSelectFromPopup(self, o):
        '''This method is called on Ref fields with link=popup[Ref], when
           a user has selected objects from the popup, to be added to existing
           tied objects, from the view widget.'''
        for tied in self.getPopupObjects(o, self.name, o.req, None):
            self.linkObject(o, tied, secure=True)

    def getLinkBackUrl(self, o, req):
        '''Get the URL to redirect the user to after having (un)linked an object
           via this Ref.'''
        # Propagate key(s) of the form "_start"
        referer = o.referer
        url = urlparse(referer)
        if not url.query: return referer
        params = {}
        for name, value in parse_qsl(url.query):
            if name.endswith('start') or (name == 'page'):
                params[name] = value
        return o.getUrl(sub='view', **params)

    traverse['onLink'] = 'perm:write'
    def onLink(self, o):
        '''Links or unlinks an object whose id is in the request'''
        o.H().commit = True
        req = o.req
        # What is the precise action to perform ?
        action = req.linkAction
        msg = None
        if not action.endswith('_many'):
            method = eval('self.%sObject' % req.linkAction)
            tied = o.getObject(int(req.targetId))
            r = method(o, tied, secure=True)
        else:
            # "link_many", "unlink_many", "delete_many". Get the (un-)checked
            # objects from the request.
            if not req.targetId:
                ids = {}
            else:
                ids = {int(sid):None for sid in req.targetId.split(',')}
            unchecked = req.semantics == 'unchecked'
            if action == 'link_many':
                # Get possible values
                values = self.getPossibleValues(o, removeLinked=True)
            else:
                # Get current values
                values = getattr(o, self.name, ())
            # Collect the objects onto which the action must be performed
            targets = []
            for value in values:
                id = value.iid
                if unchecked:
                    # Keep only objects not among ids
                    if id in ids: continue
                else:
                    # Keep only objects being in uids
                    if id not in ids: continue
                targets.append(value)
            if not targets:
                msg = o.translate('action_null')
            else:
                # Perform the action on every target. Count the number of failed
                # operations.
                failed = 0
                singleAction = action.split('_')[0]
                mustDelete = singleAction == 'delete'
                guard = o.guard
                for target in targets:
                    if mustDelete:
                        # Delete
                        if guard.mayDelete(target):
                            target.delete(historize=True)
                        else: failed += 1
                    else:
                        # Link or unlink. For unlinking, we need to perform an
                        # additional check.
                        if (singleAction == 'unlink') and \
                           not self.mayUnlinkElement(o, target):
                            failed += 1
                        else:
                            method = eval('self.%sObject' % singleAction)
                            method(o, target)
                if failed:
                    msg = o.translate('action_partial', mapping={'nb':failed})
        # Redirect the user and display a message
        o.goto(self.getLinkBackUrl(o, req),
               message=msg or o.translate('action_done'))

    def renderMinimal(self, o, objects, popup, links=False):
        '''Render tied p_objects in render mode "minimal" (or "links" if p_links
           is True).'''
        if not objects: return o.translate(self.noObjectLabel)
        r = []
        for tied in objects:
            title = self.getReferenceLabel(o, tied, True)
            if links and tied.allows('read'):
                # Wrap the title in a link
                target = popup and '_parent' or '_self'
                title = '<a href="%s" target="%s" style="padding:0">%s</a>' % \
                        (tied.url, target, title)
            r.append(title)
        return self.renderMinimalSep.join(r)

    def getNavInfo(self, o, nb, total, inPickList=False, inMenu=False):
        '''Gets the navigation info allowing to navigate from tied object number
           p_nb to its siblings.'''
        if self.isBack or inPickList or inMenu: return 'no'
        # If p_nb is None, we want to produce a generic nav info into which we
        # will insert a specific number afterwards.
        if nb is None: return 'ref.%d.%s.%%d.%d' % (o.iid, self.name, total)
        return 'ref.%d.%s.%d.%d' % (o.iid, self.name, nb, total)

    def onGotoTied(self, o):
        '''Called when the user wants to go to a tied object whose number is in
           the request.'''
        req = o.req
        number = int(req.number) - 1
        tied = o.values[self.name][number]
        tiedUrl = tied.getUrl(nav=self.getNavInfo(o, number+1, len(objects)),
                              popup=req.popup or 'False')
        return o.goto(tiedUrl)

    def getCollapseInfo(self, o, inPickList):
        '''Returns a Collapsible instance, that determines if the "tied objects"
           or "available objects" zone (depending on p_inPickList) is collapsed
           or expanded.'''
        # Create the ID of the collapsible zone
        suffix = 'poss' if inPickList else 'objs'
        id = '%s_%s_%s' % (o.class_.name, self.name, suffix)
        return ui.Collapsible(id, o.req, default='expanded', display='table')

    def getSupTitle(self, o, tied, nav):
        '''Returns the custom chunk of info that must be rendered just before
           the p_tied object's title.'''
        # A sup-title may be defined directly on this Ref...
        if self.supTitle: return self.supTitle(o, tied, nav)
        # ... or on p_tied's class itself
        return tied.getSupTitle(nav) if hasattr(tied, 'getSupTitle') else None

    def getSubTitle(self, o, tied):
        '''Returns the custom chunk of info that must be rendered just after
           the p_tied object's title.'''
        # A sub-title may be defined directly on this Ref...
        if self.subTitle: return self.subTitle(o, tied)
        # ... or on p_tied's class itself
        return tied.getSubTitle() if hasattr(tied, 'getSubTitle') else None

    def dumpSeparator(self, o, previous, next, columns):
        '''r_eturns a Separator instance if one must be inserted between
           p_previous and p_next objects.'''
        if not self.separator: return ''
        sep = self.separator(o, previous, next)
        if not sep: return ''
        css = ' class="%s"' % sep.css if sep.css else ''
        return '<tr><td colspan="%d"><div%s>%s</div></td></tr>' % \
               (len(columns), css, sep.translated or o.translate(sep.label))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def autoref(class_, field):
    '''Defines, a posteriori, a Ref from one class the same one, or to another
       one but that could not be directly declared because it would have led to
       a circular import.'''

    # class_.field is a Ref to p_class_. This kind of auto-reference can't be
    # declared in the "normal" way, like this:

    # class A:
    #     attr1 = Ref(A)

    # because at the time Python encounters the static declaration
    # "attr1 = Ref(A)", class A is not completely defined yet.

    # This method allows to overcome this problem. You can write such auto-
    #reference like this:

    # class A:
    #     attr1 = Ref(None)
    # autoref(A, A.attr1)

    # This function can also be used to avoid circular imports between 2 classes
    # from 2 different packages. Imagine class P1 in package p1 has a Ref to
    # class P2 in package p2; and class P2 has another Ref to p1.P1 (which is
    # not the back Ref of the previous one: it is another, independent Ref).

    # In p1, you have

    # from p2 import P2
    # class P1:
    #     ref1 = Ref(P2)

    # Then, if you write the following in p2, Python will complain because of a
    # circular import:

    # from p1 import P1
    # class P2:
    #     ref2 = Ref(P1)

    # The solution is to write this. In p1:

    # from p2 import P2
    # class P1:
    #     ref1 = Ref(P2)
    # autoref(P1, P2.ref2)

    # And, in p2:
    # class P2:
    #     ref2 = Ref(None)
    field.class_ = class_
    setAttribute(class_, field.back.attribute, field.back)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
