import os
import sys
import json

import BatchBuildUtils


def _updated(i, s):
    print('[{}] ({}) {}'.format(_version, i + 1, s))

dev_folder = sys.argv[1]

with open('settings.json') as f:
    settings = json.load(f)
    MASTER_VERSION = settings['MasterVersion']
_version = BatchBuildUtils.origin_version(dev_folder, MASTER_VERSION)

platforms = []
for c in sys.argv[2:]:
    if c == 'Win32':
        platforms.append(True)
    elif c == 'x64':
        platforms.append(False)
for p in platforms:
    BatchBuildUtils.copy_dlls(os.path.join(dev_folder, 'Origin'),
                              p,
                              _version,
                              _updated)
