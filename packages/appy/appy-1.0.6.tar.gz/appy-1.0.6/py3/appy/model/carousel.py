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
from appy.ui import css
from appy.model.base import Base
from appy.ui.layout import Layouts
from appy.model.fields.ref import Ref
from appy.model.fields.file import File
from appy.model.fields.dict import Dict
from appy.model.utils import Object as O
from appy.model.document import Document
from appy.model.fields.phase import Page
from appy.model.fields.color import Color
from appy.model.fields.group import Group
from appy.model.fields.string import String
from appy.model.fields.boolean import Boolean
from appy.model.fields.integer import Integer
from appy.model.fields.computed import Computed
from appy.model.workflow.standard import Anonymous
from appy.model.fields.select import Select, Selection

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Carousel(Base):
    '''A carousel is a UI element allowing to cycle through documents'''

    # By default, carousels are public, and not indexed
    workflow = Anonymous
    indexable = False
    listColumns = ('title', 'maxWidth', 'autoSwitch', 'switchInterval')
    pageListColumns = ('title', 'state')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                            Main parameters
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Fields in the main page are rendered in a grid group
    mainGroup = Group('main', ['400em', ''], style='grid', hasLabel=False)

    pc = {'label': 'Carousel', 'group': mainGroup}

    # Maximum width for documents in the carousel (in pixels)
    maxWidth = Integer(default=2277, multiplicity=(1,1), layouts=Layouts.gd,
                       alignOnEdit='center', **pc)

    # Maximum height for the carousel (bottom image excluded, see below). Set it
    # to 'none' if you don't want to define this maximum height. If 'none', the
    # real height will depend on the inner images. Whatever you choose, images'
    # width/height ratios are always kept.
    maxHeight = String(default='620px', multiplicity=(1,1), width=5,
                       layouts=Layouts.gd, **pc)

    # Must automatic switch be enabled ?
    autoSwitch = Boolean(default=True, **pc)
    # Duration between 2 switches (in seconds)
    switchInterval = Integer(default=5, multiplicity=(1,1), width=2,
                             alignOnEdit='center', **pc)

    # Default attributes for image's elements
    def listFonts(self):
        '''Lists the available Google fonts as specified in the config'''
        return [(font, font) for font in self.config.ui.googleFonts]

    def showFonts(self):
        '''Do not show font-related field if there is not Google font to
           choose.'''
        return bool(self.config.ui.googleFonts)

    defaultElemAttributes = {
      'title'     : O(color='#ffffff', font='', fontSize='3.5vw',
                      fontWeight='normal'),
      'underTitle': O(color='#afb0b9', font='', fontSize='1.5vw',
                      fontWeight='normal'),
      'buttonA'   : O(color='#ffffff', font='', fontSize='1vw',
                      fontWeight='bold'),
      'buttonB'   : O(color='#ffffff', font='', fontSize='1vw',
                      fontWeight='bold')
    }

    sub = (
      ('color', Color()), # Text color
      ('font', Select(validator=Selection(listFonts), show=showFonts)),
      ('fontSize', String(width=4, multiplicity=(1,1))),
      ('fontWeight', Select(validator=Selection(
        lambda o: [(w, o.translate('fw_%s' % w)) for w in css.fontWeigths]),
        default='normal', multiplicity=(1,1))),
      ('fontStyle', Select(validator=Selection(
        lambda o: [(s, o.translate('fs_%s' % s)) for s in css.fontStyles]),
        default='normal', multiplicity=(1,1)))
    )

    elemAttributes = Dict(lambda o: Document.listElementTypes(o), sub,
                          default=defaultElemAttributes, **pc)

    # Default attributes for links that can be set on image elements
    subl = (
      ('params', String()), # Default parameters to add to every link URL
      ('target', String(width=7)), # Link's target (_blank, iframe,...)
      ('onClick', String()), # Optional value for "onClick" attribute
    )

    linkAttributes = Dict(lambda o: Document.listElementTypes(o), subl, **pc)

    # Default background colors for buttons
    buttonBgColorA = Color(default='#88c9b5', **pc)
    buttonBgColorB = Color(default='#fcc100', **pc)
    # Map buttons types to their backgrounds
    backgroundFields = {'buttonA': 'buttonBgColorA',
                        'buttonB': 'buttonBgColorB'}

    # Colors for the controls allowing to (un)select a given image
    selectedColor = Color(default='#fcc100', **pc)
    unselectedColor = Color(default='#ffffff', **pc)

    # Image to use as bottom border
    bottomImage = File(isImage=True, resize=True, width=lambda o: o.maxWidth,
                       viewWidth='700px', layouts=Layouts.gd, cache=True, **pc)

    def getCssName(self, elemType):
        '''Gets the name of the CSS class corresponding to p_elemType'''
        return 'cl_%d_%s' % (self.iid, elemType)

    def getElementStyles(self):
        '''Generates the CSS classes to apply to elements shown on top of
           carousel's images.'''
        r = []
        attributes = self.elemAttributes
        for type in Document.elementTypes:
            # Compute background color when appropriate
            bg = Carousel.backgroundFields.get(type)
            bg = (';background-color:%s' % getattr(self, bg)) if bg else ''
            padding = ';padding:0.7em 1.7em' if bg else ''
            # Compute other CSS attributes
            attrs = attributes[type]
            font = ('"%s"' % attrs.font) if attrs.font else 'sans-serif'
            className = self.getCssName(type)
            css = '.%s {color:%s;font-family:%s;font-size:%s;font-weight:%s;' \
                  'font-style:%s%s%s}' % \
                  (className, attrs.color, font, attrs.fontSize,
                   attrs.fontWeight, attrs.fontStyle, bg, padding)
            # Add another rule for coloring the text of "a" sub-tags
            cssA = '.%s a, .%s a:visited {color:%s}' % \
                   (className, className, attrs.color)
            r.append(css)
            r.append(cssA)
        return '\n'.join(r)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                           Inner images
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # The documents being part of this carousel
    del(pc['group'])
    documents = Ref(Document, add=True, link=False, multiplicity=(0,None),
      composite=True, back=Ref(attribute='carousel', show=False),
      showHeaders=True, shownInfo=Document.listColumns, actionsDisplay='inline',
      page=Page('documents',
                show=lambda o:'view' if o.allows('write') else None),
      viaPopup=False, rowAlign='middle', **pc)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                          PX rendering
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    pxView = Px('''
     <!-- Inject styles dynamically generated for every element -->
     <style>::o.getElementStyles()</style>
     <x if="o.isEmpty('documents')">-</x>
     <div if="not o.isEmpty('documents')"
          var2="carouselId='cl_%d_%s' % (o.iid, field.name);
                count=o.countRefs('documents')"
          class="carousel" id=":carouselId" data-count=":count" data-current="1"
          data-selected-color=":o.selectedColor" 
          data-unselected-color=":o.unselectedColor"
          data-auto-switch=":str(o.autoSwitch)"
          data-switch-interval=":o.switchInterval" data-timer-id="">

      <!-- The images -->
      <div for="image in o.documents"
           var2="i=loop.image.nb"
           id=":'%s_%d' % (carouselId, i+1)"
           style=":'opacity:%s' % ('1' if i == 0 else '0')">
       <img src=":'%s/file/download' % image.url"
            style=":'max-height:%s' % o.maxHeight"/>

       <!-- The elements to superpose on the image -->
       <div class="canvas">
         <x for="element in image.getElements(o)">::element</x>
       </div>
      </div>

      <!-- The controls for selecting a specific element -->
      <svg width=":20+((count-1)*30)" height="20">
       <circle for="image in o.documents" var2="i=loop.image.nb"
               id=":'%s_circle_%d' % (carouselId, i+1)"
               class="clickable" cx=":10 + (i*30)" cy="10" r="10"
               onclick=":'carouselSelect(%s,%s,%d,true)' % \
                          (q(carouselId), q(i+1), count)"
               fill=":o.selectedColor if i == 0 else o.unselectedColor" />
      </svg>
      <script>:'carouselStart(%s)' % q(carouselId)</script>
     </div>
     <!-- Render the bottom image when present -->
     <img if="not o.isEmpty('bottomImage')" class="carouselFooter"
          src=":'%s/bottomImage/download' % o.url"/>''',

     css='''
      .carousel { position: relative }
      .carousel > div { transition: opacity 2s }
      .carousel > div:nth-child(n+2) { position: absolute; top: 0; left: 0;
                                       width: 100% }
      .carousel img { width: 100%; height: auto; object-fit: cover }
      .carousel svg { position: absolute; top: 90%; left: 50%; z-index: 2;
                      transform: translate(-50%,0%) }
      .carousel .canvas { top: 0; left: 0; position: absolute;
                          width: 90%; height: 100%; z-index: 2 }
      .carousel .canvas > div { position: absolute }
      .carouselFooter { width: 100%; height: auto; vertical-align: top }
     ''',

     js='''
      function getCarouselPart(carouselId, i, isImage) {
        /* Get the carousel part numbered p_i: the ith image if p_isImage is
           True, the selection circle else. */
        var sep = (isImage)? '_': '_circle_';
        return document.getElementById(carouselId + sep + i.toString());
      }
      function carouselSelect(carouselId, nb, count, stopTimer) {
        // Make element numbered p_nb visible in the carousel
        var nb=parseInt(nb),
            selected = getCarouselPart(carouselId, nb, true),
            carousel=document.getElementById(carouselId);
        // Stop the timer when appropriate
        if (stopTimer) {
          var timerId = carousel.dataset.timerId;
          if (timerId) clearInterval(parseInt(timerId));
        }
        // Do nothing more if the selected image is already visible
        if (selected.style.opacity == 1) return;
        // Find the element being currently shown
        var part=null, circle=null;
        for (var i=0; i<count; i++) {
          part = getCarouselPart(carouselId, i+1, true);
          if (part.style.opacity == 1) {
            // Switch the color of their corresponding circle
            circle = getCarouselPart(carouselId, i+1, false);
            circle.setAttribute('fill', carousel.dataset.unselectedColor);
            circle = getCarouselPart(carouselId, nb, false);
            circle.setAttribute('fill', carousel.dataset.selectedColor);
            // Switch visibility of parts
            selected.style.opacity = 1;
            part.style.opacity = 0;
            // Remember the new current image
            carousel.dataset.current = nb.toString();
            return;
          }
        }
      }
      function carouselSwitch(carouselId) {
        // Switch from the currently shown image to the next one
        var carousel = document.getElementById(carouselId),
            count = parseInt(carousel.dataset.count),
            current = parseInt(carousel.dataset.current),
            next=(current==count)? 1: current+1;
        carouselSelect(carouselId, next, count);
      }
      function carouselStart(carouselId) {
        var carousel = document.getElementById(carouselId),
            auto = carousel.dataset.autoSwitch == 'True',
            count = parseInt(carousel.dataset.count);
        // Do not launch it if automatic switch is disabled
        if (!auto || (count == 0)) return;
        var interval = parseInt(carousel.dataset.switchInterval),
            timerId = setInterval(
              function() {carouselSwitch(carouselId);}, interval*1000);
        carousel.dataset.timerId = timerId.toString();
      }''')

    # A field allowing to preview the carousel in one of its pages
    preview = Computed(method=pxView, page=Page('preview', show='view'),
                       layouts=Layouts.w, **pc)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
