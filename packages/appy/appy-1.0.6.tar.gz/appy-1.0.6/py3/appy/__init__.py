'''Appy is the simpliest way to build complex webapps'''

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
import pathlib
# Store here the path to the Appy root package, it is often requested
path = pathlib.Path(__file__).parent

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Config:
    '''Root of all configuration options for your app'''

    # These options are those managed by the app developer: they are not meant
    # to be edited during the app lifetime by end users. For such "end-user"
    # configuration options, you must extend the appy.model.tool.Tool class,
    # designed for that purpose. In short, this Config file represents the "RAM"
    # configuration, while the unique appy.model.tool.Tool instance within every
    # app contains its "DB" configuration.

    # In your app/__init__.py, create a class named "Config" that inherits from
    # this one and will override some of the atttibutes defined here, ie:

    # import appy
    # class Config(appy.Config):
    #     someAttribute = "someValue"

    # If "someAttribute" is not a standard Appy attribute, this is a way to add
    # your own configuration attributes.

    # If you want to modify existing attributes, like model configuration or
    # user interface configuration (that, if you have used appy/bin/make to
    # generate your app, are already instantiated in attributes "model" and
    # "ui"), after the attribute definition, modify it like this:

    # class Config(appy.Config):
    #     ...
    #     ui.languages = ('en', 'fr')
    #     model.rootClasses = ['MyClass']

    # Place here a appy.server.Config instance defining the configuration
    # of the Appy HTTP server.
    server = None
    # Place here a appy.server.guard.Config instance defining security options
    security = None
    # Place here a appy.database.Config instance defining database options
    database = None
    # Place here a appy.database.log.Config instance defining logging options
    log = None
    # Place here a appy.model.Config instance defining the application model
    model = None
    # Place here a appy.ui.Config instance defining user-interface options
    ui = None
    # When using a SMTP mail server for sending emails from your app, place an
    # instance of class appy.utils.mail.Config in the field below.
    mail = None
    # Place here a appy.server.scheduler.Config instance, defining cron-like
    # actions being automatically triggered.
    jobs = None
    # Place here an instance of appy.server.backup.Config if you want to backup
    # data and logs from a Appy site.
    backup = None
    # Place here a appy.deploy.Config instance defining how to deploy this app
    # on distant servers.
    deploy = None
    # When using Google analytics, specify here the Analytics ID
    googleAnalyticsId = None
    # When using Ogone, place an instance of appy.model.fields.ogone.Config in
    # the field below.
    ogone = None
    # When using POD fields for producing documents with appy.pod, place here an
    # instance of appy.model.fields.pod.Config
    pod = None
    # When the app has an extension, the name of this latter will be stored
    # in the following attribute. Do not set it directly: it must be done via
    # method m_declareExt below. If you use script appy/bin/make to create an
    # ext, a call to declareExt will be present in the generated ext's
    # __init__.py file.
    ext = None
    # An Appy site may communicate with peer sites. Defining peer sites is done
    # by placing, in the following attribute, an instance of appy.peer.Config.
    peers = None

    @classmethod
    def declareExt(class_, path):
        '''Declares an extension to this app, whose path is p_path'''
        name = path.name
        class_.ext = name
        # Add the ext's "static" folder to the static map
        class_.server.static.map[name] = path / 'static'

    @classmethod
    def check(self):
        '''Ensures the config is valid. Called at server startup'''
        self.server.check()
        self.server.static.check()
        self.security.check()
        if self.jobs:
            self.jobs.check()
        if self.backup:
            self.backup.check()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
