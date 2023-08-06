'''This file contains basic classes that will be added into any user
   application for creating the basic structure of the application "Tool" which
   is the set of web pages used for configuring the application.'''

# ------------------------------------------------------------------------------
import types
import appy.gen as gen
from appy.fields import Field
from appy.fields.calendar import Calendar

# Prototypical instances of every type -----------------------------------------
class Protos:
    protos = {}
    # List of attributes that can't be given to a Type constructor
    notInit = ('id', 'type', 'pythonType', 'slaves', 'isSelect', 'hasLabel',
               'hasDescr', 'hasHelp', 'required', 'filterPx', 'validable',
               'isBack', 'pageName', 'masterName', 'select', 'sselect',
               'timeslots', 'legend', 'linkInPopup')
    @classmethod
    def get(self, appyType):
        '''Returns a prototype instance for p_appyType.'''
        className = appyType.__class__.__name__
        isString = (className == 'String')
        if isString:
            # For Strings, we create one prototype per format, because default
            # values may change according to format.
            className += str(appyType.format)
        if className in self.protos: return self.protos[className]
        # The prototype does not exist yet: create it
        if isString:
            proto = appyType.__class__(format=appyType.format)
            # Now, we fake to be able to detect default values
            proto.format = 0
        elif className == 'Pod':
            # Field "template" is mandatory
            proto = appyType.__class__(template='Appy.odt')
            proto.template = ()
        else:
            proto = appyType.__class__()
        self.protos[className] = proto
        return proto

# ------------------------------------------------------------------------------
class ModelClass:
    '''This class is the abstract class of all predefined application classes
       used in the Appy model: Tool, User, etc. All methods and attributes of
       those classes are part of the Appy machinery and are prefixed with _appy_
       in order to avoid name conflicts with user-defined parts of the
       application model.'''
    # In any ModelClass subclass we need to declare attributes in the following
    # list (including back attributes), to keep track of attributes order.
    _appy_attributes = []
    folder = False
    @classmethod
    def _appy_getTypeBody(klass, appyType, wrapperName):
        '''This method returns the code declaration for p_appyType'''
        typeArgs = ''
        proto = Protos.get(appyType)
        for name, value in appyType.__dict__.iteritems():
            # Some attrs can't be given to the constructor
            if name in Protos.notInit: continue
            # If the given value corresponds to the default value, don't give it
            if value == getattr(proto, name): continue
            if name == 'layouts':
                # For Tool attributes we do not copy layout info. Indeed, most
                # fields added to the Tool are config-related attributes whose
                # layouts must be standard.
                if klass.__name__ == 'Tool': continue
                layouts = appyType.getInputLayouts()
                # For the Translation class that has potentially thousands of
                # attributes, the most used layout is cached in a global var in
                # named "tfw" in wrappers.py.
                if (klass.__name__ == 'Translation') and \
                  (layouts=='{"edit":"f","search":"f","view":"f",}'):
                    value = 'tfw'
                else:
                    value = appyType.getInputLayouts()
            elif (name == 'klass') and value and (value == klass):
                # This is a auto-Ref (a Ref that references the klass itself).
                # At this time, we can't reference the class that is still being
                # defined. So we initialize it to None. The post-init of the
                # field must be done manually in wrappers.py.
                value = 'None'
            elif isinstance(value, basestring):
                value = '"%s"' % value
            elif isinstance(value, gen.Ref):
                if not value.isBack: continue
                value = klass._appy_getTypeBody(value, wrapperName)
            elif type(value) == type(ModelClass):
                moduleName = value.__module__
                if moduleName.startswith('appy.gen'):
                    value = value.__name__
                else:
                    value = '%s.%s' % (moduleName, value.__name__)
            elif isinstance(value, gen.Selection):
                value = 'Selection("%s")' % value.methodName
            elif isinstance(value, gen.Group):
                value = 'gps["%s"]' % value.name
            elif isinstance(value, gen.Page):
                value = 'pges["%s"]' % value.name
            elif callable(value):
                className = wrapperName
                if (appyType.type == 'Ref') and appyType.isBack:
                    className = value.im_class.__name__
                value = '%s.%s' % (className, value.__name__)
            typeArgs += '%s=%s,' % (name, value)
        return '%s(%s)' % (appyType.__class__.__name__, typeArgs)

    @classmethod
    def _appy_getBody(klass):
        '''This method returns the code declaration of this class. We will dump
           this in wrappers.py in the Zope product.'''
        className = klass.__name__
        # Determine the name of the class and its wrapper. Because so much
        # attributes can be generated on a TranslationWrapper, shortcutting it
        # to 'TW' may reduce the generated file from several kilobytes.
        if className == 'Translation': wrapperName = 'WT'
        else: wrapperName = 'W%s' % className
        res = 'class %s(%s):\n' % (className, wrapperName)
        # Tool must be folderish
        if klass.folder: res += '    folder=True\n'
        # First, scan all attributes, determine all used pages and groups, and
        # create a dict with it. It will prevent us from creating a new Page
        # instance for every field.
        pages = {}
        groups = {}
        layouts = []
        for name in klass._appy_attributes:
            exec 'field = klass.%s' % name
            if field.page.name not in pages:
                pages[field.page.name] = field.page
            group = field.group
            if group and (group.name not in groups):
                groups[group.name] = group
        # Generate the dict with pages
        res += '    pges={'
        for page in pages.itervalues():
            # Determine page "show" attributes
            pShow = ''
            for attr in ('',) + page.subElements:
                attrName = 'show%s' % attr.capitalize()
                pageShow = getattr(page, attrName)
                if isinstance(pageShow, basestring): pageShow='"%s"' % pageShow
                elif callable(pageShow):
                    pageShow = '%s.%s' % (wrapperName, pageShow.__name__)
                if pageShow != True:
                    pShow += ', %s=%s' % (attrName, pageShow)
            # For translation pages, fixed labels are used
            label = ''
            if className == 'Translation':
                name = (page.name == 'main') and 'Options' or page.name
                label = ', label="%s"' % name
            else:
                label = page.label and (', label="%s"' % str(page.label)) or ''
            res += '"%s":Pge("%s"%s%s),' % (page.name, page.name, pShow, label)
        res += '}\n'
        if groups:
            # Generate the dict with groups
            res += '    gps={'
            for group in groups.itervalues():
                label = group.label and (',label="%s"' % group.label) or ''
                res += '"%s":Grp("%s",style="%s"%s),' % \
                       (group.name, group.name, group.style, label)
            res += '}\n'
        # Secondly, dump every (not Ref.isBack) attribute
        for name in klass._appy_attributes:
            exec 'appyType = klass.%s' % name
            if (appyType.type == 'Ref') and appyType.isBack: continue
            typeBody = klass._appy_getTypeBody(appyType, wrapperName)
            res += '    %s=%s\n' % (name, typeBody)
        return res

