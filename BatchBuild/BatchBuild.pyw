import sys
import os
import json
import subprocess
import winreg
import threading
from datetime import datetime as DT
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from folstools.qt.utils import *
from folstools import dir_temp_change
import BatchBuildUtils


with open('settings.json') as f:
    settings = json.load(f)
    SOURCEPATH = settings['SourcePath']
    MSBUILD = settings['MsBuild']
    VSPATH = settings['VSPath']


class GitPullThread(QThread):
    enabled = pyqtSignal(bool)
    dummy = pyqtSignal()

    def run(self):
        self.enabled.emit(False)
        print('Pulling from Git ...')
        with dir_temp_change(dev_folder):
            ret = subprocess.call('git pull --rebase')
            if ret != 0:
                self.dummy.emit()  # to eat up possible KeyboardInterrupt
        self.enabled.emit(True)


class BuildThread(QThread):
    enabled = pyqtSignal(bool)
    copydlls = pyqtSignal()
    error = pyqtSignal(str)
    dummy = pyqtSignal()
    updateStatus = pyqtSignal(str)

    def run(self):
        self.enabled.emit(False)
        self.updateStatus.emit('Building ...')
        start_time = DT.now()
        for slnfile in self.slnfiles:
            is_crashrpt = slnfile.find('CrashRpt') > 0
            ret = 0
            for config in self.buildConfigurations:
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
        if ret == 0:
            end_time = DT.now()
            elapsed = int((end_time - start_time).total_seconds())
            msg = '{} ({}s)'.format(end_time.strftime("%Y-%m-%d %H:%M:%S"),
                                    elapsed)
        else:
            msg = 'Build Failed'
        self.updateStatus.emit(msg)
        if ret == 0:
            self.copydlls.emit()
        self.enabled.emit(True)

SLN_ORIGIN = 'slnOrigin'
SLN_VIEWER = 'slnViewer'
SLN_ORGLAB = 'slnOrglab'
CHECK_32_RELEASE = 'check32Release'
CHECK_32_DEBUG = 'check32Debug'
CHECK_64_RELEASE = 'check64Release'
CHECK_64_DEBUG = 'check64Debug'
VERSION = 'version'
CHECK_COPY_DLLS = 'copyDllsAfterBuild'


