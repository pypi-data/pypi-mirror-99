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
from appy.model.fields import Field
from appy.database.operators import in_

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Integer(Field):
    view = cell = Px('''
     <x>::field.getInlineEditableValue(o, value, layout, name=name)</x>
     <input type="hidden" if="masterCss"
            class=":masterCss" value=":value" name=":name" id=":name"/>''')

    edit = Px('''
     <input type="text" id=":name" name=":name" size=":field.width"
            maxlength=":field.maxChars" readonly=":field.isReadonly(o)"
            value=":field.getInputValue(inRequest, requestValue, value)"
            style=":'text-align: %s' % field.alignOnEdit"
            autocomplete=":field.autoComplete and 'on' or 'off'"/>

     <script if="hostLayout" var2="x=o.Lock.set(o, user, field=field)">:\
      'prepareForAjaxSave(%s,%s,%s,%s)' % \
       (q(name), q(o.iid), q(o.url), q(hostLayout))</script>''')

    search = Px('''
     <!-- From -->
     <label lfor=":widgetName">:_('search_from')</label> 
     <input type="text" name=":widgetName" maxlength=":field.maxChars"
            value=":field.sdefault[0]" size=":field.swidth"/>
     <!-- To -->
     <x var="toName='%s_to' % name">
      <label lfor=":toName">:_('search_to')</label> 
      <input type="text" name=":toName" maxlength=":field.maxChars"
             value=":field.sdefault[1]" size=":field.swidth"/>
     </x><br/>''')

    @classmethod
    def inRange(class_, o, range, value):
        '''Is p_value within p_range ? If no, returns a translated message'''
        # p_range must be expressed as a tuple (min, max) or an object having
        # attributes "min" and "max".
        if isinstance(range, tuple):
            min, max = range
        else:
            min = range.min
            max = range.max
        if (value < min) or (value > max):
            r = o.translate('range_ko', mapping={'min': min, 'max': max})
        else:
            r = True
        return r

    def __init__(self, validator=None, multiplicity=(0,1), default=None,
      defaultOnEdit=None, show=True, page='main', group=None, layouts=None,
      move=0, indexed=False, mustIndex=True, indexValue=None,
      emptyIndexValue=None, searchable=False, readPermission='read',
      writePermission='write', width=5, height=None, maxChars=13, colspan=1,
      master=None, masterValue=None, focus=False, historized=False,
      mapping=None, generateLabel=None, label=None, sdefault=('',''),
      scolspan=1, swidth=None, sheight=None, persist=True, inlineEdit=False,
      view=None, cell=None, edit=None, xml=None, translations=None,
      readonly=False, alignOnEdit='left', autoComplete=True):
        # If attribute "readonly" is True (or stores a method returning True),
        # the rendered input field, on edit layouts, will have attribute
        # "readonly" set.
        self.readonly = readonly
        # On "edit", the alignment of the number encoded in the value can be
        # "left", "right" or "center".
        self.alignOnEdit = alignOnEdit
        # Activate or not browser's field auto-completion
        self.autoComplete = autoComplete
        # Call the base constructor
        Field.__init__(self, validator, multiplicity, default, defaultOnEdit,
          show, page, group, layouts, move, indexed, mustIndex, indexValue,
          emptyIndexValue, searchable, None, readPermission, writePermission,
          width, height, maxChars, colspan, master, masterValue, focus,
          historized, mapping, generateLabel, label, sdefault, scolspan, swidth,
          sheight, persist, inlineEdit, view, cell, edit, xml, translations)
        # Define the corresponding Python type for values stored for this type
        self.pythonType = int
        # Define the filter PX when appropriate
        if self.indexed:
            self.filterPx = 'pxFilterText'

    def getFormattedValue(self, o, value, layout='view', showChanges=False,
                          language=None):
        return '' if self.isEmptyValue(o, value) else str(value)

    def replaceSeparators(self, value):
        '''While integer values include no separator, sub-classes (like Float)
           may have it. This method replaces separators in such a way that
           p_value can be a valid Python literal value.'''
        return value

    def validateValue(self, o, value):
        # Replace separators when relevant
        value = self.replaceSeparators(value)
        try:
            value = self.pythonType(value)
        except ValueError:
            return o.translate('bad_%s' % self.pythonType.__name__)

    def isSortable(self, inRefs=False):
        '''Can this field be sortable ?'''
        return True if inRefs else Field.isSortable(self) # Sortable in Refs

    def getStorableValue(self, o, value, complete=False):
        if not self.isEmptyValue(o, value):
            value = self.replaceSeparators(value)
            return self.pythonType(value)

    def searchValueIsEmpty(self, req):
        '''Is there a search value or interval specified in p_form for this
           field ?'''
        # The base method determines if the "from" search field is empty
        isEmpty = Field.searchValueIsEmpty
        # We consider the search value being empty if both "from" and "to"
        # values are empty.
        return isEmpty(self, req) and \
               isEmpty(self, req, widgetName='%s_to' % self.name)

    def getSearchValue(self, req, value=None):
        '''Converts the raw search value from p_req into a single or an
           interval of typed values.'''
        # Get the "from" value
        value = Field.getSearchValue(self, req, value=value)
        index = self.getIndexType(True)
        if value:
            value = self.pythonType(value)
        # Get the "to" value
        toValue = Field.getSearchValue(self, req, '%s_to' % self.name)
        if toValue:
            toValue = self.pythonType(toValue)
        # Return an interval, excepted if both values are the same
        if value != toValue:
            r = in_(value, toValue)
        else:
            r = value
        return r
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