# The User class ---------------------------------------------------------------
class User(ModelClass):
    _appy_attributes = ['password1', 'password2', 'title', 'name', 'firstName',
      'source', 'login', 'password3', 'password4', 'encrypted', 'email',
      'roles', 'resetPassword', 'groups', 'toTool', 'syncDate', 'lastLoginDate',
      'changePasswordAtNextLogin']
    # All methods defined below are fake. Real versions are in the wrapper.
    # Passwords are on a specific page.
    def showPassword12(self): pass
    def showPassword34(self): pass
    def showCancel12(self): pass
    def validatePassword(self): pass
    pp = {'page': gen.Page('passwords', showNext=False, show=showPassword12,
                          showCancel=showCancel12, label='User_page_passwords'),
          'width': 28, 'multiplicity': (1,1), 'format': gen.String.PASSWORD,
          'show': showPassword12, 'label': 'User'}
    password1 = gen.String(validator=validatePassword, **pp)
    password2 = gen.String(**pp)

    # Fields "password3" and "password4" are only shown when creating a user.
    # After user creation, those fields are not used anymore; fields "password1"
    # and "password2" above are then used to modify the password on a separate
    # page.
    pm = {'page': gen.Page('main', showPrevious=False, label='User_page_main'),
          'width': 28, 'layouts': Field.gLayouts, 'label': 'User',
          'group': gen.Group('main', style='grid', label='User_group')}
    title = gen.String(show='xml', indexed=True, **pm)
    def showName(self): pass
    name = gen.String(show=showName, **pm)
    firstName = gen.String(show=showName, **pm)
    pm['multiplicity'] = (1,1)
    def showLogin(self): pass
    def validateLogin(self): pass
    login = gen.String(show=showLogin, validator=validateLogin,
      indexed=True, **pm)
    del pm['label']
    password3 = gen.String(validator=validatePassword, show=showPassword34,
      format=gen.String.PASSWORD, label=('User', 'password1'), **pm)
    password4 = gen.String(show=showPassword34, format=gen.String.PASSWORD,
      label=('User', 'password2'), **pm)
    def getEncryptedPassword(self): pass
    def showEncryptedPassword(self): pass
    encrypted = gen.Computed(method=getEncryptedPassword,
                             show=showEncryptedPassword, layouts='f')
    def showEmail(self): pass
    pm['label'] = 'User'
    email = gen.String(show=showEmail, **pm)
    pm['multiplicity'] = (0, None)
    del pm['width']
    def showRoles(self): pass
    roles = gen.Select(show=showRoles, indexed=True, width=40, height=10,
      validator=gen.Selection('getGrantableRoles'), render='checkbox', **pm)

    # Where is this user stored? By default, in the ZODB. But the user can be
    # stored in an external LDAP (source='ldap').
    source = gen.String(show='xml', default='zodb', layouts='f')
    def doResetPassword(self): pass
    def showResetPassword(self): pass
    resetPassword = gen.Action(action=doResetPassword, show=showResetPassword,
                          confirm=True, label='User', icon='pwd', render='icon')

    # Some hidden fields
    hidden = {'show': False, 'layouts': 'f'}
    # For external users (source != "zodb"), we store the date of the last time
    # the external user and the local copy were synchronized.
    syncDate = gen.Date(format=gen.Date.WITH_HOUR, **hidden)
    # The date of the last login for this user
    lastLoginDate = gen.Date(format=gen.Date.WITH_HOUR, **hidden)
    # We may force a local user (source=zodb) to change its password at next
    # login (ie, for users created by an admin).
    changePasswordAtNextLogin = gen.Boolean(**hidden)

