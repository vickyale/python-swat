#!/usr/bin/env python
# encoding: utf-8
#
# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

'''
SWAT C library functions

'''

from __future__ import print_function, division, absolute_import, unicode_literals

import glob
import os
import sys
from .utils.compat import PY3, WIDE_CHARS, a2u
from .exceptions import SWATError

# pylint: disable=E1101

_pyswat = None


def _import_pyswat():
    ''' Import version-specific _pyswat package '''
    global _pyswat

    import glob
    import importlib
    import os
    import sys

    platform = 'linux'
    if sys.platform.lower().startswith('win'):
        platform = 'win'
    elif sys.platform.lower().startswith('darwin'):
        platform = 'mac'

    if PY3:
        libname = '_py%s%sswat' % (sys.version_info[0], sys.version_info[1])
    elif WIDE_CHARS:
        libname = '_pyswatw'
    else:
        libname = '_pyswat'

    # Bail out if we aren't on Linux
#   if platform != 'linux':
#       raise ValueError('Currently, Linux is the only platform with support '
#                        'for the binary protocol.  You must connect to CAS '
#                        'using the REST interface on this platform.')

    # Bail out if the C extension doesn't exist
    if not glob.glob(os.path.join(os.path.dirname(__file__), 'lib',
                                  platform, libname + '.*')):
        raise ValueError('The extensions for the binary protocol have not been '
                         'installed.  You can either install them using the full '
                         'platform-dependent install file, or use the REST interface '
                         'as an alternative.')

    # Make sure the correct libssl.so is used
    libssl = list(sorted(glob.glob(os.path.join(sys.prefix, 'lib', 'libssl.so*'))))
    if libssl:
        os.environ['TKESSL_OPENSSL_LIB'] = libssl[-1]

    # Try to import the C extension
    try:
        _pyswat = importlib.import_module('.lib.%s.%s' % (platform, libname),
                                          package='swat')

    except ImportError:
        raise ValueError(('Could not import import %s.  This is likely due to an '
                          'incorrect SAS TK path or an error while loading the SAS TK '
                          'subsystem. You can try using the REST interface '
                          'as an alternative.') % libname)


def SW_CASConnection(*args, **kwargs):
    ''' Return a CASConnection (importing _pyswat as needed) '''
    if _pyswat is None:
        _import_pyswat()
    return _pyswat.SW_CASConnection(*args, **kwargs)


def SW_CASValueList(*args, **kwargs):
    ''' Return a CASValueList (importing _pyswat as needed) '''
    if _pyswat is None:
        _import_pyswat()
    return _pyswat.SW_CASValueList(*args, **kwargs)


def SW_CASFormatter(*args, **kwargs):
    ''' Return a CASFormatter (importing _pyswat as needed) '''
    if _pyswat is None:
        _import_pyswat()
    return _pyswat.SW_CASFormatter(*args, **kwargs)


def SW_CASConnectionEventWatcher(*args, **kwargs):
    ''' Return a CASConnectionEventWatcher (importing _pyswat as needed) '''
    if _pyswat is None:
        _import_pyswat()
    return _pyswat.SW_CASConnectionEventWatcher(*args, **kwargs)


def SW_CASDataBuffer(*args, **kwargs):
    ''' Return a CASDataBuffer (importing _pyswat as needed) '''
    if _pyswat is None:
        _import_pyswat()
    return _pyswat.SW_CASDataBuffer(*args, **kwargs)


def SW_CASError(*args, **kwargs):
    ''' Return a CASError (importing _pyswat as needed) '''
    if _pyswat is None:
        _import_pyswat()
    return _pyswat.SW_CASError(*args, **kwargs)


def InitializeTK(*args, **kwargs):
    ''' Initialize the TK subsystem (importing _pyswat as needed) '''
    if _pyswat is None:
        _import_pyswat()
    return _pyswat.InitializeTK(*args, **kwargs)


def errorcheck(expr, obj):
    '''
    Check for generated error message

    Parameters
    ----------
    expr : any
       Result to return if no error happens
    obj : SWIG-based class
       Object to check for messages

    Raises
    ------
    SWATError
       If error message exists

    Returns
    -------
    `expr` argument
       The result of `expr`

    '''
    if obj is not None:
        msg = obj.getLastErrorMessage()
        if msg:
            raise SWATError(a2u(msg, 'utf-8'))
    return expr
