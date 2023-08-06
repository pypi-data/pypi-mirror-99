'''Sort results produced by a catalog'''

# Code inspired by Zope's catalog

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
from BTrees.IIBTree import intersection

from appy.database.lazy import LazyCat, LazyValues

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Sorter:
    '''Sorts results as produced by a catalog'''

    # The sorter' input and output data structures are as follows.
    # --------------------------------------------------------------------------
    # input   | A result set of object IIDs as computed by a catalog, as an
    #         | instance of IISet.
    # --------------------------------------------------------------------------
    # output  | A sorted list of object IIDs, in the form of a Lazy data
    #         | structure (see appy/database/lazy.py). The sorter produces an
    #         | intermediary data structure that is more complex than a list.
    #         | Instead of directly and completely "flattening" this data
    #         | structure into a list of IIDs, we wrap it, for performance
    #         | reasons, into a Lazy data structure, that behaves like a list
    #         | and manipulates, behind the scenes, the more complex internal
    #         | structure.
    # --------------------------------------------------------------------------

    def __init__(self, sortIndex, rs, reverse):
        # The index to use for sorting
        self.sortIndex = sortIndex
        # Must we reverse results ?
        self.reverse = reverse
        # The (unsorted) result set
        self.rs = rs

    def iterateByIndex(self, r):
        '''Fills list p_r with sorted entries from p_self.rs, by iterating over
           p_self.sortIndex.'''
        rs = self.rs
        length = 0
        for value, iids in self.sortIndex.byValue.items():
            # Object "iids" share the same index "value". Intersect each set of
            # "iids" with the result set, and produce a sorted list of these
            # intersections.
            subset = intersection(rs, iids)
            if subset:
                subset = subset.keys()
                r.append((value, subset))
                length += len(subset)
        return length

    def iterateByResultSet(self, r):
        '''Fills list p_r with sorted entries frol p_self.rs by iterating over
           p_self.rs.'''
        rs = self.rs
        index = self.sortIndex
        for iid in rs:
            value = index.byObject.get(iid)
            # p_value can be None if the object is not in the sort index
            r.append((value, iid))
        return len(r)

    def run(self):
        '''Returns a Lazy data structure containing object IIDs found in
           p_self.rs, sorted by p_self.sortIndex.'''
        r = []
        # Choose what method to use for sorting p_self.rs. It is more performant
        # to iterate over the index if shorter than the result set.
        rsLength = len(self.rs)
        indexLength = len(self.sortIndex.byValue)
        algo = 'ByIndex' if rsLength > (indexLength * (rsLength / 100 + 1)) \
                         else 'ByResultSet'
        # Use the chosen algorithm to produce an intermediate result in p_r
        length = getattr(self, 'iterate%s' % algo)(r)
        # Sort p_r. Reverse the sort order when appropriate.
        r.sort(reverse=self.reverse)
        # Return the list as a "lazy" data structure (see appy.database.lazy.py)
        if algo == 'ByIndex':
            # Sort results are in the form of a list of sub-lists
            r = LazyCat(LazyValues(r), length=length)
        else:
            # Sort results are in the form of a simple list, but whose
            # sub-elements are (value, iid) tuples instead of simple IIDs.
            r = LazyValues(r)
        return r
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
