import os
import re
import shutil
import json
import subprocess
from time import sleep

import folstools.win32.utils as win32utils
from folstools import dir_temp_change


def get_origin_binaries(folder, win32, version):
    for root, dirs, files in os.walk(folder):
        for f in files:
            if os.path.splitext(f)[1].lower() in ('.exe', '.dll', '.pyd'):
                ff = os.path.join(root, f)
                itype = win32utils.get_image_file_type(ff)
                if (win32 and itype == win32utils.IMAGE_FILE_MACHINE_I386 or
                   not win32 and itype == win32utils.IMAGE_FILE_MACHINE_AMD64):
                    props = win32utils.get_file_properties(ff)
                    try:
                        sI = props['StringFileInfo']
                        if sI['CompanyName'] == 'OriginLab Corporation':
                            v = sI['ProductVersion'].replace('.', '')
                            fileflags = props['FixedFileInfo']['FileFlags']
                            if v == version and (fileflags & 1) == 0:
                                yield ff.replace(folder + '\\', '')
                    except:
                        pass


def get_current_branch(dev_folder):
    with dir_temp_change(dev_folder):
        ret = subprocess.check_output('git branch').decode()
    for s in ret.strip().split('\n'):
        if s[0] == '*':
            return s[2:]
    return ''


def is_master_branch(dev_folder):
    return get_current_branch(dev_folder) == 'master'


def origin_version(dev_folder, default):
    current_branch = get_current_branch(dev_folder)
    m = re.match('(\d+)_release', current_branch)
    return m.group(1) if m else default


def before_copy_dlls(win32, version, updated):
    platformpath = '32bit' if win32 else '64bit'
    path = os.path.join(r'\\fs1\Dev\{}_dlls'
                        .format(version),
                        'win32' if win32 else 'x64')
    updated(-1, 'Delete dlls on {} ...'.format(path))
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


def copy_dlls(binfolder, win32, version, updated):
    dlls = get_origin_binaries(binfolder, win32, version)
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
