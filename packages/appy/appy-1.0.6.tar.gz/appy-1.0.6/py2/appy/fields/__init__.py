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
# ------------------------------------------------------------------------------
import copy, types, re

from page import Page
from appy.px import Px
from appy import Object
from group import Group
from search import Search
from appy.gen import utils as gutils
from appy.shared import utils as sutils
from appy.gen.layout import Table, Layouts
from translations import FieldTranslations

# In this file, names "list" and "dict" refer to sub-modules. To use Python
# builtin types, use __builtins__['list'] and __builtins__['dict']

# ------------------------------------------------------------------------------
SEARCH_TRIGGER = '%s field %s:%s: executing search %s...'
SEARCH_DONE = 'fetched %d object(s).'

# ------------------------------------------------------------------------------
class Initiator:
    '''From a given field on a given object, it is possible to trigger the
       creation of another object. The most obvious example is the creation of a
       tied object via a Ref field with add=True. An "initiator" represents the
       (object, field) that initiates the object creation.

       In order to customize initiator behaviour, every Field sub-class can
       propose an Initiator sub-class, by overriding its static attribute
       "initiator".'''

    # Most initiators can be used as folders for the created objects
    asFolder = True

    def __init__(self, tool, req, info):
        self.tool = tool
        self.req = req
        # Extract the initiator object and field from p_info, parsed from a
        # "nav" key in the request, or simply already there as a tuple
        # (obj, field).
        if isinstance(info, basestring):
            self.info = info.split('.')
            self.obj = tool.getObject(self.info[0])
            self.field = self.extractField(req)
        else:
            self.obj, self.field = info
            self.info = None
        # After having created the object, if we are back from a popup, the
        # initiator may force to go back to some URL.
        self.backFromPopupUrl = None

    def extractField(self, req):
        '''Tries to get the initiator field from the request'''
        r = self.obj.getField(self.info[1])
        if r is None:
            # This can be an "objectless" initiator. In that case, p_self.obj is
            # the tool and the field's class is specified at another index in
            # p_self.info.
            r = self.obj.o.getAppyType(self.info[1], className=self.info[2])
        return r

    def getUrl(self):
        '''Returns the URL for going back to the initiator object, on the page
           showing self.field.'''
        return self.obj.o.getUrl(page=self.field.pageName, nav='no')

    def checkAllowed(self):
        '''Checks that adding an object via this initiator is allowed'''
        return True

    def updateParameters(self, params):
        '''Add the relevant parameters to the object edition page, related to
           this initiator.'''

    def goBack(self):
        '''Once the object has been created, where must we come back ? r_ can be
           - "view"        return to the "view" page of the created object;
           - "initiator"   return to the page, on self.obj, where self.field is.
        '''
        return 'view'

    def getNavInfo(self, new):
        '''If m_goBack is "view" and navigation-related information must be
           shown on the "view" page of the p_new object, this method returns
           it.'''

    def manage(self, new):
        '''Once the p_new object has been created, the initiator must surely
           perform a given action with it (ie, for a Ref field, the new object
           must be linked to the initiator object. This is the purpose of this
           method.'''

    def isComplete(self):
        '''We may have thought that an initiator was there, but once parsed, the
           "nav" key may reveal that there is no initiator at all. When it is
           the case, this method returns False and the initiator is considered
           to be inexistent.'''
        return True

