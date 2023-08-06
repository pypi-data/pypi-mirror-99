'''This file is responsible for perfoming the backup of a Appy site.'''

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
import time, shutil
from pathlib import Path

from DateTime import DateTime

from appy.pod import formatsByTemplate
from appy.model.utils import Object as O
from appy.utils import executeCommand, Traceback
from appy.utils.path import getShownSize, getOsTempFolder

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# If you want to configure the backup of your Appy server, place, in the main
# config's "backup" attribute, an instance of the Config class as defined below.

# Moreover, you'll have to define a job, in your main config's "jobs" attribute,
# defined with the tool method named "backup", in order to enable the backup, at
# the desired frequency and planning. For more information about jobs, check
# appy/server/scheduler.py.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
PATH_KO    = 'Backup config: folder "%s" does not exist. Please create it.'
BKP_DIS    = 'Backup cannot take place unless you configure it in ' \
             'config.backup.'
BKP_TYPE   = 'Backup type: %s (full is @%s).'
CMD        = 'Running: %s...'
DONE       = "Done in %.2f''."
S_SIZE     = 'Source file size is %s.'
PACKING    = 'Packing %s (%s)...'
COPY_LOG   = 'Copy %s to %s.'
DETAILS    = "\nMore details to be found in site's app.log file."
DELETED    = 'Deleted from %s: %s'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Config:
    '''Backup configuration'''

    def __init__(self):
        # The (absolute) folder where to store backup files. It must exist. Appy
        # will create 3 sub-folders in it:
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # zodb  | will store copies of the appy.fs file (or named differently if
        #       | you have changed the default naming convention). 2 copies will
        #       | be created: backup1.fs and backup2.fs. Everytime the backup is
        #       | launched, it will copy appy.fs to the less recent version
        #       | among these 2 files. That way, if the copy crashes, there is
        #       | always an intact copy in the "zodb" folder.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # files | will store a copy of the DB-controlled file system
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # logs  | will create a backup of log files app.log and site.log
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # If attribute "path" is None, the backup is considered to be disabled.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.path = None

        # Just before and after having copied data and logs to p_self.path, 2
        # commands may be executed. This is typically used to mount/unmount
        # p_self.path if it located on a network drive. Please specify each
        # command as a list: the first element being the name of the command,
        # the subsequent ones being args.
        self.beforeCommand = None
        # Example: ['mount', '-t', 'cifs', '//some/server', '/mnt/backup']
        self.afterCommand = None
        # Example: ['umount', '/mnt/backup']

        # The list of email recipients that will receive an email containing
        # details about the backup procedure.
        self.emails = []

        # The name of the day corresponding to a full backup, as a string that
        # can be: Mon, Tue, Wed, Thu, Fri, Sat, Sun or All. A full backup
        # distinguishes itself from a standard backup by adding:
        # - a database "pack". The ZODB stores any change made to data.
        #   "Packing" it removes previous versions of objects for which a more
        #   recent version is found. It can substantially reduce the database
        #   size.
        # - a backup of the log files. app.log and site.log are copied to the
        #   backup folder and emptied.

        # On Appy sites with a high lever of write operations, the database may
        # grow in size very quickly. In that case, it may be appropriate to
        # perform a "full" backup everyday, by using value "All".
        self.fullDay = 'Sun'

        # The following attributes stores the name of a method on the tool that
        # the backup will call after the backup procedure has been executed. You
        # could also directly define a job with this method, but by specifying
        # it here, it allows you to define a unique "backup" job, that will
        # perform the backup + run your nightlife actions.

        # Pay attention to this method: if it raises an error, the whole backup
        # job will be canceled, in order to avoid committing partial results.
        self.method = None

        # Files produced by LibreOffice in server mode, asked by the Appy
        # server, may still be in the OS temp folder. Files whose extensions are
        # listed here will be removed from the OS temp folder.
        exts = ()
        for formats in formatsByTemplate.values():
            exts += formats
        self.tempExtensions = exts

        # Must the Appy server restart at the end of the job ? If you want to
        # enable this, set an integer value representing the number of seconds
        # to wait before restarting the server. This is required to let the
        # server terminate his ongoing transaction.
        self.restart = 10

    def check(self):
        '''Checks the backup configuration'''
        # If no backup folder is defined, the backup is supposed to be disabled
        path = self.path
        if not path: return
        # Check if the backup folder exists
        path = Path(path)
        if not path.is_dir():
            raise Exception(PATH_KO % self.path)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Backup:
    '''Performs backups'''

    # Options to rsync when copying DB-controlled files
    filesOptions = ['rsync', '-Paz', '--no-o', '--no-g', '--no-l', '--delete',
                    '--quiet', '--exclude', '*.fs*', '--exclude', '*.log']

    # Type of backup: full or not
    type = { True: 'full', False: 'standard' }

    def __init__(self, tool):
        self.tool = tool
        self.config = tool.config.backup
        self.server = tool.H().server
        # All log messages will also be stored in this list, to be sent by email
        self.messages = []

    def isFull(self):
        '''Returns True if the backup must be a full backup'''
        day = self.config.fullDay
        return (day == 'All') or time.asctime().startswith(day)

    def log(self, message):
        '''Logs this m_message and adds it to p_self.messages'''
        self.tool.log(message)
        self.messages.append(message)

    def logDone(self, start):
        '''Logs the "done" message, with the time elapsed since p_start'''
        self.log(DONE % (time.time() - start))

    def runCommand(self, args, text=None):
        '''Runs and logs a commmand made of p_args'''
        start = time.time()
        self.log(CMD % ' '.join(args))
        if text: self.log(text)
        # Run the sync
        out, err = executeCommand(args)
        if err: self.log(err)
        elif out: self.log(out)
        else: self.logDone(start)

    def runMethod(self):
        '''Runs the custom method as defined in the backup config. Returns True
           if the method did not raise an exception.'''
        try:
            method = self.config.method
            start = time.time()
            self.log(CMD % ('tool::%s' % method))
            getattr(self.tool, method)()
            self.logDone(start)
            return True
        except Exception as err:
            self.log(Traceback.get().strip(), type='error')

    def copyDatabase(self):
        '''Copy the .fs file to the <backup folder>/zodb, using rsync'''
        # Create the destination folder if it does not exist
        destFolder = self.config.path / 'zodb'
        if not destFolder.is_dir(): destFolder.mkdir()
        # Get the last modification dates for backup files
        modified1 = modified2 = None
        for backupFile in destFolder.glob('backup*.fs'):
            modified = DateTime(backupFile.stat().st_mtime)
            if backupFile.name == 'backup1.fs':
                modified1 = modified
            elif backupFile.name == 'backup2.fs':
                modified2 = modified
        # Select the file whose modification date is the less recent one
        if modified1 and modified2:
            nb = 1 if modified1 < modified2 else 2
        else:
            nb = 1 if not modified1 else 2
        # Prepare the rsync command
        sourceFile = self.tool.config.database.filePath
        fileSize = getShownSize(sourceFile.stat().st_size)
        args = ['rsync', '--inplace', '--no-whole-file',
                str(sourceFile), str(destFolder / ('backup%d.fs' % nb))]
        # Run the sync
        self.runCommand(args, text=S_SIZE % fileSize)

    def copyFiles(self):
        '''Copy the files from the DB-controlled file system the
           <backup folder>/files, using rsync.'''
        # Create the destination folder if it does not exist
        destFolder = self.config.path / 'files'
        if not destFolder.is_dir(): destFolder.mkdir()
        # Prepare the rsync command
        args = list(self.filesOptions)
        args.append('%s/' % self.tool.config.database.binariesFolder)
        args.append(str(destFolder))
        # Run the sync
        self.runCommand(args)

    def copyLogs(self):
        '''Copy the log files to <backup folder>/logs and empty them'''
        # Create the destination folder if it does not exist
        destFolder = self.config.path / 'logs'
        if not destFolder.is_dir(): destFolder.mkdir()
        # Determine the "date" part to encrust in the name of the backup files
        prefix = DateTime().strftime('%Y_%m_%d_%H_%M')
        # Walk log files
        config = self.tool.config.log
        for logFile in (config.site.path, config.app.path):
            # Determine the name of the target
            destName = '%s.%s.log' % (logFile.stem, prefix)
            destPath = str(destFolder / destName)
            # Launch the copy
            self.log(COPY_LOG % (logFile.name, destPath))
            shutil.copyfile(str(logFile), destPath)
            # Clean the content of the log file
            with open(logFile, 'w'): pass

    def sendMails(self):
        '''Send details about the operation, as stored in p_self.messages, to
           the mail recipients as defined in the backup config.'''
        tool = self.tool
        # Determine a subject for the mail
        subject = 'Appy / %s / Nightlife > %s' % \
                  (tool.config.model.appName, self.config.path)
        # The body is made of messages collected in p_self.messages
        body = '\n'.join(self.messages)
        # Send the mail
        tool.sendMail(self.config.emails, subject, body)

    def cleanTempFiles(self):
        '''Cleans temp files possibly produced by LibreOffice and left in the OS
           temp folder.'''
        # Do nothing if no file extension is configured
        exts = self.config.tempExtensions
        if not exts: return
        # Browse the OS temp folder, looking for files to delete
        tempFolder = Path(getOsTempFolder())
        counts = O()
        for ext in exts:
            count = 0
            for fileName in tempFolder.glob('*.%s' % ext):
                fileName.unlink()
                count += 1
            counts[ext] = count
        # Log deletions
        deleted = ['%s: %d' % (ext, count) for ext, count in counts.d().items()]
        self.log(DELETED % (tempFolder, ' - '.join(deleted)))

    def run(self):
        '''Performs the backup and related tasks'''
        config = self.config
        tool = self.tool
        handler = tool.H()
        # The backup can't be done unless correcty configured
        if not config or not config.path:
            self.log(BKP_DIS, type='warning')
            return
        # Is that a full backup or not ?
        full = self.isFull()
        self.log(BKP_TYPE % (self.type[full], config.fullDay))
        # Execute config.method if defined
        if config.method:
            success = self.runMethod()
            # Stop here if the method produced an error, in order to avoid
            # committing some partial result.
            if not success:
                handler.commit = False
                return
        # config.method may have set handler.commit to False. Force it to True,
        # because in the context of the currently running "backup" job, a commit
        # is always required (a minima, temp objects are removed from the
        # database).
        handler.commit = True
        # Remove temp objects within the database
        database = self.server.database
        logger = self.server.loggers.app
        database.cleanTemp(handler, logger)
        # Remove temp files in the OS temp folder
        self.cleanTempFiles()
        # Pack the database file if requested
        if full: database.pack(logger=logger)
        # Execute the "before command" if defined
        config.beforeCommand: self.runCommand(config.beforeCommand)
        # Copy the database itself (.fs file)
        self.copyDatabase()
        # Copy the files from the DB-controlled file system
        self.copyFiles()
        # Copy the log files when relevant
        if full: self.copyLogs()
        # Execute the "after command" if defined
        config.afterCommand: self.runCommand(config.afterCommand)
        # Send operation details by email when relevant
        self.messages.append(DETAILS)
        if config.emails: self.sendMails()
        # Restart the Appy server if required
        if config.restart: tool.restart(wait=config.restart)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
