import os
import re
import shutil
import json
import subprocess
from time import sleep

from folstools import dir_temp_change
from folstools.orglab.release import get_origin_binaries


def get_current_branch(dev_folder):
    with dir_temp_change(dev_folder):
        ret = subprocess.check_output('git branch',
                                      stdin=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      shell=True).decode()
    for s in ret.strip().split('\n'):
        if s[0] == '*':
            return s[2:]
    return ''


def is_master_branch(dev_folder):
    return get_current_branch(dev_folder) == 'master'


def origin_version(dev_folder, default):
    current_branch = get_current_branch(dev_folder)
    m = re.match('(\d+)b?_release', current_branch)
    return m.group(1) if m else default


def before_copy_dlls(win32, version, updated):
    platformpath = '32bit' if win32 else '64bit'
    path = os.path.join(r'\\fs1\Dev\{}_dlls'
                        .format(version),
                        'win32' if win32 else 'x64')
    updated(-1, 'Deleting dlls on {} ...'.format(path))
    if not os.path.isdir(path):
        os.makedirs(path)
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except:
            pass

    os.makedirs(os.path.join(path, platformpath, 'PyDLLs'))
    os.makedirs(os.path.join(path, platformpath, 'Py27DLLs'))
    os.makedirs(os.path.join(path, r'OriginC\Originlab'))
    return path


def copy_dlls(binfolder, win32, version, updated, sln=None):
    dlls = get_origin_binaries(binfolder, win32, version, sln)
    path = before_copy_dlls(win32, version, updated)
    for i, dll in enumerate(dlls):
        updated(i, dll)
        shutil.copyfile(os.path.join(binfolder, dll),
                        os.path.join(path, dll))


if __name__ == '__main__':
    for f in get_origin_binaries(os.path.join(os.getenv('Develop'), 'Origin'),
                                 True,
                                 '95'):
        print(f)
