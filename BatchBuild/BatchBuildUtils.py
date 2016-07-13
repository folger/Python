import os
import re
import shutil
import json
from time import sleep
from PyQt4.QtGui import *
from PyQt4.QtCore import *


with open('dlls.json') as f:
    settings = json.load(f)
    BINFILE32RELEASE = settings['Bin32Release']
    BINFILE64RELEASE = settings['Bin64Release']


ORIGINFILEPATTERN = re.compile(r'(Origin)(\d+)((_64)?)')


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
        dlls = BINFILE32RELEASE if win32 else BINFILE64RELEASE
        self.setrange.emit(0, len(dlls) - 1)
        self.beforeDoJobs(win32)
        oldstatus = []
        self.getStatus.emit(oldstatus)
        for i, dll in enumerate(dlls):
            dll = ORIGINFILEPATTERN.sub(lambda m: m.group(1) +
                                        self.version() +
                                        m.group(3), dll)
            self.updated.emit(i, dll)
            self.doJob(dll)
        self.setrange.emit(0, 0)
        if oldstatus:
            self.updateStatus.emit(oldstatus[0])

    def version(self):
        if self._version:
            return self._version
        return self.parent().version.text()


class CopyDllThread(DllJobThread):
    def beforeDoJobs(self, win32):
        platformpath = '32bit' if win32 else '64bit'
        self.path = os.path.join(r'\\fs1\Dev\{}_dlls'
                                 .format(self.version()), platformpath)
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        for the_file in os.listdir(self.path):
            file_path = os.path.join(self.path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except:
                pass

        os.makedirs(os.path.join(self.path, platformpath, 'PyDLLs'))
        os.makedirs(os.path.join(self.path, platformpath, 'Py27DLLs'))
        os.makedirs(os.path.join(self.path, r'OriginC\Originlab'))

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
