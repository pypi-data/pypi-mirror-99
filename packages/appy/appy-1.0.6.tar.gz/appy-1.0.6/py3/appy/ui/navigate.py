'''Navigation management'''

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
from appy.model.batch import Batch

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Sibling:
    '''Represents a sibling element, accessible via navigation from
       another one.'''
    # Existing types of siblings
    types = ('previous', 'next', 'first', 'last')

    # Names of icons corresponding to sibling types
    icons = {'previous': 'arrow.svg',  'next': 'arrow.svg',
             'first':    'arrows.svg', 'last': 'arrows.svg'}

    # Rotations for icons
    rotate = {'previous': 90, 'next': 270, 'first': 90, 'last': 270}

    def __init__(self, o, type, nav, page, siblings):
        # The main Siblings instance
        self.container = siblings
        # The sibling object, which may be None at this time
        self.o = o
        # The type of sibling
        self.type = type
        # The "nav" key
        self.nav = nav
        # The page that must be shown on the object
        self.page = page
        # Are we in a popup or not ?
        self.popup = siblings.popup

    def getSiblingIndex(self):
        '''Return the index of the sibling to navigate to'''
        type = self.type
        if type == 'last':
            r = self.container.total - 1
        elif type == 'next':
            # "number" is already "index + 1"
            r = self.container.number
        elif type == 'previous':
            # "number" is already "index + 1"
            r = self.container.number - 2
        else: # type is "first"
            r = 0
        return r

    def get(self, ctx):
        '''Get the HTML chunk allowing to navigate to this sibling'''
        if self.o:
            # We already have the object and thus its URL
            url = "'%s'" % self.o.url
        else:
            # We only know the index of the object to go to. The object ID is in
            # the browser's session storage.
            container = self.container
            url = "buildSiblingUrl('%s','%s',%d)" % \
                  (container.tool.siteUrl, container.search.getSessionKey(),
                   self.getSiblingIndex())
        # Build the JS code allowing to navigate to the sibling element
        js = "gotoSibling(%s,'%s','%s','%s')" % \
             (url, self.nav, self.page, self.popup)
        type = self.type
        return '<img src="%s" title="%s" class="clickable iconXS" ' \
               'style="transform: rotate(%ddeg)" onclick="%s"/>' % \
               (ctx.url(Sibling.icons[type]), ctx._('goto_%s' % type),
                Sibling.rotate[type], js)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Siblings:
    '''Abstract class containing information for navigating from one object to
       its siblings.'''

    pxGotoNumber = Batch.pxGotoNumber
    # Attributes storing the siblings for going "backwards" (True) or "forwards"
    # (False)
    byType = {True: ('firstSibling', 'previousSibling'),
              False: ('nextSibling',  'lastSibling')}

    # Icons for going to the current object's siblings
    pxNavigate = Px('''<div>
      <!-- Go to the source URL (search or referred object) -->
      <div if="not popup">::self.getGotoSource(url, _)</div>

      <!-- Show other navigation icons only when relevant -->
      <div if="self.total" class="navSib">
       <!-- Form used to navigate to any sibling -->
       <form name=":self.siblingsFormName" method="post" action="">
        <input type="hidden" name="page" value=""/>
        <input type="hidden" name="popup" value=""/>
        <input type="hidden" name="criteria" value=""/>
       </form>

       <!-- Go to the first and/or previous page -->
       <x>::self.getIcons(_ctx_, previous=True)</x>

       <!-- Explain which element is currently shown -->
       <x>:self.number</x> / <x>:self.total</x> 

       <!-- Go to the next and/or last page -->
       <x>::self.getIcons(_ctx_, previous=False)</x>

       <!-- Go to the element number... -->
       <div if="self.showGotoNumber()"
            var2="field=self.field; sourceUrl=self.sourceObject.url;
                  total=self.total">:self.pxGotoNumber</div>
      </div></div>''',

     css='''.navSib { padding: |navsPadding|; font-size: 90% }''',

     js='''
       function gotoCustomSearch() {
         // Post a form allowing to re-trigger a custom search
         var f = document.forms['gotoSource'];
         // Add search criteria from the browser's session storage
         f.criteria.value = sessionStorage.getItem(f.className.value);
         f.submit();
       }
       function buildSiblingUrl(siteUrl, sessionKey, index) {
         var ids = JSON.parse(sessionStorage.getItem(sessionKey));
         if (!(index in ids)) {
           // Get siblings by performing a new server search
           var parts = sessionKey.split('_'),
               className = parts[0],
               search = parts[1],
               params = {'className':className, 'search':search, 'index':index},
               url = siteUrl + '/tool/Search/jresults';
           if (search == 'customSearch') {
             params['criteria'] = sessionStorage.getItem(className);
           }
           askAjaxChunk(url, 'POST', params, '*'+sessionKey);
           ids = JSON.parse(sessionStorage.getItem(sessionKey));
         }
         var iid = ids[index];
         return siteUrl + '/' + iid + '/view';
       }

       function gotoSibling(url, nav, page, popup) {
         var formName = (popup == 'True') ? 'siblingsPopup' : 'siblings',
             f = document.forms[formName];
         // Navigate to the sibling by posting a form
         f.action = url;
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
    def get(nav, tool, ctx):
        '''Analyse the navigation info p_nav and returns the corresponding
          concrete Siblings instance.'''
        elems = nav.split('.')
        Siblings = (elems[0] == 'ref') and RefSiblings or SearchSiblings
        return Siblings(tool, ctx, *elems[1:])

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

    def __init__(self, tool, ctx, number, total):
        self.tool = tool
        self.req = tool.req
        self.ctx = ctx
        # Are we in a popup window or not ?
        self.popup = ctx.popup
        self.siblingsFormName = 'siblingsPopup' if self.popup else 'siblings'
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
        # Get the current object's siblings
        self.siblings = siblings = self.getSiblings()
        # Compute the URL allowing to go back to the "source" = a given page of
        # query results or referred objects.
        self.sourceUrl = self.getSourceUrl()
        # Compute Sibling objects and store them in attributes named
        # "<siblingType>Sibling".
        nav = self.getNavKey()
        page = self.req.page or 'main'
        for siblingType in Sibling.types:
            needIt = eval('self.%sNeeded' % siblingType)
            name = '%sSibling' % siblingType
            setattr(self, name, None)
            if not needIt: continue
            index = eval('self.%sIndex' % siblingType)
            # If siblings are there, try to get the sibling object for this type
            if self.siblings:
                o = self.getSiblingObject(index)
                if o is None: continue
            else:
                # We do not know the sibling yet
                o = None
            # Create the Sibling instance
            sibling = Sibling(o, siblingType, nav % (index+1), page, self)
            setattr(self, name, sibling)

    def getBackTexts(self, _):
        '''Gets a tuple with the "back texts" = a tuple of 2 texts: the standard
           text (ie, "back") and a more detailed text, based on the source ref
           or search.'''
        return _('goto_source'), self.getBackText() or ''

    def getIcons(self, ctx, previous=True):
        '''Produce icons for going to
           - the first or the previous page if p_previous is True;
           - the next or last page else.
        '''
        r = ''
        for name in Siblings.byType[previous]:
            sibling = getattr(self, name)
            if sibling: r += sibling.get(ctx)
        return r

    def getGotoSource(self, url, _):
        '''Get the link allowing to return to the source URL'''
        text, message = self.getBackTexts(_)
        return '<a href="%s" title="%s"><img src="%s" class="back"/>%s</a>'% \
               (self.sourceUrl, message, url('arrowsA.svg'), text)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class RefSiblings(Siblings):
    '''Class containing information for navigating from one object to another
       within tied objects from a Ref field.'''
    prefix = 'ref'

    def __init__(self, tool, popup, sourceId, fieldName, number, total):
        # The source object of the Ref field
        self.sourceObject = tool.getObject(sourceId)
        # The Ref field in itself
        self.field = self.sourceObject.getField(fieldName)
        # Call the base constructor
        Siblings.__init__(self, tool, popup, number, total)

    def getNavKey(self):
        '''Returns the general navigation key for navigating to another
           sibling.'''
        return self.field.getNavInfo(self.sourceObject, None, self.total)

    def getBackText(self):
        '''Computes the text to display when the user want to navigate back to
           the list of tied objects.'''
        title = self.sourceObject.title
        text = self.tool.translate(self.field.labelId)
        return '%s - %s' % (title, text) if title else text

    def getBatchSize(self):
        '''Returns the maximum number of shown objects at a time for this
           ref.'''
        return self.field.maxPerPage

    def getSiblings(self):
        '''Returns the siblings of the current object'''
        return getattr(self.sourceObject, self.field.name, ())

    def getSiblingObject(self, index):
        '''Get the sibling object at this p_index'''
        try:
            r = self.siblings[index]
        except ValueError:
            r = None
        return r

    def getSourceUrl(self):
        '''Computes the URL allowing to go back to self.sourceObject's page
           where self.field lies and shows the list of tied objects, at the
           batch where the current object lies.'''
        # Allow to go back to the batch where the current object lies
        field = self.field
        startNumberKey = '%d_%s_objs_start' % \
                         (self.sourceObject.iid, field.name)
        startNumber = str(self.computeStartNumber())
        return self.sourceObject.getUrl(sub='view', page=field.pageName,
                                       nav='no', **{startNumberKey:startNumber})

    def showGotoNumber(self):
        '''Show "goto number" if the Ref field is numbered'''
        return self.field.isNumbered(self.sourceObject) and (self.total > 1)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class SearchSiblings(Siblings):
    '''Class containing information for navigating from one object to another
       within results of a search.'''
    prefix = 'search'

    def __init__(self, tool, ctx, className, searchName, number, total):
        # The class determining the type of searched objects
        self.className = className
        self.class_ = tool.model.classes[className]
        # Get the search object
        self.searchName = searchName
        self.uiSearch = tool.Search.get(searchName, tool, self.class_, ctx,
                                        ui=True)
        self.search = self.uiSearch.search
        Siblings.__init__(self, tool, ctx, number, total)

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
        '''For a search, siblings are defined in the browser's session storage.
           So here, at the server level, we do not know them.'''

    def getSourceUrl(self):
        '''Computes the (non-Ajax) URL allowing to go back to the search
           results, at the batch where the current object lies, or to the
           originating field if the search was triggered from a field.'''
        tool = self.tool
        if ',' in self.searchName:
            # Go back to the originating field
            id, name, mode = self.searchName.split(',')
            o = tool.getObject(id)
            field = o.getField(name)
            return '%s/view?page=%s' % (o.url, field.page.name)
        else:
            url = '%s/Search/results' % tool.url
            # For a custom search, do not add URL params: we will build a form
            # and perform a POST request with search criteria.
            if self.searchName == 'customSearch': return url
            params = 'className=%s&search=%s&start=%d' % \
                    (self.className, self.searchName, self.computeStartNumber())
            ref = self.req.ref
            if ref: params += '&ref=%s' % ref
            return '%s?%s' % (url, params)

    def getGotoSource(self, url, _):
        '''Get the link or form allowing to return to the source URL'''
        if self.searchName != 'customSearch':
            return Siblings.getGotoSource(self, url, _)
        # For a custom search, post a form with the search criteria retrieved
        # from the browser's session.
        text, message = self.getBackTexts(_)
        return '<form method="post" action="%s" name="gotoSource">' \
          '<input type="hidden" name="className" value="%s"/>' \
          '<input type="hidden" name="search" value="customSearch"/>' \
          '<input type="hidden" name="start" value="%d"/>' \
          '<input type="hidden" name="ref" value="%s"/>' \
          '<input type="hidden" name="criteria" value=""/></form>' \
          '<a class="clickable" title="%s" onclick="gotoCustomSearch()">' \
          '<img src="%s" class="back"/>%s</a>' % \
          (self.sourceUrl, self.className, self.computeStartNumber(),
           self.req.ref or '', message, url('arrowsA.svg'), text)

    def showGotoNumber(self): return
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
