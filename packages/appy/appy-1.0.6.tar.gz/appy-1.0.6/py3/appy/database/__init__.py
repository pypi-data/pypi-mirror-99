'''Appy module managing database files'''

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
import os, time, pathlib

from DateTime import DateTime
from zc.lockfile import LockError
from BTrees.IOBTree import IOBTree
from persistent.mapping import PersistentMapping
import ZODB, ZODB.POSException, transaction, transaction.interfaces

from appy.px import Px
from appy.utils import multicall
from appy.database.lock import Lock
from appy.database.lazy import Lazy
from appy.utils import path as putils
from appy.database.catalog import Catalog

# Constants  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
DB_CREATED   = 'Database created @%s.'
DB_NOT_FOUND = 'Database does not exist @%s.'
DB_LOCKED    = 'The database is currently locked (%s)'
DB_CORRUPTED = 'The database @%s is corrupted and probably empty. Please ' \
               'remove it and restart your site.'
DB_PACKING   = 'Packing %s (may take a while)...'
DB_PACKED    = 'Done. Went from %s to %s.'
TMP_STORE_NF = 'Temp store does not exist in %s.'
O_STORE_NF   = 'Object store does not exist in %s.'
TOOL_NF      = 'Tool does not exist in %s.'
METH_NF      = 'Method "%s" does not exist on the tool.'
TMP_STORE_E  = 'No temp object has been deleted in %s.'
TMP_OBJS_DEL = '%s temp object(s) removed.'
O_EXISTS     = 'An object with id "%s" already exists.'
CLASS_NF     = 'Class "%s" does not exist.'
CUS_ID_NO_IK = 'It is not possible to get an ikey for object having a ' \
               'custom ID (%s).'
NEW_TMP_W_ID = 'An ID cannot be specified when creating a temp object.'
CUS_ID_N_STR = 'Custom ID must be a string.'
SRCH_NO_CAT  = 'Invalid operation: there is no catalog for instances ' \
               'of class "%s".'
MISS_O_CLASS = 'Catalog for class "%s": object not found for ID "%s".'
MISS_O       = 'Object not found for ID "%s".'
MISS_IDS_DEL = 'Catalog "%s": ID(s) removed because no corresponding ' \
               'object(s) found: %s.'
