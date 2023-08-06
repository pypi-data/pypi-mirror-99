# ------------------------------------------------------------------------------
from appy.px import Px

# Input field for going to element number x. This PX is common to classes
# Siblings and Batch defined hereafter.
pxGotoNumber = Px('''
 <x var2="label=_('goto_number');
          gotoName='%s_%s_goto' % (obj.id, field.name);
          popup=inPopup and '1' or '0'">
  <span class="discreet" style="padding-left: 5px">:label</span> 
  <input type="text" size=":len(str(total)) or 1" onclick="this.select()"
         onkeydown=":'if (event.keyCode==13) document.getElementById' \
                     '(%s).click()' % q(gotoName)"/><img
         id=":gotoName" name=":gotoName"
         class="clickable" src=":url('gotoNumber')" title=":label"
         onclick=":'gotoTied(%s,%s,this.previousSibling,%s,%s)' % \
             (q(sourceUrl), q(field.name), total, q(popup))"/></x>''')

# ------------------------------------------------------------------------------
class Sibling:
    '''Represents a sibling element, accessible via navigation from
       another one.'''
    # Existing types of siblings
    types = ('previous', 'next', 'first', 'last')
    # Names of icons corresponding to sibling types
    icons = {'previous': 'arrowLeft',  'next': 'arrowRight',
             'first':    'arrowsLeft', 'last': 'arrowsRight'}

    def __init__(self, obj, type, nav, page, inPopup=False):
        # The sibling object
        self.obj = obj
        # The type of sibling
        self.type = type
        # The "nav" key
        self.nav = nav
        # The page that must be shown on the object
        self.page = page
        # Are we in a popup or not ?
        self.popup = inPopup and '1' or '0'

    def get(self, url, _):
        '''Get the HTML chunk allowing to navigate to this sibling'''
        js = "gotoSibling('%s/view','%s','%s','%s')" % \
             (self.obj.url, self.nav, self.page, self.popup)
        return '<img src="%s" title="%s" class="clickable" onclick="%s"/>' % \
               (url(Sibling.icons[self.type]), _('goto_%s' % self.type), js)

