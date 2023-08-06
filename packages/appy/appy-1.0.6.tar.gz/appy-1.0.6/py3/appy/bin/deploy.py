#!/usr/bin/python3

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
from pathlib import Path
from appy.bin import Program
from appy.deploy import Deployer

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Deploy(Program):
    '''This program allows to deploy apps in sites on distant servers'''

    # Available commands
    COMMANDS = {'list':    'Lists the available targets.',
                'info':    'Retrieve info about the target OS',
                'install': 'Install required dependencies via the OS ' \
                           'package system (currently: "apt" only).',
                'site':    'Create an Appy site on the target.',
                'update':  'Updates a site and (re)start it.',
                'view':    "View app.log's tail on the target"
    }

    def helpCommands(COMMANDS):
        '''Builds the text describing available commands'''
        r = []
        for command, text in COMMANDS.items():
            r.append('"%s": %s' % (command, text))
        return '\n'.join(r)

    # Help messages
    HELP_APP     = 'The path, on this machine, to the app to deploy ' \
                   '(automatically set if called from <site>/bin/deploy).'
    HELP_SITE    = 'The path, on this machine, to the reference site ' \
                   '(automatically set if called from <site>/bin/deploy).'
    HELP_COMMAND = 'The command to perform. Available commands are: %s' % \
                   helpCommands(COMMANDS)
    HELP_TARGET  = 'The target to deploy to. By default, target "default" ' \
                   'will be chosen.'

    # Error messages
    FOLDER_KO    = '%s does not exist or is not a folder.'
    COMMAND_KO   = 'Command "%s" does not exist.'

    def defineArguments(self):
        '''Define the allowed arguments for this program'''
        parser = self.parser
        # Positional arguments
        parser.add_argument('app', help=Deploy.HELP_APP)
        parser.add_argument('site', help=Deploy.HELP_SITE)
        parser.add_argument('command', help=Deploy.HELP_COMMAND)
        # Optional arguments
        parser.add_argument('-t', '--target', dest='target',
                            help=Deploy.HELP_TARGET)

    def analyseArguments(self):
        '''Check and store arguments'''
        args = self.args
        # Check and get the paths to the app and site
        for name in ('app', 'site'):
            path = Path(getattr(args, name))
            if not path.is_dir():
                self.exit(self.FOLDER_KO % path)
            setattr(self, name, path)
        self.command = args.command
        if self.command not in Deploy.COMMANDS:
            self.exit(self.COMMAND_KO % self.command)
        self.target = args.target

    def run(self):
        return Deployer(self.app, self.site, self.command, self.target).run()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__': Deploy().run()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
