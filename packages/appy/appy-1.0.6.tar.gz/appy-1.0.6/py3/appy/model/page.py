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
from appy.model.base import Base
from appy.model.fields import Show
from appy.model.query import Query
from appy.xml.escape import Escape
from appy.model.fields.pod import Pod
from appy.model.fields.rich import Rich
from appy.model.fields.file import File
from appy.model.fields.info import Info
from appy.model.document import Document
from appy.model.carousel import Carousel
from appy.model.fields.group import Group
from appy.ui.layout import Layout, Layouts
from appy.model.fields.select import Select
from appy.model.fields.string import String
from appy.model.fields.boolean import Boolean
from appy.model.fields.integer import Integer
from appy.model.fields.ref import Ref, autoref
from appy.model.fields.phase import Page as FPage
from appy.model.workflow.standard import Anonymous

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
EXPR_ERR = 'Page "%s" (%s): error while evaluating page expression "%s" (%s).'
DELETED  = 'Web page %s deleted.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Page(Base):
    '''Base class representing a web page'''

    # By default, web pages are public
    workflow = Anonymous

    pa = {'label': 'Page'}
    # Pages are not indexed by default
    indexable = False

    @staticmethod
    def getListColumns(tool):
        '''Show minimal info for the anonymous user'''
        if tool.user.isAnon(): return
        return ('title', 'expression', 'next', 'selectable*100px|',
                'podable*80px|', 'viewCss*100px|')
    listColumns = getListColumns

    # The POD ouput
    doc = Pod(template='/model/pod/Page.odt', formats=('pdf',), show=False,
              layouts=Pod.Layouts.inline, freezeTemplate=lambda o,tpl: ('pdf',))

    @staticmethod
    def update(class_):
        '''Configure field "title"'''
        title = class_.fields['title']
        title.show = Show.EX
        title.label = 'Page'
        title.page.show = lambda o: True if o.allows('write') else 'view'
        title.page.sticky = True

    # The POD output appears inline in the sub-breadcrumb
    def getSubBreadCrumb(self):
        '''Display an icon for downloading this page (and sub-pages if any) as a
           POD.'''
        if self.podable: return self.getField('doc').doRender('view', self)

    def getSubTitle(self):
        '''Render a link to the tied carousel and/or search'''
        r = []
        esc = Escape.xhtml
        for name in ('carousel', 'query'):
            if not self.isEmpty(name):
                o = getattr(self, name)
                label = self.translate(self.getField(name).labelId)
                r.append('<div class="discreet">%s: <a href="%s">%s</a></div>' \
                         % (esc(label), o.url, esc(o.title)))
        return '\n'.join(r)

    # A warning: image upload is impossible while the page is temp
    warning = Info(show=lambda o: 'edit' if o.isTemp() else None,
                   focus=True, layouts=Info.Layouts.n, **pa)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                            Linked carousel
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def showCarousel(self):
        '''Show field "carousel" if carousels are defined'''
        if self.tool.isEmpty('carousels'): return
        # Do not show it (except on "edit") if there is no tied carousel
        return True if not self.isEmpty('carousel') else 'edit'

    carousel = Ref(Carousel, add=False, link=True, render='links',
      select=lambda o: o.tool.carousels, shownInfo=Carousel.pageListColumns,
      show=showCarousel, layouts=Layouts.fvd,
      view=Px('''<x var="o=o.carousel">:o.pxView</x>'''),
      back=Ref(attribute='pages', multiplicity=(0,None), render='links',
               group=Carousel.mainGroup, label='Carousel'), **pa)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                            Page content
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    content = Rich(documents='documents', height='350px', inject=True,
                   viewCss=lambda o: o.viewCss, layouts=Rich.Layouts.f, **pa)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                           Linked search
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def showQuery(self):
        '''Show field "query" if queries are defined'''
        if self.tool.isEmpty('queries'): return
        # Do not show it (except on "edit") if there is no tied carousel
        return True if not self.isEmpty('query') else 'edit'

    query = Ref(Query, add=False, link=True, render='links',
      select=lambda o: o.tool.queries, shownInfo=Query.pageListColumns,
      show=showQuery, layouts=Layouts.fvd,
      view=Px('''<x var="o=o.query">:o.pxView</x>'''),
      back=Ref(attribute='pages', multiplicity=(0,None), render='links',
               group=Query.mainGroup, label='Query'), **pa)

    def forRootOnEdit(self):
        '''Determines visibility of some fields, on the "edit" layout, for root
           pages only.'''
        return Show.V_ if self.isRoot() else None

    # Is this (root) page selectable in the main dropdown ?
    selectable = Boolean(default=True, show=forRootOnEdit,
                         layouts=Boolean.Layouts.d, **pa)

    # Is PDF POD export enabled for this page ? Sub-pages can't be exported.
    podable = Boolean(layouts=Boolean.Layouts.d, show=forRootOnEdit, **pa)

    # Maximum width for images uploaded and rendered within the XHTML content
    maxWidth = Integer(default=700, show=False)

    # If this Python expression returns False, the page can't be viewed
    def showExpression(self):
        '''Show the expression to managers only'''
        # Do not show it on "view" if empty
        if self.isEmpty('expression'): return Show.V_
        return self.allows('write')

    expression = String(layouts=Layouts.d, show=showExpression, **pa)

    # Name of the CSS class applied to the page content, when rendered on view
    # or cell layouts.
    viewCss = String(default='xhtml', layouts=Layouts.d, show=Show.V_, **pa)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                           Inner images
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # The images (or other documents) that may be included in field "content"
    documents = Ref(Document, add=True, link=False, multiplicity=(0,None),
      composite=True, back=Ref(attribute='page', show=False, label='Document'),
      showHeaders=True, shownInfo=Document.listColumns, actionsDisplay='inline',
      page=FPage('images', show=lambda o:'view' if o.allows('write') else None),
      rowAlign='middle', **pa)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                         Background image
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # In most cases, when a page is shown, like any other object, the background
    # image possibly applied is baseBG.jpg. On public root pages, no background
    # is shown: the one uploaded here may be used instead.
    bip = {'page': FPage('bg', show=lambda o: o.allows('write') and o.isRoot()),
           'group': Group('main', style='grid', hasLabel=False),
           'layouts': Layouts.gd }
    bip.update(pa)

    backgroundImage = File(isImage=True, viewWidth='700px', cache=True, **bip)

    # When the background image hereabove is used, the following parameter
    # determines how it is rendered. It is the equivalent of CSS attribute
    # "background-size".
    backgroundSize = Select(validator=('cover', 'auto'), default='cover', **bip)

    def initialiseLocalPage(self, req):
        '''A page can be specifically rendered as a root public page or as
           an inner page of such a root page. In these cases, the rendering
           context must be adapted.'''
        # p_self may propose a specific background image
        if not self.isEmpty('backgroundImage'):
            style = 'background-image:url(%s/backgroundImage/download); ' \
                    'background-repeat:no-repeat; background-size:%s' % \
                    (self.url, self.backgroundSize)
        else:
            style = None
        # Use a minimal page layout that only includes the "w" part (=widgets)
        req.pageLayout = Layout('w', style=style)
        # Avoid including global page elements: they have already been included
        # by the enclosing element.
        req.notGlobal = True

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                            Next page
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Pages can be chained, in order to produce a single, composite page.
    # Chained pages must all be in the same container object.

    def listSiblings(self):
        '''Returns the pages being p_self's siblings'''
        return [page for page in self.container.pages if page != self]

    def hasContainer(self):
        '''Some fields can't be shown while a page has no container, which can
           happen when creating a page from the porlet.'''
        return Show.V_ if self.container else None

    next = Ref(None, add=False, link=True, layouts=Layouts.fvd, render='links',
               back=Ref(attribute='previous', render='links',
                        label='Page', show=Show.VE_),
               show=hasContainer, select=listSiblings, **pa)

    def getChain(self):
        '''Returns the list of pages being chained to p_self via "next" fields,
           recursively.'''
        r = [self]
        next = self.next
        return r + next.getChain() if next else r

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                            Sub-pages
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # A page can contain sub-pages
    def showSubPages(self):
        '''For non-writers, show sub-pages only if present'''
        if self.allows('write'):
            # Show it, unless the page is rendered as the next page of a
            # previous one.
            return not self.req.notGlobal
        if not self.isEmpty('pages'): return 'view'

    pages = Ref(None, multiplicity=(0,None), add=True, link=False,
      composite=True, back=Ref(attribute='parent', show=False, **pa),
      showHeaders=True, actionsDisplay='inline', show=showSubPages,
      numbered=True, checkboxes=lambda o: o.allows('write'), **pa)

    def getParents(self, includeMyself=True):
        '''Returns, as a set, p_self's parents, including p_self itself if
           p_includeMyself is True.'''
        r = {self} if includeMyself else set()
        return r if self.isRoot() else r.union(self.container.getParents())

    def mayView(self):
        '''In addition to the workflow, evaluating p_self.expression, if
           defined, determines p_self's visibility.'''
        expression = self.expression
        if not expression: return True
        user = self.user
        try:
            return eval(expression)
        except Exception as err:
            message = EXPR_ERR % (self.title, self.id, expression, str(err))
            self.log(message, type='error')
            return True

    def getMergedContent(self, r=None, level=1):
        '''Returns a list of chunks of XHTML code, one for p_self and one for
           each of its sub-pages, recursively.'''
        # More precisely, the r_result is a list of tuples of the form
        #
        #                   ~(xhtmlChunk, i_delta)~
        #
        #, "delta" being the delta to apply to the title's outline levels,
        # depending on the depth of the page within the complete tree of pages.
        #
        # p_level is the current level of recursion, while p_r is the current
        # list under creation. Indeed, in order to avoid concatenating lists, at
        # each m_getMergedContent call, the current p_r(esult) is passed.
        if r is None:
            # We are at the start of a recursive merge: there is no result yet.
            # Create it.
            r = []
        # Two pieces of information must be collected about p_self: its title
        # and content.
        if level > 1:
            # At level 1, do not dump the title
            title = self.getValue('title', type='shown')
            r.append(('<h1>%s</h1>' % Escape.xhtml(title), level-2))
        # Add p_self's content
        if not self.isEmpty('content'):
            r.append((self.getValue('content', type='shown'), level-1))
        # Add sub-pages
        if not self.isEmpty('pages'):
            for page in self.pages:
                page.getMergedContent(r, level=level+1)
        return r

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Main methods
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def inPortlet(self, selected, level=0):
        '''Returns a chunk of XHTML code for representing this page in the
           portlet.'''
        # Is this page currently selected ? A selected page is the page being
        # currently consulted on the site or any of its parent pages.
        isSelected = self in selected
        # A specific CSS class wil be applied for a selected page
        css = ' class="current"' if isSelected else ''
        # If p_self has parents, we must render it with a margin-right
        style = ' style="margin-left:%dpx"' % (level * 5) if level else ''
        r = ['<div%s><a href="%s"%s>%s</a></div>' % \
             (style, self.url, css, Escape.xhtml(self.title))]
        if isSelected and not self.isEmpty('pages'):
            for sub in self.pages:
                r.append(sub.inPortlet(selected, level+1))
        return ''.join(r)

    def isRoot(self):
        '''Is p_self a root page ?'''
        # A page created from the portlet (if class Page is declared as root)
        # has no container when under creation.
        container = self.container
        return not container or (container.class_.name == 'Tool')

    def onEdit(self, created):
        '''Link the page among root pages if created from the portlet'''
        if created and not self.initiator:
            self.tool.link('pages', self)

    def onDelete(self):
        '''Log the page deletion'''
        self.log(DELETED % self.id)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  PXs
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # This selector allows to choose one root page among published tool.pages
    pxSelector = Px('''
      <select onchange="gotoURL(this)">
       <option value="">:_('goto_link')</option>
       <option for="page in pages"
               value=":'%s/public?rp=%s' % (tool.url, page.iid)"
               selected=":req.rp == str(page.iid)">:page.title</option>
      </select>''',

     js='''
       function gotoURL(select) {
         var url = select.value;
         if (url) goto(url);
       }''')

    # PX showing all root pages in the portlet, when shown for pages
    portletBottom = Px('''
     <div class="topSpaceS" var="pages=tool.OPage.getRoot(tool)">
      <x if="pages"
         var2="selected=o.getParents() if o.class_.name == 'Page' else {}">
       <x for="page in pages">::page.inPortlet(selected)</x>
      </x>
      <i if="not pages">:_('no_page')</i>
     </div>''')

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Class methods
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    @classmethod
    def getRoot(class_, tool):
        '''Return the pages being visible by the logged user, among the site's
           root pages from p_tool.pages.'''
        # Return the cached version, if available
        cache = tool.H().cache
        if 'appyRootPages' in cache: return cache.appyRootPages
        # Compute it
        r = [page for page in tool.pages \
             if page.selectable and tool.guard.mayView(page)]
        cache.appyRootPages = r
        return r

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
autoref(Page, Page.next)
autoref(Page, Page.pages)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
