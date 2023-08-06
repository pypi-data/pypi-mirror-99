'''Create or update translation "po" files for an app'''

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
import sys, collections

from appy.tr import po
from appy import Config
from appy.model.utils import Object as O
from appy.model import Config as ModelConfig

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
WRONG_APP_NAME = 'Your app is named "%s", which is not allowed.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Migrator:
    '''Migrate po(t) files from the Appy 0.9.x format to Appy 1.x format'''

    @staticmethod
    def mustMigrate(updater):
        '''Are i18n files loaded in the p_updater to the Appy 0.9.x format ?'''
        files = updater.translationFiles
        if 'Custom.pot' in files: return # There was no Custom.pot in Appy 0.9.x
        potName = '%s.pot' % updater.appName
        if potName not in files: return # There is no file at all
        pot = files[potName]
        projectName = pot.headers['Project-Id-Version'].value
        # Appy 0.9 did not insert prefix "Appy-" for this header value
        return not projectName.startswith('Appy-')

    def __init__(self, updater):
        self.updater = updater
        # Unwrap some useful updater attributes here
        self.files = updater.translationFiles
        self.appName = updater.appName
        self.model = updater.model
        # Build a dict mapping workflow prefixes in use in Appy 0.9 and
        # workflow names.
        r = {}
        for workflow in self.model.workflows.values():
            # This prefix was used, in Appy 0.9, for all i18n messages related
            # to this workflow.
            moduleName = workflow.python.__module__.split('.')[0]
            oldPrefix = '%s_%s_%s_' % (self.appName, moduleName, workflow.name)
            r[oldPrefix.lower()] = '%s_' % workflow.name
        self.workflowNames = r

    def removeSearchPart(self, id):
        '''With Appy 0.9, label parts contained some part named "search".
           With Appy 1.0, it is not the case anymore.'''
        # With Appy 1.0, searches do not have prefix "search" anymore: their
        # labels are similar to field labels.
        id = id.replace('_search_', '_')
        # With Appy 1.0, group labels are the same, be they search or field
        # groups.
        id = id.replace('_searchgroup_', '_group_')
        return id

    def migrateMessage(self, message):
        '''Converts 0.9 p_message into a 1.0 one and return this latter'''
        id = message.id
        # Check first if this m_message is related to a workflow
        for prefix, name in self.workflowNames.items():
            if id.startswith(prefix):
                id = id.replace(prefix, name)
                message.id = id
                return message
        if id.startswith('%s_' % self.appName):
            # The ID starts with a class "package name" of the form
            #               "<appName>_<moduleName>_<className>"
            # With Appy 1.x, this prefix is simply replaced with
            #                         "<className>"
            # Indeed, it is now possible because Appy 1.0 classes and workflows
            # must all have a unique name, even if put in different modules.
            id = id.split('_', 2)[2]
            id = self.removeSearchPart(id)
        else:
            # In Appy 0.9, labels for over classes start with
            #                "<appName><baseClassName>"
            # In Appy 1.0, such labels simply start with
            #                     "<baseClassName>"
            for name in self.model.baseClasses:
                prefix = '%s%s_' % (self.appName, name)
                if id.startswith(prefix):
                    id = id.replace(prefix, '%s_' % name)
                    id = self.removeSearchPart(id)
                    break
        # Set the potentially modified ID to the p_message and return it
        message.id = id
        # Replace old-fashioned carriage returns with a simple "\n" in message
        # content and default value.
        for attribute in ('msg', 'default'):
            value = getattr(message, attribute)
            if value:
                value = value.replace('<br/><br/>', '\\n')
                setattr(message, attribute, value)
        return message

    def migrateFiles(self):
        '''Performs the migration'''
        # The files to add in it after the migration
        filesToAdd = {}
        # Browse all translation files
        trFolder = self.updater.trFolder
        for name, poFile in self.files.items():
            # Extract all messages starting with ('custom_'), remove their
            # prefix and store them in a separate collection.
            customMessages = collections.OrderedDict()
            # Put any other message in "otherMessages"
            otherMessages = collections.OrderedDict()
            for id, message in poFile.messages.items():
                if id.startswith('custom_'):
                    message.id = id[7:]
                    customMessages[message.id] = message
                else:
                    message = self.migrateMessage(message)
                    otherMessages[message.id] = message
            # Add the corresponding "Custom" file in "filesToAdd"
            fileName = 'Custom.pot' if '-' not in name \
                                    else 'Custom-%s' % name.split('-', 1)[1]
            filesToAdd[fileName] = po.File(trFolder / fileName,
                                           messages=customMessages)
            # Replace poFile's message with the remaining, migrated messages
            poFile.messages = otherMessages
            # Set the "Appy 1.0" header
            poFile.headers['Project-Id-Version'].value = 'Appy-%s'% self.appName
        # Add "filesToAdd" in "files"
        for name, poFile in filesToAdd.items(): self.files[name] = poFile

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Updater:
    '''Creates or updates translation files for an app'''
    # The updater is implemented as a visitor walking a appy.model.Model
    # instance and producing the appropriate i18n labels for every model
    # element. For every such element, a method named "visit<element>" is
    # defined hereafter.

    # Default value for "confirm" labels
    CONFIRM = 'Are you sure ?'
    unallowedAppNames = ('custom', 'appy')

    def __init__(self, trFolder):
        # The "tr" sub-folder in the app. Create it if it does not exist.
        self.trFolder = trFolder
        # The app folder
        self.appFolder = trFolder.parent
        self.appName = self.appFolder.name
        if self.appName.lower() in Updater.unallowedAppNames:
            # This would clash with the translation file named Custom.pot
            raise Exception(WRONG_APP_NAME % self.appName)
        # The list of i18n labels to generate
        self.labels = collections.OrderedDict()
        # Load the model in order to get all classes, fields, workflows, states
        # and transitions for which i18n labels must be created.
        appPath = self.appFolder / '__init__.py'
        sys.path.append(str(self.appFolder.parent))
        self.config = __import__(self.appFolder.name).Config
        modelConfig = ModelConfig()
        modelConfig.set(self.appFolder)
        self.model = modelConfig.get(self.config, appOnly=True)
        # Load translation files (.po and .pot) within the "tr" folder
        self.translationFiles = po.load(trFolder)

    def addLabel(self, id, default, nice=True):
        '''Adds a label with this p_id and p_default value in self.labels'''
        self.labels[id] = po.Message(id, '', default, niceDefault=nice)

    def mustGenerateLabels(self, field):
        '''Must i18n labels be generated for p_field ?'''
        # Generating i18n labels for p_field (from a class or inner field) must
        # not be done if it uses another field's labels or if it uses custom
        # translations.
        return not field.label and not field.translations

    def visitGroup(self, class_, group, walkedGroups):
        '''Produce labels for p_group, found in p_class_ on a search or on a
           field. p_group may itself be in another group, for which labels must
           be generated, too. This recursion may continue at any level.'''
        # Do nothing if p_group is None or if labels have already been generated
        # for him.
        if not group or (group in walkedGroups): return
        if not group.label:
            # Compute the prefix used as base label for all labels to produce
            label = '%s_group_%s' % (class_.name, group.name)
            add = self.addLabel
            if group.hasLabel: add(label, group.name)
            if group.hasDescr: add('%s_descr' % label, ' ', nice=False)
            if group.hasHelp:  add('%s_help'  % label, ' ', nice=False)
            if group.hasHeaders:
                for i in range(group.nbOfHeaders):
                    add('%s_col%d' % (label, i+1), ' ', nice=False)
        # Visit group's parent
        walkedGroups.add(group)
        self.visitGroup(class_, group.group, walkedGroups)

    def visitSelect(self, class_, field, label):
        '''Generate Select-specific labels'''
        if type(field.validator) in (list, tuple):
            # The list of possible values is fixed. Generate one label for
            # every value.
            for value in field.validator:
                self.addLabel('%s_list_%s' % (label, value), value)

    def visitBoolean(self, class_, field, label):
        '''Generate Boolean-specific labels'''
        if field.render == 'radios':
            for v in ('true', 'false'):
                self.addLabel('%s_%s' % (label, v), field.yesNo[v])

    def visitAction(self, class_, field, label):
        '''Generate Action-specific labels'''
        if field.confirm:
            self.addLabel('%s_confirm' % label, self.CONFIRM, nice=False)
    visitPod = visitAction # Same labels for Pod field

    def visitRef(self, class_, field, label):
        '''Generate Ref-specific labels'''
        # Add the label for the confirm message when relevant
        if field.addConfirm:
            self.addLabel('%s_addConfirm' % label, self.CONFIRM, nice=False)

    def visitList(self, class_, field, label):
        '''Generate List-specific labels'''
        # Generate labels for sub-fields
        walkedGroups = set()
        for name, sub in field.fields:
            if not self.mustGenerateLabels(sub): continue
            # We set "forceLabel" to True because we need a label to dump for
            # every sub-field, within List' column headers.
            subLabel = '%s_%s' % (label, name)
            self.visitField(class_, sub, subLabel, walkedGroups,forceLabel=True)
    visitDict = visitList # Same labels for Dict field

    def visitCalendar(self, class_, field, label):
        '''Generate Calendar-specific labels'''
        eTypes = field.eventTypes
        if type(eTypes) not in (list, tuple): return
        for et in eTypes:
            self.addLabel('%s_event_%s' % (label, et), et)

    def visitSwitch(self, class_, field, label):
        '''Generate Switch-specific labels'''
        walkedGroups = set()
        for fieldset, fields in field.fields:
            for name, sub in fields:
                if not self.mustGenerateLabels(sub): continue
                subLabel = '%s_%s' % (class_.name, name)
                self.visitField(class_, sub, subLabel, walkedGroups,
                                forceLabel=True)

    def visitField(self, class_, field, label, walkedGroups, forceLabel=False):
        '''Generate labels for p_field. All labels will have a common prefix
           (p_label), that includes the class name and, potentially, the name of
           some outer field if p_field is an inner field.'''
        add = self.addLabel
        # Add a label for the field name when relevant
        if forceLabel or field.hasLabel or field.generateLabel:
            # Take care of sub-fields containing stars in their name
            name = field.name
            default = name.rsplit('*', 1)[-1] if '*' in name else name
            add(label, default)
        # A longer description and a help text
        if field.hasDescr: add('%s_descr' % label, ' ', nice=False)
        if field.hasHelp:  add('%s_help' % label, ' ', nice=False)
        # Generate additional labels via a field-specific "visit" method, when
        # relevant.
        method = getattr(self, 'visit%s' % field.type, None)
        if method: method(class_, field, label)
            
    def visitSearch(self, class_, search, walkedGroups):
        '''Produce labels for a p_search in a p_class_'''
        # One label for the search name and one for a longer description
        label = '%s_%s' % (class_.name, search.name)
        self.addLabel(label, search.name)
        self.addLabel('%s_descr' % label, ' ', nice=False)
        # Produce labels for the group when relevant
        self.visitGroup(class_, search.group, walkedGroups)

    def visitPhase(self, class_, phase):
        '''Produce labels for a p_phase (and inner pages) in a p_class_'''
        # Produce the label for this p_phase, excepted if it is the only phase
        # in the p_class_.
        if len(class_.phases) != 1:
            self.addLabel('%s_phase_%s' % (class_.name, phase.name), phase.name)
        # Produce one label for every page
        for page in phase.pages.values():
            if page.label is None:
                self.addLabel('%s_page_%s' % (class_.name,page.name), page.name)

    def visitClass(self, name, class_):
        '''Produce labels for a p_class_'''
        # Produce base labels for the class name (singular and plural), but
        # only for not-over classes.
        if class_.type == 'app':
            # Class name, singular and plural
            self.addLabel(name, name, nice=False)
            self.addLabel('%s_plural' % name, name + 's', nice=False)
        # While walking fields and searches, groups will be encountered. In
        # order to avoid generating labels several times for the same group,
        # remember the already walked groups.
        walkedGroups = set()
        # Produce labels for every search defined on this p_class_
        for search in class_.searches.values():
            self.visitSearch(class_, search, walkedGroups)
        # Produce labels for every field defined on this p_class_
        for field in class_.fields.values():
            # For some fields, labels must not be produced
            if self.mustGenerateLabels(field):
                label = '%s_%s' % (name, field.name)
                self.visitField(class_, field, label, walkedGroups)
            # Produce labels for the field's group(s) when relevant
            for group in field.getGroups():
                self.visitGroup(class_, group, walkedGroups)
        # Produce labels for phases and pages. If the class is "over", some
        # pages and phases are thus already defined. From the moment the user
        # adds at least one field to an existing page or phase, we consider it
        # gives him the right to rename the page and phase and we generate a
        # label for it, that will override the existing label from Appy.pot.
        for phase in class_.phases.values():
            self.visitPhase(class_, phase)

    def visitWorkflow(self, name, workflow):
        '''Produce labels for a p_class_'''
        add = self.addLabel
        # Generate a label for every state and transition
        for attribute in workflow.attributes:
            for element in getattr(workflow, attribute).values():
                label = '%s_%s' % (name, element.name)
                add(label, element.name)
                # Add a label for a transition that must be confirmed
                if (attribute == 'transitions') and element.confirm:
                    add('%s_confirm' % label, self.CONFIRM, nice=False)

    def collectLabels(self):
        '''Collect all labels by visiting model elements'''
        model = self.model
        # Add a label for every role
        for role in model.getRoles(base=None):
            self.addLabel(*role.getLabel(withDefault=False))
        # Browse model classes
        for name, class_ in model.classes.items():
            if class_.type != 'base':
                self.visitClass(name, class_)
        # Browse model workflows
        for name, workflow in model.workflows.items():
            self.visitWorkflow(name, workflow)

    def updateFiles(self):
        '''Update po(t) files based on p_self.labels. Every file that does not
           exist is created.'''
        # 2 "pot" files exist (or will exist in a few milliseconds) in
        # p_self.trFolder, with their corresponding "po" files (one per
        # supported language):
        # ----------------------------------------------------------------------
        # <appName>.pot | will contain all i18n labels automatically managed by
        #               | Appy and that were collected in p_self.labels;
        #  Custom.pot   | will contain all additional labels managed "by hand"
        #               | by the app's developer.
        # ----------------------------------------------------------------------
        counts = {True: 0, False: 0} # Count automatic and custom labels
        for pot in ('%s.pot' % self.appName, 'Custom.pot'):
            isCustom = pot == 'Custom.pot'
            # Get or create the pot file
            if pot not in self.translationFiles:
                potFile = self.trFolder / pot
                self.translationFiles[pot] = po.File(potFile)
            pot = self.translationFiles[pot]
            # Update the app's pot file with p_self.labels
            if not isCustom:
                moves = pot.update(self.labels, removeNotNew=True,
                                   keepOrder=False)
                for move in ('added', 'removed'):
                    elems = getattr(moves, move)
                    if elems:
                        print('%s - %d %s message(s): %s.' % \
                             (pot.path.name, len(elems), move, ','.join(elems)))
            pot.generate()
            # Create or update one "po" file for every language supported by the
            # app.
            labels = pot.messages if isCustom else self.labels
            counts[isCustom] = len(labels)
            for language in self.config.ui.languages:
                poName = pot.getPoFileName(language)
                if poName not in self.translationFiles:
                    poFile = self.trFolder / poName
                    self.translationFiles[poName] = po.File(poFile)
                poFile = self.translationFiles[poName]
                poFile.update(labels, removeNotNew=True, keepOrder=False)
                poFile.generate()
        # Output a summary about the operation
        total = counts[True] + counts[False]
        print('Translation files updated - %d labels (%d automatic + %d ' \
              'custom) - %d language(s).' % (total, counts[False], counts[True],
                                             len(self.config.ui.languages)))

    def run(self):
        '''Create or update translation files in p_self.appFolder'''
        # Collect, in p_self.labels, all translation labels to generate, by
        # visiting the app's model.
        self.collectLabels()
        # Create or update translation files accordingly. As a preamble, if
        # their format is still the one from Appy 0.9, migrate them.
        if Migrator.mustMigrate(self):
            Migrator(self).migrateFiles()
        self.updateFiles()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
