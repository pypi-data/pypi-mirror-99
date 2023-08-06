'''Data structures for lazily accessing elements stored in sub-structures'''

# Code inspired by Zope's ZTUtil/Lazy.py

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
OVERRIDE_ERROR = 'Lazy subclasses must implement __getitem__.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Lazy:
    '''Abstract base class for any lazy data structure'''

    def __init__(self, seq, length=None):
        # The sequence of elements for which lazy access will be enabled
        self.seq = seq
        # The total length of p_seq's sub-elements, if known
        self.length = len(seq) if length is None else length

    def __repr__(self):
        '''p_self's string representation'''
        return repr(list(self))

    def __len__(self): return self.length

    def __getitem__(self, index):
        if isinstance(index, slice):
            r = []
            start, stop, step = index.indices(len(self))
            for i in range(start, stop, step):
                try:
                    r.append(self[i])
                except IndexError:
                    return r
            return r
        # The single index lookup is implemented in the subclasses
        raise NotImplementedError(OVERRIDE_ERROR)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class LazyValues(Lazy):
    '''Represents a list of (key, value) tuples, with lazy access to the "value"
       parts.'''

    def __getitem__(self, index):
        '''Accesses the "value" part of tuple element at p_index'''
        return self.__class__(self.seq[index]) if isinstance(index, slice) \
                                               else self.seq[index][1]

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class LazyCat(Lazy):
    '''Represents a concatenation of sub-lists whose elements are lazily
       accessed as if a single global list was existing.'''

    def __init__(self, seq, length=None):
        Lazy.__init__(self, seq, length)
        # The global list that will be built on-demand, every time an element
        # needs to be accessed. When p_self.data will be completely built,
        # p_self.seq will be set to None.
        self.data = []
        # The index of the last walked element within p_seq
        self.sindex = 0
        # The index of the last walked sub-element within p_seq[p_self.sindex]
        self.eindex = -1

    def __len__(self):
        '''Get p_self's length, ie, the sum of lengths of sub-sequences'''
        if self.length is not None: return self.length
        r = 0
        if self.seq is None:
            r = len(self.data)
        else:
            for l in self.seq:
                r += len(l)
        self.length = r
        return r

    def __getitem__(self, index):
        '''Accesses the sub-element at this p_index, as if p_self was a flat
           list.'''
        # Slices are managed by the base method
        if isinstance(index, slice):
            return super().__getitem__(index)
        # If the part of the global list (p_self.data) that includes p_index is
        # already available, get the element from it.
        seq = self.seq
        if seq is None:
            return self.data[index]
        # Manage negative indexes
        i = index
        if i < 0:
            i = len(self) + i
        if i < 0:
            raise IndexError(index)
        # Get the element from p_self.data if possible
        data = self.data
        ind = len(data)
        if i < ind:
            return data[i]
        ind -= 1
        # Complete p_self.data until we can access the element at p_index
        sindex = self.sindex
        try:
            s = seq[sindex]
        except Exception:
            raise IndexError(index)
        eindex = self.eindex
        while i > ind:
            try:
                eindex += 1
                v = s[eindex]
                data.append(v)
                ind += 1
            except IndexError:
                self.sindex = sindex = sindex + 1
                try:
                    s = self.seq[sindex]
                except Exception:
                    # We have completely walked p_self.seq. p_self.data is
                    # complete.
                    self.seq = self.sindex = self.eindex = None
                    raise IndexError(index)
                self.eindex = eindex = -1
        self.eindex = eindex
        return data[i]
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