# ------------------------------------------------------------------------------
class Siblings:
    '''Abstract class containing information for navigating from one object to
       its siblings.'''

    # Icons for going to the current object's siblings
    pxGotoNumber = pxGotoNumber
    pxNavigate = Px('''
      <!-- Go to the source URL (search or referred object) -->
      <div if="not inPopup" class="goSource">::self.getGotoSource(url, _)</div>

      <!-- Show other navigation icons only when relevant -->
      <x if="self.total">
       <!-- Form used to navigate to any sibling -->
       <form name=":self.siblingsFormName" method="post" action=""
             style="display: inline">
        <input type="hidden" name="nav" value=""/>
        <input type="hidden" name="page" value=""/>
        <input type="hidden" name="popup" value=""/>
        <input type="hidden" name="criteria" value=""/>
       </form>

       <!-- Go to the first or previous page -->
       <x if="self.firstSibling">::self.firstSibling.get(url, _)</x>
       <x if="self.previousSibling">::self.previousSibling.get(url, _)</x>

       <!-- Explain which element is currently shown -->
       <span class="discreet"> 
        <x>:self.number</x> <b>//</b> <x>:self.total</x> </span>

       <!-- Go to the next or last page -->
       <x if="self.nextSibling">::self.nextSibling.get(url, _)</x>
       <x if="self.lastSibling">::self.lastSibling.get(url, _)</x>

       <!-- Go to the element number... -->
       <x if="self.showGotoNumber()"
          var2="field=self.field; sourceUrl=self.sourceObject.absolute_url();
                total=self.total"><br/><x>:self.pxGotoNumber</x></x></x>''',
     js='''
       function gotoCustomSearch() {
         // Post a form allowing to re-trigger a custom search
         var f = document.forms['gotoSource'];
         // Add search criteria from the browser's session storage
         f.criteria.value = sessionStorage.getItem(f.className.value);
         f.submit();
       }
       function gotoSibling(url, nav, page, popup) {
         var formName = (popup == '1') ? 'siblingsPopup' : 'siblings',
             f = document.forms[formName];
         // Navigate to the sibling by posting a form
         f.action = url;
         f.nav.value = nav;
         f.page.value = page;
         f.popup.value = popup;
         if (nav) {
           // For a custom search, get criteria from the session storage
           var elems = nav.split('.');
           if ((elems[0] == 'search') && (elems[2] == 'customSearch')) {
             f.criteria.value = sessionStorage.getItem(elems[1]);
           }
           // Avoid losing navigation
           f.action = f.action + '?nav=' + nav;
         }
         f.submit();
        }''')

    @staticmethod
    def get(nav, tool, inPopup):
        '''Analyse the navigation info p_nav and returns the corresponding
          concrete Siblings instance.'''
        elems = nav.split('.')
        Siblings = (elems[0] == 'ref') and RefSiblings or SearchSiblings
        return Siblings(tool, inPopup, *elems[1:])

    def computeStartNumber(self):
        '''Returns the start number of the batch where the current element
           lies.'''
        # First index starts at O, so we calibrate self.number
        number = self.number - 1
        batchSize = self.getBatchSize()
        res = 0
        while (res < self.total):
            if (number < res + batchSize): return res
            res += batchSize
        return res

    def __init__(self, tool, inPopup, number, total):
        self.tool = tool
        self.request = tool.REQUEST
        # Are we in a popup window or not ?
        self.inPopup = inPopup
        self.siblingsFormName = inPopup and 'siblingsPopup' or 'siblings'
        # The number of the current element
        self.number = int(number)
        # The total number of siblings
        self.total = int(total)
        # Do I need to navigate to first, previous, next and/or last sibling ?
        self.previousNeeded = False # Previous ?
        self.previousIndex = self.number - 2
        if (self.previousIndex > -1) and (self.total > self.previousIndex):
            self.previousNeeded = True
        self.nextNeeded = False     # Next ?
        self.nextIndex = self.number
        if self.nextIndex < self.total: self.nextNeeded = True
        self.firstNeeded = False    # First ?
        self.firstIndex = 0
        if self.previousIndex > 0: self.firstNeeded = True
        self.lastNeeded = False     # Last ?
        self.lastIndex = self.total - 1
        if (self.nextIndex < self.lastIndex): self.lastNeeded = True
        # Compute the IDs of the siblings of the current object
        self.siblings = self.getSiblings()
        # Compute the URL allowing to go back to the "source" = a given page of
        # query results or referred objects.
        self.sourceUrl = self.getSourceUrl()
        # Compute Sibling objects and store them in attributes named
        # "<siblingType>Sibling".
        nav = self.getNavKey()
        page = self.request.get('page', 'main')
        for siblingType in Sibling.types:
            exec 'needIt = self.%sNeeded' % siblingType
            name = '%sSibling' % siblingType
            setattr(self, name, None)
            if not needIt: continue
            exec 'index = self.%sIndex' % siblingType
            id = None
            try:
                # self.siblings can be a list (ref) or a dict (search)
                id = self.siblings[index]
            except KeyError: continue
            except IndexError: continue
            if not id: continue
            obj = self.tool.getObject(id, appy=True)
            if not obj: continue
            # Create the Sibling instance
            sibling = Sibling(obj, siblingType, nav % (index+1), page, inPopup)
            setattr(self, name, sibling)

    def getSuffixedBackText(self, _):
        '''Gets the p_backText, produced by m_getBackText (see sub-classes),
           suffixed with a standard text.'''
        text = self.getBackText()
        goto = _('goto_source')
        return text and ('%s - %s' % (text, goto)) or goto

    def getGotoSource(self, url, _):
        '''Get the link allowing to return to the source URL'''
        return '<a href="%s"><img src="%s"/>%s</a>' % \
               (self.sourceUrl, url('gotoSource'), self.getSuffixedBackText(_))

