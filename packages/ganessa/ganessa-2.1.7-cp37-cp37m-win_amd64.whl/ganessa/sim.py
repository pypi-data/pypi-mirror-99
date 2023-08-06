# -*- coding: utf-8 -*-
'''
# This script is duplicated as sim.py (for hydraulic and WQ simulation)
# and th.py (for thermo-hydraulic simulation)
'''
from __future__ import (unicode_literals, print_function, absolute_import)
import os.path as OP
from os import environ
import sys
import re

from ganessa._getdll import _getdllinfo

# required numpy version
_req_np_vers = (1, 13, 1) if sys.version_info.major == 3 else (1, 7, 0)
try:
    from numpy import __version__ as np_vers
    npv = tuple(map(int, np_vers.split('.')))
    if npv < _req_np_vers:
        raise ImportError
    del npv, np_vers
except ImportError:
    from ganessa.util import unistr
    uname = unistr(__name__)
    print('Error importing "' + uname + '": numpy '+
          '.'.join(map(str, _req_np_vers)) +' or above is required.')
    sys.exit('Required component for ' + uname + ' not found.')


# call from ganessa.sim --> Piccolo; ganessa.th --> Picalor
_bth = __name__.endswith('th')

# lookup for a matching folder, dll and import it
_dll_dir, _dll_name, _dll_api, _dll_context = _getdllinfo(_bth)
if not _dll_api:
    raise ImportError('DLL ' + _dll_name + ': not found or too old.\n')

# get the lang and the protection mode from the folder name
_m = re.search('(?:pic[a-z]*\d?|gan\w+?)_?(fr|fra|eng|esp|sp|uk|us)_?(ck)?\Z',
               _dll_dir, re.IGNORECASE)
_lang, _protmode = _m.group(1, 2) if _m else (None, None)
if not _lang:
    _lang = 'FR'
if not _protmode:
    _protmode = 'Flex?'
# print('Lang is:', _lang, ' * prot is:', _protmode)

# Binary result file
subdir = dict(FR='Travail', FRA='Travail', ESP='Trabajo',
              ENG='Work', UK='Work', US='Work')
_workdir = OP.join(_dll_dir, subdir.get(_lang.upper(), ''))
# fix workdir into Virtualstore
if not OP.exists(_workdir):
    _, tail = OP.splitdrive(_workdir)
    _workdir = OP.join(environ['localappdata'], 'VirtualStore', tail.lstrip('/\\'))
if OP.exists(_workdir):
    _fresult = OP.join(_workdir, 'result.bin')
else:
    _fresult = ''
del subdir

from ganessa import __version__
# modules for both sim and th
from ganessa.core import *
from ganessa.core import _gencmdw

# modules specific to sim / th
if _bth:
    from ganessa.core_th import *
else:
    from ganessa.core_sim import *
