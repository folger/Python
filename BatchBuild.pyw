import sys
import os
import subprocess
import shutil
import winreg
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class BatchBuilder(QDialog):
    def __init__(self, parent=None):
        super(BatchBuilder, self).__init__(parent)
        self.setWindowTitle('Batch Build')

        self.progress = QProgressBar()

        layout = QVBoxLayout()
        layout.addWidget(self.createSolutionGroup())
        layout.addWidget(self.createConfigurationGroup())
        layout.addWidget(self.createActionGroup())
        layout.addWidget(self.progress)
        self.setLayout(layout)

    def createSolutionGroup(self):
        self.slnOrigin = QRadioButton('Origin')
        self.slnViewer = QRadioButton('Viewer')
        self.slnOrglab = QRadioButton('OrgLab')
        self.slnOrigin.setChecked(True)

        layout = QHBoxLayout()
        layout.addWidget(self.slnOrigin)
        layout.addWidget(self.slnViewer)
        layout.addWidget(self.slnOrglab)
        group = QGroupBox('Soluntion')
        group.setLayout(layout)
        return group

    def createConfigurationGroup(self):
        self.check32Release = QCheckBox('32bit Release')
        self.check32Debug = QCheckBox('32bit Debug')
        self.check64Release = QCheckBox('64bit Release')
        self.check64Debug = QCheckBox('64bit Debug')
        self.check32Release.setChecked(True)

        layout = QGridLayout()
        layout.addWidget(self.check32Release, 0, 0)
        layout.addWidget(self.check64Release, 0, 1)
        layout.addWidget(self.check32Debug, 1, 0)
        layout.addWidget(self.check64Debug, 1, 1)
        group = QGroupBox('Configuration')
        group.setLayout(layout)
        return group

    def createActionGroup(self):
        self.btnBatchBuild = QPushButton('Batch Build')
        self.btnCopyToFS1 = QPushButton('Copy to fs1(Release)')
        self.btnDeleteBin = QPushButton('Delete Binaries')
        self.btnClean = QPushButton('Clean Files')
        self.btnVerifyBin = QPushButton('Verify Binary Files')
        self.checkCopyAfterBuild = QCheckBox('Copy files after Build')
        self.checkCopyAfterBuild.setChecked(True)

        self.connect(self.btnBatchBuild, SIGNAL("clicked()"), self.batchBuild)
        self.connect(self.btnCopyToFS1, SIGNAL("clicked()"), self.copyToFS1)
        self.connect(self.btnDeleteBin, SIGNAL("clicked()"), self.deleteBin)
        self.connect(self.btnClean, SIGNAL("clicked()"), self.clean)
        self.connect(self.btnVerifyBin, SIGNAL("clicked()"), self.verifyBin)

        layout = QVBoxLayout()
        layout.addWidget(self.checkCopyAfterBuild)
        layout.addWidget(self.btnBatchBuild)
        layout.addWidget(self.btnCopyToFS1)
        layout.addWidget(self.btnDeleteBin)
        layout.addWidget(self.btnClean)
        layout.addWidget(self.btnVerifyBin)
        group = QGroupBox('Action')
        group.setLayout(layout)
        return group

    def batchBuild(self):
        sourcefolder = self.getSourceFolder()
        if len(sourcefolder) == 0:
            return

        slnfile = os.path.join(sourcefolder, r'vc32\orgmain', self.getSolutionFile())

        build_configurations = []
        if self.check32Release.isChecked():
            build_configurations.append(self.getBuildConfiguration(True, True))
        if self.check32Debug.isChecked():
            build_configurations.append(self.getBuildConfiguration(True, False))
        if self.check64Release.isChecked():
            build_configurations.append(self.getBuildConfiguration(False, True))
        if self.check64Debug.isChecked():
            build_configurations.append(self.getBuildConfiguration(False, False))

        class BuildThread(QThread):
            enabled = pyqtSignal(bool)
            copydlls = pyqtSignal()
            def run(self):
                self.enabled.emit(False)
                for config in self.build_configurations:
                    try:
                        ret = subprocess.call(config + [self.slnfile], shell=True)
                    except KeyboardInterrupt:
                        ret = 1
                    if ret != 0:
                        break
                else:
                    if self.copyAfterBuild:
                        self.copydlls.emit()
                self.enabled.emit(True)

        mythread = BuildThread(self)
        mythread.enabled.connect(self.enableAll)
        mythread.copydlls.connect(self.copyToFS1)
        mythread.build_configurations = build_configurations
        mythread.slnfile = slnfile
        mythread.copyAfterBuild = self.checkCopyAfterBuild.isChecked()
        mythread.start()

    def copyToFS1(self):
        BinFile32Release = (
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
            r"32bit\PyDLLs\_PyOrigin.pyd"
            )
        BinFile64Release = (
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
            r"64bit\PyDLLs\_PyOrigin.pyd",
            )
        assert(len(BinFile32Release)+1 == len(BinFile64Release))

        class CopyThread(QThread):
            setrange = pyqtSignal(int, int)
            updated = pyqtSignal(int)
            enabled = pyqtSignal(bool)
            def run(self):
                self.enabled.emit(False)
                if self.win32:
                    self.copydlls(True)
                if self.x64:
                    self.copydlls(False)
                self.enabled.emit(True)

            def copydlls(self, win32):
                dlls = BinFile32Release if win32 else BinFile64Release
                self.setrange.emit(0, len(dlls)-1)
                platformpath = '32bit' if win32 else '64bit'
                path = os.path.join(r'\\fs1\dev\92_dlls', platformpath)
                try:
                    shutil.rmtree(path)
                except FileNotFoundError:
                    pass
                os.mkdir(path)
                os.makedirs(os.path.join(path, platformpath, 'PyDLLs'))
                os.makedirs(os.path.join(path, r'OriginC\Originlab'))
                for i, dll in enumerate(dlls):
                    self.updated.emit(i)
                    shutil.copy(os.path.join(self.binfolder, dll), os.path.join(path, dll))

        mythread = CopyThread(self)
        mythread.setrange.connect(self.setProgressRange)
        mythread.updated.connect(self.updateProgress)
        mythread.enabled.connect(self.enableAll)
        mythread.binfolder = self.getBinFolder()
        mythread.win32 = self.check32Release.isChecked()
        mythread.x64 = self.check64Release.isChecked()
        mythread.start()

    def deleteBin(self):
        print('deleteBin')

    def clean(self):
        print('clean')

    def verifyBin(self):
        print('verifyBin')

    def updateProgress(self, val):
        self.progress.setValue(val)

    def setProgressRange(self, min, max):
        self.progress.setRange(min, max)

    def enableAll(self, enable):
        self.slnOrigin.setEnabled(enable)
        self.slnViewer.setEnabled(enable)
        self.slnOrglab.setEnabled(enable)

        self.check32Release.setEnabled(enable)
        self.check32Debug.setEnabled(enable)
        self.check64Release.setEnabled(enable)
        self.check64Debug.setEnabled(enable)

        self.btnBatchBuild.setEnabled(enable)
        self.btnCopyToFS1.setEnabled(enable)
        self.btnDeleteBin.setEnabled(enable)
        self.btnClean.setEnabled(enable)
        self.btnVerifyBin.setEnabled(enable)
        self.checkCopyAfterBuild.setEnabled(enable)

    def getSourceFolder(self):
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

    def getBinFolder(self):
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
    def getSolutionFile(self):
        if self.slnOrigin.isChecked():
            return 'OriginAll.sln'
        if self.slnViewer.isChecked():
            return 'OrgViewer.sln'
        if self.slnOrglab.isChecked():
            return 'OrgLab.sln'

    def getBuildConfiguration(self, win32, release):
        config = ['msbuild', '/m']
        config.append('/p:configuration={}'.format('Release' if release else 'Debug'))
        config.append('/p:platform={}'.format('Win32' if win32 else 'x64'))
        return config

app = QApplication(sys.argv)
dlg = BatchBuilder()
dlg.show()
app.exec_()
