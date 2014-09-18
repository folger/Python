import sys
import os
import subprocess
import shutil
import winreg
from time import sleep, localtime, strftime

from PyQt4.QtGui import *
from PyQt4.QtCore import *


def BinFile32Release():
    return (
        "gsodbc9.dll",
        "Lababf32.dll",
        "libapr.dll",
        "libsie.dll",
        "MOCABaseTypes9.dll",
        "nlsf9.dll",
        "O3DGL9.dll",
        "oc3dx9.dll",
        "OCcontour9.dll",
        "ocim9.dll",
        "ocmath29.dll",
        "ocMath9.dll",
        "ocmathsp9.dll",
        "OCMmLink9.dll",
        "OCntrls9.dll",
        "OCompiler9.dll",
        "ocStatEx9.dll",
        "octree_Utils9.dll",
        "OCTree9.dll",
        "ocUtils9.dll",
        "ocuv9.dll",
        "OCVImg.dll",
        "OD9.dll",
        "odbc9.dll",
        "odcfl9.dll",
        "oExtFile9.dll",
        "offt9.dll",
        "OFFTW9.dll",
        "ofgp9.dll",
        "OFIO9.dll",
        "ogrid9.dll",
        "ohtmlhelp9.dll",
        "ohttp9.dll",
        "OIFileDlg9.dll",
        "oimg9.dll",
        "OImgLT9.dll",
        "OK3DGL9.dll",
        "ok9.dll",
        "okUtil9.dll",
        "OKXF9.dll",
        "OlbtEdit9.dll",
        "OLTmsg9.dll",
        "omail9.dll",
        "OMat9.dll",
        "omocavc9.dll",
        "ONAG_ex9.dll",
        "ONag9.dll",
        "ONLSF9.dll",
        "OODBC9.dll",
        "OODR9.dll",
        "ooff60.dll",
        "OPack9.dll",
        "OPattern_Utils9.dll",
        "opencv_core.dll",
        "opencv_highgui.dll",
        "opencv_imgproc.dll",
        "OPfm9.dll",
        "OPFMFuncs9.dll",
        "orespr9.dll",
        "Origin92.exe",
        "OStat.dll",
        "Osts9.dll",
        "otext9.dll",
        "OTools.dll",
        "OTreeEditor9.dll",
        "oTreeGrid9.dll",
        "ou9.dll",
        "OUim9.dll",
        "Outl9.dll",
        "OVideoReader9.dll",
        "OVideoWriter9.dll",
        "owxGrid9.dll",
        "wxbase28.dll",
        "wxmsw28_core.dll",
        "oErrMsg.dll",
        "nlsfWiz9.dll",
        "oImgProc.dll",
        "OImage.dll",
        "libgif.dll",
        r"OriginC\OriginLab\ODlg.dll",
        r"OriginC\OriginLab\ODlg8.dll",
        r"OriginC\OriginLab\ODlgA9.dll",
        r"OriginC\OriginLab\ImportWiz.dll",
        r"CrashRpt1402.dll",
        r"32bit\CrashSender1402.exe",
        r"32bit\dbghelp.dll",
        r"32bit\PyDLLs\OPython.dll",
        r"32bit\Py27DLLs\OPython27.dll",
        r"32bit\PyDLLs\_PyOrigin.pyd"
        )