FOLDER_DEL   = 'Folder %s deleted and moved to /tmp for object %d (%s).'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Config:
    '''Database-related parameters. The database used by Appy is the Zope Object
       Database (ZODB).'''

    def __init__(self):
        # The path to the .fs file, the main database file
        self.filePath = None
        # The path to the folder containing database-controlled binary files
        self.binariesFolder = None
        # Typically, we have this configuration: within a Appy <site>, we have a
        # folder named "var" containing all database-related stuff: the main
        # database file named appy.fs and the sub-folders containing
        # database-controlled binaries. In this case:
        #   "filePath"       is <site>/var/appy.fs
        #   "binariesFolder" is <site>/var

        # What roles can unlock locked pages ? By default, only a Manager can
        # do it. You can place here roles expressed as strings or Role
        # instances, global or local.
        self.unlockers = ['Manager']
        # Number of times a transaction is retried after a conflict error has
        # occurred.
        self.conflictRetries = 3

    def set(self, folder, filePath=None):
        '''Sets site-specific configuration elements. If filePath is None,
           p_folder will both hold binaries and the database file that will be
           called appy.fs.'''
        self.binariesFolder = pathlib.Path(folder)
        if filePath is None:
            self.filePath = self.binariesFolder / 'appy.fs'
        else:
            self.filePath = pathlib.Path(filePath)

    def getDatabase(self, server, handler, poFiles, method=None):
        '''Create and/or connect to the site's database (as instance of class
           Database), set it as attribute to p_server and perform the task
           linked to p_server.mode.'''
        path = str(self.filePath)
        logger = server.loggers.app
        server.database = None
        # Are we running the server in "classic" mode (fg or bg) ?
        classic = server.mode in ('fg', 'bg')
        if not self.filePath.exists():
            # The database does not exist. For special modes, stop here.
            if not classic:
                logger.error(DB_NOT_FOUND % str(self.filePath))
                return
            # The database will be created - log it
            logger.info(DB_CREATED % path)
            created = True
        else:
            created = False
        # Create or get the ZODB database
        try:
            database = Database(path, server)
        except LockError as err:
            logger.error(DB_LOCKED % str(err))
            return
        server.database = database
        # Perform the appropriate action on this database, depending on server
        # mode.
        if classic:
            # We are starting the server: initialise the database. This is the
            # "initialization" connection, allowing to perform database
            # initialization or update at server startup.
            database.init(created, handler, poFiles)
        elif server.mode == 'clean':
            # Clean the database temp folder and pack it
            database.clean(handler, logger)
        elif server.mode == 'run':
            # Execute method named p_method on the tool
            database.run(method, handler, logger)

    def getDatabaseSize(self, formatted=False):
        '''Returns the database size'''
        r = os.stat(self.filePath).st_size
        return putils.getShownSize(r) if formatted else r

    def getZodbVersion(self):
        '''Gets the version of the ZODB'''
        try:
            import pkg_resources
            r = pkg_resources.get_distribution('zodb').version
        except ImportError:
            r = 'unknown'
        return r

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Database:
    '''Represents the app's database'''

    # Database-specific exception class
    class Error(Exception): pass

    # ZODB exceptions that identify a conflict error
    ConflictErrors = (transaction.interfaces.TransactionFailedError,
                      transaction.interfaces.TransientError,
                      ZODB.POSException.ConflictError)

    # Modulo for computing "ikeys" (see m_init's doc) from object's integer IDs
    MOD_IKEY = 10000

    def __init__(self, path, server):
        # The ZODB database object
        self.db = ZODB.DB(path)
        # The main HTTP server
        self.server = server

    def openConnection(self):
        '''Opens and returns a connection to this database'''
        return self.db.open()

    def closeConnection(self, connection):
        '''Closes the p_connection to this database'''
        try:
            connection.close()
        except ZODB.POSException.ConnectionStateError:
            # Some updates are probably uncommitted. Abort the current
            # transaction and then try again to close the connection.
            transaction.abort()
            connection.close()

    def listConnections(self):
        '''Returns the list of active connections to the database'''
        return self.db.connectionDebugInfo()

    def commit(self, handler):
        '''Commits the current transaction related to p_handler'''
        transaction.commit()

    def abort(self, connection=None, message=None, logger=None):
        '''Abort the current transaction'''
        # Logs a p_message when requested
        if message: logger.error(message)
        # Abort the ongoing transaction
        transaction.abort()
        # Close the p_connection if given
        if connection: connection.close()

    def close(self, abort=False):
        '''Closes the database'''
        # Must we first abort any ongoing transaction ?
        if abort: transaction.abort()
        try:
            self.db.close()
        except ZODB.POSException.ConnectionStateError:
            # Force aborting any ongoing transaction
            transaction.abort()
            self.db.close()

    def init(self, created, handler, poFiles):
        '''Create the basic data structures and objects in the database'''
        # Get a connection to the database. This is the "initialization"
        # connection, allowing to perform database initialization or update at
        # server startup.
        connection = self.db.open()
        # Make this connection available to the initialisation p_handler
        handler.dbConnection = connection
        # Get the root object
        root = connection.root
        # If the database is being p_created, add the following attributes to
        # the root object. Class "PersistentMapping" is named "PM" for
        # conciseness.
        # ----------------------------------------------------------------------
        # name       |  type  | description
        # ----------------------------------------------------------------------
        # iobjects   |  PM+   | The main persistent dict, storing all persistent
        #            |        | objects. Any object stored here has an attribute
        #            |        | named "iid" storing an identifier being an
        #            |        | incremental integer value. The last used integer
        #            |        | is in attribute "lastId" (see below). The dict
        #            |        | is structured that way: keys are integers made
        #            |        | of the 4 last digits of objects identifiers
        #            |        | (such a key is named an "ikey"), and values are
        #            |        | IOBTrees whose keys are object identifiers and
        #            |        | values are the objects themselves.
        # ----------------------------------------------------------------------
        # objects    |  PM    | A secondary persistent dict storing objects
        #            |        | that, in addition to their integer ID, have
        #            |        | also a string identifier, in attribute "id".
        #            |        | Such a string ID is part of the object URL and
        #            |        | is defined for its readability or ease of use.
        #            |        | The number of objects getting this kind of ID is
        #            |        | not meant to be huge: this is why we have chosen
        #            |        | not to store them in a OOBTree, but in a
        #            |        | PersistentMapping. Basic objects, like the tool
        #            |        | and translations, get such an ID. Unlike
        #            |        | "iobjects", the "objects" data structure has a
        #            |        | single level: keys are IDs (as strings) and
        #            |        | values are the objects themselves.
        #            |        |
        #            |        | An object without string ID:
        #            |        | - has attributes "id" and "iid" both storing the
        #            |        |   integer ID;
        #            |        | - is stored exclusively in "iobjects".
        #            |        |
        #            |        | An object with a string ID:
        #            |        | - has attribute "id" storing the string ID;
        #            |        | - has attribute "iid" storing the integer ID;
        #            |        | - is stored both in "iobjects" (based on its
        #            |        |   "iid") and in "objects" (based on is "id").
        # ----------------------------------------------------------------------
        # temp       |  PM    | A persistent mapping storing objects being
        #            |        | created via the ui. The process of creating an
        #            |        | object is the following: a temporary object is
        #            |        | created in this dict, with a negative integer ID
        #            |        | being an incremental value (see attribute
        #            |        | "lastTempId" below). The dict's keys are such
        #            |        | IDs, while values are the temp objects under
        #            |        | creation. Once the user has filled and saved
        #            |        | the corresponding form in the ui, the object is
        #            |        | moved to "iobjects"; additionally, it is also
        #            |        | stored in "objects" if its ID is a string ID.
        #            |        | If the user cancels the form, the object is
        #            |        | simply deleted from the "temp" dict. Restarting
        #            |        | the site does not empty the "temp" folder;
        #            |        | cleaning it may occur in the "nightlife" script.
        #            |        | Objects created "from code" do not follow the
        #            |        | same route and are directly created in
        #            |        | "(i)objects".
        # ----------------------------------------------------------------------
        # lastId     |  int   | An integer storing the last ID granted to an
        #            |        | object being stored in "iobjects".
        # ----------------------------------------------------------------------
        # lastTempId |  int   | An integer storing the last ID granted to a
        #            |        | temporary object stored in "temp".
        # ----------------------------------------------------------------------
        # catalogs   |  PM    | A persistent mapping of catalogs. For every
        #            |        | "indexable" class in the model, there will be
        #            |        | one entry whose key is the class name and whose
        #            |        | value is a Catalog instance
        #            |        | (see appy/database/catalog.py).
        # ----------------------------------------------------------------------
        if created:
            root.iobjects = PersistentMapping()
            root.objects = PersistentMapping()
            root.temp = PersistentMapping()
            root.lastId = root.lastTempId = 0
            root.catalogs = PersistentMapping()
        # The "iobjects" structure, made of 2 levels, allows to have the first
        # level as an always-in-memory persistent mapping made of at most
        # 10 000 entries. This structure, when full, should be of approximately
        # 100Kb. The second level is made of IOBTrees. An IOBTree is an optimal
        # data structure for storing a large number of objects. Like any BTree
        # structure, it behaves like a dict, but, internally, is made of
        # sub-nodes that, for some of them, can be on disk and others can be
        # loaded in memory. On the contrary, a standard mapping (or its
        # persistent counterpart) must be loaded in memory in its entirety.
        # BTree's sub-nodes group objects by sorted identifiers. By using
        # incremental integers, objects are grouped in some chronological way.
        # Sub-nodes corresponding to past objects are probably less loaded in
        # memory. Getting a recent object loads the sub-node in memory, with
        # objects that could also need to be retrieved by other requests because
        # of their temporal proximity.
        # ----------------------------------------------------------------------
        # Ensure all base objects are created in the database: the tool, base
        # users, translation files and catalogs. Create any object that would
        # be missing.
        # ----------------------------------------------------------------------
        if not hasattr(root, 'objects'):
            raise Database.Error(DB_CORRUPTED % self.db.storage._file_name)
        try:
            # Create the tool if it does not exist yet
            tool = root.objects.get('tool') or \
                   self.new(handler, 'Tool', id='tool', secure=False)
            # Update the initialisation handler
            handler.tool = tool
            # Create or update catalogs
            Catalog.manageAll(root, handler)
            # Let the tool initialise itself and create sub-objects as required
            tool.init(handler, poFiles)
            # Commit changes (forced, even if handler.commit is False)
            transaction.commit()
        except self.Error as e:
            transaction.abort()
            raise e
        except Exception as e:
            transaction.abort()
            raise e
        finally:
            connection.close()

    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Methods for searching objects
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def search(self, handler, className, ids=False, **kwargs):
        '''Perform a search on instances of a class whose name is p_className
           and return the list of matching objects. If p_ids is True, it returns
           a list of object IDS instead of a list of true objects.'''
        # p_ids being True can be useful for some usages like determining the
        # number of objects without needing to get information about them.
        # ~~~
        # Ensure there is a catalog for p_className
        catalog = handler.dbConnection.root.catalogs.get(className)
        if not catalog:
            raise self.Error(SRCH_NO_CAT % className)
        # Get the IIDs of matching objects
        iids = catalog.search(handler, **kwargs)
        # Return IIDs if requested
        if ids or not iids: return iids or []
        # Convert the list of IIDs to real objects
        return self.getObjects(handler, iids, className)

    def reindexObject(self, handler, o, **kwargs):
        '''(re)indexes this object in the catalog corresponding to its class'''
        # Ensure p_o is "indexable"
        className = o.class_.name
        catalog = handler.dbConnection.root.catalogs.get(className)
        if not catalog:
            raise self.Error(SRCH_NO_CAT % className)
        return catalog.reindexObject(o, **kwargs)

    def count(self, className): pass
    def compute(self, className): pass

    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Global database operations
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def pack(self, logger=None):
        '''Packs the database'''
        # Get the absolute path to the database file
        path = self.db.storage.getName()
        # Get its size, in bytes, before the pack
        size = os.stat(path).st_size
        # Perform the pack
        logger.info(DB_PACKING % path)
        self.db.pack()
        # Get its size, in bytes, after the pack
        newSize = os.stat(path).st_size
        # Log the operation
        if logger:
            logger.info(DB_PACKED % (putils.getShownSize(size),
                                     putils.getShownSize(newSize)))

    def cleanTemp(self, handler, logger, count=None):
        '''Removes any object from the temp store'''
        connection = handler.dbConnection
        if count is None:
            # We have not counted the temp objects yet
            store = getattr(connection.root, 'temp', None)
            count = len(store) if store else 0
        # For removing temp objects, it is useless to call m_delete on each one,
        # because they are not yet linked to any other object, do not have yet a
        # related filesystem space, etc.
        connection.root.temp = PersistentMapping()
        # Reset the ID counter
        connection.root.lastTempId = 0
        logger.info(TMP_OBJS_DEL % count)

    def clean(self, handler, logger):
        '''Cleaning the database means (a) removing any temp object from it and
           (b) packing it.'''
        # Create a specific connection
        connection = handler.dbConnection = self.db.open()
        # Get the temp store
        temp = getattr(connection.root, 'temp', None)
        dbFile = handler.server.config.database.filePath
        dbPath = str(dbFile)
        if temp is None:
            return self.abort(connection, TMP_STORE_NF % dbPath, logger)
        count = len(temp)
        if count == 0:
            logger.info(TMP_STORE_E % dbPath)
        else:
            self.cleanTemp(handler, logger, count=count)
            transaction.commit()
        connection.close()
        # Pack the database
        self.pack(logger)

    def run(self, method, handler, logger):
        '''Executes method named m_method on the tool'''
        # Create a specific connection
        connection = handler.dbConnection = self.db.open()
        # Get the store containing the tool
        root = connection.root
        store = getattr(root, 'objects', None)
        dbFile = handler.server.config.database.filePath
        dbPath = str(dbFile)
        # Ensure the "objects" store exists
        abort = self.abort
        if store is None:
            return abort(connection, O_STORE_NF % dbPath, logger)
        # Ensure the tool exists
        tool = handler.tool = root.objects.get('tool')
        if tool is None:
            return abort(connection, TOOL_NF % dbPath, logger)
        # Ensure p_method is defined on the tool
        if not hasattr(tool, method):
            return abort(connection, METH_NF % method, logger)
        # Execute the method
        try:
            getattr(tool, method)()
        except Exception as err:
            handler.server.logTraceback()
            return abort(connection)
        # Make a commit when relevant
        if handler.commit:
            transaction.commit()
        connection.close()

    def getIkey(self, id=None, o=None):
        '''Gets an "ikey" = the first level key for finding an object in store
           "iobjects" (more info on m_init). The ikey can be computed from a
           given integer p_id or from p_o's ID.'''
        id = id if o is None else o.id
        if not isinstance(id, int):
            raise self.Error(CUS_ID_NO_IK % id)
        return abs(id) % Database.MOD_IKEY

    def newId(self, root, temp=False):
        '''Computes and returns a new integer ID for an object to create'''
        # Get the attribute storing the last used ID
        attr = 'lastTempId' if temp else 'lastId'
        # Get the last ID in use
        last = getattr(root, attr)
        r = last + 1
        setattr(root, attr, r)
        return -r if temp else r

    def getStore(self, o=None, id=None, root=None, create=False):
        '''Get the store where p_o is supposed to be contained according to its
           ID. Instead of p_o, an p_id can be given. If p_create is True, the
           object's ID is a positive integer and the sub-store at its "ikey"
           does not exist, it is created. If the p_root database object is None,
           it will be retrieved from p_o.'''
        # Get the root database object
        root = root or o.H().dbConnection.root
        id = o.id if id is None else id
        # It may be the store of objects with custom IDs...
        if isinstance(id, str):
            r = root.objects
        # ... or the temp store ...
        elif id < 0:
            r = root.temp
        # ... or a sub-store in the standard store "iobjects"
        else:
            r = root.iobjects
            ikey = self.getIkey(id=id)
            if ikey in r:
                r = r[ikey]
            else:
                # The sub-store does not exist. Create it if required.
                if create:
                    r[ikey] = sub = IOBTree()
                    r = sub
                else:
                    r = None
        return r

    def exists(self, o=None, id=None, store=None, raiseError=False):
        '''Checks whether an object exists in the database, or an ID is already
           in use.'''

        # If p_o is...
        # ----------------------------------------------------------------------
        # not None | p_id and p_store are ignored, and the method checks if p_o
        #          | is present in the database.
        # ----------------------------------------------------------------------
        #   None   | p_id and p_store must be non empty and the method checks if
        #          | p_id is already in use in p_store.
        # ----------------------------------------------------------------------
        # If p_raiseError is True, if the object or ID exists, the method raises
        # an error. Else, it returns a boolean value.
        # ----------------------------------------------------------------------

        if id is None:
            id = o.id
            store = self.getStore(o)
        # Check the existence of the ID in the store
        r = id in store if store else None
        # Return the result or raise an error when appropriate
        if r and raiseError:
            raise self.Error(O_EXISTS % id)
        return r

    def new(self, handler, className, id=None, temp=False, secure=True,
            initialComment=None, initialState=None):
        '''Creates, in the database, a new object as an instance of p_className.
           p_handler is the current request handler. If p_id is not None, it is
           a string identifier that will be set in addition to an integer ID
           that will always be computed.'''

        # * Preamble * Read appy.database.Config::init for more info about the
        #              database structure.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # If p_temp is ...
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # True            | A temp object is created in the "temp" dict. Later,
        #                 | if its creation is confirmed, he will be moved to a
        #                 | "final" part of the database;
        # False (default) | A "final" object is added in the database, in the
        #                 | "objects" and/or "iobjects" dict, depending on its
        #                 | identifier.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # If p_secure is ...
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # True (default) | Appy will raise an error if the currently logged
        #                | user is not allowed to perform such creation;
        # False          | the security check will be bypassed.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # When the object is created, an initial entry is created in its
        # history. p_initialComment, if given, will be set as comment for this
        # initial entry. p_initialState (str) can be used to force the object to
        # get this particular state instead of its workflow's initial state.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # Ensure p_id's validity
        custom = id is not None
        if custom and not isinstance(id, str):
            raise self.Error(CUS_ID_N_STR)
        # Find the class corresponding to p_className
        class_ = handler.server.model.classes.get(className)
        if not class_: raise self.Error(CLASS_NF % className)
        # Security check
        guard = handler.guard
        if secure:
            guard.mayInstantiate(class_, checkInitiator=True, raiseOnError=True)
        # The root database object
        root = handler.dbConnection.root
        # Define the object IDs: "id" and "iid"
        if custom and temp: raise self.Error(NEW_TMP_W_ID)
        iid = self.newId(root, temp=temp)
        # Determine the place to store the object
        store = self.getStore(id=iid, root=root, create=True)
        # Prevent object creation if "iid" or "id" refer to an existing object
        self.exists(id=iid, store=store, raiseError=True)
        if custom: self.exists(id=id, store=root.objects, raiseError=True)
        # Create the object
        id = id or iid
        o = class_.new(iid, id, guard.userLogin, initialComment, initialState)
        # Store the newly created object in the database
        store[iid] = o
        if custom:
            root.objects[id] = o
        return o

    def move(self, o):
        '''Move the temp object p_o from the "temp" store to one of the final
           stores, "objects" or "iobjects".'''
        # The root database object
        root = o.H().dbConnection.root
        # A method named "generateId" may exist on p_o's class, for producing a
        # database ID for the object. If such method is found, it must return a
        # string ID and the object will be added to store "objects" in addition
        # to store "iobjects".
        iid = self.newId(root, temp=False)
        id = o.class_.generateId(o) or iid
        custom = id != iid
        # Determine the store where to move the object. Create the ad-hoc
        # sub-store in store "iobjects" if it does not exist yet.
        store = self.getStore(id=iid, root=root, create=True)
        # Prevent object creation if "iid" or "id" refer to an existing object
        self.exists(id=iid, store=store, raiseError=True)
        if custom: self.exists(id=id, store=root.objects, raiseError=True)
        # Perform the move
        del(root.temp[o.iid])
        o.iid = iid
        o.id = id
        store[iid] = o
        if custom:
            root.objects[id] = o

    def update(self, o, validator, initiator=None):
        '''Update object p_o from data collected from the UI via a p_validator.
           The possible p_initiator object may be given. Returns a message to
           return to the UI, or None if p_o has already been deleted.'''
        o.H().commit = True
        isTemp = o.isTemp()
        # If p_o is temp, convert it to a "final" object, by changing its ID and
        # moving it from dict "temp" to "objects" or "iobjects".
        if isTemp: self.move(o)
        # If p_o is not temp, as a preamble, remember the previous values of
        # fields, for potential historization.
        currentValues = None if isTemp \
                             else o.history.getCurrentValues(o,validator.fields)
        # Store, on p_o, new values for fields as collected on p_validator
        for field in validator.fields:
            field.store(o, validator.values[field.name])
        # Keep in history potential changes on historized fields
        if currentValues:
            o.history.historize(currentValues)
        # In the remaining of this method, at various places, we will check if
        # p_o has already been deleted or not. Indeed, p_o may just have been a
        # transient object whose only use was to collect data from the UI.
        # ---
        # Call the custom "onEditEarly" if available. This method is called
        # *before* potentially linking p_o to its initiator.
        if isTemp:
            multicall(o, 'onEditEarly', False, None)
            if not self.exists(o=o): return
        # Manage the relationship between the initiator and the new object
        if isTemp and initiator:
            r = initiator.manage(o)
            if not self.exists(o=o): return r
        # Update last modification date
        if not isTemp: o.history.modified = DateTime()
        # Call the custom "onEdit" if available. It may return a translated msg.
        r = multicall(o, 'onEdit', False, isTemp)
        if not self.exists(o=o): return
        # Unlock the currently saved page on the object
        Lock.remove(o, o.req.page)
        # Reindex the object when appropriate
        if o.class_.isIndexable():
            o.reindex()
        return r or o.translate('object_saved')

    def delete(self, o, historize=False, executeMethods=True, root=None,
               ignore=None):
        '''Delete object p_o from the database. When unlinking it from other
           objects, if the concerned Ref fields are historized and p_historize
           is True, this deletion is noted in tied object's histories.'''
        # ~~~
        # If p_executeMethods is False, the custom "onDelete" method, even if
        # present on p_o, will not be executed.
        # ~~~
        # If this object is cascade-deleted from another one, p_ignore contains
        # the back ref pointing to the deleting object, that must not be walked
        # again.
        # ~~~
        # For performance, when available, the p_root database object is passed
        # ~~~
        # If the deletion is aborted by custom method "onDelete", a translated
        # error message is returned.
        # ~~~
        isTemp = o.isTemp()
        # Call a custom "onDelete" if it exists
        if not isTemp and executeMethods and hasattr(o, 'onDelete'):
            message = o.onDelete()
            # If a return message is present, the deletion is aborted
            if message: return message
        handler = o.H()
        handler.commit = True
        # Remove any link to any object and cascade-delete contained objects
        title = o.getShownValue()
        for field in o.class_.fields.values():
            # Browse only Ref fields
            if field.type != 'Ref': continue
            # Do not browse the field mentioned in p_ignore
            if ignore and (field.name == ignore.name): continue
            # Browse tied objects
            contained = field.composite
            for tied in field.getValue(o, single=False):
                # Delete the tied object if contained within this one
                if contained:
                    self.delete(tied, historize=historize, ignore=field.back,
                                executeMethods=executeMethods, root=root)
                    continue
                # Unlink the tied object else
                back = field.back
                if back is None: continue
                field.back.unlinkObject(tied, o, back=True)
                # Historize this unlinking when relevant
                if historize and field.back.getAttribute(tied, 'historized'):
                    className = o.translate(tied.class_.name)
                    tied.history.add('Unlink', deletion=True,
                                     comment='%s: %s' % (className, title))
        if not isTemp:
            # Unindex p_o if it was indexed
            if o.class_.isIndexable(): o.reindex(unindex=True)
            # Delete the filesystem folder corresponding to this object
            folder = self.getFolder(o, create=False)
            if folder.exists():
                # Try to move it to the OS temp folder; if it fails, delete it
                putils.FolderDeleter.delete(folder, move=True)
                o.log(FOLDER_DEL % (folder, o.iid, o.title))
        # Get the store containing p_o
        root = root or o.H().dbConnection.root
        iid = o.iid
        store = self.getStore(id=iid, root=root)
        # Remove p_o from this store, and potentially from root.objects, too
        try:
            del(store[iid])
        except KeyError:
            pass # The object may already have been deleted
        if o.id != iid:
            try:
                del(root.objects[o.id])
            except KeyError:
                pass # The object may already have been deleted

    def getObject(self, handler, id, logMissing=False, className=None):
        '''Gets an object given its p_id'''
        # If p_logMissing is True and no object is found corresponding to the
        # passed p_id, an error message will be logged. If the caller knows it,
        # the p_className may be passed, producing a more precise error message.
        # ~~~
        # Convert p_id to an int if it is an integer coded in a string
        if isinstance(id, str) and (id.isdigit() or id.startswith('-')):
            id = int(id)
        store = self.getStore(id=id, root=handler.dbConnection.root)
        r = store.get(id) if store else None
        if (r is None) and logMissing:
            # Log the fact that no object has been found
            sid = str(id)
            if className:
                message = MISS_O_CLASS % (className, sid)
            else:
                message = MISS_O % sid
            handler.log('app', 'error', message)
        return r

    def getObjects(self, handler, ids, className=None, start=0, size=None):
        '''Returns a list of objects from their p_ids'''
        # ~~~
        # p_ids can be a list or a IISet. If p_size is not None, it represents a
        # number of IDs: only this number of IDs will be retrieved from p_ids,
        # starting at index p_start.
        # ~~~
        # IDs for which no object is found are removed from their catalog (if
        # p_className is not None).
        r = [] # The retrieved objects
        missing = None # IDs for which no object could be found
        if not isinstance(ids, Lazy):
            # Browse IDs from a IISet
            for id in ids:
                o = self.getObject(handler, id, logMissing=True,
                                   className=className)
                if o is not None:
                    # The object has been found; add it to the result
                    r.append(o)
                    # Stop now if p_size is reached
                    if (size is not None) and (len(r) >= size):
                        break
                else:
                    # No object was found: add the id among missing IDs
                    if missing is None: missing = []
                    missing.append(id)
        else:
            # Browse IDs from a sorted list of IIDs
            i = start
            total = len(ids) # The total number of IDs in p_ids
            end = total if size is None else start + size
            while (i < end) and (i < total):
                id = ids[i]
                o = self.getObject(handler, id, logMissing=True,
                                   className=className)
                if o is not None:
                    # The object has been found; add it to the result
                    r.append(o)
                else:
                    # No object was found: add the id among missing IDs
                    if missing is None: missing = []
                    missing.append(id)
                i += 1
        # If missing IDs were found, clean it from the corresponding catalog
        if missing and className:
            catalog = handler.dbConnection.root.catalogs.get(className)
            if catalog:
                for id in missing:
                    catalog.unindexObject(id)
                missing = [str(iid) for iid in missing]
                message = MISS_IDS_DEL % (className, ', '.join(missing))
                handler.log('app', 'info', message)
                handler.commit = True # Force a commit in that case
        return r

    def getFolder(self, o, create=True, withRelative=False):
        '''Gets, as a pathlib.Path instance, the folder where binary files
           related to p_o are (or will be) stored on the database-controlled
           filesystem. If p_create is True and the folder does not exist, it is
           created (together with potentially missing parent folders).'''
        # If p_withRelative is True, the methods returns a tuple
        #                         (path, relative),
        # where "path" is the Path instance as described hereabove, and
        # "relative" is a string containing the part of the path that does not
        # contain its start (= the root folder containing binaries).
        # ~~~
        # Start with getting the root folder storing site binaries
        r = o.config.database.binariesFolder
        # Add the object-specific path, depending on its ID
        id = o.iid
        ikey = str(self.getIkey(id=id))
        sid = str(abs(id))
        r = r / ikey / sid
        # Create this folder if p_create is True and it does not exist yet
        if create and not r.exists():
            r.mkdir(parents=True)
        # Return the path, together with its relative part if requested
        return r if not withRelative else (r, ('%s/%s' % (ikey, sid)))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                                 PXs
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    view = Px('''
     <h2>Main configuration</h2>
     <table class="small"
            var="cfg=config.database; root=handler.dbConnection.root">
      <tr><th>Database (ZODB)</th><td>:cfg.filePath</td></tr>
      <tr><th>Database size</th><td>:cfg.getDatabaseSize(True)</td></tr>
      <tr><th>Binaries</th><td>:cfg.binariesFolder</td></tr>
      <tr><th>Last object ID</th><td>:root.lastId</td></tr>
      <tr><th>Last temp ID</th><td>:root.lastTempId</td></tr>
      <tr><th>ZODB version</th><td>:cfg.getZodbVersion()</td></tr>
     </table>

     <x var="connections=handler.server.database.listConnections()">
      <h2>Active connections <x>:'(%d)' % len(connections)</x></h2>
      <table class="small">
       <tr for="info in connections">
        <th>:info['info']</th>
        <td>
         <div for="k,v in info.items()" if="k!='info'">
          <b>:k</b> : <x>:v or '-'</x></div>
        </td></tr>
      </table></x>''')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
