import os
import sys
import json
from argparse import ArgumentParser

from BatchBuildUtils import origin_version, copy_dlls


def _updated(i, s):
    if i < 0:
        print(s)
    else:
        print('[{}] ({}) {}'.format(_version, i + 1, s))

parser = ArgumentParser()
parser.add_argument('devfolder',
                    help='Develop Folder contains source files, '
                    'where subfolder "Origin" contans output dlls')
parser.add_argument('-w', '--Win32',
                    help='Platform Win32',
                    action='store_true')
parser.add_argument('-x', '--x64',
                    help='Platform x64',
                    action='store_true')
args = parser.parse_args()

with open('settings.json') as f:
    settings = json.load(f)
    MASTER_VERSION = settings['MasterVersion']
    PROJ_SUFFIX = settings.get('PorjSubffix', '')
_version = origin_version(args.devfolder, MASTER_VERSION)

platforms = []
if args.Win32:
    platforms.append(True)
if args.x64:
    platforms.append(False)
for p in platforms:
    copy_dlls(os.path.join(args.devfolder, 'Origin'),
              p,
              _version,
              _updated,
              os.path.join(args.devfolder, 'Source/vc32/orgmain/OriginAll{}.sln'.format(PROJ_SUFFIX)),)