# ------------------------------------------------------------------------------
class RefSiblings(Siblings):
    '''Class containing information for navigating from one object to another
       within tied objects from a Ref field.'''
    prefix = 'ref'

    def __init__(self, tool, inPopup, sourceUid, fieldName, number, total):
        # The source object of the Ref field
        self.sourceObject = tool.getObject(sourceUid)
        # The Ref field in itself
        self.field = self.sourceObject.getAppyType(fieldName)
        # Call the base constructor
        Siblings.__init__(self, tool, inPopup, number, total)

    def getNavKey(self):
        '''Returns the general navigation key for navigating to another
           sibling.'''
        return self.field.getNavInfo(self.sourceObject, None, self.total)

    def getBackText(self):
        '''Computes the text to display when the user want to navigate back to
           the list of tied objects.'''
        _ = self.tool.translate
        return '%s - %s' % (self.sourceObject.Title(), _(self.field.labelId))

    def getBatchSize(self):
        '''Returns the maximum number of shown objects at a time for this
           ref.'''
        return self.field.maxPerPage

    def getSiblings(self):
        '''Returns the siblings of the current object'''
        return getattr(self.sourceObject, self.field.name, ())

    def getSourceUrl(self):
        '''Computes the URL allowing to go back to self.sourceObject's page
           where self.field lies and shows the list of tied objects, at the
           batch where the current object lies.'''
        # Allow to go back to the batch where the current object lies
        field = self.field
        startNumberKey = '%s_%s_objs_startNumber' % \
                         (self.sourceObject.id,field.name)
        startNumber = str(self.computeStartNumber())
        return self.sourceObject.getUrl(**{startNumberKey:startNumber,
                                           'page':field.pageName, 'nav':'no'})

    def showGotoNumber(self):
        '''Show "goto number" if the Ref field is numbered.'''
        return self.field.isNumbered(self.sourceObject)

# ------------------------------------------------------------------------------
class SearchSiblings(Siblings):
    '''Class containing information for navigating from one object to another
       within results of a search.'''
    prefix = 'search'

    def __init__(self, tool, inPopup, className, searchName, number, total):
        # The class determining the type of searched objects
        self.className = className
        # Get the search object
        self.searchName = searchName
        self.uiSearch = tool.getSearch(className, searchName, ui=True)
        self.search = self.uiSearch.search
        Siblings.__init__(self, tool, inPopup, number, total)

    def getNavKey(self):
        '''Returns the general navigation key for navigating to another
           sibling.'''
        return 'search.%s.%s.%%d.%d' % (self.className, self.searchName,
                                        self.total)

    def getBackText(self):
        '''Computes the text to display when the user want to navigate back to
           the list of searched objects.'''
        return self.uiSearch.translated

    def getBatchSize(self):
        '''Returns the maximum number of shown objects at a time for this
           search.'''
        return self.search.maxPerPage

    def getSiblings(self):
        '''Returns the siblings of the current object. For performance reasons,
           only a part of it is stored, in the session object.'''
        session = self.request.SESSION
        searchKey = self.search.getSessionKey(self.className)
        if session.has_key(searchKey): res = session[searchKey]
        else: res = {}
        if (self.previousNeeded and not res.has_key(self.previousIndex)) or \
           (self.nextNeeded and not res.has_key(self.nextIndex)):
            # The needed sibling UID is not in session. We will need to
            # retrigger the query by querying all objects surrounding this one.
            newStartNumber = (self.number-1) - (self.search.maxPerPage / 2)
            if newStartNumber < 0: newStartNumber = 0
            self.tool.executeQuery(self.className, search=self.search,
                                   startNumber=newStartNumber, remember=True)
            res = session[searchKey]
        # For the moment, for first and last, we get them only if we have them
        # in session.
        if not res.has_key(0): self.firstNeeded = False
        if not res.has_key(self.lastIndex): self.lastNeeded = False
        return res

    def getSourceUrl(self):
        '''Computes the (non-Ajax) URL allowing to go back to the search
           results, at the batch where the current object lies, or to the
           originating field if the search was triggered from a field.'''
        if ',' in self.searchName:
            # Go back to the originating field
            id, name, mode = self.searchName.split(',')
            obj = self.tool.getObject(id, appy=True)
            field = obj.getField(name)
            return '%s?page=%s' % (obj.url, field.page.name)
        else:
            url = '%s/query' % self.tool.absolute_url()
            # For a custom search, do not add URL params: we will build a form
            # and perform a POST request with search criteria.
            if self.searchName == 'customSearch': return url
            params = 'className=%s&search=%s&startNumber=%d' % \
                    (self.className, self.searchName, self.computeStartNumber())
            ref = self.request.get('ref', None)
            if ref: params += '&ref=%s' % ref
            return '%s?%s' % (url, params)

    def getGotoSource(self, url, _):
        '''Get the link or form allowing to return to the source URL'''
        if self.searchName != 'customSearch':
            return Siblings.getGotoSource(self, url, _)
        # For a custom search, post a form with the search criteria retrieved
        # from the browser's session.
        return '<form method="post" action="%s" name="gotoSource">' \
          '<input type="hidden" name="className" value="%s"/>' \
          '<input type="hidden" name="search" value="customSearch"/>' \
          '<input type="hidden" name="startNumber" value="%d"/>' \
          '<input type="hidden" name="ref" value="%s"/>' \
          '<input type="hidden" name="criteria" value=""/></form>' \
          '<a class="clickable" onclick="gotoCustomSearch()">' \
          '<img src="%s"/>%s</a>' % \
          (self.sourceUrl, self.className, self.computeStartNumber(),
           self.request.get('ref', ''), url('gotoSource'),
           self.getSuffixedBackText(_))

    def showGotoNumber(self): return