# The Group class --------------------------------------------------------------
class Group(ModelClass):
    _appy_attributes = ['title', 'login', 'roles', 'users', 'toTool2']
    # All methods defined below are fake. Real versions are in the wrapper.
    m = {'group': gen.Group('main', style='grid', label='Group_group'),
         'width': 25, 'indexed': True, 'layouts': Field.gLayouts,
         'label': 'Group'}
    title = gen.String(multiplicity=(1,1), **m)
    def showLogin(self): pass
    def validateLogin(self): pass
    login = gen.String(show=showLogin, validator=validateLogin,
                       multiplicity=(1,1), **m)
    roles = gen.String(validator=gen.Selection('getGrantableRoles'),
                       multiplicity=(0,None), **m)
    users = gen.Ref(User, multiplicity=(0,None), add=False, link='popup',
      height=15, back=gen.Ref(attribute='groups', show=User.showRoles,
                              multiplicity=(0,None), label='User'),
      showHeaders=True, shownInfo=('title', 'login', 'state*100px|'),
      actionsDisplay='inline', label='Group')

# The Translation class --------------------------------------------------------
class Translation(ModelClass):
    _appy_attributes = ['po', 'title', 'sourceLanguage', 'trToTool']
    # All methods defined below are fake. Real versions are in the wrapper.
    ta = {'label': 'Translation'}
    title = gen.String(show=False, indexed=True,
                     page=gen.Page('main', label='Translation_page_main'), **ta)
    def getPoFile(self): pass
    po = gen.Action(action=getPoFile, result='file', **ta)
    sourceLanguage = gen.String(width=4, **ta)
    def label(self): pass
    def show(self, name): pass

# The Page class ---------------------------------------------------------------
class Page(ModelClass):
    _appy_attributes = ['doc', 'title', 'content', 'pages', 'parent',
                        'expression', 'toTool3']
    folder = True
    pa = {'label': 'Page'}
    doc = gen.Pod(template='/gen/templates/Page.odt', formats=('pdf',),
                  show=False, layouts=gen.Table('f', width=None,
                                                css_class='inline', align=''))
    title = gen.String(show=('edit','xml'), multiplicity=(1,1),
                       indexed=True, **pa)
    content = gen.String(format=gen.String.XHTML, layouts='f')
    # If this Python expression returns False, the page can't be viewed
    def showExpression(self): pass
    expression = gen.String(layouts=Field.dLayouts, show=showExpression, **pa)
    # Pages can contain other pages
    def showSubPages(self): pass
    pages = gen.Ref(None, multiplicity=(0,None), add=True, link=False,
      composite=True, back=gen.Ref(attribute='parent', show=False, **pa),
      numbered=True, show=showSubPages, **pa)