def BinFile64Release():
    return (
        "gsodbc9_64.dll",
        "libapr_64.dll",
        "libsie_64.dll",
        "MOCABaseTypes9_64.dll",
        "nlsf9_64.dll",
        "O3DGL9_64.dll",
        "OABFFIO64.dll",
        "oc3dx9_64.dll",
        "OCallFN64.dll",
        "OCcontour9_64.dll",
        "ocim9_64.dll",
        "ocmath29_64.dll",
        "ocMath9_64.dll",
        "ocmathsp9_64.dll",
        "OCMmLink9_64.dll",
        "OCntrls9_64.dll",
        "OCompiler9_64.dll",
        "ocStatEx9_64.dll",
        "octree_Utils9_64.dll",
        "OCTree9_64.dll",
        "ocUtils9_64.dll",
        "ocuv9_64.dll",
        "OCVImg_64.dll",
        "OD9_64.dll",
        "odbc9_64.dll",
        "odcfl9_64.dll",
        "oExtFile9_64.dll",
        "offt9_64.dll",
        "OFFTW9_64.dll",
        "ofgp9_64.dll",
        "OFIO9_64.dll",
        "ogrid9_64.dll",
        "ohtmlhelp9_64.dll",
        "ohttp9_64.dll",
        "OIFileDlg9_64.dll",
        "oimg9_64.dll",
        "OImgLT9_64.dll",
        "OK3DGL9_64.dll",
        "ok9_64.dll",
        "okUtil9_64.dll",
        "OKXF9_64.dll",
        "OlbtEdit9_64.dll",
        "OLTmsg9_64.dll",
        "omail9_64.dll",
        "OMat9_64.dll",
        "omocavc9_64.dll",
        "ONAG_ex9_64.dll",
        "ONag9_64.dll",
        "ONLSF9_64.dll",
        "OODBC9_64.dll",
        "OODR9_64.dll",
        "ooff60_64.dll",
        "OPack9_64.dll",
        "OPattern_Utils9_64.dll",
        "opencv_core_64.dll",
        "opencv_highgui_64.dll",
        "opencv_imgproc_64.dll",
        "OPfm9_64.dll",
        "OPFMFuncs9_64.dll",
        "orespr9_64.dll",
        "Origin92_64.exe",
        "OStat_64.dll",
        "Osts9_64.dll",
        "otext9_64.dll",
        "OTools_64.dll",
        "OTreeEditor9_64.dll",
        "oTreeGrid9_64.dll",
        "ou9_64.dll",
        "OUim9_64.dll",
        "Outl9_64.dll",
        "OVideoReader9_64.dll",
        "OVideoWriter9_64.dll",
        "owxGrid9_64.dll",
        "wxbase28_64.dll",
        "wxmsw28_core_64.dll",
        "oErrMsg_64.dll",
        "nlsfWiz9_64.dll",
        "oImgProc_64.dll",
        "OImage_64.dll",
        "libgif_64.dll",
        r"OriginC\OriginLab\ODlg_64.dll",
        r"OriginC\OriginLab\ODlg8_64.dll",
        r"OriginC\OriginLab\ODlgA9_64.dll",
        r"OriginC\OriginLab\ImportWiz_64.dll",
        r"CrashRpt1402_64.dll",
        r"64bit\CrashSender1402.exe",
        r"64bit\dbghelp.dll",
        r"64bit\PyDLLs\OPython.dll",
        r"64bit\Py27DLLs\OPython27.dll",
        r"64bit\PyDLLs\_PyOrigin.pyd",
        )


