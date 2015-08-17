import sys
import os
import json
import subprocess
import shutil
import winreg
from time import sleep, localtime, strftime
from PyQt4.QtGui import *
from PyQt4.QtCore import *
try:
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
except Exception:
    pass


with open('settings.json') as f:
    settings = json.load(f)
    SOURCEPATH = settings['SourcePath']
    MSBUILD = settings['MsBuild']
    VSPATH = settings['VSPath']
    BinFile32Release = settings['Bin32Release']
    BinFile64Release = settings['Bin64Release']


assert(len(BinFile32Release)+1 == len(BinFile64Release))


class DllJobThread(QThread):
    setrange = pyqtSignal(int, int)
    updated = pyqtSignal(int, str)
    enabled = pyqtSignal(bool)
    error = pyqtSignal(str)
    getStatus = pyqtSignal(list)
    updateStatus = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setrange.connect(parent.setProgressRange)
        self.updated.connect(parent.updateProgress)
        self.enabled.connect(parent.enableAll)
        self.error.connect(parent.errorReport)
        self.getStatus.connect(parent.getStatus)
        self.updateStatus.connect(parent.updateStatus)

    def run(self):
        # 32bit only dlls : Lababf32.dll
        # 64bit only dlls : OABFFIO64.dll, OCallFN64.dll

        self.enabled.emit(False)
        try:
            if self.win32:
                self.doJobs(True)
            if self.x64:
                self.doJobs(False)
        except WindowsError as e:
            self.error.emit(str(e))
        self.enabled.emit(True)

    def doJobs(self, win32):
        dlls = BinFile32Release if win32 else BinFile64Release
        self.setrange.emit(0, len(dlls)-1)
        self.beforeDoJobs(win32)
        oldstatus = []
        self.getStatus.emit(oldstatus)
        for i, dll in enumerate(dlls):
            self.updated.emit(i, dll)
            self.doJob(dll)
        self.setrange.emit(0, 0)
        self.updateStatus.emit(oldstatus[0])


class CopyDllThread(DllJobThread):
    def beforeDoJobs(self, win32):
        platformpath = '32bit' if win32 else '64bit'
        self.path = os.path.join(r'\\fs1\dev\93_dlls', platformpath)
        try:
            shutil.rmtree(self.path)
        except FileNotFoundError:
            pass

        sleep(2)
        os.mkdir(self.path)
        os.makedirs(os.path.join(self.path, platformpath, 'PyDLLs'))
        os.makedirs(os.path.join(self.path, platformpath, 'Py27DLLs'))
        os.makedirs(os.path.join(self.path, r'OriginC\Originlab'))

    def doJob(self, dll):
        shutil.copyfile(os.path.join(self.binfolder, dll),
                        os.path.join(self.path, dll))


class DeleteDllThread(DllJobThread):
    def beforeDoJobs(self, win32): pass

    def doJob(self, dll):
        if dll.lower().endswith('dbghelp.dll'):
            return
        try:
            os.remove(os.path.join(self.binfolder, dll))
        except FileNotFoundError:
            pass


class CopyFilesThread(QThread):
    setrange = pyqtSignal(int, int)
    updated = pyqtSignal(int, str)
    enabled = pyqtSignal(bool)
    error = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setrange.connect(parent.setProgressRange)
        self.updated.connect(parent.updateProgress)
        self.enabled.connect(parent.enableAll)
        self.error.connect(parent.errorReport)

    def run(self):
        try:
            shutil.rmtree(self.desfolder)
        except FileNotFoundError:
            pass
        os.mkdir(self.desfolder)

        files = os.listdir(self.srcfolder)
        self.enabled.emit(False)
        self.setrange.emit(0, len(files)-1)
        try:
            for i, f in enumerate(files):
                self.updated.emit(i, f)
                shutil.copyfile(os.path.join(self.srcfolder, f),
                                os.path.join(self.desfolder, f))
        except WindowsError as e:
            self.error.emit(str(e))
        self.enabled.emit(True)
        self.setrange.emit(0, 0)


