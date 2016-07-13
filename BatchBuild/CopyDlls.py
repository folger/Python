import os
import sys
import BatchBuildUtils
from PyQt4.QtGui import *
from PyQt4.QtCore import *


def _updated(i, s):
    print('{} {}'.format(i + 1, s))


dev_folder = sys.argv[1]
app = QApplication([])
mt = BatchBuildUtils.CopyDllThread(None, sys.argv[2], app)
mt.binfolder = os.path.join(dev_folder, 'Origin')
mt.updated.connect(_updated)
mt.win32 = False
mt.x64 = False
for c in sys.argv[3:]:
    if c == 'Win32':
        mt.win32 = True
    elif c == 'x64':
        mt.x64 = True
mt.start()
app.exec()
