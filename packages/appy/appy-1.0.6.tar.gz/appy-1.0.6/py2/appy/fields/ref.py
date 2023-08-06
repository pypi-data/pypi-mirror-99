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
# ------------------------------------------------------------------------------
import sys, re, os.path
from appy import Object
from appy.fields import Field, Initiator
from appy.fields.search import Search
from appy.px import Px
from appy.gen.layout import Table, Layouts
from appy.gen import utils as gutils
from appy.gen.navigate import Batch
from appy.shared import utils as sutils
from appy.gen.indexer import ValidValue

# Constants --------------------------------------------------------------------
ATTRIBUTE_EXISTS = 'Attribute "%s" already exists on class "%s". Note that ' \
  'several back references pointing to the same class must have different ' \
  'names, ie: back=Ref(attribute="every_time_a_distinct_name",...).'
ADD_LINK_BOTH_USED = 'Parameters "add" and "link" can\'t both be used.'
BACK_COMPOSITE = 'Only forward references may be composite.'
BACK_COMPOSITE_NOT_ONE = 'The backward ref of a composite ref must have an ' \
  'upper multiplicity of 1. Indeed, a component can not be contained in more ' \
  'than one composite object.'
LINK_POPUP_ERROR = 'When "link" is "popup", "select" must be a ' \
  'appy.fields.search.Search instance or a method that returns such an ' \
  'instance.'
OBJECT_NOT_FOUND = 'Ref field %s on %s: missing tied object with ID=%s.'
RADIOS_KO = "This field can't be rendered as radio buttons because it may " \
            "contain several values (max multiplicity is higher than 1)."
CBS_KO    = "This field can't be rendered as checkboxes because it can " \
            "only contain a single value (max multiplicity is 1)."

def setAttribute(klass, name, value):
    '''Sets on p_klass attribute p_name having some p_value. If this attribute
       already exists, an exception is raised.'''
    if hasattr(klass, name):
        raise Exception(ATTRIBUTE_EXISTS % (name, klass.__name__))
    setattr(klass, name, value)

# ------------------------------------------------------------------------------
class Position:
    '''When inserting some object among a list of tied objects, this class gives
       information about where to insert it.'''
    def __init__(self, place, obj, id=False):
        # p_obj is an object (or its ID if p_id is True) among tied objects that
        # will be the reference point for the insertion.
        self.insertId = id and obj or obj.id
        # p_place can be "before" or "after" and indicates where to insert the
        # new object relative to p_obj.
        self.place = place

    def getInsertIndex(self, refs):
        '''Gets the index, within tied objects p_refs, where to insert the newly
           created object.'''
        res = refs.index(self.insertId)
        if self.place == 'after':
            res += 1
        return res

# ------------------------------------------------------------------------------
class RefInitiator(Initiator):
    '''When an object is added via a Ref field, this class gives information
       about the initiator Ref field and its object.'''

    def __init__(self, tool, req, info):
        Initiator.__init__(self, tool, req, info)
        # We may have information about the place to insert the newly created
        # object into the Ref.
        self.insertInfo = req.get('insert')
        if self.insertInfo:
            place, objectId = self.insertInfo.split('.')
            self.position = Position(place, objectId, id=True)
        else:
            self.position = None

    def checkAllowed(self):
        '''Checks that adding an object via self.field is allowed'''
        return self.field.checkAdd(self.obj.o)

    def updateParameters(self, params):
        '''Add the relevant parameters to the object edition page, related to
           this initiator.'''
        # Get potential information about where to insert the object
        if self.insertInfo: params['insert'] = self.insertInfo

    def goBack(self):
        '''After the object has been created, go back to its "view" page or go
           back to the initiator.'''
        return self.field.viewAdded and 'view' or 'initiator'

    def getNavInfo(self, new):
        '''Compute the correct nav info at the newly inserted p_new object'''
        # At what position is p_new among tied objects ?
        zobj = self.obj.o
        position = self.field.getIndexOf(zobj, new.id) + 1
        total = len(getattr(zobj.aq_base, self.field.name, ()))
        return self.field.getNavInfo(zobj, position, total)

    def manage(self, new):
        '''The p_new object must be linked with the initiator object and the
           action must potentially be historized.'''
        # Link the new object to the initiator
        self.field.linkObject(self.obj, new, at=self.position)
        # Record this change into the initiator's history when relevant
        zobj = self.obj.o
        if self.field.getAttribute(zobj, 'historized'):
            title = new.getValue('title', formatted='shown')
            className = self.tool.o.getPortalType(new.klass)
            msg = '%s: %s' % (self.tool.translate(className), title)
            zobj.addHistoryEvent('_dataadd_', comments=msg)

# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
class Ref(Field):
    # Make sub-classes available here
    Position = Position
    Separator = Separator

    # Unique, static cell layout
    cellLayout = Layouts.Ref.cell

    # Getting a ref value is something special: disable the standard Appy
    # machinery for this.
    customGetValue = True

    # A Ref has a specific initiator class
    initiator = RefInitiator

    # This PX displays the title of a referenced object, with a link on it to
    # reach the consult view for this object. If we are on a back reference, the
    # link allows to reach the correct page where the forward reference is
    # defined. If we are on a forward reference, the "nav" parameter is added to
    # the URL for allowing to navigate from one object to the next/previous one.
    pxObjectTitle = Px('''
     <x var="navInfo=field.getNavInfo(zobj, batch.start + currentNumber, \
                                      batch.total, inPickList, inMenu);
             pageName=field.isBack and field.back.pageName or 'main';
             titleMode=field.getTitleMode(selector);
             selectJs=selector and 'onSelectObject(%s,%s,%s)' % (q(cbId), \
                         q(selector.initiatorHook), q(selector.initiator.url))">
      <x if="not selectable">::field.getSupTitle(obj, tied, navInfo)</x>
      <x>::tied.o.getListTitle(mode=titleMode, nav=navInfo, target=target, \
             page=pageName, inPopup=inPopup, selectJs=selectJs)</x>
      <x if="not selectable">
       <span style=":showSubTitles and 'display:inline' or 'display:none'"
            name="subTitle" class=":tied.o.getCssFor('subTitle')"
            var="sub=field.getSubTitle(obj, tied)" if="sub">::sub</span>
      </x></x>''')

    # This PX displays buttons for triggering global actions on several linked
    # objects (delete many, unlink many,...)
    pxGlobalActions = Px('''
     <div class="globalActions">
      <!-- Insert several objects (if in pick list) -->
      <input if="inPickList"
             var2="action='link'; label=_('object_link_many');
                   css=ztool.getButtonCss(label)"
             type="button" class=":css" value=":label"
             onclick=":'onLinkMany(%s,%s,%s)' % \
                        (q(action), q(ajaxHookId), q(batch.start))"
             style=":url('linkMany', bg=True)"/>
      <!-- Unlink several objects -->
      <input if="mayUnlink and not selector"
             var2="imgName=linkList and 'unlinkManyUp' or 'unlinkMany';
                   action='unlink'; label=_('object_unlink_many');
                   css=ztool.getButtonCss(label)"
             type="button" class=":css" value=":label"
             onclick=":'onLinkMany(%s,%s,%s)' % \
                        (q(action), q(ajaxHookId), q(batch.start))"
             style=":url(imgName, bg=True)"/>
      <!-- Delete several objects -->
      <input if="mayEdit and field.delete and not selector"
             var2="action='delete'; label=_('object_delete_many');
                   css=ztool.getButtonCss(label)"
             type="button" class=":css" value=":label"
             onclick=":'onLinkMany(%s,%s,%s)' % \
                        (q(action), q(ajaxHookId), q(batch.start))"
             style=":url('deleteMany', bg=True)"/>
      <!-- Select objects and close the popup -->
      <input if="selector" type="button"
             var="label=_('object_link_many'); css=ztool.getButtonCss(label)"
             value=":label" class=":css" style=":url('linkMany', bg=True)"
             onclick=":'onSelectObjects(%s,%s,%s,%s,%s)' % \
              (q('%s_%s' % (zobj.id, field.name)), q(selector.initiatorHook), \
               q(selector.initiator.url), q(selector.initiatorMode), \
               q(selector.onav))"/>
     </div>''')

    # This PX displays icons for triggering actions on some tied object
    # (edit, delete, etc).
    pxObjectActions = Px('''
     <div if="field.showActions" class="objectActions"
          style=":'display:%s' % field.actionsDisplay"
          var2="layoutType='buttons';
                ztied=tied.o;
                editable=ztied.mayEdit();
                locked=ztied.isLocked(user, 'main')">
      <!-- Arrows for moving objects up or down -->
      <x if="(batch.total &gt;1) and changeOrder and not inPickList \
             and not inMenu"
         var2="js='askBunchMove(%s,%s,%s,%%s)' % \
                   (q(batch.hook), q(batch.start), q(tiedUid))">
       <!-- Move to top -->
       <img if="objectIndex &gt; 1" class="clickable" src=":url('arrowsUp')"
            title=":_('move_top')" onclick=":js % q('top')"/>
       <!-- Move to bottom -->
       <img if="objectIndex &lt; (batch.total-2)" class="clickable"
            src=":url('arrowsDown')" title=":_('move_bottom')"
            onclick=":js % q('bottom')"/>
       <!-- Move up -->
       <img if="objectIndex &gt; 0" class="clickable" src=":url('arrowUp')"
            title=":_('move_up')" onclick=":js % q('up')"/>
       <!-- Move down -->
       <img if="objectIndex &lt; (batch.total-1)" class="clickable"
            src=":url('arrowDown')" title=":_('move_down')"
            onclick=":js % q('down')"/>
      </x>
      <!-- Edit -->
      <x if="editable and (create != 'noForm')">
       <a if="not locked"
          var2="navInfo=field.getNavInfo(zobj, batch.start + currentNumber, \
                                         batch.total);
                linkInPopup=inPopup or (target.target != '_self')"
          href=":ztied.getUrl(mode='edit', page='main', nav=navInfo, \
                              inPopup=linkInPopup)"
          target=":target.target" onclick=":target.onClick">
        <img src=":url('edit')" title=":_('object_edit')"/>
       </a>
       <x if="locked"
          var2="zobj=ztied; lockStyle=''; page='main'">::tied.pxLock</x>
      </x>
      <!-- Delete -->
      <img var="mayDeleteViaField=inPickList or field.delete;
                back=(inMenu and (layoutType=='buttons')) and \
                     q(zobj.id) or 'null'"
        if="not locked and mayEdit and mayDeleteViaField and ztied.mayDelete()"
        class="clickable" title=":_('object_delete')" src=":url('delete')"
        onclick=":'onDeleteObject(%s,%s)' % (q(tiedUid), back)"/>
      <!-- Unlink -->
      <img if="mayUnlink and field.mayUnlinkElement(obj, tied)"
           var2="imgName=linkList and 'unlinkUp' or 'unlink'"
           class="clickable" title=":_('object_unlink')" src=":url(imgName)"
           onClick=":field.getOnUnlink(q, _, zobj, tiedUid, batch)"/>
      <!-- Insert (if in pick list) -->
      <img if="inPickList" var2="action='link'" class="clickable"
           title=":_('object_link')" src=":url(action)"
           onclick=":'onLink(%s,%s,%s,%s)' % (q(action), q(zobj.id), \
                      q(field.name), q(tiedUid))"/>
      <!-- Insert another object before this one -->
      <x if="not inPickList and (mayAdd == 'anywhere')">
       <img if="not createFromSearch"
            src=":url('addAbove')" class="clickable"
            title=":_('object_add_above')"
            onclick=":'onAdd(%s,%s,%s)' % \
                      (q('before'), q(addFormName), q(tiedUid))"/>
       <a if="createFromSearch" target="appyIFrame"
          href=":ztool.getCreateLink(tiedClassName, create, addFormName, \
                  sourceField=prefixedName, insert='before.%s' % tiedUid)">
        <img src=":url('addAboveFrom')" class="clickable"
             title=":_('object_add_above_from')"
             onclick="openPopup('iframePopup')"/>
       </a>
      </x>
      <!-- Fields (actions) defined with layout "buttons" -->
      <x if="not inPopup and (field.showActions == 'all')"
         var2="fields=ztied.getAppyTypes('buttons', 'main');
               layoutType='cell';
               zobj=ztied">
       <!-- Call pxCell and not pxRender to avoid having a table -->
       <x for="field in fields"
          var2="name=field.name; smallButtons=True">:field.pxCell</x>
      </x>
      <!-- Workflow transitions -->
      <x if="ztied.showTransitions('result')"
         var2="targetObj=ztied">:tied.pxTransitions</x>
     </div>''')

    # Displays the button allowing to add a new object through a Ref field, if
    # it has been declared as addable and if multiplicities allow it.
    pxAdd = Px('''
     <x if="mayAdd and not inPickList">
      <form class=":inMenu and 'addFormMenu' or 'addForm'"
            name=":addFormName" id=":addFormName" target=":target.target"
            action=":'%s/do' % folder.absolute_url()">
       <input type="hidden" name="action" value="Create"/>
       <input type="hidden" name="className" value=":tiedClassName"/>
       <input type="hidden" name="template" value=""/>
       <input type="hidden" name="insert" value=""/>
       <input type="hidden" name="nav"
              value=":field.getNavInfo(zobj, 0, batch.total)"/>
       <input type="hidden" name="popup"
              value=":(inPopup or (target.target != '_self')) and '1' or '0'"/>
       <input if="not createFromSearch"
              type=":(field.addConfirm or (create == 'noForm')) \
                     and 'button' or 'submit'"
        var="addLabel=_(field.addLabel);
             label=inMenu and tiedClassLabel or addLabel;
             css=ztool.getButtonCss(label)" class=":css"
        value=":label" style=":url('add', bg=True)" title=":addLabel"
        onclick=":field.getOnAdd(q, addFormName, addConfirmMsg, target, \
                                 ajaxHookId, batch.start, create)"/>
      </form>
      <!-- Button for creating an object from a template when relevant -->
      <x if="createFromSearch"
         var2="fromRef=True; className=tiedClassName;
               sourceField=prefixedName">:tool.pxAddFrom</x>
     </x>''')

    # Displays the button allowing to select, from a popup, objects to be linked
    # via the Ref field.
    pxLink = Px('''
     <a target=":inPopup and 'subIFrame' or 'appyIFrame'"
        var="tiedClassName=tiedClassName|ztool.getPortalType(field.klass);
             className=ztool.getPortalType(obj.klass);
             popupId=inPopup and 'iframeSub' or 'iframePopup'"
        href=":field.getPopupLink(obj, tiedClassName, popupMode, name)"
        onclick=":'openPopup(%s)' % q(popupId)">
      <div var="repl=popupMode == 'repl';
                labelId=repl and 'search_button' or field.addLabel;
                icon=repl and 'search' or 'add';
                label=_(labelId);
                css=ztool.getButtonCss(label)"
           class=":css"
           style=":field.getLinkStyle(icon, layoutType, url)">:label</div>
     </a>''')

    # This PX displays, in a cell header from a ref table, icons for sorting the
    # ref field according to the field that corresponds to this column.
    pxSortIcons = Px('''
     <x if="changeOrder and (len(objects) &gt; 1) and \
            refField.isSortable(usage='ref')">
      <img class="clickable" src=":url('sortAsc')"
           var="js='askBunchSortRef(%s, %s, %s, %s)' % \
                  (q(ajaxHookId), q(batch.start), q(refField.name), q('False'))"
           onclick=":'askConfirm(%s,%s,%s)' % (q('script'), q(js,False), \
                                               q(sortConfirm))"/>
      <img class="clickable" src=":url('sortDesc')"
           var="js='askBunchSortRef(%s, %s, %s, %s)' % \
                  (q(ajaxHookId), q(batch.start), q(refField.name), q('True'))"
           onclick=":'askConfirm(%s,%s,%s)' % (q('script'), q(js,False), \
                                               q(sortConfirm))"/>
     </x>''')

    # Shows the object number in a numbered list of tied objects
    pxNumber = Px('''
     <x if="not changeNumber">:objectIndex+1</x>
     <div if="changeNumber" class="dropdownMenu"
          var2="id='%s_%d' % (ajaxHookId, objectIndex);
                imgId='%s_img' % id;
                inputId='%s_v' % id"
          onmouseover="toggleDropdown(this)"
          onmouseout="toggleDropdown(this,'none')">
      <input type="text" size=":numberWidth" id=":inputId"
             value=":objectIndex+1" onclick="this.select()"
             onkeydown=":'if (event.keyCode==13) \
                              document.getElementById(%s).click()' % q(imgId)"/>
      <!-- The menu -->
      <div class="dropdown">
       <img class="clickable" src=":url('move')" id=":imgId"
            title=":_('move_number')"
            onclick=":'askBunchMove(%s,%s,%s,this)' % \
                       (q(batch.hook), q(batch.start), q(tiedUid))"/>
      </div>
     </div>''')

    # PX displaying tied objects as a list
    pxViewList = Px('''
     <div id=":ajaxHookId"
          var="colsets=field.getColSets(obj, ztool, tiedClassName, dir, \
                addNumber=numbered and not inPickList and not selector, \
                addCheckboxes=checkboxes)">
      <div if="(layoutType == 'view') or mayAdd or mayLink" class="refBar">
       <x if="field.collapsible and objects">:collapse.px</x>
       <span if="subLabel" class="discreet">:_(subLabel)</span>
       <x if="len(objects) &gt; 1">
        (<span class="discreet">:batch.total</span>)</x>
       <x if="not selector">:field.pxAdd</x>
       <!-- This button opens a popup for linking additional objects -->
       <x if="mayLink and not inPickList and not selector and field.linkInPopup"
          var2="popupMode='add'">:field.pxLink</x>
       <!-- The search button if field is queryable -->
       <input if="objects and field.queryable" type="button"
              var2="label=_('search_button'); css=ztool.getButtonCss(label)"
              value=":label" class=":css" style=":url('search', bg=True)"
              onclick=":'goto(%s)' % \
               q('%s/search?className=%s&amp;ref=%s:%s' % \
               (ztool.absolute_url(), tiedClassName, zobj.id, field.name))"/>
       <!-- The colset selector if multiple colsets are available -->
       <select if="len(colsets) &gt; 1" class="discreet"
               onchange=":'askBunchSwitchColset(%s,this.value)'% q(ajaxHookId)">
        <option for="cset in colsets" value=":cset.identifier"
                selected=":cset.identifier==colset">:_(cset.label)</option>
       </select>
      </div>
      <script>:field.getAjaxData(ajaxHookId, zobj, popup=int(inPopup), \
        checkboxes=checkboxes, startNumber=batch.start, sourceId=zobj.id, \
        totalNumber=batch.total, refFieldName=field.name,layoutType=layoutType,\
        inPickList=inPickList, numbered=numbered, colset=colset)</script>

      <!-- (Top) navigation -->
      <x>:batch.pxNavigate</x>

      <!-- No object is present -->
      <p class="discreet" if="not objects">:_(field.noObjectLabel)</p>

      <!-- Linked objects -->
      <table if="objects" id=":collapse.id" style=":collapse.style"
             class=":ztool.getResultCss(tiedClassName, layoutType)"
             width=":field.width or field.layouts['view'].width"
             var2="columns=field.getCurrentColumns(colset, colsets);
                   currentNumber=0">
       <tr if="field.showHeaders">
        <th for="column in columns" width=":column.width"
            align=":column.align" var2="refField=column.field">
         <x if="column.header">
          <x if="refField == '_checkboxes'">
           <img src=":url('checkall')" class="clickable"
                title=":_('check_uncheck')"
                onclick=":'toggleAllCbs(%s)' % q(ajaxHookId)"/>
          </x>
          <x if="not column.special">
           <span>::_(refField.labelId)</span>
           <x if="not selector">:field.pxSortIcons</x>
           <x var="className=tiedClassName;
                   field=refField">:tool.pxShowDetails</x>
          </x>
         </x>
        </th>
       </tr>
       <!-- Loop on every (tied or selectable) object -->
       <x for="tied in objects"
          var2="@currentNumber=currentNumber + 1;
                rowCss=loop.tied.odd and 'even' or 'odd'">
        <x if="field.separator">::field.dumpSeparator(obj, loop.tied.previous, \
                                                      tied, columns)</x>
        <x>:tied.pxViewAsTied</x></x>
      </table>
      <!-- Global actions -->
      <x if="mayEdit and checkboxes and field.getAttribute(obj, \
              'showGlobalActions')">:field.pxGlobalActions</x>
      <!-- (Bottom) navigation -->
      <x>:batch.pxNavigate</x>
      <!-- Init checkboxes if present -->
      <script if="checkboxes">:'initCbs(%s)' % q(ajaxHookId)</script>
     </div>''')

    # PX that displays referred objects as dropdown menus
    pxMenu = Px('''
     <img if="menu.icon" src=":menu.icon" title=":menu.text"/> <x
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
        <x if="singleObject" var2="tied=menu.objects[0]; zt=tied.o">
         <x if="field.menuUrlMethod"
            var2="mUrl,mTarget=field.getMenuUrl(
                   zobj,tied,target)">::zt.getListTitle(target=mTarget,
                   baseUrl=mUrl, css='dropdownMenu',
                   linkTitle=zt.getShownValue('title'), title=field.pxMenu)</x>
         <x if="not field.menuUrlMethod"
            var2="linkInPopup=inPopup or (target.target != '_self');
                  baseUrl=zt.getUrl(nav='no',
                    inPopup=linkInPopup)">::zt.getListTitle(target=target,
                baseUrl=baseUrl, css='dropdownMenu', \
                linkTitle=zt.getShownValue('title'), title=field.pxMenu)</x>
        </x>
        <b if="not singleObject"
           class=":field.getMenuCss(obj, menu)">:field.pxMenu</b>

        <!-- The dropdown menu containing tied objects -->
        <div class="dropdown" style="width:150px">
         <div for="tied in menu.objects"
              var2="batch=field.getBatchFor(batch.hook, len(menu.objects));
                    tiedUid=tied.id"
              class=":not loop.tied.first and 'refMenuItem' or ''">
          <!-- A specific link may have to be computed from
               field.menuUrlMethod -->
          <x if="field.menuUrlMethod"
             var2="mUrl,mTarget=field.getMenuUrl(zobj,tied,\
                target)">::tied.o.getListTitle(target=mTarget, baseUrl=mUrl)</x>
          <!-- Show standard pxObjectTitle else -->
          <x if="not field.menuUrlMethod">:field.pxObjectTitle</x>
          <x if="tied.o.mayAct()">:field.pxObjectActions</x>
         </div>
        </div>
       </div>
      </div><x>:field.pxAdd</x></x> ''')

    # Simplified widget for fields with render="minimal"
    pxViewMinimal = Px('''
     <x><x>::field.renderMinimal(obj, objects, inPopup)</x>
      <!-- If this field is a master field -->
      <input type="hidden" if="masterCss and (layoutType == 'view')"
             name=":name" id=":name" class=":masterCss"
             value=":[o.id for o in objects]" /></x>''')

    # Simplified widget for fields with render="links"
    pxViewLinks = Px('''
     <x>::field.renderMinimal(obj, objects, inPopup, links=True)</x>''')

    # PX that displays referred objects through this field.
    # In mode link="list", if request key "scope" is:
    # - not in the request, the whole field is shown (both available and already
    #   tied objects);
    # - "objs", only tied objects are rendered;
    # - "poss", only available objects are rendered (the pick list).
    # ! scope is forced to "objs" on non-view "inner" (cell, buttons) layouts.
    pxView = Px('''
     <x var="layoutType=layoutType|req.get('layoutType', 'view');
             colset=req.get('colset', 'main');
             render=field.getRenderMode(layoutType);
             name=name|field.name;
             prefixedName='%s:%s' % (zobj.id, name);
             selector=field.getSelector(obj, req);
             selectable=bool(selector) and inPopup;
             linkList=field.link == 'list';
             scope=(layoutType != 'view') and 'objs' or \
                   scope|req.get('scope', 'all');
             inPickList=(scope == 'poss');
             create=field.getAttribute(zobj, 'create');
             createFromSearch=not isinstance(create, basestring);
             ajaxSuffix=inPickList and 'poss' or 'objs';
             ajaxHookId='%s_%s_%s' % (zobj.id, name, ajaxSuffix);
             inMenu=False;
             batch=field.getBatch(render, req, ajaxHookId);
             info=field.getViewValues(zobj, name, scope, batch);
             objects=info.objects;
             dummy=batch.update(total=info.totalNumber, size=info.batchSize, \
                                length=len(objects));
             numberWidth=len(str(batch.total));
             folder=zobj.getCreateFolder();
             tiedClassName=ztool.getPortalType(field.klass);
             tiedClassLabel=_(tiedClassName);
             backHook=(layoutType == 'cell') and zobj.id or None;
             target=ztool.getLinksTargetInfo(field.klass, backHook);
             mayEdit=(layoutType != 'edit') and \
                     zobj.mayEdit(field.writePermission);
             mayEd=not inPickList and mayEdit;
             mayAdd=mayEd and field.mayAdd(zobj, checkMayEdit=False);
             addFormName=mayAdd and '%s_%s_add' % (zobj.id, field.name) or '';
             mayLink=mayEd and field.mayAdd(zobj, mode='link', \
                                            checkMayEdit=False);
             mayUnlink=mayLink and field.getAttribute(zobj, 'unlink');
             addConfirmMsg=field.addConfirm and \
                           _('%s_addConfirm' % field.labelId) or '';
             changeOrder=mayEd and field.getAttribute(zobj, 'changeOrder');
             sortConfirm=changeOrder and _('sort_confirm');
             numbered=not inPickList and field.isNumbered(zobj);
             gotoNumber=numbered;
             changeNumber=not inPickList and numbered and changeOrder and \
                          (batch.total &gt; 3);
             checkboxesEnabled=(layoutType != 'cell') and \
                               field.getAttribute(zobj, 'checkboxes');
             checkboxes=checkboxesEnabled and ((batch.total &gt; 1) or inPopup);
             collapse=field.getCollapseInfo(obj, inPickList);
             showSubTitles=req.get('showSubTitles', 'true') == 'true'">
      <!-- JS tables storing checkbox statuses if checkboxes are enabled -->
      <script if="checkboxesEnabled and (render == 'list') and \
                  (scope == 'all')">:field.getCbJsInit(zobj)</script>
      <!-- The list of possible values, when relevant -->
      <x if="linkList and (scope == 'all') and mayEdit"
         var2="scope='poss'; layoutType='view'">:field.pxView</x>
      <!-- The list of tied or possible values, depending on scope -->
      <x if="render == 'list'"
         var2="subLabel=field.getListLabel(inPickList)">:field.pxViewList</x>
      <x if="render in ('menus', 'minimal', 'links')">:getattr(field, \
         'pxView%s' % render.capitalize())</x>
     </x>''')

    pxCell = pxView

    # Edit widget, for Refs with link == 'popup'
    pxEditPopup = Px('''
     <x var="objects=field.getPopupObjects(obj, name, req, requestValue);
             onChangeJs=field.getOnChange(zobj, layoutType);
             charsWidth=field.getWidthInChars(False)">
      <!-- The select field allowing to store the selected objects -->
      <select if="objects" name=":name" id=":name" multiple="multiple"
              size=":field.getSelectSize(False, isMultiple)"
              style=":field.getSelectStyle(False, isMultiple)"
              onchange=":onChangeJs">
       <option for="tied in objects" value=":tied.uid" selected="selected"
               var2="title=field.getReferenceLabel(obj, tied, unlimited=True)"
               title=":title">:ztool.truncateValue(title, charsWidth)</option>
      </select>
      <!-- Back from a popup, force executing onchange JS code above, for
           updating potential master/slave relationships. -->
      <script if="objects and \
         ('semantics' in req)">:'getNode(%s,true).onchange()' % q(name)</script>
      <span if="not objects">-</span>
      <!-- The button for opening the popup -->
      <x var="popupMode='repl'">:field.pxLink</x></x>''')

    pxEdit = Px('''
     <x if="field.link and (field.link != 'list')">

      <!-- Choose a value from a popup -->
      <x if="field.linkInPopup">:field.pxEditPopup</x>

      <!-- Choose a value from a select widget, radio buttons or checkboxes -->
      <x if="not field.linkInPopup"
         var2="isSelect=field.link == True;
               objects=field.getPossibleValues(zobj);
               uids=[o.id for o in field.getValue(zobj, name, \
                                               layout=layoutType, appy=False)]">
       <select if="isSelect" var="charsWidth=field.getWidthInChars(False)"
               name=":name" id=":name" multiple=":isMultiple"
               size=":field.getSelectSize(False, isMultiple)"
               style=":field.getSelectStyle(False, isMultiple)"
               onchange=":field.getOnChange(zobj, layoutType)">
        <option value="" if="not isMultiple">:_(field.noValueLabel)</option>
        <option for="tied in objects"
               var2="uid=tied.id;
                     title=field.getReferenceLabel(obj, tied, unlimited=True)"
               selected=":field.valueIsSelected(uid, inRequest, uids, \
                                                requestValue)" value=":uid"
               title=":title">:ztool.truncateValue(title, charsWidth)</option>
       </select>
       <div if="not isSelect" style=":field.getRadioStyle()">
        <div for="tied in objects"
             var2="uid=tied.id;
                   vid='%s_%s' % (name, uid);
                   text=field.getReferenceLabel(obj, tied, unlimited=True)">
         <input type=":field.link" name=":name" id=":vid" value=":uid"
          class=":masterCss" onchange=":field.getOnChange(zobj, layoutType)"
          checked=":field.valueIsSelected(uid, inRequest, uids, requestValue)"/>
         <label lfor=":vid" class="subLabel">::text</label>
        </div>
       </div>
      </x>
     </x>''')

    pxSearch = Px('''
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
     <select var="objects=field.getPossibleValues(ztool, usage='search');
                  charsWidth=field.getWidthInChars(True)"
             name=":widgetName" multiple="multiple"
             size=":field.getSelectSize(True, True)"
             style=":field.getSelectStyle(True, True)"
             onchange=":field.getOnChange(ztool, 'search', className)">
      <option if="field.emptyIndexValue"
              value=":field.emptyIndexValue">:_('no_object')</option>
      <option for="tied in objects" value=":tied.id"
              var2="title=field.getReferenceLabel(obj, tied, unlimited=True)"
              title=":title">:ztool.truncateValue(title, charsWidth)</option>
     </select>''')

    # Widget for filtering object values on query results
    pxFilterSelect = Px('''
     <select var="name=field.name;
                  filterId='%s_%s' % (mode.ajaxHookId, name);
                  charsWidth=field.getWidthInChars(True);
                  emptyVal=field.emptyIndexValue;
                  objects=field.getPossibleValues(ztool, usage='filter')"
          if="objects" id=":filterId" name=":filterId" class="discreet"
          onchange=":'askBunchFiltered(%s,%s)' % (q(mode.ajaxHookId), q(name))">
      <option value="">:_('everything')</option>
      <option if="emptyVal" value=":emptyVal"
              selected=":mode.inFilter(name, emptyVal)">:_('no_object')</option>
      <option for="tied in objects" value=":tied.id"
       var2="title=field.getReferenceLabel(obj, tied, unlimited=True, \
                                           usage='filter')"
       selected=":mode.inFilter(name, tied.id)"
       title=":title">:ztool.truncateValue(title, charsWidth)</option>
     </select>''')

    def __init__(self, klass=None, attribute=None, validator=None,
      composite=False, multiplicity=(0,1), default=None, defaultOnEdit=None,
      add=False, addConfirm=False, delete=None, create='form', creators=None,
      link=True, unlink=None, linkMethod=None, unlinkElement=None,
      unlinkConfirm=True, insert=None, beforeLink=None, afterLink=None,
      afterUnlink=None, back=None, backSecurity=True, show=True, page='main',
      group=None, layouts=None, showHeaders=False, shownInfo=None,
      fshownInfo=None, select=None, maxPerPage=30, move=0, indexed=False,
      mustIndex=True, indexValue=None, emptyIndexValue='', searchable=False,
      specificReadPermission=False, specificWritePermission=False, width=None,
      height=5, maxChars=None, colspan=1, master=None, masterValue=None,
      focus=False, historized=False, mapping=None, generateLabel=None,
      label=None, queryable=False, queryFields=None, queryNbCols=1,
      navigable=False, changeOrder=True, numbered=False, checkboxes=True,
      checkboxesDefault=False, sdefault='', scolspan=1, swidth=None,
      sheight=None, sselect=None, persist=True, render='list',
      renderMinimalSep=', ', menuIdMethod=None, menuInfoMethod=None,
      menuUrlMethod=None, menuCss=None, view=None, cell=None, edit=None,
      xml=None, translations=None, showActions='all', actionsDisplay='block',
      showGlobalActions=True, collapsible=False, links=True, viewAdded=True,
      noValueLabel='choose_a_value', noObjectLabel='no_ref',
      addLabel='object_add', filterable=True, supTitle=None, subTitle=None,
      separator=None):
        # The class whose tied objects will be instances of
        self.klass = klass
        # Specify "attribute" only for a back reference: it will be the name
        # (a string) of the attribute that will be defined on self's class and
        # will allow, from a linked object, to access the source object.
        self.attribute = attribute
        # If this Ref is "composite", it means that the source object will be
        # a composite object and tied object(s) will be its components.
        self.composite = composite
        # May the user add new objects through this ref ? "add" may hold the
        # following values:
        # - True        (boolean value): the object will be created and inserted
        #               at the place defined by parameter "insert" (see below);
        # - "anywhere"  (string) the object can be inserted at any place in the
        #               list of already linked objects ("insert" is bypassed);
        # - a method producing one of the hereabove values.
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
        #               | attribute "addConfirm" will be ignored. "create" may
        #               | also hold a method returning one of the
        #               | above-mentioned values.
        # ----------------------------------------------------------------------
        self.create = create
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
        # May the user link existing objects through this ref ? If "link" is:
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
        #   "list"   | the user will, on the view page, choose objects from a
        #            | list of objects which is similar to those rendered in
        #            | pxViewList ;
        # ----------------------------------------------------------------------
        #  "popup"   | the user will, on the edit page, choose objects from a
        #            | popup window. In this case, parameter "select" can hold a
        #            | Search instance or a method ;
        # ----------------------------------------------------------------------
        # "popupRef" | the user will choose objects from a popup window, that
        #            | will display objects tied via a Ref field. In this case,
        #            | parameter "select" must be a method that returns a tuple
        #            | (obj, name), "obj" being the source object of the Ref
        #            | field whose name is in "name".
        # ----------------------------------------------------------------------
        self.link = link
        self.linkInPopup = link in ('popup', 'popupRef')
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
        # it inserted? If "insert" is:
        # None,     it will be inserted at the end;
        # "start",  it will be inserted at the start of the tied objects;
        # a method, (called with the object to insert as single arg), its return
        #           value (a number or a tuple of numbers) will be
        #           used to insert the object at the corresponding position
        #           (this method will also be applied to other objects to know
        #           where to insert the new one);
        # a tuple,  ('sort', method), the given method (called with the object
        #           to insert as single arg) will be used to sort tied objects
        #           and will be given as param "key" of the standard Python
        #           method "sort" applied on the list of tied objects.
        # With value ('sort', method), a full sort is performed and may hardly
        # reshake the tied objects; with value "method" alone, the tied
        # object is inserted at some given place: tied objects are more
        # maintained in the order of their insertion.
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
            # klass may be None in the case we are defining an auto-Ref to the
            # same class as the class where this field is defined. In this case,
            # when defining the field within the class, write
            # myField = Ref(None, ...)
            # and, at the end of the class definition (name it K), write:
            # K.myField.klass = K
            # setattr(K, K.myField.back.attribute, K.myField.back)
            if klass and back: setAttribute(klass, back.attribute, back)
            # A composite ref must have a back ref having an upper
            # multiplicity = 1
            if self.composite and back and (back.multiplicity[1] != 1):
                raise Exception(BACK_COMPOSITE_NOT_ONE)
        else:
            self.isBack = True
            if self.composite: raise Exception(BACK_COMPOSITE)
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
        # Search.ColSet instances. In this case, several sets of columns are
        # available and the user can switch between those sets when consulting
        # the field.
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
        # If param p_queryable is True, the user will be able to perform queries
        # from the UI within referenced objects.
        self.queryable = queryable
        # Here is the list of fields that will appear on the search screen.
        # If None is specified, by default we take every indexed field
        # defined on referenced objects' class.
        self.queryFields = queryFields
        # The search screen will have this number of columns
        self.queryNbCols = queryNbCols
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
        # There are different ways to render a bunch of linked objects:
        # - "list"  (the default) renders them as a list (=a XHTML table);
        # - "menus" renders them as a series of popup menus, grouped by type.
        #           Note that render mode "menus" will only be applied in "cell"
        #           and "buttons" layouts. Indeed, we need to keep the "list"
        #           rendering in the "view" layout because the "menus" rendering
        #           is minimalist and does not allow to perform all operations
        #           on linked objects (add, move, delete, edit...);
        # - "minimal" renders a list not-even-clickable data about the tied
        #           objects (according to shownInfo);
        # - "links" renders a list of clickable comma-separated data about the
        #           tied objects (according to shownInfo).
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
        # With the underlying ZCTextIndex index for this field, it is impossible
        # to perform queries like
        #         "tiedObjectId1 OR tiedObjectId2 OR <<no object at all>>"
        # If you have to perform such queries, specify some predefined string
        # that represents an empty value, ie, "_empty_". This way, you will be
        # able to express the previous example as
        #         "tiedObjectId1 OR tiedObjectId2 OR _empty_"
        self.emptyIndexValue = emptyIndexValue
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
        #  supTitle   may hold a method accepting 2 args: the tied object and
        #             the navigation string;
        #  subTitle   may hold a method accepting the tied object as single arg.
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
        # Call the base constructor
        Field.__init__(self, validator, multiplicity, default, defaultOnEdit,
          show, page, group, layouts, move, indexed, mustIndex, indexValue,
          searchable, specificReadPermission, specificWritePermission, width,
          height, None, colspan, master, masterValue, focus, historized,
          mapping, generateLabel, label, sdefault, scolspan, swidth, sheight,
          persist, False, view, cell, edit, xml, translations)
        self.validable = bool(self.link)
        # Initialise filterPx when relevant. If you want to disable filtering
        # although it could be proposed, set p_filterable to False. This can be
        # useful when there would be too many values to filter.
        if (self.link == True) and indexed and filterable:
            self.filterPx = 'pxFilterSelect'
        self.checkParameters()

    def checkParameters(self):
        '''Ensures this Ref is correctly defined'''
        # For forward Refs, "add" and "link" can't both be used
        if not self.isBack and (self.add and self.link):
            raise Exception(ADD_LINK_BOTH_USED)
        # If link is "popup", "select" must hold a Search instance
        if (self.link == 'popup') and \
           (not isinstance(self.select, Search) and not callable(self.select)):
            raise Exception(LINK_POPUP_ERROR)
        # Valid link modes depend on multiplicities
        multiple = self.isMultiValued()
        if multiple and (self.link == 'radio'):
            raise Exception(RADIOS_KO)
        if not multiple and (self.link == 'checkbox'):
            raise Exception(CBS_KO)

    def isShowable(self, obj, layoutType):
        res = Field.isShowable(self, obj, layoutType)
        if not res: return res
        # We add here specific Ref rules for preventing to show the field under
        # some inappropriate circumstances.
        if layoutType == 'edit':
            if self.mayAdd(obj): return
            if self.link in (False, 'list'): return
        if self.isBack:
            if layoutType == 'edit': return
            else: return getattr(obj.aq_base, self.name, None)
        return res

    def isRenderable(self, layoutType):
        '''Only Ref fields with render = "menus" can be rendered on "button"
           layouts.'''
        if layoutType == 'buttons': return self.render == 'menus'
        return True

    def valueIsSelected(self, id, inRequest, dbValue, requestValue):
        '''In pxEdit, is object whose ID is p_id selected?'''
        if inRequest:
            return id in requestValue
        else:
            return id in dbValue

    def getValue(self, obj, name=None, layout=None, appy=True,
      noListIfSingleObj=False, startNumber=None, someObjects=False,
      maxPerPage=None):
        '''Returns the objects linked to p_obj through this Ref field. It
           returns Appy wrappers if p_appy is True, the Zope objects else.

           * If p_startNumber is None, it returns all referred objects;
           * if p_startNumber is a number, it returns p_maxPerPage objects
             (or self.maxPerPage if p_maxPerPage is None), starting at
             p_startNumber.

           If p_noListIfSingleObj is True, it returns the single reference as
           an object and not as a list.

           If p_someObjects is True, it returns an instance of SomeObjects
           instead of returning a list of references.'''
        # Get the value from the database
        uids = self.getStoredValue(obj, name) or []
        if not uids:
            # Maybe is there a default value ?
            defValue = Field.getValue(self, obj, name, layout)
            if defValue:
                if type(defValue) in sutils.sequenceTypes:
                    uids = [o.o.id for o in defValue]
                else:
                    uids = [defValue.o.id]
        # Prepare the result: an instance of SomeObjects, that will be unwrapped
        # if not required.
        res = gutils.SomeObjects()
        res.totalNumber = res.batchSize = len(uids)
        batchNeeded = startNumber != None
        if batchNeeded:
            res.batchSize = maxPerPage or self.maxPerPage
        if startNumber != None:
            res.startNumber = startNumber
        # Get the objects given their uids
        i = res.startNumber
        tool = obj.getTool()
        while i < (res.startNumber + res.batchSize):
            if i >= res.totalNumber: break
            # Retrieve every reference in the correct format according to p_type
            tied = tool.getObject(uids[i])
            if not tied:
                obj.log(OBJECT_NOT_FOUND % (self.name, obj.id, uids[i]),
                        type='error')
            else:
                if appy: tied = tied.appy()
                res.objects.append(tied)
            i += 1
        # Manage parameter p_noListIfSingleObj
        if noListIfSingleObj and (self.multiplicity[1] == 1):
            if res.objects:
                res.objects = res.objects[0]
            else:
                res.objects = None
        if someObjects: return res
        return res.objects

    def getCopyValue(self, obj):
        '''Here, as "value ready-to-copy", we return the list of tied object
           ids, because m_store on the destination object can store tied
           objects based on such a list.''' 
        r = getattr(obj.aq_base, self.name, None)
        # Return a copy: it can be dangerous to give the real database value
        if r: return list(r)

    def getXmlValue(self, obj, value):
        '''The default XML value for a Ref is the list of tied object URLs.'''
        # Bypass the default behaviour if a custom method is given
        if self.xml: return self.xml(obj, value)
        return ['%s/xml' % tied.o.absolute_url() for tied in value]

    def getSelect(self, obj, forSearch=False):
        '''self.select can hold a Search instance or a method. In this latter
           case, call the method and return its result, that can be a Search
           instance or a list of objects.'''
        method = not forSearch and self.select or self.sselect
        if isinstance(method, Search): return method
        if method.__class__.__name__ == 'staticmethod':
            method = method.__get__(method)
        return self.callMethod(obj, method)

    def getPossibleValues(self, obj, startNumber=None, someObjects=False,
                          removeLinked=False, maxPerPage=None, usage='edit'):
        '''This method returns the list of all objects that can be selected
           to be linked as references to p_obj via p_self. It is applicable only
           for Ref fields with link!=False. If master values are present in the
           request, we use field.masterValues method instead of self.[s]select.

           If p_startNumber is a number, it returns p_maxPerPage objects (or
           self.maxPerPage if p_maxPerPage is None), starting at p_startNumber.
           If p_someObjects is True, it returns an instance of SomeObjects
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
        req = obj.REQUEST
        aobj = obj.appy()
        paginated = startNumber != None
        maxPerPage = maxPerPage or self.maxPerPage
        isSearch = False
        master = self.master
        if master and callable(self.masterValue):
            # This field is an ajax-updatable slave
            if usage == 'filter':
                # A filter will not get any master. We need to display all the
                # slave values from all the master values the user may see.
                objects = None
                for masterValue in master.getPossibleValues(obj):
                    if objects is None:
                        objects = self.masterValue(aobj, masterValue)
                    else:
                        # Ensure there is no duplicate among collected objects
                        for mo in self.masterValue(aobj, masterValue):
                            if mo not in objects:
                                objects.append(mo)
                objects = objects or []
            else:
                # Usage is "edit" or "search". Get the master value...
                if master.valueIsInRequest(obj, req):
                    # ... from the request if available
                    requestValue = master.getRequestValue(obj)
                    masterValues = master.getStorableValue(obj, requestValue,
                                                           complete=True)
                elif usage == 'edit':
                    # ... or from the database if we are editing an object
                    masterValues = master.getValue(obj, layout=usage,
                                                   noListIfSingleObj=True)
                else: # usage is "search" and we don't have any master value
                    masterValues = None
                # Get the possible values by calling self.masterValue
                if masterValues:
                    objects = self.masterValue(aobj, masterValues)
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
                objects = aobj.search(self.klass)
            else:
                # "[s]select" can be/return a Search instance or return objects
                search = self.getSelect(aobj, forSearch)
                if isinstance(search, Search):
                    isSearch = True
                    maxResults = paginated and maxPerPage or 'NO_LIMIT'
                    start = startNumber or 0
                    className = obj.getTool().getPortalType(self.klass)
                    objects = obj.executeQuery(className, search=search,
                        startNumber=start, maxResults=maxResults)
                    objects.objects = [o.appy() for o in objects.objects]
                else:
                    # "[s]select" has returned objects
                    objects = search
        # Remove already linked objects if required
        if removeLinked:
            uids = getattr(obj.aq_base, self.name, None)
            if uids:
                # Browse objects in reverse order and remove linked objects
                if isSearch: objs = objects.objects
                else: objs = objects
                i = len(objs) - 1
                while i >= 0:
                    if objs[i].id in uids: del objs[i]
                    i -= 1
        # If possible values are not retrieved from a Search, restrict (if
        # required) the result to "maxPerPage" starting at p_startNumber.
        # Indeed, in this case, unlike m_getValue, we already have all objects
        # in "objects": we can't limit objects "waking up" to at most
        # "maxPerPage".
        if isSearch:
            total = objects.totalNumber
        else:
            total = len(objects)
        if paginated and not isSearch:
            objects = objects[startNumber:startNumber + maxPerPage]
        # Return the result, wrapped in a SomeObjects instance if required
        if not someObjects:
            if isSearch: return objects.objects
            return objects
        if isSearch: return objects
        res = gutils.SomeObjects()
        res.totalNumber = total
        res.batchSize = maxPerPage
        res.startNumber = startNumber
        res.objects = objects
        return res

    def getViewValues(self, obj, name, scope, batch):
        '''Gets the values as must be shown on pxView. If p_scope is "poss", it
           is the list of possible, not-yet-linked, values. Else, it is the list
           of linked values. In both cases, we take the sub-set starting at
           p_batch.start.'''
        if scope == 'poss':
            return self.getPossibleValues(obj, startNumber=batch.start,
                     someObjects=True, removeLinked=True, maxPerPage=batch.size)
        # Return the list of already linked values
        return self.getValue(obj, name=name, startNumber=batch.start,
                             someObjects=True, maxPerPage=batch.size)

    def getLinkedObjectsByMenu(self, obj, objects):
        '''This method groups p_objects into sub-lists of objects, grouped by
           menu (happens when self.render == 'menus').'''
        if not objects: return ()
        res = []
        # We store in "menuIds" the already encountered menus:
        # ~{s_menuId : i_indexInRes}~
        menuIds = {}
        # Browse every object from p_objects and put them in their menu
        # (within "res").
        for tied in objects:
            menuId = self.menuIdMethod(obj, tied)
            if menuId in menuIds:
                # We have already encountered this menu
                menuIndex = menuIds[menuId]
                res[menuIndex].objects.append(tied)
            else:
                # A new menu
                menu = Object(id=menuId, objects=[tied])
                res.append(menu)
                menuIds[menuId] = len(res) - 1
        # Complete information about every menu by calling self.menuInfoMethod
        for menu in res:
            text, icon = self.menuInfoMethod(obj, menu.id)
            menu.text = text
            menu.icon = icon
        return res

    def getLinkStyle(self, icon, layoutType, url):
        '''Gets the CSS styles to apply for rendering the "search" button that
           opens the popup for linking objects.'''
        # Get the value for CSS attribute "float". On the "edit" layout, always
        # put the button on the right.
        if layoutType == 'edit':
            align = 'right'
        else:
            align = (self.multiplicity[1] == 1) and 'right' or 'left'
        return '%s; background-position: 10%% 50%%; float: %s' % \
               (url(icon, bg=True), align)

    def getColSets(self, obj, tool, tiedClassName, dir, usage=None,
                   addNumber=False, addCheckboxes=False):
        '''Gets the ColSet instances corresponding to every showable set of
           columns.'''
        attr = (usage == 'filter') and 'fshownInfo' or 'shownInfo'
        res = self.getAttribute(obj, attr)
        # We can have either a list of strings (a single set) or a list of
        # ColSet instances.
        if isinstance(res[0], basestring):
            # A single set
            columns = tool.getColumnsSpecifiers(tiedClassName, res, dir,
                               addNumber=addNumber, addCheckboxes=addCheckboxes)
            return [Search.ColSet('main', '', columns, specs=True)]
        else:
            # Several sets
            for colset in res:
                colset.specs = tool.getColumnsSpecifiers(tiedClassName,
                  colset.columns, dir, addNumber=addNumber,
                  addCheckboxes=addCheckboxes)
        return res

    def getCurrentColumns(self, identifier, colsets):
        '''Gets the columns defined for the current colset, whose p_identifier
           is given. The list of available p_colsets is also given.'''
        for cset in colsets:
            if cset.identifier == identifier:
                return cset.specs
        # If no one is found, return the first one, considered the default
        return colsets[0].specs

    def isNumbered(self, obj):
        '''Must we show the order number of every tied object?'''
        res = self.getAttribute(obj, 'numbered')
        if not res: return res
        # Returns the column width
        if not isinstance(res, basestring): return '15px'
        return res

    def getMenuUrl(self, zobj, tied, target):
        '''We must provide the URL of the p_tied object, when shown in a Ref
           field in render mode 'menus'. If self.menuUrlMethod is specified,
           use it. Else, returns the "normal" URL of the view page for the tied
           object, but without any navigation information, because in this
           render mode, tied object's order is lost and navigation is
           impossible.'''
        if self.menuUrlMethod:
            r = self.menuUrlMethod(zobj.appy(), tied)
            if r is None:
                # There is no specific link to build
                return None, target
            elif isinstance(r, str):
                # The method has just returned an URL
                return r, gutils.LinkTarget()
            else:
                # The method has returned a tuple (url, target)
                target = gutils.LinkTarget()
                target.target = r[1]
                return r[0], target
        return tied.o.getUrl(nav='no'), target

    def getMenuCss(self, obj, menu):
        '''Gets the CSS class that will be applied to a menu'''
        if not self.menuCss: return ''
        if callable(self.menuCss): return self.menuCss(obj, menu.objects) or ''
        return self.menuCss

    def getBatch(self, render, req, hookId):
        '''This method returns Batch instance determining a sub-set of the tied
           objects, or None if all linked objects must be shown at once (it
           happens when p_render is "menus". The batch size (= maximum number of
           objects shown at once) is defined in the request or is
           self.maxPerPage.'''
        # The Batch instance created here will be completed later on: we do not
        # know (yet) the total number of objects.
        r = Batch(hookId, total=None, length=None, size=None, start=None)
        # When using any render mode, "list" excepted, all objects must be shown
        if render != 'list': return r
        # Get the index of the first object to show
        key = '%s_startNumber' % hookId
        start = req.has_key(key) and req[key] or req.get('startNumber', 0)
        r.start = int(start)
        # Get batch size
        r.size = int(req.get('maxPerPage', self.maxPerPage))
        # The total nb of elements may be in the request (if we are ajax-called)
        total = req.get('totalNumber')
        if total: r.total = int(total)
        return r

    def getBatchFor(self, hook, total):
        '''Return a Batch instance for a p_total number of objects'''
        return Batch(hook, total, length=total, size=None, start=0)

    def getFormattedValue(self, obj, value, layoutType='view',
                          showChanges=False, language=None):
        return value

    def getIndexType(self): return 'ListIndex'

    def getIndexValue(self, obj, forSearch=False):
        '''Value for indexing is the list of UIDs of linked objects. If
           p_forSearch is True, it will return a list of the linked objects'
           titles instead.'''
        # Must we produce an index value?
        if not self.getAttribute(obj, 'mustIndex'): return
        if not forSearch:
            res = getattr(obj.aq_base, self.name, None)
            return ValidValue.forRef(self, res)
        else:
            # For the global search: return linked objects' titles
            return ' '.join([o.getShownValue('title') \
                             for o in self.getValue(obj, appy=False)])

    def hasSortIndex(self):
        '''An indexed Ref field is of type "ListIndex", which is not sortable.
           So an additional FieldIndex is required.'''
        return True

    def validateValue(self, obj, value):
        if not self.link: return
        # We only check "link" Refs because in edit views, "add" Refs are
        # not visible. So if we check "add" Refs, on an "edit" view we will
        # believe that that there is no referred object even if there is.
        # Also ensure that multiplicities are enforced.
        if not value:
            nbOfRefs = 0
        elif isinstance(value, basestring):
            nbOfRefs = 1
        else:
            nbOfRefs = len(value)
        minRef = self.multiplicity[0]
        maxRef = self.multiplicity[1]
        if maxRef is None:
            maxRef = sys.maxint
        if nbOfRefs < minRef:
            return obj.translate('min_ref_violated')
        elif nbOfRefs > maxRef:
            return obj.translate('max_ref_violated')

    def linkObject(self, obj, value, back=False, noSecurity=True,
                   executeMethods=True, at=None):
        '''This method links p_value (which can be a list of objects) to p_obj
           through this Ref field. When linking 2 objects via a Ref,
           p_linkObject must be called twice: once on the forward Ref and once
           on the backward Ref. p_back indicates if we are calling it on the
           forward or backward Ref. If p_noSecurity is True, we bypass security
           checks (has the logged user the right to modify this Ref field?).
           If p_executeMethods is False, we do not execute methods that
           customize the object insertion (parameters insert, beforeLink,
           afterLink...). This can be useful while migrating data or duplicating
           an object. If p_at is specified, it is a Position instance indicating
           where to insert the object: it then overrides self.insert.

           The method returns the effective number of linked objects.'''
        zobj = obj.o
        # Security check
        if not noSecurity: zobj.mayEdit(self.writePermission, raiseError=True)
        # p_value can be a list of objects
        if type(value) in sutils.sequenceTypes:
            count = 0
            for v in value:
                count += self.linkObject(obj, v, back, noSecurity,
                                         executeMethods, at)
            return count
        # Gets the list of referred objects (=list of uids), or create it.
        refs = getattr(zobj.aq_base, self.name, None)
        if refs is None:
            refs = zobj.getProductConfig().PersistentList()
            setattr(zobj, self.name, refs)
        # Insert p_value into it
        uid = value.o.id
        if uid in refs: return 0
        # Execute p_self.beforeLink if present
        if executeMethods and self.beforeLink:
            r = self.beforeLink(obj, value)
            # Abort object linking if required by p_self.beforeLink
            if r is False: return 0
        # Where must we insert the object ?
        if at and (at.insertId in refs):
            # Insertion logic is overridden by this Position instance, that
            # imposes obj's position within tied objects.
            refs.insert(at.getInsertIndex(refs), uid)
        elif not self.insert or not executeMethods:
            refs.append(uid)
        elif self.insert == 'start':
            refs.insert(0, uid)
        elif callable(self.insert):
            # It is a method. Use it on every tied object until we find where to
            # insert the new object.
            tool = zobj.getTool()
            insertOrder = self.insert(obj, value)
            i = 0
            inserted = False
            while i < len(refs):
                tied = tool.getObject(refs[i], appy=True)
                if self.insert(obj, tied) > insertOrder:
                    refs.insert(i, uid)
                    inserted = True
                    break
                i += 1
            if not inserted: refs.append(uid)
        else:
            # It is a tuple ('sort', method). Perform a full sort.
            refs.append(uid)
            tool = zobj.getTool()
            # Warning: "refs" is a persistent list whose method "sort" has no
            # param "key".
            refs.data.sort(key=lambda uid:self.insert[1](obj, \
                                                tool.getObject(uid, appy=True)))
            refs._p_changed = 1
        # Update the back reference (if existing)
        if not back and self.back:
            # Force "no security" when required
            if not noSecurity and not self.backSecurity:
                noSecurity = True
            self.back.linkObject(value, obj, True, noSecurity, executeMethods)
        # Execute self.afterLink if present
        if executeMethods and self.afterLink: self.afterLink(obj, value)
        return 1

    def unlinkObject(self, obj, value, back=False, noSecurity=True,
                     executeMethods=True):
        '''This method unlinks p_value (which can be a list of objects) from
           p_obj through this Ref field. For an explanation about parameters
           p_back, p_noSecurity and p_executeMethods, check m_linkObject's doc
           above.'''
        zobj = obj.o
        # Security check
        if not noSecurity:
            zobj.mayEdit(self.writePermission, raiseError=True)
            if executeMethods:
                self.mayUnlinkElement(obj, value, raiseError=True)
        # p_value can be a list of objects
        if type(value) in sutils.sequenceTypes:
            for v in value:
                self.unlinkObject(obj, v, back, noSecurity, executeMethods)
            return
        refs = getattr(zobj.aq_base, self.name, None)
        if not refs: return
        # Unlink p_value
        uid = value.o.id
        if uid in refs:
            refs.remove(uid)
            # Update the back reference (if existing)
            if not back and self.back:
                # Force "no security" when required
                if not noSecurity and not self.backSecurity:
                    noSecurity = True
                self.back.unlinkObject(value,obj,True,noSecurity,executeMethods)
            # Execute self.afterUnlink if present
            if executeMethods and self.afterUnlink: self.afterUnlink(obj, value)

    def getStorableValue(self, obj, value, complete=False):
        '''Even if multiplicity is (x,1), the storable value for a Ref (to be
           given to m_store, when p_complete is False) must always be a list.

           If we need to produce a p_complete version, this method returns an
           Appy object or a list of Appy objects.'''
        if not value: return value
        if not complete:
            # Ensure p_value is a list
            if isinstance(value, str): value = [value]
            return value
        else:
            # Produce an Appy object or a list of Appy objects
            tool = obj.getTool()
            if isinstance(value, str):
                return tool.getObject(value, appy=True)
            else:
                if self.multiplicity[1] == 1:
                    return tool.getObject(value[0], appy=True)
                else:
                    return [tool.getObject(v, appy=True) for v in value]

    def store(self, obj, value):
        '''Stores on p_obj, the p_value, which can be:
           * None;
           * an object UID (=string);
           * a list of object UIDs (=list of strings). Generally, UIDs or lists
             of UIDs come from Ref fields with link:True edited through the web;
           * a Zope object;
           * a Appy object;
           * a list of Appy or Zope objects.'''
        if not self.persist: return
        # Standardize p_value into a list of Appy objects
        objects = value
        if not objects: objects = []
        if type(objects) not in sutils.sequenceTypes: objects = [objects]
        tool = obj.getTool()
        for i in range(len(objects)):
            if isinstance(objects[i], basestring):
                # We have an UID here
                objects[i] = tool.getObject(objects[i], appy=True)
            else:
                # Be sure to have an Appy object
                objects[i] = objects[i].appy()
        uids = [o.o.id for o in objects]
        appyObj = obj.appy()
        # Unlink objects that are not referred anymore
        refs = getattr(obj.aq_base, self.name, None)
        if refs:
            i = len(refs)-1
            while i >= 0:
                if refs[i] not in uids:
                    tied = tool.getObject(refs[i], appy=True)
                    if self.back:
                        # Unlink objects (both sides) via the back reference
                        self.back.unlinkObject(tied, appyObj)
                    else:
                        # One-way-unlink the tied object
                        self.unlinkObject(appyObj, tied)
                i -= 1
        # Link new objects
        if objects: self.linkObject(appyObj, objects)

    def repair(self, obj):
        '''Repairs this Ref on p_obj by removing, among tied objects IDs, those
           that do not correspond to any object anymore. This should never
           happen but could, when a folder object is removed from the ZODB
           without removing its contained objects individually (via
           p_onDelete).'''
        ids = getattr(obj.o.aq_base, self.name, None)
        if not ids: return
        tool = obj.tool
        i = len(ids) - 1
        deleted = 0
        while i >= 0:
            try:
                tied = tool.getObject(ids[i])
            except KeyError, ke:
                tied = None
            if not tied:
                del ids[i]
                deleted += 1
            i -= 1
        if deleted:
            tool.log('%s::%s: %d tied ID(s) removed (no object).' % \
                     (obj.id, self.name, deleted), type='warning')

    def mayLink(self, obj):
        '''If p_self defines a link method, this method evaluates it and returns
           its result. Else, the method returns True.'''
        method = self.linkMethod
        if method is None:
            r = True
        else:
            r = self.getAttribute(obj, 'linkMethod')
        return r

    def mayAdd(self, obj, mode='create', checkMayEdit=True):
        '''May the user create (if p_mode == "create") or link
           (if mode == "link") (a) new tied object(s) from p_obj via this Ref ?
           If p_checkMayEdit is False, it means that the condition of being
           allowed to edit this Ref field has already been checked somewhere
           else (it is always required, we just want to avoid checking it
           twice).'''
        # We can't (yet) do that on back references
        if self.isBack: return gutils.No('is_back')
        res = True
        # Check if this Ref is addable/linkable
        if mode == 'create':
            res = self.getAttribute(obj, 'add')
            if not res: return gutils.No('no_add')  
        elif mode == 'link':
            if not self.link or not self.isMultiValued() or \
               not self.mayLink(obj):
                return
        # Have we reached the maximum number of referred elements ?
        if self.multiplicity[1] != None:
            refCount = len(getattr(obj, self.name, ()))
            if refCount >= self.multiplicity[1]: return gutils.No('max_reached')
        # May the user edit this Ref field ?
        if checkMayEdit:
            if not obj.mayEdit(self.writePermission):
                return gutils.No('no_write_perm')
        # May the user create instances of the referred class ?
        if mode == 'create':
            tool = obj.getTool()
            if self.creators and hasattr(tool, 'REQUEST'):
                checkInitiator = True
                initiator = RefInitiator(tool, tool.REQUEST, (obj, self))
            else:
                checkInitiator = False
                initiator = None
            if not tool.userMayCreate(self.klass, checkInitiator, initiator):
                return gutils.No('no_create_perm')
        return res

    def checkAdd(self, obj):
        '''Compute m_mayAdd above, and raise an Unauthorized exception if
           m_mayAdd returns False.'''
        may = self.mayAdd(obj)
        if not may:
            obj.raiseUnauthorized("User can't write Ref field '%s' (%s)." % \
                                  (self.name, may.msg))

    def getOnAdd(self, q, formName, addConfirmMsg, target, hookId,
                 startNumber, create):
        '''Computes the JS code to execute when button "add" is clicked'''
        if create == 'noForm':
            # Ajax-refresh the Ref with a special param to link a newly created
            # object.
            res = "askAjax('%s', null, {'startNumber':'%d', " \
                  "'action':'doCreateWithoutForm'})" % (hookId, startNumber)
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

    def getOnUnlink(self, q, _, obj, tiedId, batch):
        '''Computes the JS code to execute when button "unlink" is clicked'''
        js = "onLink('unlink','%s','%s','%s','%s','%s')" % \
             (obj.id, self.name, tiedId, batch.hook, batch.start)
        if not self.unlinkConfirm: return js
        return "askConfirm('script', %s, %s)" % \
               (q(js, False), q(_('action_confirm')))

    def getAddLabel(self, obj, addLabel, tiedClassLabel, inMenu):
        '''Gets the label of the button allowing to add a new tied object. If
           p_inMenu, the label must contain the name of the class whose instance
           will be created by clincking on the button.'''
        if not inMenu: return obj.translate(self.addLabel)
        return tiedClassLabel

    def getListLabel(self, inPickList):
        '''If self.link == "list", a label must be shown in front of the list.
           Moreover, the label is different if the list is a pick list or the
           list of tied objects.'''
        if self.link != 'list': return
        return inPickList and 'selectable_objects' or 'selected_objects'

    def mayUnlinkElement(self, obj, tied, raiseError=False):
        '''May we unlink from this Ref field this specific p_tied object?'''
        if not self.unlinkElement: return True
        res = self.unlinkElement(obj, tied)
        if res: return True
        else:
            if not raiseError: return
            # Raise an exception.
            obj.o.raiseUnauthorized('field.unlinkElement prevents you to ' \
                                    'unlink this object.')

    def getCbJsInit(self, obj):
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
        default = self.getAttribute(obj, 'checkboxesDefault') and \
                  'unchecked' or 'checked'
        code = "\nnode['_appy_%%s_cbs']={};\nnode['_appy_%%s_sem']='%s';" % \
               default
        poss = (self.link == 'list') and (code % ('poss', 'poss')) or ''
        return "var node=findNode(this, '%s_%s');%s%s" % \
               (obj.id, self.name, code % ('objs', 'objs'), poss)

    def getAjaxData(self, hook, zobj, **params):
        '''Initializes an AjaxData object on the DOM node corresponding to this
           Ref field.'''
        # Complete params with default parameters
        params['ajaxHookId'] = hook;
        params['scope'] = hook.rsplit('_', 1)[-1]
        req = zobj.REQUEST
        selector = req.get('selector')
        if selector: params['selector'] = selector
        params['onav'] = req.get('onav') or ''
        params = sutils.getStringFrom(params)
        return "new AjaxData('%s', '%s:pxView', %s, null, '%s')" % \
               (hook, self.name, params, zobj.absolute_url())

    def getAjaxDataRow(self, obj, parentHook, **params):
        '''Initializes an AjaxData object on the DOM node corresponding to
           p_hook = a row within the list of referred objects.'''
        hook = obj.id
        return "new AjaxData('%s', 'pxViewAsTiedFromAjax', %s, '%s', '%s')" % \
               (hook, sutils.getStringFrom(params), parentHook, obj.url)

    def doChangeOrder(self, obj):
        '''Moves a referred object up/down/top/bottom'''
        rq = obj.REQUEST
        # How to move the item?
        move = rq['move']
        # Get the UID of the tied object to move
        uid = rq['refObjectUid']
        uids = getattr(obj.aq_base, self.name)
        oldIndex = uids.index(uid)
        if move == 'up':
            newIndex = oldIndex - 1
        elif move == 'down':
            newIndex = oldIndex + 1
        elif move == 'top':
            newIndex = 0
        elif move == 'bottom':
            newIndex = len(uids) - 1
        elif move.startswith('index'):
            # New index starts at 1 (oldIndex starts at 0)
            try:
                newIndex = int(move.split('_')[1]) - 1
            except ValueError:
                newIndex = -1
        # If newIndex is negative, it means that the move can't occur
        if newIndex > -1:
            uids.remove(uid)
            uids.insert(newIndex, uid)

    def doCreateWithoutForm(self, obj):
        '''This method is called when a user wants to create a object from a
           reference field, automatically (without displaying a form).'''
        obj.appy().create(self.name)

    xhtmlToText = re.compile('<.*?>', re.S)
    def getReferenceLabel(self, obj, refObject, unlimited=False, dir='ltr',
                          usage=None):
        '''p_self must have link=True. I need to display, on an edit view, the
           p_refObject in the listbox that will allow the user to choose which
           object(s) to link through the Ref. The information to display may
           only be the object title or more if "shownInfo" is used.'''
        res = ''
        # p_obj may not be present, if we are on a search screen
        tool = refObject.tool.o
        className = tool.getPortalType(refObject.klass)
        for col in self.getColSets(obj,tool,className,dir,usage=usage)[0].specs:
            name = col.field.name
            refType = refObject.o.getAppyType(name)
            value = getattr(refObject, name)
            value = refType.getShownValue(refObject.o, value) or '-'
            if refType.type == 'String':
                if refType.format == 2:
                    value = self.xhtmlToText.sub(' ', value)
                elif type(value) in sutils.sequenceTypes:
                    value = ', '.join(value)
            prefix = res and ' | ' or ''
            res += prefix + value
        if unlimited: return res
        maxWidth = self.width or 30
        if len(res) > maxWidth:
            res = tool.truncateValue(res, maxWidth)
        return res

    def getIndexOf(self, obj, tiedUid, raiseError=True):
        '''Gets the position of tied object identified by p_tiedUid within this
           field on p_obj.'''
        uids = getattr(obj.aq_base, self.name, None)
        if not uids:
            if raiseError: raise IndexError()
            else: return
        if tiedUid in uids:
            return uids.index(tiedUid)
        else:
            if raiseError: raise IndexError()
            else: return

    def getPageIndexOf(self, obj, tiedId):
        '''Returns the index of the first object of the page where the tied
           object whose ID is p_tiedId is.'''
        index = self.getIndexOf(obj, tiedId)
        return int(index/self.maxPerPage) * self.maxPerPage

    def sort(self, obj):
        '''Called when the user wants to sort the content of this field.'''
        rq = obj.REQUEST
        sortKey = rq.get('sortKey')
        reverse = rq.get('reverse') == 'True'
        obj.appy().sort(self.name, sortKey=sortKey, reverse=reverse)

    def getRenderMode(self, layoutType):
        '''Gets the render mode, determined by self.render and some
           exceptions.'''
        if (layoutType == 'view') and (self.render == 'menus'): return 'list'
        return self.render

    def getTitleMode(self, selector):
        '''How will we render the tied objects's titles ?'''
        if selector: return 'select'
        if self.links: return 'link'
        return 'text'

    def getPopupLink(self, obj, tiedClassName, popupMode, name):
        '''Gets the link leading to the page to show in the popup for selecting
           objects.'''
        # Transmit the original navigation when existing
        nav = obj.request.get('nav')
        suffix = nav and ('&onav=%s' % nav) or ''
        if self.link == 'popup':
            # Go to the page for querying objects
            res = '%s/query?className=%s&search=%s,%s,%s&popup=1%s' % \
                  (obj.tool.url, tiedClassName, obj.id, name, popupMode, suffix)
        elif self.link == 'popupRef':
            # Go to the page that displays a single field
            popupObj, fieldName = self.select(obj)
            res = '%s/field?name=%s&navStrip=0&popup=1&maxPerPage=%d' \
                  '&selector=%s,%s,%s%s' % (popupObj.url, fieldName,
                  self.maxPerPage, obj.id, name, popupMode, suffix)
        return res

    def getSelector(self, obj, req):
        '''When this Ref field is shown in a popup for selecting objects to be
           included in an "originator" Ref field, this method gets info from the
           request about this originator.'''
        if not req.has_key('selector'): return
        id, name, mode = req['selector'].split(',')
        # The initiator may be under creation
        get = obj.tool.getObject
        initiator = get(id) or get(id, temp=True)
        initiatorField = obj.getField(name)
        return Object(initiator=initiator, initiatorField=initiatorField,
                      initiatorMode=mode, onav=req.get('onav') or '',
                      initiatorHook='%s_%s' % (initiator.id, name))

    def getPopupObjects(self, obj, name, rq, requestValue):
        '''Gets the list of objects that were selected in the popup (for Ref
           fields with link=popup or popupRef).'''
        if requestValue:
            # We are validating the form. Return the request value instead of
            # the popup value.
            tool = obj.tool
            if isinstance(requestValue, basestring):
                return [tool.getObject(requestValue)]
            else:
                return [tool.getObject(rv) for rv in requestValue]
        res = []
        # No object can be selected if the popup has not been opened yet
        if 'semantics' not in rq:
            # In this case, display already linked objects if any
            if not obj.isEmpty(name): return self.getValue(obj.o, name=name)
            return res
        uids = rq['selected'].split(',')
        tool = obj.tool
        if rq['semantics'] == 'checked':
            # Simply get the selected objects from their uid
            return [tool.getObject(uid) for uid in uids]
        else:
            # If link=popup, replay the search in self.select to get the list of
            # uids that were shown in the popup. If link=popupRef, simply get
            # the list of tied object uids for this Ref.
            if self.link == 'popup':
                ztool = tool.o
                className = ztool.getPortalType(self.klass)
                brains = ztool.executeQuery(className, brainsOnly=True,
                  search=self.getSelect(obj), maxResults='NO_LIMIT',
                  sortBy=rq.get('sortKey'), sortOrder=rq.get('sortOrder'),
                  filters=ztool.getFilters(self.klass))
                linkUids = [os.path.basename(b.getPath()) for b in brains]
            elif self.link == 'popupRef':
                initiatorObj, fieldName = self.select(obj)
                linkUids = initiatorObj.ids(fieldName)
            for uid in linkUids:
                if uid not in uids:
                    res.append(tool.getObject(uid))
        return res

    def onSelectFromPopup(self, obj):
        '''This method is called on Ref fields with link=popup[Ref], when
           a user has selected objects from the popup, to be added to existing
           tied objects, from the view widget.'''
        obj = obj.appy()
        for tied in self.getPopupObjects(obj, self.name, obj.request, None):
            self.linkObject(obj, tied, noSecurity=False)

    def renderMinimal(self, obj, objects, inPopup, links=False):
        '''Render tied p_objects in render mode "minimal" (or "links" if p_links
           is True).'''
        if not objects: return obj.translate(self.noObjectLabel)
        r = []
        for tied in objects:
            title = self.getReferenceLabel(obj, tied, True)
            if links and tied.allows('read'):
                # Wrap the title in a link
                target = inPopup and '_parent' or '_self'
                title = '<a href="%s" target="%s">%s</a>' % \
                        (tied.url, target, title)
            r.append(title)
        return self.renderMinimalSep.join(r)

    def getLinkBackUrl(self, obj, req):
        '''Get the URL to redirect the user to after having (un)linked an object
           via this Ref.'''
        url, params = sutils.urlsplit(obj.getReferer())
        # Propagate key of the form "_startNumber"
        for name, value in req.form.iteritems():
            if name.endswith('startNumber'):
                if params is None:
                    params = {name:value}
                else:
                    params[name] = value
        if params:
            r = obj.getUrl(url, **params)
        else:
            r = obj.getUrl(url)
        return r

    def onUiRequest(self, obj, rq):
        '''This method is called when an action tied to this Ref field is
           triggered from the user interface (link, unlink, link_many,
           unlink_many, delete_many).'''
        action = rq['linkAction']
        tool = obj.getTool()
        msg = None
        appyObj = obj.appy()
        if not action.endswith('_many'):
            # "link" or "unlink"
            tied = tool.getObject(rq['targetId'], appy=True)
            exec 'self.%sObject(appyObj, tied, noSecurity=False)' % action
        else:
            # "link_many", "unlink_many", "delete_many". As a preamble, perform
            # a security check once, instead of doing it on every object-level
            # operation.
            obj.mayEdit(self.writePermission, raiseError=True)
            # Get the (un-)checked objects from the request
            uids = rq['targetId'].split(',')
            unchecked = rq['semantics'] == 'unchecked'
            if action == 'link_many':
                # Get possible values (objects)
                values = self.getPossibleValues(obj, removeLinked=True)
                isObj = True
            else:
                # Get current values (uids)
                values = getattr(obj.aq_base, self.name, ())
                isObj = False
            # Collect the objects onto which the action must be performed
            targets = []
            for value in values:
                uid = not isObj and value or value.uid
                if unchecked:
                    # Keep only objects not among uids
                    if uid in uids: continue
                else:
                    # Keep only objects being in uids
                    if uid not in uids: continue
                # Collect this object
                target = not isObj and tool.getObject(value, appy=True) or \
                         value
                targets.append(target)
            if not targets:
                msg = obj.translate('action_null')
            else:
                # Perform the action on every target. Count the number of failed
                # operations.
                failed = 0
                singleAction = action.split('_')[0]
                mustDelete = singleAction == 'delete'
                for target in targets:
                    if mustDelete:
                        # Delete
                        if target.o.mayDelete():
                            target.o.delete(historize=True)
                        else: failed += 1
                    else:
                        # Link or unlink. For unlinking, we need to perform an
                        # additional check.
                        if (singleAction == 'unlink') and \
                           not self.mayUnlinkElement(appyObj, target):
                            failed += 1
                        else:
                            exec 'self.%sObject(appyObj, target)' % singleAction
                if failed:
                    msg = obj.translate('action_partial', mapping={'nb':failed})
        if not msg: msg = obj.translate('action_done')
        appyObj.say(msg)
        tool.goto(self.getLinkBackUrl(obj, rq))

    def getNavInfo(self, obj, nb, total, inPickList=False, inMenu=False):
        '''Gets the navigation info allowing to navigate from tied object number
           p_nb to its siblings.'''
        if self.isBack or inPickList or inMenu: return 'no'
        # If p_nb is None, we want to produce a generic nav info into which we
        # will insert a specific number afterwards.
        if nb is None: return 'ref.%s.%s.%%d.%d' % (obj.id, self.name, total)
        return 'ref.%s.%s.%d.%d' % (obj.id, self.name, nb, total)

    def onGotoTied(self, obj):
        '''Called when the user wants to go to a tied object whose number is in
           the request.'''
        rq = obj.REQUEST
        number = int(rq['number']) - 1
        uids = getattr(obj.aq_base, self.name)
        tiedUid = uids[number]
        tied = obj.getTool().getObject(tiedUid)
        tiedUrl = tied.getUrl(nav=self.getNavInfo(obj, number+1, len(uids)),
                              popup=rq.get('popup', '0'))
        return obj.goto(tiedUrl)

    def getCollapseInfo(self, obj, inPickList):
        '''Returns a Collapsible instance, that determines if the "tied objects"
           or "available objects" zone (depending on p_inPickList) is collapsed
           or expanded.'''
        # Create the ID of the collapsible zone
        suffix = inPickList and 'poss' or 'objs'
        id = '%s_%s_%s' % (obj.klass.__name__, self.name, suffix)
        return gutils.Collapsible(id, obj.request, default='expanded',
                                  display='table')

    def getSupTitle(self, obj, tied, nav):
        '''Returns the custom chunk of info that must be rendered just before
           the p_tied object's title.'''
        return self.supTitle and \
               self.supTitle(obj, tied, nav) or tied.o.getSupTitle(nav)

    def getSubTitle(self, obj, tied):
        '''Returns the custom chunk of info that must be rendered just after
           the p_tied object's title.'''
        return self.subTitle and self.subTitle(obj,tied) or tied.o.getSubTitle()

    def dumpSeparator(self, obj, previous, next, columns):
        '''r_eturns a Separator instance if one must be inserted between
           p_previous and p_next objects.'''
        if not self.separator: return ''
        sep = self.separator(obj, previous, next)
        if not sep: return ''
        css = sep.css and ' class="%s"' % sep.css or ''
        return '<tr><td colspan="%d"><div%s>%s</div></td></tr>' % \
               (len(columns), css, sep.translated or obj.translate(sep.label))

def autoref(klass, field):
    '''klass.field is a Ref to p_klass. This kind of auto-reference can't be
       declared in the "normal" way, like this:

       class A:
           attr1 = Ref(A)

       because at the time Python encounters the static declaration
       "attr1 = Ref(A)", class A is not completely defined yet.

       This method allows to overcome this problem. You can write such
       auto-reference like this:

       class A:
           attr1 = Ref(None)
       autoref(A, A.attr1)

       This function can also be used to avoid circular imports between 2
       classes from 2 different packages. Imagine class P1 in package p1 has a
       Ref to class P2 in package p2; and class P2 has another Ref to p1.P1
       (which is not the back Ref of the previous one: it is another,
       independent Ref).

       In p1, you have

       from p2 import P2
       class P1:
           ref1 = Ref(P2)

       Then, if you write the following in p2, Python will complain because of a
       circular import:

       from p1 import P1
       class P2:
           ref2 = Ref(P1)

       The solution is to write this. In p1:

       from p2 import P2
       class P1:
           ref1 = Ref(P2)
       autoref(P1, P2.ref2)

       And, in p2:
       class P2:
           ref2 = Ref(None)
    '''
    field.klass = klass
    setAttribute(klass, field.back.attribute, field.back)
# ------------------------------------------------------------------------------