class BuildThread(QThread):
    enabled = pyqtSignal(bool)
    copydlls = pyqtSignal()
    error = pyqtSignal(str)
    dummy = pyqtSignal()
    updateStatus = pyqtSignal(str)

    def run(self):
        self.enabled.emit(False)
        for slnfile in self.slnfiles:
            is_crashrpt = slnfile.find('CrashRpt') > 0
            ret = 0
            for config in self.build_configurations:
                skip = False
                if is_crashrpt:
                    for c in config:
                        if c.find('Debug') > 0:
                            skip = True
                            break
                if skip:
                    continue
                ret = subprocess.call(config + [slnfile])
                if ret != 0:
                    break
            if ret != 0:
                self.dummy.emit()  # to eat up possible KeyboardInterrupt
                self.error.emit('Build Error, check Command Window')
                break
        self.updateStatus.emit(strftime("%Y-%m-%d %H:%M:%S", localtime())
                               if ret == 0 else "Build Failed")
        if ret == 0:
            self.copydlls.emit()
        self.enabled.emit(True)

MAIN_WINDOW_GEOMETRY = 'mainWindowGeometry'
SLN_ORIGIN = 'slnOrigin'
SLN_VIEWER = 'slnViewer'
SLN_ORGLAB = 'slnOrglab'
CHECK_32_RELEASE = 'check32Release'
CHECK_32_DEBUG = 'check32Debug'
CHECK_64_RELEASE = 'check64Release'
CHECK_64_DEBUG = 'check64Debug'
CHECK_COPY_DLLS_AFTER_BUILD = 'copyDllsAfterBuild'


