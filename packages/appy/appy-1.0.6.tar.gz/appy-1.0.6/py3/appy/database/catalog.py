'''A catalog is a dict of database indexes storing information about instances
   of a given class from an Appy app's model.'''

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
from BTrees.IIBTree import IITreeSet, difference
from persistent.mapping import PersistentMapping

from appy.database.indexes import Index
from appy.database.indexes.ref import RefIndex
from appy.database.indexes.date import DateIndex
from appy.database.indexes.text import TextIndex
from appy.database.indexes.rich import RichIndex
from appy.database.indexes.float import FloatIndex
from appy.database.indexes.boolean import BooleanIndex

from appy.px import Px
from appy.ui.template import Template
from appy.database.sorter import Sorter
from appy.model.utils import Object as O
from appy.database.operators import Operator

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
CTL_CREATED = 'Catalog created for class "%s".'
CTL_REMOVED = 'Catalog removed for class "%s".'
IDXS_POP    = '%d/%d object(s) reindexed during population of index(es) %s.'
IDXS_CLEAN  = '%d catalog entries removed (inexistent objects).'
IDX_NF      = 'There is no indexed field named "%s" on class "%s".'
OBJECT_NF   = 'Object with IID %d does not exist in catalog "%s".'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Changes:
    '''This class represents a set of changes within a catalog's indexes'''

    # Types of changes
    types = ('created', # Indexes having been created
             'updated', # Indexes whose type has been changed
             'deleted') # Indexes having been deleted because there is no more
                        # corresponding indexed field on the related class.

    def __init__(self, handler, class_):
        self.handler = handler
        self.class_ = class_
        for type in Changes.types:
            setattr(self, type, [])

    def log(self):
        '''Dump an info in the log if at least one change has occurred'''
        r = []
        for type in Changes.types:
            names = getattr(self, type)
            # Ignore this type of change if no change of this type has occurred
            if not names: continue
            prefix = 'index' if len(names) == 1 else 'indexes'
            names = ', '.join(['"%s"' % name for name in names])
            r.append('%s %s %s' % (prefix, names, type))
        for info in r:
            self.handler.log('app', 'info', 'Class %s: %s.' % \
                             (self.class_.name, info))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Catalog(PersistentMapping):
    '''Catalog of database indexes for a given class'''

    traverse = {}

    # Catalog-specific exception class
    class Error(Exception): pass

    # A catalog is a dict of the form ~{s_name: Index_index}~
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # name    | The name of an indexed field on the class corresponding to this
    #         | catalog.
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # index   | An instance of one of the Index sub-classes as defined in
    #         | package appy/database/indexes.
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def __init__(self, handler, class_):
        PersistentMapping.__init__(self)
        # The name of the corresponding Appy class
        self.name = class_.name
        # A set containing all instances (stored as iids) of p_class
        self.all = IITreeSet()

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Class methods
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @classmethod
    def populate(class_, root, handler, populate):
        '''Called by the framework, this method populates new indexes or indexes
           whose type has changed. The list of indexes to populate is given in
           p_populate, as produced by m_manageAll.'''
        counts = O(total=0, updated=0, lost=[])
        # Browse indexes to populate
        database = handler.server.database
        for className, indexes in populate.items():
            # Browse all instances of the class corresponding to this catalog
            # and reindex those being concerned by "indexes".
            catalog = root.catalogs[className]
            for iid in catalog.all:
                o = database.getObject(handler, iid)
                if o is None:
                    # This object, referenced in the catalog, does not exist
                    counts.lost.append((className, iid))
                    continue
                # Count this object
                counts.total += 1
                # Submit the object to every index to populate
                updated = o.reindex(indexes=indexes)
                if updated:
                    counts.updated += 1
        # Remove index entries for which no object has been found
        for className, iid in counts.lost:
            root.catalogs[className].unindexObject(iid)
        # At the time the database is created, there is a single object in it:
        # the tool.
        if counts.total > 1:
            # Log details about the operation
            names = [] # The names of the populated indexes
            for className, indexes in populate.items():
                for index in indexes:
                    names.append('%s::%s' % (className, index.name))
            message = IDXS_POP % (counts.updated, counts.total,
                                  ', '.join(names))
            handler.log('app', 'info', message)
        if counts.lost:
            message = IDXS_CLEAN % len(counts.lost)
            handler.log('app', 'warning', message)

    @classmethod
    def manageAll(class_, root, handler):
        '''Called by the framework, this method creates or updates, at system
           startup, catalogs required by the app's model .'''
        # Ensure a catalog exists for every indexable class
        model = handler.server.model
        catalogs = root.catalogs
        # Maintain a dict of indexable classes ~{s_name: None}~. It will allow,
        # at the end of the process, to remove every index that do not
        # correspond to any indexable class anymore.
        indexable = {}
        names = list(catalogs.keys())
        # Maintain a dict, keyed by class name, of the indexes to populate, from
        # all catalogs. Indeed, populating any index requires to scan all
        # database objects. This scanning will be done only once, at the end of
        # this method, after having created, updated or deleted all indexes from
        # all catalogs.
        populate = {} #~{s_className: [Index]}~
        # Browse all model classes, looking for catalogs and indexes to manage
        for modelClass in model.classes.values():
            name = modelClass.name
            # Ignore non-indexable classes
            if not modelClass.isIndexable(): continue
            indexable[name] = None
            if name not in catalogs:
                catalog = catalogs[name] = Catalog(handler, modelClass)
                handler.log('app', 'info', CTL_CREATED % name)
            else:
                catalog = catalogs[name]
            # Potentially update indexes in this catalog
            toPopulate = catalog.updateIndexes(handler, modelClass)
            if toPopulate:
                populate[name] = toPopulate
        # Remove catalogs for which no indexable class has been found
        for name in names:
            if name not in indexable:
                del(catalogs[name])
                handler.log('app', 'info', CTL_REMOVED % name)
        # Populate indexes requiring it
        if populate:
            class_.populate(root, handler, populate)

    def updateIndexes(self, handler, class_):
        '''Create or update indexes for p_class_. Returns the list of indexes
           that must be populated.'''
        changes = Changes(handler, class_)
        r = [] # The indexes that must be populated
        all = [] # Remember the names of all indexes
        # Browse fields
        for field in class_.fields.values():
            # Ignore fields requiring no index
            if not field.indexed: continue
            name = field.name
            all.append(name)
            # Get the name of the index class to use
            indexType = field.getIndexType()
            # Does the index already exist ?
            if name in self:
                # Do nothing if the index exists and is of the correct type
                index = self[name]
                if index.__class__.__name__ == indexType:
                    continue
                else:
                    # There is a mismatch between the index currently created
                    # and the index to use according to the field. It probably
                    # corresponds to a change in the field definition: delete
                    # the existing index and recreate it with the correct type.
                    del(self[name])
                    changes.updated.append(name)
            else:
                # The index must be created
                changes.created.append(name)
            # Create the index: it does not exist yet
            index = self[name] = eval(indexType)(field, self)
            r.append(index)
        # Browse indexes, looking for indexes to delete
        for name in self.keys():
            if name not in all:
                changes.deleted.append(name)
        # Delete indexes for which there is no more corresponding indexed field
        for name in changes.deleted:
            del(self[name])
        # Log info if changes have been performed
        changes.log()
        # Return the list of indexes to populate
        return r

    def getIndex(self, name):
        '''Get the index named p_name or raise an exception if no such index
           exists in this catalog.'''
        r = self.get(name)
        if not r: raise self.Error(IDX_NF % (name, self.name))
        return r

    def getField(self, name, handler):
        '''Gets the field whose name is p_name'''
        return handler.server.model.classes.get(self.name).fields.get(name)

    def getSorted(self, r, sortBy, sortOrder):
        '''Gets, from search results p_r (=a IITreeSet of IIDs), a list of
           sorted IIDs.'''
        # If the result must not be sorted, return the result set as-is
        if not sortBy: return r
        if r is None: return
        # Find the sort index
        sortIndex = self.getIndex(sortBy)
        # Get sorted results
        return Sorter(sortIndex, r, reverse=sortOrder=='desc').run()

    def search(self, handler, secure=False, sortBy=None, sortOrder='asc',
               **fields):
        '''Performs a search in this catalog. Returns a IITreeSet object if
           results are found, None else.'''
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Param      | Description
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # secure     | If not True, security checks depending on user
        #            | permissions are bypassed.
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # sortBy     | If specified, it must be the name of an indexed field on
        #            | p_className.
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # sortOrder  | Can be "asc" (ascending, the defaut) or "desc"
        #            | (descending).
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # fields     | Keyword args must correspond to valid indexed field names
        #            | on p_className. For every such arg, the specified value
        #            | must be a valid value according to the field definition.
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Add the security-related search parameter if p_secure is True
        if secure and ('allowed' not in fields):
            fields['allowed'] = handler.guard.userAllowed
        # The result set, as a IITreeSet instance (or None)
        r = None
        # p_fields items can be of 2 kinds.
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # If...    | It determines...
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # positive | a set of matching objects. A single value or an operator
        #          | like "and" or "or" is positive;
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # negative | a set of objects that must be excluded from the result. The
        #          | "not" operator is negative.
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        positive = False # True if at least one positive arg is met
        negative = None # The list of negative args encountered
        # Browse search values from p_fields. Those values are implicitly
        # AND-ed: as soon as one value does not match, there is no match at all.
        for name, value in fields.items():
            if isinstance(value, Operator) and value.negative:
                # A negative operator. Do not manage it now, store it for later.
                neg = (name, value)
                if negative is None:
                    negative = [neg]
                else:
                    negative.append(neg)
            else:
                # A positive operator or a value
                positive = True
                # Get the corresponding index
                index = self.getIndex(name)
                # Update "r" with the objects matching "value" in index
                # named "name".
                r = index.search(value, self.getField(name, handler), r)
                if not r: return # There is no match at all
        # If there was no positive arg at all, take, as basis for the search,
        # all instances from this class' catalog.
        r = self.all if not positive else r
        if not r or not negative: return self.getSorted(r, sortBy, sortOrder)
        # Apply negative args
        for name, value in negative:
            field = self.getField(name, handler)
            ids = self.getIndex(name).search(value, field, r)
            if ids:
                r = difference(r, ids)
                if not r: return
        # Convert the IITreeSet to a sorted list of IIDs and return it
        return self.getSorted(r, sortBy, sortOrder)

    def unindexObject(self, iid, log=None):
        '''Unindexes object having this p_iid from this catalog. Returns True if
           at least one entry from one index has actually been removed within
           this catalog.'''
        r = False
        for index in self.values():
            changed = index.unindexObject(iid)
            if changed: r = True
        # Remove it from p_self.all
        try:
            self.all.remove(iid)
        except KeyError:
            # The object is not in the catalog, issue a warning
            if log: log(OBJECT_NF % (iid, self.name), type='warning')
        return r
        
    def reindexObject(self, o, fields=None, indexes=None, unindex=False,
                      exclude=False):
        '''(Re-/un-)indexes this p_o(bject). In most cases, you, app developer,
           don't have to reindex objects "manually" with this method. When an
           object is modified after some user action has been performed, Appy
           reindexes it automatically. But if your code modifies other objects,
           Appy may not know that they must be reindexed, too. So use this
           method in those cases.'''
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # The method returns False if it has produced no effect, True else.
        # "Producing an effect" means: object-related data as stored in indexes
        # has been modified (addition, change or removal) for at least one
        # index.
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Method parameters are described hereafter.
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #  unindex | If True, the object is unindexed instead of being
        #          | (re)indexed.
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #  fields  | p_fields may hold a list of indexed field names. In that
        #          | case, only these fields will be reindexed. If None (the
        #          | default), all indexable fields defined on p_o's class (via
        #          | attribute "indexed") are (re)indexed.
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #  indexes | As an alternative to p_fields, you may, instead, specify,
        #          | in p_indexes, a list of appy.database.indexes.Index
        #          | instances. Appy uses this; the app developer should use
        #          | p_fields instead.
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #  exclude | If p_exclude is True, p_fields is interpreted as containing
        #          | the list of indexes NOT TO recompute: all the indexes not
        #          | being in this list will be recomputed. p_exclude has sense
        #          | only if p_unindex is False and p_fields is not None.
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        r = False
        # Manage unindexing
        if unindex: return self.unindexObject(o.iid, o.log)
        # Manage (re)indexing
        if indexes:
            # The list of indexes to update is given
            for index in indexes:
                changed = index.indexObject(o)
                if changed: r = True
        elif fields:
            # The list of field names is given
            if not exclude:
                # Index only fields as listed in p_fields
                for name in fields:
                    # Get the corresponding index
                    if name not in self:
                        raise self.Error(IDX_NF % (name, self.name))
                    changed = self[name].indexObject(o)
                    if changed: r = True
            else:
                # Index only fields not being listed in p_fields
                for name, index in self.items():
                    if name in fields: continue
                    changed = index.indexObject(o)
                    if changed: r = True
        else:
            # Reindex all available indexes
            for index in self.values():
                changed = index.indexObject(o)
                if changed: r = True
            # Ensure the object is in p_self.all
            if r: self.all.insert(o.iid)
        return r

    traverse['reindex'] = 'Manager'
    def reindex(self, o):
        '''Reindexes p_o (triggered from the UI)'''
        # Get the name of the index to recompute, or 'all' if all indexes must
        # be recomputed.
        name = o.req.indexName
        if name == '_all_':
            self.reindexObject(o)
        else:
            self.reindexObject(o, fields=(name,))
        o.H().commit = True
        o.goto(o.referer, message=o.translate('action_done'))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PX
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # PX displaying info stored in this catalog's indexes for some object
    forObject = Px('''<x var="catalog=o.getCatalog(raiseError=True)">
     <h3><a href=":o.url">:o.getValue('title', type='shown')</a></h3>
     <form name="reindexForm" method="post"
           action=":'%s/catalog/reindex' % o.url">
      <input type="hidden" name="indexName"/>
      <table class="small">
       <!-- 1st line: dump local roles, by the way -->
       <tr>
        <td>Local roles</td>
        <td colspan="3"><x>:o.localRoles</x></td>
       </tr>
       <tr>
        <td>Local roles only ?</td>
        <td colspan="3"><x>:'Yes' if o.localRoles.only else 'No'</x></td>
       </tr>
       <tr><th>Index name</th><th>Type</th><th>Content</th><th>
        <img src=":url('reindex')" class="clickable" title="Reindex all indexes"
             onclick="reindexObject(\'_all_\')"/></th></tr>
       <tr for="name, index in catalog.items()"
           class=":loop.name.odd and 'odd' or 'even'">
         <td>:name</td><td>:index.__class__.__name__</td>
         <td>:o.getField(index.name).getCatalogValue(o, index)</td>
         <td><img src=":url('reindex')" class="clickable"
                  title="Reindex this index only"
                  onclick=":'reindexObject(%s)' % q(name)"/></td>
       </tr>
      </table>
     </form>
    </x>''',

     js='''
      function reindexObject(indexName){
        var f = document.forms['reindexForm'];
        f.indexName.value = indexName;
        f.submit();
      }''',
     template=Template.px, hook='content')

    # The default PX shown indexed info about the currently traversed object
    default = forObject
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
