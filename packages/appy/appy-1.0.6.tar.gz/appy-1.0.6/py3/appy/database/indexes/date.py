'''An index for Date fields'''

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
from DateTime import DateTime
from appy.database.indexes import Index

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class DateIndex(Index):
    '''Index for a Date field'''

    @classmethod
    def toIndexed(class_, value, field):
        '''Converts p_value, a DateTime instance, to its internal representation
           in the index.'''
        if not value: return
        if isinstance(value, int):
            # p_value is already an internal index representation, ready to be
            # indexed (probably a default value to index from
            # p_field.emptyIndexValue).
            return value
        # p_value is a DateTime instance that we will convert to an integer
        # ~~~
        # This code is inspired by the Zope catalog
        year,month,day,hours,minutes,seconds,zone = value.toZone('UTC').parts()
        r = (((year * 12 + month) * 31 + day) * 24 + hours) * 60 + minutes
        # Flatten to precision
        if field.indexPrecision > 1:
            r -= r % field.indexPrecision
        return r

    @classmethod
    def toTerm(class_, value, field):
        '''The passed p_value may already be an integer value (=the internal
           representation for a date in the index).'''
        return value if isinstance(value, int) \
                     else class_.toIndexed(value, field)

    @classmethod
    def fromIndexed(class_, value, field):
        '''Converts p_value, the internal integer representation of a date,
           into a DateTime instance.'''
        # p_indexed represents a number of minutes
        minutes = value % 60
        value = (value - minutes) / 60 # The remaining part, in hours
        # Get hours
        hours = value % 24
        value = (value - hours) / 24 # The remaining part, in days
        # Get days
        day = value % 31
        if day == 0: day = 31
        value = (value - day) / 31 # The remaining part, in months
        # Get months
        month = value % 12
        if month == 0: month = 12
        year = (value - month) / 12
        date= DateTime('%d/%d/%d %d:%d UTC'% (year, month, day, hours, minutes))
        return date.toZone(date.localZone())

    @classmethod
    def toString(class_, o, value):
        '''Returns the string representation of the date in p_value'''
        return o.tool.formatDate(value, format='%dt %d %mt %Y') if value \
                                                                else None
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