class BatchBuilder(QDialog):
    def __init__(self, parent=None, devFolder=''):
        super().__init__(parent)
        self._devFolder = devFolder
        self.setWindowTitle(self.developFolder)
        self.setFixedSize(250, 500)

        icon = QIcon()
        icon.addPixmap(QPixmap('main.ico'))
        self.setWindowIcon(icon)

        self.progress = QProgressBar()
        self.label_status = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.createSolutionGroup())
        layout.addWidget(self.createConfigurationGroup())
        layout.addWidget(self.createActionGroup())
        layout.addWidget(self.progress)
        layout.addWidget(self.label_status)
        self.setLayout(layout)

        self.loadSetting(MAIN_WINDOW_GEOMETRY,
                         lambda val: self.restoreGeometry(val))

        def setChecked(var):
            def wrapper(val):
                var.setChecked(val == 'true' or val == 'True')
            return wrapper
        self.loadSetting(SLN_ORIGIN, setChecked(self.slnOrigin))
        self.loadSetting(SLN_VIEWER, setChecked(self.slnViewer))
        self.loadSetting(SLN_ORGLAB, setChecked(self.slnOrglab))
        self.loadSetting(CHECK_32_RELEASE, setChecked(self.check32Release))
        self.loadSetting(CHECK_32_DEBUG, setChecked(self.check32Debug))
        self.loadSetting(CHECK_64_RELEASE, setChecked(self.check64Release))
        self.loadSetting(CHECK_64_DEBUG, setChecked(self.check64Debug))
        self.loadSetting(CHECK_COPY_DLLS_AFTER_BUILD,
                         setChecked(self.checkCopyAfterBuild))
        self.onConfigurationChanged()

    def createSolutionGroup(self):
        self.slnOrigin = QRadioButton('Origin')
        self.slnViewer = QRadioButton('Viewer')
        self.slnOrglab = QRadioButton('OrgLab')
        self.slnOrigin.setChecked(True)

        layout = QHBoxLayout()
        layout.addWidget(self.slnOrigin)
        layout.addWidget(self.slnViewer)
        layout.addWidget(self.slnOrglab)
        group = QGroupBox('Solution')
        group.setLayout(layout)
        return group

    def createConfigurationGroup(self):
        self.check32Release = QCheckBox('32bit Release')
        self.check32Debug = QCheckBox('32bit Debug')
        self.check64Release = QCheckBox('64bit Release')
        self.check64Debug = QCheckBox('64bit Debug')
        self.check32Release.setChecked(True)

        self.connect(self.check32Release, SIGNAL("clicked()"),
                     self.onConfigurationChanged)
        self.connect(self.check32Debug, SIGNAL("clicked()"),
                     self.onConfigurationChanged)
        self.connect(self.check64Release, SIGNAL("clicked()"),
                     self.onConfigurationChanged)
        self.connect(self.check64Debug, SIGNAL("clicked()"),
                     self.onConfigurationChanged)

        layout = QGridLayout()
        layout.addWidget(self.check32Release, 0, 0)
        layout.addWidget(self.check64Release, 0, 1)
        layout.addWidget(self.check32Debug, 1, 0)
        layout.addWidget(self.check64Debug, 1, 1)
        group = QGroupBox('Configuration')
        group.setLayout(layout)
        return group

    def createActionGroup(self):
        layout = QVBoxLayout()

        def create_button(label, func):
            btn = QPushButton(label)
            btn.setFixedHeight(30)
            self.connect(btn, SIGNAL("clicked()"), func)
            layout.addWidget(btn)
            return btn

        self.checkCopyAfterBuild = QCheckBox('Copy files after Build '
                                             '(Release)')
        self.checkCopyAfterBuild.setChecked(True)
        layout.addWidget(self.checkCopyAfterBuild)

        self.btnBuild = create_button('Build', self.build)
        self.btnClean = create_button('Clean', self.clean)
        self.btnCopyToFS1 = create_button('Copy to fs1 (Release)',
                                          self.copyToFS1)
        self.btnDeleteBin = create_button('Delete Binaries (Release)',
                                          self.deleteBin)
        self.btnCopyPDB = create_button('Copy PDBs (Release)', self.copyPDB)
        self.btnCopyMAP = create_button('Copy MAPs (Release)', self.copyMAP)
        self.btnOpenSln = create_button('Open Solution in Visual Studio', self.openSln)

        group = QGroupBox('Action')
        group.setLayout(layout)
        return group

    def build(self):
        mt = BuildThread(self)
        mt.enabled.connect(self.enableAll)
        if self.checkCopyAfterBuild.isChecked():
            mt.copydlls.connect(self.copyToFS1)
        mt.error.connect(self.errorReport)
        mt.dummy.connect(self.dummy)
        mt.updateStatus.connect(self.updateStatus)
        mt.build_configurations = self.getBuildConfigurations()
        mt.slnfiles = self.solutionFiles
        mt.start()

    def copyToFS1(self):
        mt = CopyDllThread(self)
        mt.binfolder = self.binFolder
        mt.win32 = self.check32Release.isChecked()
        mt.x64 = self.check64Release.isChecked()
        mt.start()

    def deleteBin(self):
        mt = DeleteDllThread(self)
        mt.binfolder = self.binFolder
        mt.win32 = self.check32Release.isChecked()
        mt.x64 = self.check64Release.isChecked()
        mt.start()

    def clean(self):
        mt = BuildThread(self)
        mt.enabled.connect(self.enableAll)
        mt.build_configurations = self.getBuildConfigurations(['/t:clean'])
        mt.slnfiles = self.solutionFiles
        mt.start()

    def copyPDB(self):
        mt = CopyFilesThread(self)
        mt.srcfolder = os.path.join(self.outFolder, 'PDB_Release')
        mt.desfolder = r'\\fs1\dev\PDBs\GZBuild'
        mt.start()

    def copyMAP(self):
        mt = CopyFilesThread(self)
        mt.srcfolder = os.path.join(self.outFolder, 'MapFiles')
        mt.desfolder = r'\\fs1\dev\Maps\GZBuild'
        mt.start()

    def openSln(self):
        subprocess.Popen([VSPATH, self.solutionFiles[1]]) # the first one is CrashRpt

    def onConfigurationChanged(self):
        enableRelease = (self.check32Release.isChecked() or
                         self.check64Release.isChecked())
        self.btnCopyToFS1.setEnabled(enableRelease)
        self.btnDeleteBin.setEnabled(enableRelease)
        self.checkCopyAfterBuild.setEnabled(enableRelease)

        enable = (enableRelease or self.check32Debug.isChecked() or
                  self.check64Debug.isChecked())
        self.btnBuild.setEnabled(enable)
        self.btnClean.setEnabled(enable)

        self.btnCopyPDB.setEnabled(True)
        self.btnCopyMAP.setEnabled(True)

    def updateProgress(self, val, name):
        self.progress.setValue(val)
        self.label_status.setText(name)

    def setProgressRange(self, min, max):
        if min == 0 and max == 0:
            self.progress.reset()
            self.label_status.setText('')
        else:
            self.progress.setRange(min, max)

    def enableAll(self, enable):
        self.slnOrigin.setEnabled(enable)
        self.slnViewer.setEnabled(enable)
        self.slnOrglab.setEnabled(enable)

        self.check32Release.setEnabled(enable)
        self.check32Debug.setEnabled(enable)
        self.check64Release.setEnabled(enable)
        self.check64Debug.setEnabled(enable)

        if enable:
            self.onConfigurationChanged()
        else:
            self.checkCopyAfterBuild.setEnabled(False)
            self.btnBuild.setEnabled(False)
            self.btnCopyToFS1.setEnabled(False)
            self.btnDeleteBin.setEnabled(False)
            self.btnClean.setEnabled(False)
            self.btnCopyPDB.setEnabled(False)
            self.btnCopyMAP.setEnabled(False)

    def errorReport(self, s):
        QMessageBox.information(self, 'Error', s)

    def dummy(self):
        pass

    def updateStatus(self, s):
        self.label_status.setText(s)

    def getStatus(self, oldstatus):
        oldstatus.append(self.label_status.text())

    @property
    def developFolder(self):
        if self._devFolder:
            return self._devFolder
        return SOURCEPATH

    @property
    def binFolder(self):
        return self.getFolder('BuildBinDir', 'Origin',
                              'Fail to detect binary folder')

    @property
    def solutionFiles(self):
        def getSourceFolder():
            return self.getFolder('BuildCodeBaseDir', 'Source',
                                  'Fail to detect build source folder')

        def getSln():
            if self.slnOrigin.isChecked():
                return 'OriginAll.sln'
            if self.slnViewer.isChecked():
                return 'OrgViewer.sln'
            if self.slnOrglab.isChecked():
                return 'OrgLab.sln'
        return [os.path.join(getSourceFolder(), r'CrashRpt\CrashRpt.sln'),
                os.path.join(getSourceFolder(), r'vc32\orgmain', getSln())]

    @property
    def outFolder(self):
        return self.getFolder('BuildOutDir', 'Out',
                              'Fail to detect Out folder')

    def getFolder(self, subkey, subfolder, error):
        key = None
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r'Software\OriginLab\VS')
            return winreg.QueryValueEx(key, subkey)[0]
        except WindowsError:
            pass
        finally:
            if key:
                winreg.CloseKey(key)
        try:
            return os.path.join(self.developFolder, subfolder)
        except KeyError:
            print(error)
        return ''

    def getBuildConfigurations(self, extra_option=[]):
        def getBuildConfiguration(win32, release):
            config = [MSBUILD, '/m']
            config.append('/p:configuration={}'
                          .format('Release' if release else 'Debug'))
            config.append('/p:platform={}'
                          .format('Win32' if win32 else 'x64'))
            return config + extra_option

        build_configurations = []
        if self.check32Release.isChecked():
            build_configurations.append(getBuildConfiguration(True, True))
        if self.check32Debug.isChecked():
            build_configurations.append(getBuildConfiguration(True, False))
        if self.check64Release.isChecked():
            build_configurations.append(getBuildConfiguration(False, True))
        if self.check64Debug.isChecked():
            build_configurations.append(getBuildConfiguration(False, False))
        return build_configurations

    def reject(self):
        self.close()

    def closeEvent(self, event):
        if not self.slnOrigin.isEnabled():
            QMessageBox.information(self, 'Cannot Quit',
                                    'Please wait for building process finish')
            event.ignore()
        else:
            settings = QSettings()
            settings.setValue(MAIN_WINDOW_GEOMETRY,
                              self.saveGeometry())
            settings.setValue(SLN_ORIGIN,
                              self.slnOrigin.isChecked())
            settings.setValue(SLN_VIEWER,
                              self.slnViewer.isChecked())
            settings.setValue(SLN_ORGLAB,
                              self.slnOrglab.isChecked())
            settings.setValue(CHECK_32_RELEASE,
                              self.check32Release.isChecked())
            settings.setValue(CHECK_32_DEBUG,
                              self.check32Debug.isChecked())
            settings.setValue(CHECK_64_RELEASE,
                              self.check64Release.isChecked())
            settings.setValue(CHECK_64_DEBUG,
                              self.check64Debug.isChecked())
            settings.setValue(CHECK_COPY_DLLS_AFTER_BUILD,
                              self.checkCopyAfterBuild.isChecked())

    def loadSetting(self, key, func):
        settings = QSettings()
        value = settings.value(key)
        if value:
            func(value)


app = QApplication([])
app.setOrganizationDomain('originlab.com')
app.setOrganizationName('Originlab')
app.setApplicationName('BatchBuild')
app.setApplicationVersion('1.0.0')
dlg = BatchBuilder(None, sys.argv[1] if len(sys.argv) > 1 else '')
dlg.show()
app.exec_()
