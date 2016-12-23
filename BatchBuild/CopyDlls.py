import os
import sys
import json

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import BatchBuildUtils


def _updated(i, s):
    print('{} {}'.format(i + 1, s))


def _version():
    with open('settings.json') as f:
        settings = json.load(f)
        MASTER_VERSION = settings['MasterVersion']
    return BatchBuildUtils.origin_version(dev_folder, MASTER_VERSION)


dev_folder = sys.argv[1]
app = QApplication([])
mt = BatchBuildUtils.CopyDllThread(None, _version(), app)
mt.binfolder = os.path.join(dev_folder, 'Origin')
mt.updated.connect(_updated)
mt.win32 = False
mt.x64 = False
for c in sys.argv[2:]:
    if c == 'Win32':
        mt.win32 = True
    elif c == 'x64':
        mt.x64 = True
mt.start()
app.exec()
