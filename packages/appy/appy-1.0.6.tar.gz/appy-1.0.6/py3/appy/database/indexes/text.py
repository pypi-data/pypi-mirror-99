'''An index for Text fields, splitting text into words'''

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
from appy.database.indexes import Index
from appy.utils.string import Normalize

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class TextIndex(Index):
    '''Index for Text fields'''

    # For a Text index, a value to store in the index is already and always
    # built as a tuple (by m_toIndexed hereabove): so it it always considered to
    # be "multiple", and it is useless to convert it to a tuple.
    def isMultiple(self, value, inIndex=False): return isinstance(value, tuple)
    def getMultiple(self, value): return value

    # A Text index potentially contains a large number of values. Comparing
    # values while reindexing an object may be inefficient, so here, we force
    # bypassing value comparison: everytime an object will be reindexed, all
    # existing values for a Text index will be removed and new ones will be
    # re-inserted.
    def valueEquals(self, value, current): return

    @classmethod
    def toIndexed(class_, value, field, normalize=True, ignore=2,
                  ignoreNumbers=False):
        '''Splits the plain text p_value into words'''
        # Words whose length is <= p_ignore are ignored, excepted, if
        # p_ignoreNumbers is False, words being numbers.
        if not value: return
        # Create a set
        r = set()
        if normalize:
            value = Normalize.text(value)
        for word in value.split():
            # Keep this word or not ?
            if len(word) <= ignore:
                keepIt = not ignoreNumbers and word.isdigit()
            else:
                keepIt = True
            if keepIt:
                r.add(word)
        return tuple(r)

    # No need to override m_toString in order to normalize the value: it will be
    # done by the global "searchable" index.

    @classmethod
    def toTerm(class_, value, field):
        '''Normalizes p_value in order to be used as a search term'''
        return Normalize.text(value)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