Page.pages.klass = Page
setattr(Page, Page.pages.back.attribute, Page.pages.back)

# The Tool class ---------------------------------------------------------------
# Prefixes of the fields generated on the Tool
defaultToolFields = ('title', 'appyVersion', 'dateFormat', 'hourFormat',
                     'numberOfResultsPerPage', 'users', 'connectedUsers',
                     'synchronizeExternalUsers', 'groups', 'translations',
                     'loadTranslationsAtStartup', 'pages', 'calendar')

class Tool(ModelClass):
    # In a ModelClass we need to declare attributes in the following list
    _appy_attributes = list(defaultToolFields)
    folder = True

    # Tool attributes
    def forToolWriters(self): pass
    def pageForToolWriters(self): pass
    lf = {'layouts':'f'}
    title = gen.String(show=False, default='Configuration',
      page=gen.Page('main', show=False), **lf)
    appyVersion = gen.String(**lf)
    dateFormat = gen.String(default='%d/%m/%Y', **lf)
    hourFormat = gen.String(default='%H:%M', **lf)
    numberOfResultsPerPage = gen.Integer(default=30, **lf)

    # Ref(User) will maybe be transformed into Ref(CustomUserClass)
    ta = {'label': 'Tool'}
    userPage = gen.Page('users', show=pageForToolWriters,
                        label='Tool_page_users')
    users = gen.Ref(User, multiplicity=(0,None), add=True, link=False,
      composite=True, back=gen.Ref(attribute='toTool', show=False, layouts='f'),
      page=userPage, queryable=True, queryFields=('title', 'login', 'roles'),
      show=forToolWriters, showHeaders=True, actionsDisplay='inline',
      shownInfo=('title', 'name*15%|', 'login*20%|',
                 'roles*20%|', 'state*100px|'), **ta)

    def computeConnectedUsers(self): pass
    connectedUsers = gen.Computed(method=computeConnectedUsers, page=userPage,
                                  show='view', **ta)
    def doSynchronizeExternalUsers(self): pass
    def showSynchronizeUsers(self): pass
    synchronizeExternalUsers = gen.Action(action=doSynchronizeExternalUsers,
        show=showSynchronizeUsers, confirm=True, page=userPage, **ta)

    groups = gen.Ref(Group, multiplicity=(0,None), add=True, link=False,
      composite=True, back=gen.Ref(attribute='toTool2', show=False,layouts='f'),
      page=gen.Page('groups', show=pageForToolWriters,label='Tool_page_groups'),
      show=forToolWriters, queryable=True, queryFields=('title', 'login'),
      showHeaders=True, actionsDisplay='inline',
      shownInfo=('title', 'login*20%|', 'roles*20%|'), **ta)

    pt = gen.Page('translations', show=pageForToolWriters,
                  label='Tool_page_translations')
    translations = gen.Ref(Translation, multiplicity=(0,None), add=False,
      link=False, composite=True, show='view', page=pt, actionsDisplay='inline',
      back=gen.Ref(attribute='trToTool', show=False, layouts='f'), **ta)
    loadTranslationsAtStartup = gen.Boolean(default=True, show=False, page=pt,
                                            layouts='f')
    pages = gen.Ref(Page, multiplicity=(0,None), add=True, link=False,
      composite=True, show=('view', 'xml'), actionsDisplay='inline',
      back=gen.Ref(attribute='toTool3', show=False, layouts='f'),
      page=gen.Page('pages', show=pageForToolWriters, label='Tool_page_pages'),
      **ta)

    # This calendar is used for searches' "calendar" mode
    def calendarPreCompute(self, first, grid): pass
    def calendarAdditionalInfo(self, date, preComputed): pass
    calendar = Calendar(preCompute=calendarPreCompute,
                        additionalInfo=calendarAdditionalInfo, **ta)

    @classmethod
    def _appy_clean(klass):
        toClean = []
        for k, v in klass.__dict__.iteritems():
            if not k.startswith('__') and (not k.startswith('_appy_')):
                if k not in defaultToolFields:
                    toClean.append(k)
        for k in toClean:
            exec 'del klass.%s' % k
        klass._appy_attributes = list(defaultToolFields)
        klass.folder = True
# ------------------------------------------------------------------------------