# ------------------------------------------------------------------------------
class Batch:
    '''Class for navigating between parts (=batches) within lists of objects'''
    def __init__(self, hook, total, length, size=30, start=0):
        # The ID of the DOM node containing the list of objects
        self.hook = hook
        # The total number of objects
        self.total = total
        # The effective number of objects in the current batch
        self.length = length
        # The maximum number of objects shown at once (in the batch). If p_size
        # is None, all objects are shown.
        self.size = size
        # The index of the first object in the current batch
        self.start = start

    def update(self, **kwargs):
        '''Update p_self's attributes with values from p_kwargs'''
        for name, value in kwargs.iteritems():
            setattr(self, name, value)

    def __repr__(self):
        return '<Batch hook=%s,start=%s,length=%s,size=%s,total=%s>' % \
               (self.hook, self.start, self.length, self.size, self.total) 

    # Icons for navigating among a list of objects: next, back, first, last...
    pxGotoNumber = pxGotoNumber
    pxNavigate = Px('''
     <div if="batch.total &gt; batch.size" align=":dright"
          var2="hook=q(batch.hook); size=q(batch.size)">

      <!-- Go to the first page -->
      <img if="(batch.start != 0) and (batch.start != batch.size)"
           class="clickable" src=":url('arrowsLeft')" title=":_('goto_first')"
           onclick=":'askBunch(%s,%s,%s)'% (hook, q(0), size)"/>

      <!-- Go to the previous page -->
      <img var="sNumber=batch.start - batch.size" if="batch.start != 0"
           class="clickable" src=":url('arrowLeft')" title=":_('goto_previous')"
           onclick=":'askBunch(%s,%s,%s)' % (hook, q(sNumber), size)"/>

      <!-- Explain which elements are currently shown -->
      <span class="discreet"> 
       <x>:batch.start + 1</x> <img src=":url('to')"/> 
       <x>:batch.start + batch.length</x> <b>//</b> <x>:batch.total</x>
      </span>

      <!-- Go to the next page -->
      <img var="sNumber=batch.start + batch.size" if="sNumber &lt; batch.total"
           class="clickable" src=":url('arrowRight')" title=":_('goto_next')"
           onclick=":'askBunch(%s,%s,%s)' % (hook, q(sNumber), size)"/>

      <!-- Go to the last page -->
      <img var="lastPageIsIncomplete=batch.total % batch.size;
                nbOfCompletePages=batch.total / batch.size;
                nbOfCountedPages=lastPageIsIncomplete and \
                                 nbOfCompletePages or nbOfCompletePages-1;
                sNumber= nbOfCountedPages * batch.size"
           if="(batch.start != sNumber) and \
               (batch.start != (sNumber-batch.size))" class="clickable"
           src=":url('arrowsRight')" title=":_('goto_last')"
           onclick=":'askBunch(%s,%s,%s)' % (hook, q(sNumber), size)"/>

      <!-- Go to the element number... -->
      <x var="gotoNumber=gotoNumber|False" if="gotoNumber"
         var2="sourceUrl=obj.url; total=batch.total">:batch.pxGotoNumber</x>
     </div>''')
# ------------------------------------------------------------------------------
