import os
import re
import shutil
import json
import subprocess
from time import sleep

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import folstools.win32.utils as win32utils
from folstools import dir_temp_change


class DllJobThread(QThread):
    setrange = pyqtSignal(int, int)
    updated = pyqtSignal(int, str)
    enabled = pyqtSignal(bool)
    error = pyqtSignal(str)
    getStatus = pyqtSignal(list)
    updateStatus = pyqtSignal(str)

    def __init__(self, parent=None, version=None, app=None):
        super().__init__(parent)
        if parent:
            self.setrange.connect(parent.setProgressRange)
            self.updated.connect(parent.updateProgress)
            self.enabled.connect(parent.enableAll)
            self.error.connect(parent.errorReport)
            self.getStatus.connect(parent.getStatus)
            self.updateStatus.connect(parent.updateStatus)
        self._version = version
        self._app = app

    def run(self):
        self.enabled.emit(False)
        try:
            if self.win32:
                self.doJobs(True)
            if self.x64:
                self.doJobs(False)
        except WindowsError as e:
            self.error.emit(str(e))
        self.enabled.emit(True)
        if self._app:
            self._app.quit()

    def doJobs(self, win32):
        dlls = list(get_origin_binaries(self.binfolder, win32, self.version()))
        self.setrange.emit(0, len(dlls) - 1)
        self.beforeDoJobs(win32)
        oldstatus = []
        self.getStatus.emit(oldstatus)
        for i, dll in enumerate(dlls):
            self.updated.emit(i, dll)
            self.doJob(dll)
        self.setrange.emit(0, 0)
        if oldstatus:
            self.updateStatus.emit(oldstatus[0])

    def version(self):
        if self._version:
            return self._version
        return self.parent().version


class CopyDllThread(DllJobThread):
    def beforeDoJobs(self, win32):
        self.path = before_copy_dlls(win32, self.version())

    def doJob(self, dll):
        shutil.copyfile(os.path.join(self.binfolder, dll),
                        os.path.join(self.path, dll))


class DeleteDllThread(DllJobThread):
    def beforeDoJobs(self, win32):
        pass

    def doJob(self, dll):
        if dll.lower().endswith('dbghelp.dll'):
            return
        try:
            os.remove(os.path.join(self.binfolder, dll))
        except FileNotFoundError:
            pass


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


def before_copy_dlls(win32, version):
    platformpath = '32bit' if win32 else '64bit'
    path = os.path.join(r'\\fs1\Dev\{}_dlls'
                        .format(version),
                        'win32' if win32 else 'x64')
    print('Deleting dlls on {} ...'.format(path))
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
    path = before_copy_dlls(win32, version)
    for i, dll in enumerate(dlls):
        updated(i, dll)
        shutil.copyfile(os.path.join(binfolder, dll),
                        os.path.join(path, dll))


if __name__ == '__main__':
    for f in get_origin_binaries(os.path.join(os.getenv('Develop'), 'Origin'),
                                 True,
                                 '95'):
        print(f)
