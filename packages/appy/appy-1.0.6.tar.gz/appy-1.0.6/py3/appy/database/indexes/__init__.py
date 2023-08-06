'''Module defining database indexes'''

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
# The class hierarchy defined in this module is inspired by sub-package
# "PluginIndexes" within the "Products.ZCatalog" product published by the Zope
# foundation at https://github.com/zopefoundation/Products.ZCatalog. The
# objective is to get similar indexes, but independently of Zope.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import persistent
from BTrees.OOBTree import OOBTree
from BTrees.IOBTree import IOBTree
from BTrees.IIBTree import IITreeSet, intersection

from appy.database.operators import Operator

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
INVALID_VALUE = 'Index "%s" in catalog "%s": wrong %s "%s".'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Index(persistent.Persistent):
    '''Abstract base class for any index'''

    # Index-specific exception class
    class Error(Exception): pass

    # Values considered as empty, non-indexable values
    emptyValues = (None, [], ())

    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # An index is made of 2 main dicts: "byValue" stores objects keyed by their
    # index values (this is the "forward" index), while "byObject" stores index
    # values keyed by object ID (this the "reverse" index).
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Let's take an example. Suppose we want to index values for some
    # attribute on 3 objects. Here are the attribute values.
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Object   | Attribute value
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # obj1     | value1
    # obj2     | value2
    # obj3     | value1
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Here are the content for dicts "byValue" and "byObject".
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Dict     | Value
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # byValue  | { value1: [obj1, obj3], value2: [obj2] }
    # byObject | { obj1: value1, obj2: value2, obj3: value1 }
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # In m_init below, you will get more precisions about the data structures in
    # use. For example, object integer IDs are stored (from their attribute
    # o.iid), and not the objects themselves. For more info about object IIDs,
    # see appy/database/__init__.py).
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def __init__(self, field, catalog):
        '''Index constructor'''
        # The name of the index is the name of this p_field on some Appy class
        self.name = field.name
        # The catalog storing this index
        self.catalog = catalog
        self.init()

    def __repr__(self):
        '''p_self's string representation'''
        return '<index %s::%s>' % (self.catalog.name, self.name)

    def init(self):
        '''Initialisation (or cleaning) of the index main data structures'''

        # Dict "byValue" is a OOBTree of the form ~{indexValue: objectIds}~
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # indexValue   | Is an index value, produced from an object's attribute
        #              | value via m_getIndexValue on the corresponding field.
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # objectIds    | Is a list of object IDs having this index value,
        #              | implemented as a IITreeSet.
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.byValue = OOBTree()

        # Dict "byObjects" is a IOBTree of the form ~{i_objectId: indexValue}~
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # objectId     | Is the object IID as stored in attribute object.iid
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # indexValue   | Is the value currently stored by the index for this
        #              | object.
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.byObject = IOBTree()

    def getByValue(self, value, field):
        '''Returns the object IDs matching this p_value by performing a lookup
           in p_self.byValue.'''
        return self.byValue.get(self.toTerm(value, field), None)

    def getByRange(self, lo, hi, field):
        '''Returns the object IDs matching, within p_self.byValue, the range of
           values specified by p_lo(w) and p_hi(gh).'''
        if hi is None:
            r = self.byValue.values(self.toTerm(lo, field))
        else:
            r = self.byValue.values(self.toTerm(lo, field),
                                    self.toTerm(hi, field))
        return r

    def getByObject(self, o, field):
        '''Returns the value currently stored for p_o in p_self'''
        r = self.byObject.get(o.iid)
        if not r: return
        # Take care of converting the value from the internal to the standard
        # data format.
        return self.fromIndexed(r, field)

    def isMultiple(self, value, inIndex=False):
        '''Is p_value considered to be "multiple"? If yes, p_value will be
           considered as a sequence of several values; each of them must have a
           separate entry in p_self.byValue.'''
        # If p_inIndex is False, p_value is stored in the database, on some
        # object. If p_inIndex is True, p_value comes from within an index.
        type = tuple if inIndex else list
        # Indeed, multiple values stored in the database are lists, while
        # multiple values are stored in indexes are tuples.
        return isinstance(value, type)

    def getMultiple(self, value):
        '''Return a copy of this multiple p_value ready to be stored in
           p_self.byObject.'''
        return tuple(value)

    def valueEquals(self, value, current):
        '''Returns True if p_value and p_current are equal'''
        if not self.isMultiple(value):
            r = value == current
        else:
            # p_value may be a list, and p_current a p_tuple
            size = len(value)
            r = size == len(current)
            if r:
                i = 0
                while i < size:
                    if value[i] != current[i]:
                        r = False
                        break
                    i += 1
        return r

    def removeByValueEntry(self, value, id):
        '''Removes (non-multiple) p_value from p_self.byValue, for this p_id'''
        ids = self.byValue.get(value)
        if ids is None: return
        # Remove reference to p_id for this p_value
        try:
            ids.remove(id)
        except (ValueError, KeyError):
            pass
        # If no object uses p_value anymore, remove the whole entry
        if not ids:
            del(self.byValue[value])

    def removeEntry(self, id):
        '''Remove the currently indexed value for this p_id'''
        # Remove the entry in dict "byObject"
        value = self.byObject[id]
        del(self.byObject[id])
        # Remove the entry (or entries) in dict "byValue"
        if self.isMultiple(value, inIndex=True):
            # A multi-value
            for v in value:
                self.removeByValueEntry(v, id)
        else:
            self.removeByValueEntry(value, id)

    def addEntry(self, id, value, byValueOnly=False):
        '''Add, in this index, an entry with this p_id and p_value.

           If p_byValueOnly is True, it updates p_self.byValue but not
           p_self.byObject. It happens when m_addEntry is called recursively,
           for adding multiple entries corresponding to a multi-value. '''
        if self.isMultiple(value):
            # A multi-value. Get it as a ready-to-store value.
            value = self.getMultiple(value)
            # Add an entry in p_self.byObject
            self.byObject[id] = value
            # Add one entry for every single value in p_self.byValue
            for v in value:
                self.addEntry(id, v, byValueOnly=True)
        else:
            # A single value. Add it to p_self.byObject when relevant.
            if not byValueOnly:
                self.byObject[id] = value
            # Add it in p_self.byValue
            if value in self.byValue:
                self.byValue[value].insert(id)
            else:
                self.byValue[value] = IITreeSet((id,))

    def indexObject(self, o):
        '''Index object p_o. Returns True if the index has been changed
           regarding p_o, ie, entries have been added or removed.'''
        # Get the value to index
        value = o.getField(self.name).getIndexValue(o)
        id = o.iid
        if value in Index.emptyValues:
            # There is nothing to index for this object
            if id not in self.byObject: return
            # The object is yet indexed: remove the entry
            self.removeEntry(id)
        else:
            # We must index this value
            if id not in self.byObject:
                # No trace from this object in the index, add an entry
                self.addEntry(id, value)
            else:
                # The object is already indexed. Get the currently indexed value
                current = self.byObject[id]
                # Do nothing if the current value is the right one
                if self.valueEquals(value, current): return
                # Remove the current entry and replace it with the new one
                self.removeEntry(id)
                self.addEntry(id, value)
        return True

    def unindexObject(self, iid):
        '''Unindex object whose IID is p_iid. Returns True if an entry has
           actually been removed from the index.'''
        # Do nothing if there is no trace from this object in this index
        if iid not in self.byObject: return
        self.removeEntry(iid)
        return True

    def search(self, value, field, rs):
        '''Computes the objects matching p_value, updates the global result
           set p_rs and returns the updated result.'''
        isOperator = isinstance(value, Operator)
        try:
            if isOperator:
                # p_value is an operator on one or several values
                r, rsUpdated = value.apply(self, field, rs)
            else:
                # A single value
                r = self.byValue.get(self.toTerm(value, field), None)
                rsUpdated = False
            if r is None:
                # No match for this index = no match at all
                return r
            else:
                # Applying the operator may already have updated the global
                # resultset p_rs.
                return r if rsUpdated else intersection(r, rs)
        except TypeError:
            # p_value (or one of the value operators if p_value is an operator)
            # is not a valid value for this index.
            term = 'operator' if isOperator else 'index value'
            raise self.Error(INVALID_VALUE % \
                             (self.name, self.catalog.name, term, str(value)))

    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Conversion methods
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @classmethod
    def toIndexed(class_, value, field):
        '''Returns p_value's internal index representation'''
        return value # Is overridden by some child index classes

    @classmethod
    def fromIndexed(class_, value, field):
        '''Converts p_value, the internal representation of a value in this
           index, into the effective value.'''
        return value # Is overridden by some child index classes

    @classmethod
    def toTerm(class_, value, field):
        '''p_value is used as term for performing a search. This method converts
           it in such a way that it can be used as a valid search term for
           performing searches in the index.'''
        # Most of the time, p_value's internal representation in the index is a
        # suitable search term.
        return class_.toIndexed(value, field)

    @classmethod
    def toString(class_, o, value):
        '''Returns the string representation of this p_value'''
        if value is None: return
        return value if isinstance(value, str) else str(value)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
