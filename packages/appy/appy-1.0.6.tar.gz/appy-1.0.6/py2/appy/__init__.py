'''Appy allows you to create easily complete applications in Python'''

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
# ------------------------------------------------------------------------------
import os.path
import version
commercial = False

# ------------------------------------------------------------------------------
def getPath(): return os.path.dirname(__file__)

def getVersion():
    '''Returns a string containing the short and verbose Appy version'''
    if version.short == 'dev': return 'dev'
    return '%s (%s)' % version.short, version.verbose

def versionIsGreaterThanOrEquals(v):
    '''This method returns True if the current Appy version is greater than or
       equals p_v. p_v must have a format like "0.5.0".'''
    if version.short == 'dev':
        # We suppose that a developer knows what he is doing, so we return True
        return True
    else:
        paramVersion = [int(i) for i in v.split('.')]
        currentVersion = [int(i) for i in version.short.split('.')]
        return currentVersion >= paramVersion

# ------------------------------------------------------------------------------
class Object:
    '''At every place we need an object, but without any requirement on its
       class (methods, attributes,...) we will use this minimalist class.'''

    def __init__(self, **fields):
        for k, v in fields.iteritems():
            setattr(self, k, v)

    def __repr__(self):
        res = u'<O '
        for attrName, attrValue in self.__dict__.iteritems():
            v = attrValue
            if hasattr(v, '__repr__'):
                v = v.__repr__()
            try:
                res += u'%s=%s ' % (attrName, v)
            except UnicodeDecodeError:
                res += u'%s=<encoding problem> ' % attrName
        res  = res.strip() + '>'
        return res.encode('utf-8')

    def __nonzero__(self): return bool(self.__dict__)

    def d(self): return self.__dict__

    def get(self, name, default=None): return getattr(self, name, default)

    def __getitem__(self, k):
        '''Dict-like attribute get'''
        return getattr(self, k)

    def __setitem__(self, k, v):
        '''Dict-like attribute set'''
        self.__dict__[k] = v

    def __eq__(self, other):
        '''Equality between objects is, like standard Python dicts, based on
           equality of all their attributes and values.'''
        if isinstance(other, Object):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def update(self, other):
        '''Includes information from p_other into p_self'''
        for k, v in other.__dict__.iteritems():
            setattr(self, k, v)

    def clone(self):
        r = Object()
        r.update(self)
        return r

# ------------------------------------------------------------------------------
class Hack:
    '''This class proposes methods for patching some existing code with
       alternative methods.'''
    @staticmethod
    def patch(method, replacement, klass=None):
        '''This method replaces m_method with a p_replacement method, but
           keeps p_method on its class under name
           "_base_<initial_method_name>_". In the patched method, one may use
           Hack.base to call the base method. If p_method is static, you must
           specify its class in p_klass.'''
        # Get the class on which the surgery will take place
        isStatic = klass
        klass = klass or method.im_class
        # On this class, store m_method under its "base" name
        name = isStatic and method.func_name or method.im_func.__name__
        baseName = '_base_%s_' % name
        if isStatic:
            # If "staticmethod" isn't called hereafter, the static functions
            # will be wrapped in methods.
            method = staticmethod(method)
            replacement = staticmethod(replacement)
        setattr(klass, baseName, method)
        setattr(klass, name, replacement)

    @staticmethod
    def base(method, klass=None):
        '''Allows to call the base (replaced) method. If p_method is static,
           you must specify its p_klass.'''
        isStatic = klass
        klass = klass or method.im_class
        name = isStatic and method.func_name or method.im_func.__name__
        return getattr(klass, '_base_%s_' % name)

    @staticmethod
    def inject(patchClass, klass, verbose=False):
        '''Injects any method or attribute from p_patchClass into klass.'''
        # As a preamble, inject methods and attributes from p_patchClass's base
        # classes, if any.
        for base in patchClass.__bases__:
            Hack.inject(base, klass, verbose=verbose)
        patched = []
        added = []
        # Inject p_patchClass' own methods and attributes
        for name, attr in patchClass.__dict__.items():
            if name.startswith('__'): continue # Ignore special methods
            # Unwrap functions from static methods
            try:
                className = attr.__class__.__name__
            except AttributeError:
                # In Python 2, classes themselves have no defined class
                className = 'type'
            if className == 'staticmethod':
                attr = attr.__get__(attr)
                static = True
            else:
                static = False
            # Is this name already defined on p_klass ?
            if hasattr(klass, name):
                hasAttr = True
                klassAttr = getattr(klass, name)
            else:
                hasAttr = False
                klassAttr = None
            if hasAttr and (className != 'type') and \
               callable(attr) and callable(klassAttr):
                # Patch this method via Hack.patch
                if static:
                    Hack.patch(klassAttr, attr, klass)
                else:
                    Hack.patch(klassAttr, attr)
                patched.append(name)
            else:
                # Simply replace the static attr or add the new static
                # attribute or method.
                setattr(klass, name, attr)
                added.append(name)
        if verbose:
            pName = patchClass.__name__
            cName = klass.__name__
            print '%d method(s) patched from %s to %s (%s)' % \
                  (len(patched), pName, cName, str(patched))
            print '%d method(s) and/or attribute(s) added from %s to %s (%s)'%\
                  (len(added), pName, cName, str(added))
# ------------------------------------------------------------------------------