class BatchBuilder(QDialog):
    def __init__(self, parent=None, devFolder=''):
        super().__init__(parent)
        self._devFolder = devFolder
        self.setWindowTitle(self.developFolder)
        self.setFixedSize(250, 550)

        icon = QIcon()
        icon.addPixmap(QPixmap('main.ico'))
        self.setWindowIcon(icon)

        self.progress = QProgressBar()
        self.labelStatus = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.createSolutionGroup())
        layout.addWidget(self.createConfigurationGroup())
        layout.addWidget(self.createActionGroup())
        layout.addWidget(self.progress)
        layout.addWidget(self.labelStatus)
        self.setLayout(layout)

        load_settings(
            (MAIN_WINDOW_GEOMETRY, lambda val: self.restoreGeometry(val)),
            (SLN_ORIGIN, settings_set_checked(self.slnOrigin)),
            (SLN_VIEWER, settings_set_checked(self.slnViewer)),
            (SLN_ORGLAB, settings_set_checked(self.slnOrglab)),
            (CHECK_32_RELEASE, settings_set_checked(self.check32Release)),
            (CHECK_32_DEBUG, settings_set_checked(self.check32Debug)),
            (CHECK_64_RELEASE, settings_set_checked(self.check64Release)),
            (CHECK_64_DEBUG, settings_set_checked(self.check64Debug)),
            (VERSION, self.version.setText),
            (CHECK_COPY_DLLS, settings_set_checked(self.checkCopyAfterBuild)))

        self.onConfigurationChanged()

    @create_group('Solution')
    def createSolutionGroup(self):
        layout = QHBoxLayout()

        def createRadio(label):
            radio = QRadioButton(label)
            self.connect(radio, SIGNAL("clicked()"),
                         self.onConfigurationChanged)
            layout.addWidget(radio)
            return radio

        self.slnOrigin = createRadio('&Origin')
        self.slnViewer = createRadio('&Viewer')
        self.slnOrglab = createRadio('Or&gLab')
        self.slnOrigin.setChecked(True)
        return layout

    @create_group('Configuration')
    def createConfigurationGroup(self):
        layout = QGridLayout()

        def createCheck(label, row, col):
            check = QCheckBox(label)
            self.connect(check, SIGNAL("clicked()"),
                         self.onConfigurationChanged)
            layout.addWidget(check, row, col)
            return check

        self.check32Release = createCheck('&32bit Release', 0, 0)
        self.check64Release = createCheck('&64bit Release', 0, 1)
        self.check32Debug = createCheck('3&2bit Debug', 1, 0)
        self.check64Debug = createCheck('6&4bit Debug', 1, 1)
        self.check32Release.setChecked(True)

        layout.addWidget(QLabel('Version'), 2, 0)
        for dll in BatchBuildUtils.BINFILE32RELEASE:
            m = BatchBuildUtils.ORIGINFILEPATTERN.match(dll)
            if m:
                version = m.group(2)
        self.version = QLineEdit(version)
        layout.addWidget(self.version, 2, 1)
        return layout

    @create_group('Action')
    def createActionGroup(self):
        layout = QVBoxLayout()

        def createButton(label, func):
            btn = QPushButton(label)
            btn.setFixedHeight(30)
            self.connect(btn, SIGNAL("clicked()"), func)
            layout.addWidget(btn)
            return btn

        self.checkCopyAfterBuild = QCheckBox('Copy &files after Build '
                                             '(Release)')
        self.checkCopyAfterBuild.setChecked(True)
        layout.addWidget(self.checkCopyAfterBuild)

        self.btnPull = createButton('', self.pull)
        self.updatePullLabel()
        self.btnBuild = createButton('&Build', self.build)
        # self.btnBuild.setAutoDefault(True)
        self.btnClean = createButton('&Clean', self.clean)
        self.btnCopyToFS1 = createButton('Copy to fs1 (Release)',
                                         self.copyToFS1)
        self.btnDeleteBin = createButton('Delete Binaries (Release)',
                                         self.deleteBin)
        self.btnCopyPDB = createButton('Copy PDBs (Release)', self.copyPDB)
        self.btnCopyMAP = createButton('Copy MAPs (Release)', self.copyMAP)
        self.btnOpenSln = createButton('Open Solution in Visual Studio',
                                       self.openSln)
        return layout

    def pull(self):
        mt = GitPullThread(self)
        mt.enabled.connect(self.enableAll)
        mt.dummy.connect(self.dummy)
        mt.start()

    def build(self):
        mt = BuildThread(self)
        mt.enabled.connect(self.enableAll)
        if self.checkCopyAfterBuild.isChecked():
            mt.copydlls.connect(self.copyToFS1)
        mt.error.connect(self.errorReport)
        mt.dummy.connect(self.dummy)
        mt.updateStatus.connect(self.updateStatus)
        mt.buildConfigurations = self.getBuildConfigurations()
        mt.slnfiles = self.solutionFiles
        mt.start()

    def copyToFS1(self):
        if not self.slnOrigin.isChecked():
            return
        mt = BatchBuildUtils.CopyDllThread(self)
        mt.binfolder = self.binFolder
        mt.win32 = self.check32Release.isChecked()
        mt.x64 = self.check64Release.isChecked()
        mt.start()

    def deleteBin(self):
        mt = BatchBuildUtils.DeleteDllThread(self)
        mt.binfolder = self.binFolder
        mt.win32 = self.check32Release.isChecked()
        mt.x64 = self.check64Release.isChecked()
        mt.start()

    def clean(self):
        if QMessageBox.question(self, 'Think Hard !!', 'Clean Solution ?',
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.Yes) == QMessageBox.Yes:
            mt = BuildThread(self)
            mt.enabled.connect(self.enableAll)
            mt.buildConfigurations = self.getBuildConfigurations(['/t:clean'])
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
        # the first one is CrashRpt
        subprocess.Popen([VSPATH, self.solutionFiles[1]])

    def onConfigurationChanged(self):
        enableRelease = (self.check32Release.isChecked() or
                         self.check64Release.isChecked())
        enableCopyDlls = enableRelease and self.slnOrigin.isChecked()
        for btn in (self.btnCopyToFS1, self.btnDeleteBin,
                    self.checkCopyAfterBuild,
                    self.btnCopyPDB, self.btnCopyMAP):
            btn.setEnabled(enableCopyDlls)

        enable = (enableRelease or self.check32Debug.isChecked() or
                  self.check64Debug.isChecked())
        for btn in (self.btnBuild, self.btnClean):
            btn.setEnabled(enable)

        self.btnPull.setEnabled(True)
        self.btnOpenSln.setEnabled(True)

    def updateProgress(self, val, name):
        self.progress.setValue(val)
        self.labelStatus.setText(name)

    def setProgressRange(self, min, max):
        if min == 0 and max == 0:
            self.progress.reset()
            self.labelStatus.setText('')
        else:
            self.progress.setRange(min, max)

    def enableAll(self, enable):
        for btn in (self.slnOrigin, self.slnViewer, self.slnOrglab,
                    self.version,
                    self.check32Release, self.check32Debug,
                    self.check64Release, self.check64Debug):
            btn.setEnabled(enable)

        if enable:
            self.onConfigurationChanged()
        else:
            for btn in (self.checkCopyAfterBuild, self.btnPull, self.btnBuild,
                        self.btnCopyToFS1, self.btnDeleteBin, self.btnClean,
                        self.btnCopyPDB, self.btnCopyMAP, self.btnOpenSln):
                btn.setEnabled(False)

    def errorReport(self, s):
        QMessageBox.information(self, 'Error', s)

    def dummy(self):
        pass

    def updateStatus(self, s):
        self.labelStatus.setText(s)

    def getStatus(self, oldstatus):
        oldstatus.append(self.labelStatus.text())

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
        return [os.path.join(getSourceFolder(), *args)
                for args in ((r'CrashRpt\CrashRpt.sln',),
                             (r'vc32\orgmain', getSln()))]

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

    def getBuildConfigurations(self, extraOption=[]):
        buildConfigurations = []
        configurations = (
            (self.check32Release, True, True),
            (self.check32Debug, True, False),
            (self.check64Release, False, True),
            (self.check64Debug, False, False))
        for check, win32, release in configurations:
            if check.isChecked():
                config = [MSBUILD, '/m']
                config.append('/p:configuration={}'
                              .format('Release' if release else 'Debug'))
                config.append('/p:platform={}'
                              .format('Win32' if win32 else 'x64'))
                buildConfigurations.append(config + extraOption)
        return buildConfigurations

    def updatePullLabel(self):
        with dir_temp_change(dev_folder):
            ret = subprocess.check_output('git branch').decode()
        for s in ret.strip().split('\n'):
            if s[0] == '*':
                current_branch = s[2:]
                break
        if current_branch[0] != '(':
            current_branch = '({})'.format(current_branch)
        self.btnPull.setText('Pull from Git {}'.format(current_branch))
        self.update_pull_timer = threading.Timer(3, self.updatePullLabel)
        self.update_pull_timer.start()

    def reject(self):
        self.close()

    def closeEvent(self, event):
        if not self.slnOrigin.isEnabled():
            QMessageBox.information(self, 'Cannot Quit',
                                    'Please wait for building process finish')
            event.ignore()
        else:
            if self.update_pull_timer:
                self.update_pull_timer.cancel()
            save_settings(
                (MAIN_WINDOW_GEOMETRY, self.saveGeometry()),
                (SLN_ORIGIN, self.slnOrigin.isChecked()),
                (SLN_VIEWER, self.slnViewer.isChecked()),
                (SLN_ORGLAB, self.slnOrglab.isChecked()),
                (CHECK_32_RELEASE, self.check32Release.isChecked()),
                (CHECK_32_DEBUG, self.check32Debug.isChecked()),
                (CHECK_64_RELEASE, self.check64Release.isChecked()),
                (CHECK_64_DEBUG, self.check64Debug.isChecked()),
                (VERSION, self.version.text()),
                (CHECK_COPY_DLLS, self.checkCopyAfterBuild.isChecked()))

dev_folder = sys.argv[1] if len(sys.argv) > 1 else ''
app = QApplication([])
app.setOrganizationDomain('originlab.com')
app.setOrganizationName('Originlab')
app.setApplicationName('BatchBuild({})'.format(dev_folder.replace('\\', '/')))
app.setApplicationVersion('1.0.0')
dlg = BatchBuilder(None, dev_folder)
dlg.show()
app.exec_()