assert(len(BinFile32Release())+1 == len(BinFile64Release()))


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
        dlls = BinFile32Release() if win32 else BinFile64Release()
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
        self.path = os.path.join(r'\\fs1\dev\92_dlls', platformpath)
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
        shutil.copyfile(os.path.join(self.binfolder, dll), os.path.join(self.path, dll))


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
                shutil.copyfile(os.path.join(self.srcfolder, f), os.path.join(self.desfolder, f))
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
        self.updateStatus.emit(strftime("%Y-%m-%d %H:%M:%S", localtime()) if ret == 0 else "Build Failed")
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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Batch Build')
        self.setFixedSize(250, 460)

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

        self.loadSetting(MAIN_WINDOW_GEOMETRY, lambda val: self.restoreGeometry(val))

        def str2bool(s): return s == 'true' or s == 'True'
        self.loadSetting(SLN_ORIGIN, lambda val: self.slnOrigin.setChecked(str2bool(val)))
        self.loadSetting(SLN_VIEWER, lambda val: self.slnViewer.setChecked(str2bool(val)))
        self.loadSetting(SLN_ORGLAB, lambda val: self.slnOrglab.setChecked(str2bool(val)))
        self.loadSetting(CHECK_32_RELEASE, lambda val: self.check32Release.setChecked(str2bool(val)))
        self.loadSetting(CHECK_32_DEBUG, lambda val: self.check32Debug.setChecked(str2bool(val)))
        self.loadSetting(CHECK_64_RELEASE, lambda val: self.check64Release.setChecked(str2bool(val)))
        self.loadSetting(CHECK_64_DEBUG, lambda val: self.check64Debug.setChecked(str2bool(val)))
        self.loadSetting(CHECK_COPY_DLLS_AFTER_BUILD, lambda val: self.checkCopyAfterBuild.setChecked(str2bool(val)))
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

        self.connect(self.check32Release, SIGNAL("clicked()"), self.onConfigurationChanged)
        self.connect(self.check32Debug, SIGNAL("clicked()"), self.onConfigurationChanged)
        self.connect(self.check64Release, SIGNAL("clicked()"), self.onConfigurationChanged)
        self.connect(self.check64Debug, SIGNAL("clicked()"), self.onConfigurationChanged)

        layout = QGridLayout()
        layout.addWidget(self.check32Release, 0, 0)
        layout.addWidget(self.check64Release, 0, 1)
        layout.addWidget(self.check32Debug, 1, 0)
        layout.addWidget(self.check64Debug, 1, 1)
        group = QGroupBox('Configuration')
        group.setLayout(layout)
        return group

    def createActionGroup(self):
        self.btnBuild = self.createButton('Build')
        self.btnClean = self.createButton('Clean')
        self.btnCopyToFS1 = self.createButton('Copy to fs1 (Release)')
        self.btnDeleteBin = self.createButton('Delete Binaries (Release)')
        self.btnCopyPDB = self.createButton('Copy PDBs (Release)')
        self.btnCopyMAP = self.createButton('Copy MAPs (Release)')
        self.checkCopyAfterBuild = QCheckBox('Copy files after Build (Release)')
        self.checkCopyAfterBuild.setChecked(True)

        self.connect(self.btnBuild, SIGNAL("clicked()"), self.build)
        self.connect(self.btnCopyToFS1, SIGNAL("clicked()"), self.copyToFS1)
        self.connect(self.btnDeleteBin, SIGNAL("clicked()"), self.deleteBin)
        self.connect(self.btnClean, SIGNAL("clicked()"), self.clean)
        self.connect(self.btnCopyPDB, SIGNAL("clicked()"), self.copyPDB)
        self.connect(self.btnCopyMAP, SIGNAL("clicked()"), self.copyMAP)

        layout = QVBoxLayout()
        layout.addWidget(self.checkCopyAfterBuild)
        layout.addWidget(self.btnBuild)
        layout.addWidget(self.btnClean)
        layout.addWidget(self.btnCopyToFS1)
        layout.addWidget(self.btnDeleteBin)
        layout.addWidget(self.btnCopyPDB)
        layout.addWidget(self.btnCopyMAP)
        group = QGroupBox('Action')
        group.setLayout(layout)
        return group

    def createButton(self, text):
        btn = QPushButton(text)
        btn.setFixedHeight(30)
        return btn

    def build(self):
        mythread = BuildThread(self)
        mythread.enabled.connect(self.enableAll)
        if self.checkCopyAfterBuild.isChecked():
            mythread.copydlls.connect(self.copyToFS1)
        mythread.error.connect(self.errorReport)
        mythread.dummy.connect(self.dummy)
        mythread.updateStatus.connect(self.updateStatus)
        mythread.build_configurations = self.getBuildConfigurations()
        mythread.slnfiles = self.solutionFiles
        mythread.start()

    def copyToFS1(self):
        mythread = CopyDllThread(self)
        mythread.binfolder = self.binFolder
        mythread.win32 = self.check32Release.isChecked()
        mythread.x64 = self.check64Release.isChecked()
        mythread.start()

    def deleteBin(self):
        mythread = DeleteDllThread(self)
        mythread.binfolder = self.binFolder
        mythread.win32 = self.check32Release.isChecked()
        mythread.x64 = self.check64Release.isChecked()
        mythread.start()

    def clean(self):
        mythread = BuildThread(self)
        mythread.enabled.connect(self.enableAll)
        mythread.build_configurations = self.getBuildConfigurations(['/t:clean'])
        mythread.slnfiles = self.solutionFiles
        mythread.start()

    def copyPDB(self):
        mythread = CopyFilesThread(self)
        mythread.srcfolder = os.path.join(self.outFolder, 'PDB_Release')
        mythread.desfolder = r'\\fs1\dev\PDBs\GZBuild'
        mythread.start()

    def copyMAP(self):
        mythread = CopyFilesThread(self)
        mythread.srcfolder = os.path.join(self.outFolder, 'MapFiles')
        mythread.desfolder = r'\\fs1\dev\Maps\GZBuild'
        mythread.start()

    def onConfigurationChanged(self):
        enableRelease = self.check32Release.isChecked() or self.check64Release.isChecked()
        self.btnCopyToFS1.setEnabled(enableRelease)
        self.btnDeleteBin.setEnabled(enableRelease)
        self.checkCopyAfterBuild.setEnabled(enableRelease)

        enable = enableRelease or self.check32Debug.isChecked() or self.check64Debug.isChecked()
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
    def binFolder(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\OriginLab\VS')
        try:
            return winreg.QueryValueEx(key, 'BuildBinDir')[0]
        except WindowsError:
            pass
        finally:
            winreg.CloseKey(key)
        try:
            return os.path.join(os.environ['develop'], 'Origin')
        except KeyError:
            print('Fail to detect binary folder')
        return ''

    @property
    def solutionFiles(self):
        def getSourceFolder():
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r'Software\OriginLab\VS')
            try:
                return winreg.QueryValueEx(key, 'BuildCodeBaseDir')[0]
            except WindowsError:
                pass
            finally:
                winreg.CloseKey(key)
            try:
                return os.path.join(os.environ['develop'], 'Source')
            except KeyError:
                print('Fail to detect build source folder')
            return ''

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
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\OriginLab\VS')
        try:
            return winreg.QueryValueEx(key, 'BuildOutDir')[0]
        except WindowsError:
            pass
        finally:
            winreg.CloseKey(key)
        try:
            return os.path.join(os.environ['develop'], 'Out')
        except KeyError:
            print('Fail to detect Out folder')
        return ''

    def getBuildConfigurations(self, extra_option=[]):
        def getBuildConfiguration(win32, release):
            config = ['msbuild', '/m']
            config.append('/p:configuration={}'.format('Release' if release else 'Debug'))
            config.append('/p:platform={}'.format('Win32' if win32 else 'x64'))
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
            QMessageBox.information(self, 'Cannot Quit', 'Please wait for building process finish')
            event.ignore()
        else:
            settings = QSettings()
            settings.setValue(MAIN_WINDOW_GEOMETRY, self.saveGeometry())
            settings.setValue(SLN_ORIGIN, self.slnOrigin.isChecked())
            settings.setValue(SLN_VIEWER, self.slnViewer.isChecked())
            settings.setValue(SLN_ORGLAB, self.slnOrglab.isChecked())
            settings.setValue(CHECK_32_RELEASE, self.check32Release.isChecked())
            settings.setValue(CHECK_32_DEBUG, self.check32Debug.isChecked())
            settings.setValue(CHECK_64_RELEASE, self.check64Release.isChecked())
            settings.setValue(CHECK_64_DEBUG, self.check64Debug.isChecked())
            settings.setValue(CHECK_COPY_DLLS_AFTER_BUILD, self.checkCopyAfterBuild.isChecked())

    def loadSetting(self, key, func):
        settings = QSettings()
        value = settings.value(key)
        if value:
            func(value)


app = QApplication(sys.argv)
app.setOrganizationDomain('originlab.com')
app.setOrganizationName('originlab')
app.setApplicationName('BatchBuild')
app.setApplicationVersion('1.0.0')
dlg = BatchBuilder()
dlg.show()
app.exec_()