# ------------------------------------------------------------------------------
class Field:
    '''Basic abstract class for defining any field'''
    Translations = FieldTranslations

    # Some global static variables
    nullValues = (None, '', [], {}, ())
    validatorTypes = (types.FunctionType, types.UnboundMethodType,
                      type(re.compile('')))
    labelTypes = ('label', 'descr', 'help')
    viewLayouts = ('view', 'cell')
    layoutTypes = ('view','edit','result','query','buttons','xml','sidebar')
    explicitLayoutTypes = ('buttons', 'sidebar')

    # Those attributes can be overridden by subclasses for defining,
    # respectively, names of CSS and Javascript files that are required by this
    # field, keyed by layoutType.
    cssFiles = {}
    jsFiles = {}

    # Some predefined layouts
    bLayouts = Table('lrv-f', width=None)
    dLayouts = 'lrv-d-f'
    # The *d*escription is visible, even on the *v*iew layout
    dvLayouts = {'edit': dLayouts, 'view': 'l-d-f'}
    hLayouts = 'lhrv-f'
    wLayouts = Table('lrv-f')
    # The following layouts are for fields within groups with style="grid"
    gLayouts = {'edit': 'frvl', 'search': 'l-f'}
    gdLayouts = {'edit': Table('frvl-d', width='99%'), 'search': 'l-f'}
    ghLayouts = {'edit': 'fhrvl', 'search': 'l-f'}
    gdhLayouts = {'edit': 'fhrvl-d', 'search': 'l-f'}
    # Unique, static cell layout
    cellLayout = Layouts.cell

    # For most fields, getting its value on some object is automatically done at
    # the framework level. Fields for which this must be disabled override the
    # following static attribute.
    customGetValue = False
    # Some fields are "outer": they are composed or inner fields
    outer = False
    # Parameters needed to re-trigger a search. Some fields applying on sets of
    # objects may need to re-trigger a search from these request parameters.
    searchParams = ('className', 'search', 'sortKey', 'sortOrder', 'filters')

    # The initiator class related to the Field
    initiator = Initiator

    # Render a field. Optional vars:
    # * fieldName   can be given as different as field.name for fields included
    #               in List fields: in this case, fieldName includes the row
    #               index.
    # * showChanges If True, a variant of the field showing successive changes
    #               made to it is shown.
    # * minimal     If True, the PX related to p_layoutType is directly called
    #               (pxView, pxCell, etc), instead of layout.pxRender. While
    #               this disables some functions like master/slave
    #               relationships, it returns a more lightweight code.
    pxRender = Px('''<x var="minimal=minimal|False;
      showChanges=showChanges|req.get('showChanges') == 'True';
      layoutType=layoutType|req.get('layoutType');
      isSearch=layoutType == 'search';
      hostLayout=req.get('hostLayout');
      name=fieldName or field.name|field.name;
      widgetName=isSearch and ('w_%s' % name) or name;
      rawValue=field.getValueIf(zobj, name, layoutType, disable=isSearch);
      value=not isSearch and \
            field.getFormattedValue(zobj,rawValue,layoutType,showChanges);
      requestValue=not isSearch and field.getStoredValue(zobj,name,True);
      inRequest=field.valueIsInRequest(zobj, req, name, layoutType);
      error=req.get('%s_error' % name) or req.validator.errors.get(name)|None;
      isMultiple=field.isMultiValued();
      masterCss=field.slaves and ('master_%s' % name) or '';
      tagCss=tagCss|None;
      tagCss=field.getTagCss(tagCss, layoutType);
      zobj=zobj or ztool;
      tagId='%s_%s' % (zobj.id, name);
      tagName=field.master and 'slave' or '';
      layoutTarget=field">:field.getPx(minimal, \
                                       hostLayout or layoutType, _ctx_)</x>''')

    def doRender(self, layoutType, obj, name=None, minimal=False, tagCss=None,
                 specific=None):
        '''Allows to call pxRender from code, to display the content of this
           field on p_obj in some specific context, for example in a Computed
           field.'''
        context = {'layoutType': layoutType, 'field': self, 'minimal': minimal,
                   'name': name or self.name, 'obj': obj, 'zobj': obj.o}
        if tagCss: context['tagCss'] = tagCss
        if specific: context.update(specific)
        # Get the current PX context: we will need to copy some entries from it.
        # If no such context exists, create one.
        req = obj.request
        if hasattr(req, 'pxContext'):
            ctx = req.pxContext
            Px.copyBaseVariables(context, ctx)
        else:
            ctx = Px.setBaseVariables(obj.tool, context, obj)
        # Call pxRender
        return self.pxRender(context).encode('utf-8')

    # Show the field content for some object on a list of referred objects
    pxRenderAsTied = Px('''
     <!-- The "title" field -->
     <x if="refField.name == 'title'">
      <x if="mayView">
       <x if="not field.menuUrlMethod or \
              (layoutType!='cell')">:field.pxObjectTitle</x>
       <x if="field.menuUrlMethod and (layoutType=='cell')"
          var2="info=field.getMenuUrl(zobj, \
           tied)">::tied.o.getListTitle(target=info[1], baseUrl=info[0])</x>
       <x if="not selector and tied.o.mayAct()">:field.pxObjectActions</x>
      </x>
      <div if="not mayView">
       <img src=":url('fake')" style="margin-right: 5px"/>
       <x>:_('unauthorized')</x></div>
     </x>
     <!-- Any other field -->
     <x if="(refField.name != 'title') and mayView">
      <x var="zobj=tied.o; obj=tied; layoutType='cell'; field=refField;
              fieldName=refField.name; minimal=not refField.inlineEdit"
         if="field.isShowable(zobj,'result')">:field.pxRender</x>
     </x>''')

    # Show the field content for some object on a list of results
    pxRenderAsResult = Px('''
     <!-- Title -->
     <x if="field.name=='title'"
        var2="navInfo=mode.getNavInfo(currentNumber); target=mode.target;
              backHook=backHook|None">
      <x if="mayView"
         var2="pageName=zobj.getDefaultViewPage();
               selectJs=inPopup and \
                        uiSearch.initiator.jsSelectOne(q, cbId) or ''">
       <x var="sup=zobj.getSupTitle(navInfo)" if="sup">::sup</x>
       <x>::zobj.getListTitle(mode=mode.titleMode, nav=navInfo, target=target, \
          page=pageName, inPopup=inPopup, selectJs=selectJs, highlight=True, \
          backHook=backHook)</x>
       <span style=":mode.showSubTitles and 'display:inline' or 'display:none'"
             name="subTitle" var="sub=zobj.getSubTitle()"
             class=":zobj.getCssFor('subTitle')"
             if="sub">::zobj.highlight(sub)</span>

       <!-- Actions -->
       <div if="not inPopup and uiSearch.showActions and zobj.mayAct()"
            class="objectActions" style=":'display:%s'% uiSearch.actionsDisplay"
            var2="layoutType='buttons';
                  editable=zobj.mayEdit();
                  locked=zobj.isLocked(user, 'main')">
        <!-- Edit -->
        <x if="editable">
         <a if="not locked"
            var2="linkInPopup=inPopup or (target.target != '_self')"
            target=":target.target"
            onclick=":target.getOnClick(backHook or zobj.id)"
            href=":zobj.getUrl(mode='edit', page=zobj.getDefaultEditPage(), \
                               nav=navInfo, inPopup=linkInPopup)">
          <img src=":url('edit')" title=":_('object_edit')"/>
         </a>
         <x if="locked" var2="lockStyle=''; page='main'">::obj.pxLock</x>
        </x>
        <!-- Delete -->
        <img if="not locked and zobj.mayDelete()" class="clickable"
             src=":url('delete')" title=":_('object_delete')"
             onClick=":'onDeleteObject(%s)' % q(zobj.id)"/>
        <!-- Fields (actions) defined with layout "buttons" -->
        <x if="not inPopup and (uiSearch.showActions == 'all')"
           var2="fields=zobj.getAppyTypes('buttons', 'main');
                 layoutType='cell'">
         <!-- Call pxCell and not pxRender to avoid having a table -->
         <x for="field in fields"
            var2="name=field.name; smallButtons=True">:field.pxCell</x>
        </x>
        <!-- Workflow transitions -->
        <x if="zobj.showTransitions('result')"
           var2="targetObj=zobj">:targetObj.appy().pxTransitions</x>
       </div>
      </x>
      <x if="not mayView">
       <img src=":url('fake')" style="margin-right: 5px"/>
       <x>:_('unauthorized')</x>
      </x>
     </x>
     <!-- Any other field -->
     <x if="(field.name != 'title') and mayView" var2="layoutType='cell'">
      <x if="field.isShowable(zobj, 'result')"
         var2="fieldName=field.name;
               minimal=not field.inlineEdit">:field.pxRender</x>
     </x>''')

    # Displays a field label
    pxLabel = Px('''<label if="field.hasLabel and field.renderLabel(layoutType)"
     lfor=":field.name">::_('label', field=field)</label>''')

    # Displays a field description
    pxDescription = Px('''<span if="field.hasDescr"
     class="discreet">::_('descr', field=field)</span>''')

    # Displays a field help
    pxHelp = Px('''<abbr title=":_('help', field=field)"><img
     src=":url('help')"/></abbr>''')

    # Displays validation-error-related info about a field
    pxValidation = Px('''<x><abbr if="error" title=":error"><img
     src=":url('warning')"/></abbr><img if="not error"
     src=":url('warning_no.gif')"/></x>''')

    # Displays the fact that a field is required
    pxRequired = Px('''<img src=":url('required.gif')"/>''')

    # Button for showing changes to the field
    pxChanges = Px('''
     <div if="zobj.hasHistory(name)" style="margin-bottom: 5px">
      <!-- Button for showing the field version containing changes -->
      <input if="not showChanges"
             var2="label=_('changes_show');
                   css=ztool.getButtonCss(label)" type="button" class=":css"
             value=":label" style=":url('changes', bg=True)"
             onclick=":'askField(%s,%s,%s,null,%s)' % \
                       (q(tagId), q(obj.url), q('view'), q('True'))"/>
      <!-- Button for showing the field version without changes -->
      <input if="showChanges"
             var2="label=_('changes_hide');
                  css=ztool.getButtonCss(label)" type="button" class=":css"
             value=":label" style=":url('changesNo', bg=True)"
             onclick=":'askField(%s,%s,%s,null,%s)' % \
                       (q(tagId), q(obj.url), q('view'), q('False'))"/>
     </div>''')

    # Widget for filtering object values on query results
    pxFilterText = Px('''
     <x var="name=field.name;
             filterId='%s_%s' % (mode.ajaxHookId, name);
             filterIdIcon='%s_icon' % filterId">
      <!-- Pressing the "enter" key in the field clicks the icon (onkeydown) -->
      <input type="text" size="7" id=":filterId"
             value=":mode.filters.get(name, '')"
             onkeydown=":'if (event.keyCode==13) document.getElementById ' \
                         '(%s).click()' % q(filterIdIcon)"/>
      <img id=":filterIdIcon" class="clickable" src=":url('funnel')"
           onclick=":'askBunchFiltered(%s,%s)' % (q(mode.ajaxHookId),q(name))"/>
     </x>''')

    def __init__(self, validator, multiplicity, default, defaultOnEdit, show,
      page, group, layouts, move, indexed, mustIndex, indexValue, searchable,
      specificReadPermission, specificWritePermission, width, height, maxChars,
      colspan, master, masterValue, focus, historized, mapping, generateLabel,
      label, sdefault, scolspan, swidth, sheight, persist, inlineEdit, view,
      cell, edit, xml, translations):
        # The validator restricts which values may be defined. It can be an
        # interval (1,None), a list of string values ['choice1', 'choice2'],
        # a regular expression, a custom function, a Selection instance, etc.
        self.validator = validator
        # Multiplicity is a 2-tuple indicating the minimum and maximum
        # occurrences of values.
        self.multiplicity = multiplicity
        # Is the field required or not ? (derived from multiplicity)
        self.required = self.multiplicity[0] > 0
        # Default value
        self.default = default
        # Default value on layout "edit". If None, self.default is used instead.
        self.defaultOnEdit = defaultOnEdit
        # Must the field be visible or not ?
        self.show = show
        # When displaying/editing the whole object, on what page and phase must
        # this field value appear?
        self.page = Page.get(page)
        self.pageName = self.page.name
        # Within self.page, in what group of fields must this one appear?
        self.group = Group.get(group)
        # The following attribute allows to move a field back to a previous
        # position (useful for moving fields above predefined ones).
        self.move = move
        # If indexed is True, a database index will be set on the field for
        # fast access.
        self.indexed = indexed
        # If "mustIndex", True by default, is specified, it must be a method
        # returning a boolean value. Indexation will only occur when this value
        # is True.
        self.mustIndex = mustIndex
        if not mustIndex and not callable(mustIndex):
            raise Exception('Value for param "mustIndex" must be a method.')
        # For an indexed field, the value stored in the index is deduced from
        # the field value and from the index type. If, for some reason, you want
        # to store another value, specify in parameter "indexValue" a method,
        # accepting the stored value as single arg, that can return an
        # alternative/transformed value to index.
        self.indexValue = indexValue
        # If specified "searchable", the field will be added to some global
        # index allowing to perform application-wide, keyword searches.
        self.searchable = searchable
        # Normally, permissions to read or write every attribute in a type are
        # granted if the user has the global permission to read or
        # edit instances of the whole type. If you want a given attribute
        # to be protected by specific permissions, set one or the 2 next boolean
        # values to "True". In this case, you will create a new "field-only"
        # read and/or write permission. If you need to protect several fields
        # with the same read/write permission, you can avoid defining one
        # specific permission for every field by specifying a "named"
        # permission (string) instead of assigning "True" to the following
        # arg(s). A named permission will be global to your application, so
        # take care to the naming convention. Typically, a named permission is
        # of the form: "<yourAppName>: Write|Read ---". If, for example, I want
        # to define, for my application "MedicalFolder" a specific permission
        # for a bunch of fields that can only be modified by a doctor, I can
        # define a permission "MedicalFolder: Write medical information" and
        # assign it to the "specificWritePermission" of every impacted field.
        self.specificReadPermission = specificReadPermission
        self.specificWritePermission = specificWritePermission
        # Widget width and height
        self.width = width
        self.height = height
        # While width and height refer to widget dimensions, maxChars hereafter
        # represents the maximum number of chars that a given input field may
        # accept (corresponds to HTML "maxlength" property). "None" means
        # "unlimited".
        self.maxChars = maxChars or ''
        # If the widget is in a group with multiple columns, the following
        # attribute specifies on how many columns to span the widget.
        self.colspan = colspan or 1
        # The list of slaves of this field, if it is a master
        self.slaves = []
        # The behaviour of this field may depend on another, "master" field
        self.setMaster(master, masterValue)
        # If a field must retain attention in a particular way, set focus=True.
        # It will be rendered in a special way.
        self.focus = focus
        # If we must keep track of changes performed on a field, "historized"
        # must be set to True.
        self.historized = historized
        # Mapping is a dict of contexts that, if specified, are given when
        # translating the label, descr or help related to this field.
        self.mapping = self.formatMapping(mapping)
        self.id = id(self)
        self.type = self.__class__.__name__
        self.pythonType = None # The True corresponding Python type
        # Get the layouts. Consult layout.py for more info about layouts.
        self.layouts = self.formatLayouts(layouts)
        # Can this field have values that can be edited and validated?
        self.validable = True
        # By default, if the base label for a field is in use in at least one of
        # its layouts (in p_self.layouts), it will be generated automatically in
        # your app's .pot and .po files. That being said, if the base label is
        # not used in any layout, but you still want it to be generated, for
        # using it in some other, non standard place like a pod or a custom
        # report, set the following attribute to True.
        self.generateLabel = generateLabel
        # If you want to avoid generating translation labels for this field, and
        # use instead translations already defined on another field, use the
        # following attribute "label". A label is made of 2 parts: the prefix,
        # based on class name, and the name, which is the field name by default.
        # ----------------------------------------------------------------------
        # If "label" is... | it will be understood as...
        # ----------------------------------------------------------------------
        # a string         | a new prefix = a new class name. Your field will
        #                  | use the label of an homonym field on another class.
        # ----------------------------------------------------------------------
        # a tuple          | a tuple (prefix, name), defining both a new prefix
        #                  | and a new field name. Your field will get the label
        #                  | of a field from another class, having another name.
        #                  | And if you want to reuse labels of another field
        #                  | defined on the same class, use a tuple of the form
        #                  |                 (None, name)
        # ----------------------------------------------------------------------
        self.label = label
        # When you specify a default value "for search" (= "sdefault"), on a
        # search screen, in the search field corresponding to this field, this
        # default value will be present.
        self.sdefault = sdefault
        # Colspan for rendering the search widget corresponding to this field.
        self.scolspan = scolspan or 1
        # Width and height for the search widget
        self.swidth = swidth or width
        self.sheight = sheight or height
        # "persist" indicates if field content must be stored in the database.
        # For some fields it is not wanted (ie, fields used only as masters to
        # update slave's selectable values). If you place a method in attribute
        # "persist", similarly, field value will not be stored, but your method
        # will receive it and you will do whatever you want with it.
        self.persist = persist
        # Can the field be inline-edited (on "view" or "cell" layouts)? A method
        # can be specified. If "inlineEdit" is or returns True, a click within
        # the field value as shown on the "view" or "cell" layout will switch
        # the widget to "edit" mode. If it returns 'icon', Switching to "edit"
        # will be done via an "edit" icon.
        self.inlineEdit = inlineEdit
        # If you want to use alternate PXs than Field.pxView, Field.pxCell and
        # Field.pxEdit, you can specify it in parameters "view", "cell" and
        # "edit". Instance attributes "pxView", "pxCell" and "pxEdit" below will
        # override their corresponding class attributes.
        if view is not None: self.pxView = view
        if cell is not None: self.pxCell = cell
        if edit is not None: self.pxEdit = edit
        # Standard marshallers are provided for converting values of this field
        # into XML. If you want to customize the marshalling process, you can
        # define a method in "xml" that will accept a field value and will
        # return a possibly different value. Be careful: do not return a chunk
        # of XML here! Simply return an alternate value, that will be
        # XML-marshalled.
        self.xml = xml
        # The PX for filtering field values. If None, it means that the field is
        # not filterable.
        self.filterPx = None
        # The standard system for getting field translations (label,
        # description, etc) is based on translations stored in persistent
        # Translation instances in tool.translations. But one may bypass this
        # system by placing an instance of class
        #            appy.fields.translations.FieldTranslations
        # in this attribute.
        self.translations = translations

    def init(self, name, klass, appName):
        '''When the application server starts, this secondary constructor is
           called for storing the name of the Appy field (p_name) and other
           attributes that are based on the name of the Appy p_klass, and the
           application name (p_appName).'''
        if hasattr(self, 'name'): return # Already initialized
        self.name = name
        # Determine prefix for this class
        if not klass: prefix = appName
        else:         prefix = gutils.getClassName(klass, appName)
        # Recompute the ID (and derived attributes) that may have changed if
        # we are in debug mode (because we recreate new Field instances).
        self.id = id(self)
        # Remember master name on every slave
        for slave in self.slaves: slave.masterName = name
        # Determine ids of i18n labels for this field, excepted if translations
        # are already present in self.tranlations.
        if not self.translations:
            labelName = name
            trPrefix = None
            if self.label:
                if isinstance(self.label, basestring): trPrefix = self.label
                else: # It is a tuple (trPrefix, name)
                    if self.label[1]: labelName = self.label[1]
                    if self.label[0]: trPrefix = self.label[0]
            if not trPrefix:
                trPrefix = prefix
            # Determine name to use for i18n
            self.labelId = '%s_%s' % (trPrefix, labelName)
            self.descrId = self.labelId + '_descr'
            self.helpId  = self.labelId + '_help'
        # Determine read and write permissions for this field
        rp = self.specificReadPermission
        if rp and not isinstance(rp, basestring):
            self.readPermission = '%s: Read %s %s' % (appName, prefix, name)
        elif rp and isinstance(rp, basestring):
            self.readPermission = rp
        else:
            self.readPermission = 'read'
        wp = self.specificWritePermission
        if wp and not isinstance(wp, basestring):
            self.writePermission = '%s: Write %s %s' % (appName, prefix, name)
        elif wp and isinstance(wp, basestring):
            self.writePermission = wp
        else:
            self.writePermission = 'write'
        if (self.type == 'Ref') and not self.isBack and self.back:
            # We must initialise the corresponding back reference
            self.back.klass = klass
            self.back.init(self.back.attribute, self.klass, appName)
        if self.type in ('List', 'Dict'):
            for subName, subField in self.fields:
                fullName = '%s_%s' % (name, subName)
                subField.init(fullName, klass, appName)
                subField.name = '%s*%s' % (name, subName)
        elif self.type == 'Switch':
            for case, fields in self.fields:
                for name, field in fields:
                    field.init(name, klass, appName)

    def __repr__(self):
        name = hasattr(self, 'name') and (':%s' % self.name) or ''
        return '<Field %s%s>' % (self.__class__.__name__, name)

    def reload(self, klass, obj):
        '''In debug mode, we want to reload layouts without restarting Zope.
           So this method will prepare a "new", reloaded version of p_self,
           that corresponds to p_self after a "reload" of its containing Python
           module has been performed.'''
        res = getattr(klass, self.name, None)
        if not res: return self
        if (self.type == 'Ref') and self.isBack: return self
        res.init(self.name, klass, obj.getProductConfig().PROJECTNAME)
        return res

    def isMultiValued(self):
        '''Does this type definition allow to define multiple values?'''
        maxOccurs = self.multiplicity[1]
        return (maxOccurs is None) or (maxOccurs > 1)

    def isSortable(self, usage):
        '''Can fields of this type be used for sorting purposes, when sorting
           search results (p_usage="search") or when sorting reference fields
           (p_usage="ref")?'''
        if usage == 'search':
            indexed = self.indexed
            return indexed and (indexed != 'TextIndex') and \
                   not self.isMultiValued()
        # For usage being "ref", this method will be overridden by fields for
        # which sort is allowed.

    def isShowable(self, obj, layoutType):
        '''When displaying p_obj on a given p_layoutType, must we show this
           field?'''
        # Check if the user has the permission to view or edit the field
        perm = (layoutType == 'edit') and self.writePermission or \
                                          self.readPermission
        if not obj.allows(perm): return
        # Evaluate self.show
        if callable(self.show):
            res = self.callMethod(obj, self.show)
        else:
            res = self.show
        # Take into account possible values 'view', 'edit', 'result'...
        if type(res) in sutils.sequenceTypes:
            for r in res:
                if r == layoutType: return True
            return
        elif res in self.layoutTypes:
            return res == layoutType
        # For showing a field on some layouts, they must be explicitly be
        # returned by the show method.
        if layoutType not in self.explicitLayoutTypes:
            return bool(res)

    def isRenderable(self, layoutType):
        '''In some contexts, computing m_isShowable can be a performance
           problem. For example, when showing fields of some object on layout
           "buttons", there are plenty of fields that simply can't be shown on
           this kind of layout: it is no worth computing m_isShowable for those
           fields. m_isRenderable is meant to define light conditions to
           determine, before calling m_isShowable, if some field has a chance to
           be shown or not.

           In other words, m_isRenderable defines a "structural" condition,
           independent of any object, while m_isShowable defines a contextual
           condition, depending on some object.'''
        # Most fields are not renderable on layout "buttons"
        if layoutType == 'buttons': return
        return True

    def isClientVisible(self, obj):
        '''This method returns True if this field is visible according to
           master/slave relationships.'''
        masterData = self.getMasterData()
        if not masterData: return True
        else:
            master, masterValue = masterData
            if masterValue and callable(masterValue): return True
            # Get the master value from the request
            rq = obj.REQUEST
            if not rq.has_key(master.name) and rq.has_key(self.name):
                # The master is not there: we cannot say if the slave must
                # be visible or not. But the slave is in the request. So we
                # should not prevent this value from being taken into account.
                return True
            reqValue = master.getRequestValue(obj)
            # reqValue can be a list or not
            if type(reqValue) not in sutils.sequenceTypes:
                return reqValue in masterValue
            else:
                for m in masterValue:
                    for r in reqValue:
                        if m == r: return True

    def inGrid(self, layout='edit'):
        '''Is this field in a group with style "grid" on p_layout?'''
        if not self.group: return
        if isinstance(self.group, __builtins__['dict']):
            for lay, group in self.group.iteritems():
                if lay != layout: continue
                return group and (group.style == 'grid')
            return
        return self.group.style == 'grid'

    def formatMapping(self, mapping):
        '''Creates a dict of mappings, one entry by label type (label, descr,
           help).'''
        if isinstance(mapping, __builtins__['dict']):
            # Is it a dict like {'label':..., 'descr':...}, or is it directly a
            # dict with a mapping?
            for k, v in mapping.iteritems():
                if (k not in self.labelTypes) or isinstance(v, basestring):
                    # It is already a mapping
                    return {'label':mapping, 'descr':mapping, 'help':mapping}
            # If we are here, we have {'label':..., 'descr':...}. Complete
            # it if necessary.
            for labelType in self.labelTypes:
                if labelType not in mapping:
                    mapping[labelType] = None # No mapping for this value
            return mapping
        else:
            # Mapping is a method that must be applied to any i18n message
            return {'label':mapping, 'descr':mapping, 'help':mapping}

    def formatLayouts(self, layouts):
        '''Standardizes the given p_layouts'''
        # First, get the layouts as a dictionary, if p_layouts is None or
        # expressed as a simple string.
        areDefault = False
        if not layouts: # Get the default ones as defined by the subclass
            layouts = self.computeDefaultLayouts()
            areDefault = True
        if isinstance(layouts, basestring):
            # This is a single layoutString, the "edit" one
            layouts = {'edit': layouts}
        elif isinstance(layouts, Table):
            # Idem, but with a Table instance
            layouts = {'edit': Table(other=layouts)}
        else:
            # Make a copy of the layouts, because every layout can be different,
            # even if the user decides to reuse one from one field to another.
            # This is because we modify every layout for adding
            # master/slave-related info, focus-related info, etc, which can be
            # different from one field to the other.
            layouts = copy.deepcopy(layouts)
            if 'edit' not in layouts:
                default = self.computeDefaultLayouts()
                if isinstance(default, __builtins__['dict']):
                    default = default['edit']
                layouts['edit'] = default
        # We have now a dict of layouts in p_layouts. Ensure now that a Table
        # instance is created for every layout (=value from the dict). Indeed,
        # a layout could have been expressed as a simple layout string.
        for layoutType in layouts.iterkeys():
            if isinstance(layouts[layoutType], basestring):
                layouts[layoutType] = Table(layouts[layoutType])
        # Derive "view" & "search" layouts from the "edit" layout when relevant
        if 'view' not in layouts:
            layouts['view'] = Table(other=layouts['edit'], derivedType='view')
        if 'search' not in layouts:
            layouts['search'] = Table(other=layouts['view'],
                                      derivedType='search')
        if self.focus:
            # We need to make it flashy
            layouts['view'].addCssClasses('focus')
            layouts['edit'].addCssClasses('focus')
        # If layouts are the default ones, set width=None instead of width=100%
        # for the field if it is not in a group (excepted for rich texts, refs
        # and calendars).
        if areDefault and not self.group and \
           not ((self.type == 'String') and (self.format == self.XHTML)) and \
           (self.type not in ('Ref', 'Calendar')):
            for layoutType in layouts.iterkeys():
                layouts[layoutType].width = ''
        # Remove letters "r" from the layouts if the field is not required
        if not self.required:
            for layoutType in layouts.iterkeys():
                layouts[layoutType].removeElement('r')
        # Derive some boolean values from the layouts
        self.hasLabel = self.hasLayoutElement('l', layouts)
        self.hasDescr = self.hasLayoutElement('d', layouts)
        self.hasHelp  = self.hasLayoutElement('h', layouts)
        return layouts

    def getPx(self, minimal, layoutType, context):
        '''Returns the PX corresponding to p_layoutType'''
        if minimal:
            # Call directly the layout-related PX on the field (bypass the
            # layout PX)
            r = getattr(self, 'px%s' % layoutType.capitalize())
        else:
            # Get the layout related to p_layoutType and render its PX
            if layoutType == 'cell':
                layout = self.cellLayout
            else:
                layout = self.layouts[layoutType]
            # Add the layout in the context, it is required by its PX
            context['layout'] = layout
            r = layout.pxRender
        return r

    def setMandatoriness(self, required):
        '''Updating mandatoriness for a field is not easy, this is why this
           method exists.'''
        # Update attributes "required" and "multiplicity"
        self.required = required
        if not required:
            minMult = 0
        else:
            minMult = 1
        self.multiplicity = (minMult, self.multiplicity[1])
        # Update the "edit" layout. We will not update editLayout.layoutString,
        # too tricky.
        editLayout = self.layouts['edit']
        if not required:
            # Remove pxRequired
            for row in editLayout.rows:
                for cell in row.cells:
                    for elem in cell.content:
                        if elem == 'pxRequired':
                            cell.content.remove(elem)
                            return
        else:
            # Add pxRequired
            content = editLayout.rows[0].cells[0].content
            content.insert(1, 'pxRequired')

    def setMaster(self, master, masterValue):
        '''Initialises the master and the master value if any'''
        self.master = master
        if master: self.master.slaves.append(self)
        # The semantics of attribute "masterValue" below is as follows:
        # - if "masterValue" is anything but a method, the field will be shown
        #   only when the master has this value, or one of it if multivalued;
        # - if "masterValue" is a method, the value(s) of the slave field will
        #   be returned by this method, depending on the master value(s) that
        #   are given to it, as its unique parameter.
        self.masterValue = gutils.initMasterValue(masterValue)

    def hasLayoutElement(self, element, layouts):
        '''This method returns True if the given layout p_element can be found
           at least once among the various p_layouts defined for this field.'''
        for layout in layouts.itervalues():
            if element in layout.layoutString: return True
        return False

    def getDefaultLayouts(self):
        '''Any subclass can define this for getting a specific set of default
           layouts. If None is returned, a global set of default layouts will be
           used.'''

    def getInputLayouts(self):
        '''Gets, as a string, the layouts as could have been specified as input
           value for the Field constructor.'''
        res = '{'
        for k, v in self.layouts.iteritems():
            res += '"%s":"%s",' % (k, v.layoutString)
        res += '}'
        return res

    def computeDefaultLayouts(self):
        '''This method gets the default layouts from a Field or the global
           default field layouts when they are not available.'''
        return self.getDefaultLayouts() or Layouts.defaults(self)

    def getCss(self, layoutType, res, config):
        '''This method completes the list p_res with the names of CSS files
           that are required for displaying widgets of self's type on a given
           p_layoutType. p_res is not a set because order of inclusion of CSS
           files may be important and may be loosed by using sets.'''
        if layoutType in self.cssFiles:
            for fileName in self.cssFiles[layoutType]:
                if fileName not in res:
                    res.append(fileName)

    def getJs(self, layoutType, res, config):
        '''This method completes the list p_res with the names of Javascript
           files that are required for displaying widgets of self's type on a
           given p_layoutType. p_res is not a set because order of inclusion of
           CSS files may be important and may be loosed by using sets.'''
        if layoutType in self.jsFiles:
            for fileName in self.jsFiles[layoutType]:
                if fileName not in res:
                    res.append(fileName)

    def isInner(self):
        '''Returns True if p_self is an inner field within a container field'''
        return '*' in self.name

    def getStoredValue(self, obj, name=None, fromRequest=False):
        '''Gets the value in its form as stored in the database, or in the
           request if p_fromRequest is True. It differs from calling
           m_getRequestValue because here, in the case of an inner field, the
           request value is searched within the outer value build and stored on
           the request.'''
        if self.isInner():
            # p_self is a sub-field into a List/Dict: p_name is of the form
            #            [outerName]*[name]*[rowId]
            outerName, name, rowId = name.split('*')
            if rowId == '-1': res = None # It is a template row
            else:
                # Get the outer value
                if fromRequest: res = obj.REQUEST.get(outerName, None)
                else:           res = getattr(obj.aq_base, outerName, None)
                # Access the inner value
                if res:
                    if rowId.isdigit():
                        rowId = int(rowId)
                        if rowId < len(res):
                            res = getattr(res[rowId], name, None)
                        else:
                            res = None
                    else:
                        res = res.get(rowId, None)
                        if res: res = res.get(name, None)
            # Return an empty string if fromRequest is True
            if fromRequest and (res is None): res = ''
        else:
            if fromRequest: res = self.getRequestValue(obj, self.name)
            else:           res = getattr(obj.aq_base, self.name, None)
        return res

    def getRequestValue(self, obj, requestName=None):
        '''Gets a value for this field as carried in the request object. In the
           simplest cases, the request value is a single value whose name in the
           request is the name of the field.

           Sometimes, several request values must be combined (ie: see the
           overriden method in the Date class).

           Sometimes (ie, a field within a List/Dict), the name of the request
           value(s) representing the field value does not correspond to the
           field name (ie: the request name includes information about
           the container field). In this case, p_requestName must be used for
           searching into the request, instead of the field name (self.name).'''
        name = requestName or self.name
        return obj.REQUEST.get(name, None)

    def setRequestValue(self, obj):
        '''Sets, in the request, field value on p_obj in its "request" form
           (=the way the value is carried in the request).'''
        # Get a copy of the field value on p_obj and put it in the request
        value = self.getCopyValue(obj)
        if value is not None:
            obj.REQUEST[self.name] = value

    def getRequestSuffix(self):
        '''In most cases, in the user interface, there is one homonym HTML
           element for representing this field. Sometimes, several HTML elements
           are used to represent one field (ie, for dates: one field for the
           year, one for the month, etc). In this case, every HTML element's
           name has the form <field name><suffix>. This method returns the
           suffix of the "main" HTML element.'''
        return ''

    def getValue(self, obj, name=None, layout=None):
        '''Gets, on_obj, the value for this field (p_self)'''
        # Possible values for parameters are described hereafter.
        # ----------------------------------------------------------------------
        # name    | p_name can be different from self.name if p_self is a
        #         | sub-field into a List: in this case, it includes the row
        #         | number.
        # ----------------------------------------------------------------------
        # layout  | In most cases, we don't care about the layout for getting
        #         | the value of p_self on p_obj. One exception is that a
        #         | default value can be defined specifically on layout "edit".
        #         | In that case, p_layout must be available in order to
        #         | determine the possible specific default value for this
        #         | layout.
        # ----------------------------------------------------------------------
        # Get the value from the database
        value = self.getStoredValue(obj, name)
        if self.isEmptyValue(obj, value):
            # If there is no value, get the default value if any. Determine
            # which one must be used: p_self.default or p_self.defaultOnEdit.
            if layout == 'edit':
                default = self.defaultOnEdit
                if default is None: default = self.default
            else:
                default = self.default
            # Get the default value, which can be a method
            if callable(default):
                try:
                    # Caching a default value can lead to problems. For example,
                    # the process of creating an object from another one, or
                    # from some data, sometimes consists in (a) creating an
                    # "empty" object, (b) initializing its values and
                    # (c) reindexing it. Default values are computed in (a),
                    # but it they depend on values set at (b), and are cached
                    # and indexed, (c) will get the wrong, cached value.
                    default = self.callMethod(obj, default, cache=False)
                except Exception:
                    # Already logged. Here I do not raise the exception,
                    # because it can be raised as the result of reindexing
                    # the object in situations that are not foreseen by
                    # method in self.default.
                    default = None
            return default
        return value

    def getValueIf(self, obj, name, layout, disable=False):
        '''Special method only called by the framework. For some fields (or
           according to some p_disable condition), value retrieval as performed
           here must be disabled.'''
        if disable or self.customGetValue: return
        return self.getValue(obj, name, layout)

    def getCopyValue(self, obj):
        '''Gets the value of this field on p_obj as with m_getValue above. But
           if this value is mutable, get a copy of it.'''
        return self.getValue(obj)

    def getComparableValue(self, obj):
        '''Get the value of this field on p_obj, as can be compared with its new
           version, coming from the validator.'''
        # For immutable values, it simply returns the currently stored value.
        # For mutable values, there are 2 cases:
        # (a) the value as produced by the validator completely overwrites the
        #     existing value. Thus, the previous and new versions can safely be
        #     compared, because being completely distinct. In this case, as for
        #     immutable values, the currently stored value can also be used
        #     as-is, as "comparable" value ;
        # (b) the value as produced by the validator updates the stored value.
        #     In this case, comparing the previous and new versions would lead
        #     to comparing the same value. Here, the "comparable" value must be
        #     a deep copy of the previous value and not the stored value itself.
        return self.getValue(obj)

    def getFormattedValue(self, obj, value, layoutType='view',
                          showChanges=False, language=None):
        '''p_value is a real p_obj(ect) value from a field from this type. This
           method returns a pretty, string-formatted version, for displaying
           purposes. Needs to be overridden by some child classes. If
           p_showChanges is True, the result must also include the changes that
           occurred on p_value across the ages. If the formatting implies
           translating some elements, p_language will be used if given, the
           user language else.'''
        if self.isEmptyValue(obj, value): return ''
        return value

    def getShownValue(self, obj, value, layoutType='view',
                      showChanges=False, language=None):
        '''Similar to m_getFormattedValue, but in some contexts, only a part of
           p_value must be shown. For example, sometimes we need to display only
           a language-specific part of a multilingual field (see overridden
           method in string.py).'''
        return self.getFormattedValue(obj,value,layoutType,showChanges,language)

    def getXmlValue(self, obj, value):
        '''This method allows a developer to customize the value that will be
           marshalled into XML. It makes use of attribute "xml".'''
        if not self.xml: return value
        return self.xml(obj, value)

    def getSearchValue(self, form, widgetName=None):
        '''Returns the search value (or interval of values) that has been
           encoded in a search p_form for matching values for this field.'''
        # The base search widget corresponding to p_self is prefixed with "w_".
        # p_widgetName can be specified to get the sub-value of another widget
        # that is part of the complete search widget for p_self.
        widgetName = widgetName or ('w_%s' % self.name)
        # p_value is the base (string) value encoded in the search form. But
        # the search value (or interval of values) can be made of several form
        # fields: overriden methods of this method in Field sub-classes may be
        # much more complex.
        r = form.get(widgetName)
        if isinstance(r, __builtins__['list']):
            # It is a list of values. Check if we have an operator for the
            # field, to see if we make an "and" or "or" for all those values.
            # "or" will be the default.
            operKey = 'o_%s' % self.name
            oper = ' %s ' % form.get(operKey, 'or').upper()
            r = oper.join(r)
        elif r:
            r = r.strip()
        return r or None

    def searchValueIsEmpty(self, form, widgetName=None):
        '''In some search p_form, can the search value or interval of values
           specified for this field (p_self) be considered as empty ?'''
        # If, for example, the search widget for this field is made of an
        # interval (from, to), p_widgetName can be given to correspond to the
        # widget part "to", while, by default, the specified part is "from". For
        # some Field sub-classes, the search widget may be even more complex and
        # made of more parts.
        widgetName = widgetName or ('w_%s' % self.name)
        # Conditions in overriden methods can be more complex. For example, if
        # an interval of values (min, max) is expected, specifying only "min" or
        # "max" will allow to perform a search. In this case, we will consider
        # the search value as empty if both "min" and "max" are not specified.
        value = form.get(widgetName)
        if value and isinstance(value, basestring): value = value.strip()
        return not value

    def getInlineEditableValue(self, obj, value, layoutType, name=None):
        '''Returns p_value as it must appear on a view layout, with code
           allowing to inline-edit it when relevant.'''
        # Disable inline-edition if not specified
        inlineEdit = self.getAttribute(obj, 'inlineEdit')
        if not inlineEdit: return value
        # Disable inline-edition if the user can't modify the value
        if not obj.allows(self.writePermission) \
           or obj.o.isLocked(obj.user, self.page.name):
            return value
        # Enable inline-edition, either via an additional icon or by clicking
        # in the value.
        hook = '%s_%s' % (obj.id, name or self.name)
        onClick = 'onclick="askField(\'%s\',\'%s\',\'edit:%s\')"' % \
                  (hook, obj.url, layoutType)
        if inlineEdit == 'icon':
            url = obj.tool.o.getIncludeUrl
            r = '<img src="%s" title="%s" class="inlineIcon" %s/>%s' % \
                (url('edit'), obj.translate('object_edit'), onClick, value)
        else:
            r = '<span class="editable" %s>%s</span>' % (onClick, value)
        return r

    def getFakeObject(self, value, request):
        '''Returns a fake object, to mimic an object storing this p_value for
           field p_self.'''
        r = Object()
        setattr(r, self.name, value)
        return Object(aq_base=r, REQUEST=request, id='0')

    def getIndexType(self):
        '''Returns the name of the technical, Zope-level index type for this
           field.'''
        # Normally, self.indexed contains a Boolean. If a string value is given,
        # we consider it to be an index type. It allows to bypass the standard
        # way to decide what index type must be used.
        if isinstance(self.indexed, str): return self.indexed
        if self.name == 'title': return 'TextIndex'
        return 'FieldIndex'

    def getIndexValue(self, obj, forSearch=False):
        '''This method returns a version for this field value on p_obj that is
           ready for indexing purposes. Needs to be overridden by some child
           classes.

           If p_forSearch is True, it will return a "string" version of the
           index value suitable for a global search.'''
        # Must we produce an index value?
        if not self.getAttribute(obj, 'mustIndex'): return
        # Start by getting the field value on p_obj
        res = self.getValue(obj)
        # Possibly transform the value
        if self.indexValue:
            res = self.indexValue(obj.appy(), res)
        # Zope catalog does not like unicode strings
        if isinstance(res, unicode): res = res.encode('utf-8')
        if forSearch and (res is not None):
            if type(res) in sutils.sequenceTypes:
                vals = []
                for v in res:
                    if isinstance(v, unicode): vals.append(v.encode('utf-8'))
                    else: vals.append(str(v))
                res = ' '.join(vals)
            else:
                res = str(res)
        return res

    def getIndexName(self, usage='search'):
        '''Gets the name of the Zope index that corresponds to this field.
           Indexes can be used for searching (p_usage="search"), filtering
           ("filter") or sorting ("sort"). The method returns None if the field
           named p_fieldName can't be used for p_usage.'''
        # Manage special cases
        if self.name == 'title':
            # For field 'title', Appy has a specific index 'SortableTitle',
            # because index 'Title' is a TextIndex (for searchability) and can't
            # be used for sorting.
            if usage == 'sort': return 'SortableTitle'
            elif usage == 'filter':
                return self.searchable and 'SearchableText' or 'Title'
            else: return 'Title'
        elif self.name == 'state': return 'State'
        elif self.name == 'SearchableText': return 'SearchableText'
        else:
            res = 'get%s%s'% (self.name[0].upper(), self.name[1:])
            if (usage == 'sort') and self.hasSortIndex(): res += '_sort'
        return res

    def hasSortIndex(self):
        '''Some fields have indexes that prevents sorting (ie, list indexes).
           Those fields may define a secondary index, specifically for sorting.
           This is the case of Ref fields for example.'''
        return

    def getSortValue(self, obj):
        '''Return the value of p_self on p_obj that must be used for sorting.
           While the raw p_value may be the value to use in most cases, it is
           not always true. For example, a string like "Gaëtan" could have
           "gaetan" as sort value.'''
        return self.getValue(obj)

    def getCatalogValue(self, obj, usage='search'):
        '''This method returns the index value that is currently stored in the
           catalog for this field on p_obj.'''
        if not self.indexed:
            raise Exception('Field %s: cannot retrieve catalog version of ' \
                            'unindexed field.' % self.name)
        return obj.getTool().getCatalogValue(obj, self.getIndexName(usage))

    def valueIsInRequest(self, obj, request, name=None, layoutType='view'):
        '''Is there a value corresponding to this field in the request? p_name
           can be different from self.name (ie, if it is a field within another
           (List) field). In most cases, checking that this p_name is in the
           request is sufficient. But in some cases it may be more complex, ie
           for string multilingual fields.'''
        return request.has_key(name or self.name)

    def getStorableValue(self, obj, value, complete=False):
        '''p_value is a valid value initially computed through calling
           m_getRequestValue. So, it is a valid representation of the field
           value coming from the request. This method computes the value
           (potentially converted or manipulated in some other way) as can be
           stored in the database.'''
        # More precisely, m_getStorableValue computes a value that can be used
        # as input for m_store. But this latter can further transform it. For
        # example, a value produced by p_getStorableValue for a Ref field can be
        # a list of object IDs; method Ref.store will then convert it to a list
        # of Appy objects and make cross-links between them and p_obj. If
        # p_complete is True, the value produced will be forced to be
        # as close as possible as the database value. In our Ref example, it
        # will be a list of Appy objects (but cross-links will not be
        # established).
        if self.isEmptyValue(obj, value): return
        return value

    def getInputValue(self, inRequest, requestValue, value):
        '''Gets the value that must be filled in the "input" widget
           corresponding to this field.'''
        if inRequest:
            return requestValue or ''
        else:
            return value or ''

    def isReadonly(self, obj):
        '''Returns True if, when this field is rendered on an edit layout as an
           input field, it must have attribute "readonly" set.'''
        return bool(self.getAttribute(obj, 'readonly'))

    def setSlave(self, slaveField, masterValue):
        '''Sets p_slaveField as slave of this field. Normally, master/slave
           relationships are defined when a slave field is defined. At this time
           you specify parameters "master" and "masterValue" for this field and
           that's all. This method is used to add a master/slave relationship
           that was not initially foreseen.'''
        slaveField.master = self
        slaveField.masterValue = gutils.initMasterValue(masterValue)
        if slaveField not in self.slaves:
            self.slaves.append(slaveField)
        # Master's init method may not have been called yet
        slaveField.masterName = getattr(self, 'name', None)

    def getMasterData(self):
        '''Gets the master of this field (and masterValue) or, recursively, of
           containing groups when relevant.'''
        if self.master: return self.master, self.masterValue
        group = self.getGroup('edit')
        if group: return group.getMasterData()

    def getMasterTag(self, layoutType):
        '''Generally, for a field, the name of the tag serving as master for
           driving slave fields is the name of the field itself. But sometimes
           it can be different (see Field sub-classes).'''
        return self.name

    def getTagCss(self, tagCss, layoutType):
        '''Gets the CSS class(es) that must apply to XHTML tag representing this
           field in the ui. p_tagCss may already give some base class(es).'''
        res = []
        isInner = self.isInner()
        if tagCss and not isInner:
            # For an inner tag, it has no sense to "inherit" from p_tagCss
            res.append(tagCss)
        # Add a special class when this field is the slave of another field
        if self.master:
            css = 'slave*%s*' % self.master.getMasterTag(layoutType)
            if not callable(self.masterValue):
                css += '*'.join(self.masterValue)
            else:
                css += '+'
            res.insert(0, css)
        # Define a base CSS class when the field is a sub-field in a List
        if isInner: res.append('no')
        return ' '.join(res)

    def getOnChange(self, zobj, layoutType, className=None):
        '''When this field is a master, this method computes the call to the
           Javascript function that will be called when its value changes (in
           order to update slaves).'''
        if not self.slaves: return ''
        q = zobj.getTool().quote
        # When the field is on a search screen, we need p_className
        cName = className and q(className) or 'null'
        return 'updateSlaves(this,null,%s,%s,%s,true)' % \
               (q(zobj.absolute_url()), q(layoutType), cName)

    def isEmptyValue(self, obj, value):
        '''Returns True if the p_value must be considered as an empty value.'''
        return value in self.nullValues

    def isCompleteValue(self, obj, value):
        '''Returns True if the p_value must be considered as "complete". While,
           in most cases, a "complete" value simply means a "non empty" value
           (see m_isEmptyValue above), in some special cases it is more subtle.
           For example, a multilingual string value is not empty as soon as a
           value is given for some language but will not be considered as
           complete while a value is missing for some language. Another example:
           a Date with the "hour" part required will not be considered as empty
           if the "day, month, year" part is present but will not be considered
           as complete without the "hour, minute" part.'''
        return not self.isEmptyValue(obj, value)

    def getCheckedInfo(self, req):
        '''Gets the status of checked elements from the p_req(uest)'''
        # It returns a tuple (ids, unchecked):
        # ----------------------------------------------------------------------
        #   "ids"     | is a list of object IDs;
        # "unchecked" | is True if these objects are unchecked, or False if
        #             | they are checked.
        # ----------------------------------------------------------------------
        ids = req['checkedUids'] and req['checkedUids'].split(',') or []
        unchecked = req['checkedSem'] == 'unchecked'
        return ids, unchecked

    def getSearchParams(self, req, layoutType):
        '''This method encodes in a string all the params in the request that
           are required for re-triggering a search.'''
        if not req.has_key('search') or (layoutType == 'cell'): return ''
        return ':'.join([req.get(key,'') for key in Field.searchParams])

    def getSearchResults(self, tool, searchParams):
        '''Execute the search whose parameters (p_searchParams) are returned by
           m_getSearchParams and return its results. Log the operation.'''
        # Get search parameters as local variables
        cmd = ', '.join(Field.searchParams)
        cmd += " = searchParams.split(':',%d)" % (len(Field.searchParams) - 1)
        exec cmd
        # Retrieve a Ref object when relevant
        refObject, refField = tool.getRefInfo()
        # Executing the query may take some time and potentially slow down
        # the system: log this action.
        tool.log(SEARCH_TRIGGER % (self.type, className, self.name, search))
        # (Re-)execute the query, but without any limit on the number of
        # results; return Appy objects.
        class_ = tool.getAppyClass(className)
        objs = tool.executeQuery(className, searchName=search, sortBy=sortKey,
                                 sortOrder=sortOrder, maxResults='NO_LIMIT',
                                 filters=tool.getFilters(class_, filters),
                                 refObject=refObject, refField=refField)
        r = [o.appy() for o in objs.objects]
        tool.log(SEARCH_DONE % len(r))
        return r

    def keepCheckedResults(self, req, objects):
        '''Among p_objects as retrieved via m_getSearchResults, keep only those
           being checked, according to m_getCheckedInfo.'''
        ids, unchecked = self.getCheckedInfo(req)
        i = len(objects) - 1
        # Remove, from search results, unchecked objects
        while i >= 0:
            if unchecked: remove = objects[i].id in ids
            else:         remove = objects[i].id not in ids
            if remove:
                del objects[i]
            i -= 1

    def validateValue(self, obj, value):
        '''This method may be overridden by child classes and will be called at
           the right moment by m_validate defined below for triggering
           type-specific validation. p_value is never empty.'''
        return

    def securityCheck(self, obj, value):
        '''This method performs some security checks on the p_value that
           represents user input.'''
        if not isinstance(value, basestring): return
        # Search Javascript code in the value (prevent XSS attacks)
        if '<script' in value:
            obj.log('Detected Javascript in user input.', type='error')
            raise Exception('Your behaviour is considered a security ' \
                            'attack. System administrator has been warned.')

    def validate(self, obj, value):
        '''This method checks that p_value, coming from the request (p_obj is
           being created or edited) and formatted through a call to
           m_getRequestValue defined above, is valid according to this type
           definition. If it is the case, None is returned. Else, a translated
           error message is returned.'''
        # If the value is required, check that a (complete) value is present
        if not self.isCompleteValue(obj, value):
            if self.required and self.isClientVisible(obj):
                # If the field is required, but not visible according to
                # master/slave relationships, we consider it not to be required.
                return obj.translate('field_required')
            else:
                return
        # Perform security checks on p_value
        self.securityCheck(obj, value)
        # Triggers the sub-class-specific validation for this value
        message = self.validateValue(obj, value)
        if message: return message
        # Evaluate the custom validator if one has been specified
        value = self.getStorableValue(obj, value)
        if self.validator and (type(self.validator) in self.validatorTypes):
            obj = obj.appy()
            if type(self.validator) != self.validatorTypes[-1]:
                # It is a custom function: execute it
                try:
                    validValue = self.validator(obj, value)
                    if isinstance(validValue, basestring) and validValue:
                        # Validation failed; and p_validValue contains an error
                        # message.
                        return validValue
                    else:
                        if not validValue:
                            return obj.translate('field_invalid')
                except Exception, e:
                    return str(e)
                except:
                    return obj.translate('field_invalid')
            else:
                # It is a regular expression
                if not self.validator.match(value):
                    return obj.translate('field_invalid')

    def store(self, obj, value):
        '''Stores, on p_obj, the p_value (produced by m_getStorableValue) that
           complies to p_self's type definition.'''
        persist = self.persist
        if not persist: return
        elif callable(persist):
            # Do not store the value but let this method do whatever she wants
            # with it.
            self.persist(obj.appy(), value)
        else:
            # Store the value on p_obj
            setattr(obj, self.name, value)

    def storeValueFromAjax(self, obj, value, previousData):
        '''Called by m_storeValueFromAjax to save p_value on p_obj'''
        self.store(obj, self.getStorableValue(obj, value))
        # Overridden methods may return some custom message part
        return ''

    def storeFromAjax(self, obj):
        '''Stores the new field value from an Ajax request, or do nothing if
           the action was canceled.'''
        rq = obj.REQUEST
        # Be the operation a "save" or "cancel", remove the lock on the page
        # (if is was set).
        obj.removeLock(field=self)
        # Do nothing more when canceling the ajax-save
        if rq.get('cancel') == 'True': return
        # Get the new value
        requestValue = rq['fieldContent']
        # Are we working on a normal or inner field ?
        if not self.isInner():
            # A normal field. Remember its previous value if it is historized.
            isHistorized = self.getAttribute(obj, 'historized')
            previousData = None
            if isHistorized: previousData = obj.rememberPreviousData(self)
            # Validate the value
            if self.validate(obj, requestValue):
                # Be minimalist: do nothing and return the previous value
                return
            # Store the new value on p_obj
            part = self.storeValueFromAjax(obj, requestValue, previousData)
            # Update the object history when relevant
            if isHistorized and previousData: obj.historizeData(previousData)
        else:
            # An inner field. No historization (yet) for it.
            part = ''
            # Retrieve the outer, inner fields and row number
            name, px = rq['px'].rsplit(':', 1)
            outer, inner, i = name.split('*')
            outer = obj.getAppyType(outer)
            # Update the value
            value = outer.getValue(obj)
            row = value[int(i)]
            setattr(row, inner, requestValue)
            # Store the complete value again on p_obj
            setattr(obj.aq_base, outer.name, value)
        # Update obj's last modification date
        from DateTime import DateTime
        obj.modified = DateTime()
        obj.reindex()
        obj.log('ajax-edited %s%s on %s.' % (self.name, part, obj.id))

    def callMethod(self, obj, method, cache=True):
        '''This method is used to call a p_method on p_obj. p_method is part of
           this type definition (ie a default method, the method of a Computed
           field, a method used for showing or not a field...). Normally, those
           methods are called without any arg. But one may need, within the
           method, to access the related field. This method tries to call
           p_method with no arg *or* with the field arg.'''
        obj = obj.appy()
        try:
            return gutils.callMethod(obj, method, cache=cache)
        except TypeError, te:
            # Try a version of the method that would accept self as an
            # additional parameter. In this case, we do not try to cache the
            # value (we do not call gutils.callMethod), because the value may
            # be different depending on the parameter.
            tb = sutils.Traceback.get()
            try:
                return method(obj, self)
            except Exception, e:
                obj.log('method %s:\n%s' % (method.func_name, tb), type='error')
                # Raise the initial error
                raise te
        except Exception, e:
            obj.log(sutils.Traceback.get(), type='error')
            raise e

    def getAttribute(self, obj, name, cache=True):
        '''Gets the value of attribute p_name on p_self, which can be a simple
           value or the result of a method call on p_obj.'''
        res = getattr(self, name)
        if not callable(res): return res
        return self.callMethod(obj, res, cache=cache)

    def getGroup(self, layoutType):
        '''Gets the group into wich this field is on p_layoutType'''
        if not self.group: return
        if isinstance(self.group, Group): return self.group
        # The group depends on p_layoutType
        if layoutType in self.group: return self.group[layoutType]

    def getGroups(self):
        '''Returns groups as a list'''
        res = []
        if not self.group: return res
        if isinstance(self.group, Group):
            res.append(self.group)
        else: # A dict
            for group in self.group.itervalues():
                if group and (group not in res):
                    res.append(group)
        return res

    def process(self, obj):
        '''This method is a general hook allowing a field to perform some
           processing after an URL on an object has been called, of the form
           <objUrl>/onProcess.'''
        return obj.goto(obj.absolute_url())

    def renderLabel(self, layoutType):
        '''Indicates if the existing label (if hasLabel is True) must be
           rendered by pxLabel. For example, if field is an action, the
           label will be rendered within the button, not by pxLabel.'''
        if not self.hasLabel: return
        # Label is always shown in search forms
        if layoutType == 'search': return True
        # If the field is within a "tabs" group, the label will already be
        # rendered in the corresponding tab. If the field is in a "grid" group,
        # the label is already rendered in a separate column.
        group = self.getGroup(layoutType)
        if group and (group.style in ('tabs', 'grid')): return
        return True

    def getSelectSize(self, isSearch, isMultiple):
        '''If this field must be rendered as a HTML "select" field, get the
           value of its "size" attribute. p_isSearch is True if the field is
           being rendered on a search screen, while p_isMultiple is True if
           several values must be selected.'''
        if not isMultiple: return 1
        prefix = isSearch and 's' or ''
        height = getattr(self, '%sheight' % prefix)
        if isinstance(height, int): return height
        # "height" can be defined as a string. In this case it is used to define
        # height via a attribute "style", not "size".
        return ''

    def getSelectStyle(self, isSearch, isMultiple):
        '''If this field must be rendered as a HTML "select" field, get the
           value of its "style" attribute. p_isSearch is True if the field is
           being rendered on a search screen, while p_isMultiple is True if
           several values must be selected.'''
        prefix = isSearch and 's' or ''
        # Compute CSS attributes
        res = []
        # Height
        height = getattr(self, '%sheight' % prefix)
        if isMultiple and isinstance(height, str):
            res.append('height: %s' % height)
            # If height is an integer value, it will be dumped in attribute
            # "size", not in CSS attribute "height".
        # Width
        width = getattr(self, '%swidth' % prefix)
        if isinstance(width, str):
            res.append('width: %s' % width)
            # If width is an integer value, it represents a number of chars
            # (usable for truncating the shown values), not a width for the CSS
            # attribute.
        return ';'.join(res)

    def getRadioStyle(self, isSearch=False):
        '''If this field must be rendered as radio buttons or checkboxes, and
           its height is specified as a string, restrict the visible part of the
           widget to this height, with a scrollbar when appropriate.'''
        prefix = isSearch and 's' or ''
        r = []
        height = getattr(self, '%sheight' % prefix)
        if isinstance(height, str):
            r.append('height:%s;overflow-y:auto' % height)
        width = getattr(self, '%swidth' % prefix)
        if isinstance(width, str):
            r.append('width:%s;overflow-x:auto' % width)
        return ';'.join(r)

    def getWidthInChars(self, isSearch):
        '''If attribute "width" contains an integer value, it contains the
           number of chars shown in this field (a kind of "logical" width). If
           it contains a string, we must convert the value expressed in px
           (or in another CSS-compliant unit), to a number of chars.'''
        prefix = isSearch and 's' or ''
        width = getattr(self, '%swidth' % prefix)
        if isinstance(width, int): return width
        if isinstance(width, str) and width.endswith('px'):
            return int(width[:-2]) / 5
        return 30 # Other units are currently not supported

    def getListHeader(self, ctx):
        '''When p_self is used as inner-field, within a table-like rendered
           container field, this method returns the content of the header row
           corresponding to this inner field.'''
        return ctx['_']('label', field=self)
# ------------------------------------------------------------------------------
