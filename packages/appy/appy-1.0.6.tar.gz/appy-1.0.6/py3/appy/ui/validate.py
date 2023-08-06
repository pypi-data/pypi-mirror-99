'''Validation-related stuff'''

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
from appy.utils import string as sutils
from appy.model.utils import Object as O

# Errors - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
FIELD_NOT_FOUND = 'field %s::%s was not found.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Validator:
    '''Class responsible for validating data encoded by the user in the UI'''    

    # PX rendering the "yellow box" containing validation errors
    pxErrors = Px('''
     <table class="small" width="100%">
      <tr><th>:_('field_name')</th><th>:_('error_name')</th></tr>
      <tr for="labels, message in validator.getGroupedErrors()">
       <td>::labels</td><td>::message</td></tr>
     </table>''')

    def __init__(self, o, saveConfirmed):
        # A validator is created every time an p_o(bject) is created or updated
        # from the UI via a web form.
        self.o = o
        self.req = o.req
        # The (sub/standard/switch) fields whose widgets have received data from
        # the UI.
        self.fields = []
        self.fieldsByName = {}
        # The field values extracted from the request and converted
        self.values = O() # ~{O(s_fieldName=fieldValue)}~
        # When validation errors are encountered, they are stored in the
        # following dict. For example, if an error occurs on field named
        # "field1", an entry at key "field1" will be stored on this instance,
        # holding the translated error message.
        self.errors = O() # ~{O(s_fieldName=s_errorMessage)}~
        # The standard translated error message
        self.errorMessage = o.translate('validation_error')
        # If a confirmation was requested, has it already be done ?
        self.saveConfirmed = saveConfirmed

    def intraFieldValidation(self, fields=None):
        '''This method performs field-specific validation for every field from
           the page being created or edited. For every field whose validation
           generates an error, we add an entry in p_self.errors. For every
           field, we add in p_self.values an entry with the "ready-to-store"
           field value.

           Il p_fields are given, we use them instead of getting currently
           edited fields on the current page for p_self.o. ie, p_fields can be
           fields from a switch.
        '''
        o = self.o
        page = self.req.page or 'main'
        # Browse p_o's fields
        for field in o.getFields('edit', page, fields=fields):
            if not field.validable or not field.isClientVisible(o): continue
            value = field.getRequestValue(o)
            # Perform individual field validation
            message = field.validate(o, value)
            if message:
                self.errors[field.name] = message
            else:
                self.values[field.name] = field.getStorableValue(o, value)
            # Store this field
            self.fields.append(field)
            self.fieldsByName[field.name] = field
            # Validate inner fields within outer fields
            if field.outer: field.subValidate(o, value, self.errors)
            # Validate fields inside switch fields
            if field.type == 'Switch':
                fieldset, subFields = field.getChosenFields(o, fieldset=value)
                if subFields:
                    self.intraFieldValidation(fields=subFields)

    def interFieldValidation(self):
        '''This method is called when individual validation of all fields
           succeeds (when editing or creating an object, see
           m_intraFieldValidation). Then, this method performs inter-field
           validation. This way, the user must first correct individual fields
           before being confronted to potential inter-field validation
           errors.'''
        o = self.o
        if not hasattr(o, 'validate'): return
        msg = o.validate(self.values, self.errors)
        # Those custom validation methods may have added fields in the given
        # p_errors object. Within this object, for every error message that is
        # not a string, we replace it with the standard validation error for the
        # corresponding field.
        for k, v in self.errors.d().items():
            if not isinstance(v, str):
                self.errors[k] = o.translate('field_invalid')
        return msg

    def addMessage(self, r, messages, label, message):
        '''Used by m_getGroupedErrors, this method adds, in p_r, the error
           p_message about a field whose label is p_label. Indexes of messages
           already stored in p_r are in dict p_messages.'''
        if message in messages:
            # We have already encountered this message
            r[messages[message]][0] += '<br/>%s' % label
        else:
            r.append([label, message])
            messages[message] = len(r) - 1

    def getGroupedErrors(self):
        '''Returns the list of all errors, grouped by message: if the same error
           message concerns several fields, a single entry is inserted in the
           list.'''
        o = self.o
        _ = o.translate
        # A list of tuples (labels, message): "labels" being the list of field
        # labels whose error is described in "message".
        r = []
        # Remember, for every message stored in p_r, its index
        messages = {} # ~{s_message: i_index}~
        # Walk fields in the order of their definition, via self.fields
        for field in self.fields:
            # Is there an error for this field ?
            message = self.errors.get(field.name)
            if not message: continue
            label = _('label', field=field)
            self.addMessage(r, messages, label, message)
        # Add summarized messages for compound fields
        compound = []
        summaryMessage = _('validation_sub_error')
        for name, message in self.errors.d().items():
            # Ignore already-managed, not-compound fields
            if '*' not in name: continue
            name = name.split('*', 1)[0]
            # Ignore already-encountered compound (sub-)fields
            if name in compound: continue
            compound.append(name)
            # Get the label for this compound field
            field = self.fieldsByName.get(name)
            if not field:
                label = name
                o.log(FIELD_NOT_FOUND % (o.class_.name, name), type='error')
            else:
                label = _('label', field=field)
            self.addMessage(r, messages, label, summaryMessage)
        return r

    def gotoEdit(self):
        '''Brings the user to the edit page for p_self.o. This method takes care
           of not carrying any password value. Unlike m_goto above, there is no
           HTTP redirect here: we execute directly PX "edit" and we return the
           result.'''
        o = self.o
        page = self.req.page or 'main'
        for field in o.getFields('edit', page):
            if field.type == 'Password':
                self.req[field.name] = ''
        return o.edit(o.H().traversal.createContext('edit'))

    def run(self):
        '''Runs all validation steps'''
        o = self.o
        # Trigger field-specific validation
        self.intraFieldValidation()
        if self.errors:
            o.say(self.errorMessage)
            return self.gotoEdit()

        # Trigger inter-field validation
        msg = self.interFieldValidation() or self.errorMessage
        if self.errors:
            o.say(msg)
            return self.gotoEdit()

        # Before saving data, must we ask a confirmation by the user ?
        if not self.saveConfirmed and hasattr(o, 'confirm'):
            msg = o.confirm(self.values)
            if msg:
                self.req.confirmText = msg.replace("'", "\\'")
                return self.gotoEdit()

    @classmethod
    def getJsErrors(class_, handler):
        '''Generates the definition of a JavaScript associative array
           containing all errors collected in p_handler.validator.errors.'''
        validator = handler.validator
        if validator and validator.errors:
            array = sutils.getStringFrom(validator.errors.d())
        else:
            array = 'null'
        return 'var errors = %s;' % array
# ------------------------------------------------------------------------------
