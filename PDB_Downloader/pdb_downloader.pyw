import sys
import os
import re
import json
import zipfile
from urllib.request import urlretrieve
from urllib.error import URLError
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sip


class PDBDownloader(QDialog):
    stop = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        with open('settings.json') as fr:
            settings = json.load(fr)
            self.buildPrefix = settings['CurrentBuildPrefix']
            self.curVer = re.search(r'Ir(\d+)', self.buildPrefix).group(1)
            self.ftp = settings['FTP']
            self.username = settings['Username']
            self.password = settings['Password']

        self.setWindowTitle('PDB Downloader({})'.
                            format(self.curVer))
        self.setFixedSize(250, 550)

        layout = QVBoxLayout()
        layout.addLayout(self.createBuildNumberLayout())
        layout.addWidget(self.createFileTypeGroup())
        layout.addWidget(self.createPlatformGroup())
        layout.addWidget(self.createModulesGroup())
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        layout.addLayout(self.createActionLayout())
        self.setLayout(layout)

    def createBuildNumberLayout(self):
        label = QLabel('Build Number')
        self.buildNum = QLineEdit('136')

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.buildNum)
        return layout

    def createFileTypeGroup(self):
        self.pdb = QCheckBox("PDB")
        self.pdb.setChecked(True)
        self.map = QCheckBox("MAP")

        layout = QHBoxLayout()
        layout.addWidget(self.pdb)
        layout.addWidget(self.map)
        group = QGroupBox('File Type')
        group.setLayout(layout)
        return group

    def createPlatformGroup(self):
        self.win32 = QCheckBox("Win32")
        self.win32.setChecked(True)
        self.x64 = QCheckBox("x64")

        layout = QHBoxLayout()
        layout.addWidget(self.win32)
        layout.addWidget(self.x64)
        group = QGroupBox('Platform')
        group.setLayout(layout)
        return group

    def createActionLayout(self):
        self.filename = QLabel('')
        self.start = QPushButton('Start')
        self.connect(self.start, SIGNAL("clicked()"), self.onStart)

        layout = QHBoxLayout()
        layout.addWidget(self.filename)
        layout.addStretch()
        layout.addWidget(self.start)
        return layout

    def createModulesGroup(self):
        modules = (
                "ok9",
                "okUtil9",
                "Outl9",
                "Origin93",
                "ou9",
                "OD9",
                "O3DGL9",
                "OK3DGL9",
                "OCntrls9",
                "ogrid9",
                "OKXF9",
                "omocavc9",
                "OCompiler9",
                "ocMath9",
                "octree_Utils9",
                "ocUtils9",
                "gsodbc9",
                "Lababf32",
                "libapr",
                "libsie",
                "MOCABaseTypes9",
                "nlsf9",
                "oc3dx9",
                "OCcontour9",
                "ocim9",
                "ocmath29",
                "ocmathsp9",
                "OCMmLink9",
                "ocStatEx9",
                "OCTree9",
                "ocuv9",
                "OCVImg",
                "odbc9",
                "odcfl9",
                "oExtFile9",
                "offt9",
                "OFFTW9",
                "ofgp9",
                "OFIO9",
                "ohtmlhelp9",
                "ohttp9",
                "OIFileDlg9",
                "oimg9",
                "OImgLT9",
                "OlbtEdit9",
                "OLTmsg9",
                "omail9",
                "OMat9",
                "ONAG_ex9",
                "ONag9",
                "ONLSF9",
                "OODBC9",
                "OODR9",
                "ooff60",
                "OPack9",
                "OPattern_Utils9",
                "opencv_core",
                "opencv_highgui",
                "opencv_imgproc",
                "OPfm9",
                "OPFMFuncs9",
                "orespr9",
                "OStat",
                "Osts9",
                "otext9",
                "OTools",
                "OTreeEditor9",
                "oTreeGrid9",
                "OUim9",
                "OVideoReader9",
                "OVideoWriter9",
                "owxGrid9",
                "wxbase28",
                "wxmsw28_core",
                "oErrMsg",
                "nlsfWiz9",
                "oImgProc",
                "OImage",
                "libgif",
                "ORserve9",
                )

        self.view = QListView()
        moduleItems = QStandardItemModel(self.view)
        for m in modules:
            item = QStandardItem(m)
            item.setCheckState(Qt.Unchecked)
            item.setCheckable(True)
            moduleItems.appendRow(item)
        self.view.setModel(moduleItems)

        self.resetChecks = QPushButton('Reset Checks')
        self.connect(self.resetChecks, SIGNAL("clicked()"), self.onResetChecks)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.resetChecks)
        group = QGroupBox('Modules')
        group.setLayout(layout)
        return group

    def onResetChecks(self):
        for module in self.modules():
            module.setCheckState(Qt.Unchecked)

    def onStart(self):
        if not self.pdb.isEnabled():
            self.stop.emit()
            return

        def files(module):
            def _format(fm): return fm.format(module)
            if self.pdb.isChecked():
                if self.win32.isChecked():
                    yield _format('{}.pdb.zip')
                if self.x64.isChecked():
                    yield _format('{}_64.pdb.zip')
            if self.map.isChecked():
                if self.win32.isChecked():
                    yield _format('{}.map.zip')
                if self.x64.isChecked():
                    yield _format('{}_64.map.zip')

        def all_files():
            for module in self.modules():
                if module.checkState() == Qt.Checked:
                    for f in files(module.text()):
                        buildFolder = self.buildPrefix + self.buildNum.text()
                        filename = os.path.join(os.environ['home'],
                                                'Desktop', buildFolder, f)
                        try:
                            os.makedirs(os.path.dirname(filename))
                        except FileExistsError:
                            pass
                        ftp = ('ftp://{}:{}@{}/Builds/{}/'
                               'MAP_and_PDB/{}/{}'
                               ).format(self.username,
                                        self.password,
                                        self.ftp,
                                        self.curVer,
                                        buildFolder,
                                        f)
                        yield ftp, filename

        dt = DownloadThread(self)
        dt.setfilename.connect(self.setFileName)
        dt.setrange.connect(self.setProgressRange)
        dt.progress.connect(self.updateProgress)
        dt.enable.connect(self.enableGUI)
        dt.error.connect(self.errorReport)
        dt.all_files = all_files
        dt.start()

    def setFileName(self, text):
        self.filename.setText(text)

    def updateProgress(self, val):
        self.progress.setValue(val)

    def setProgressRange(self, min, max):
        if min == 0 and max == 0:
            self.progress.reset()
        else:
            self.progress.setRange(min, max)

    def modules(self):
        moduleItems = self.view.model()
        for i in range(moduleItems.rowCount()):
            yield moduleItems.item(i, 0)

    def enableGUI(self, enable):
        self.buildNum.setEnabled(enable)
        self.pdb.setEnabled(enable)
        self.map.setEnabled(enable)
        self.win32.setEnabled(enable)
        self.x64.setEnabled(enable)
        self.view.setEnabled(enable)
        self.resetChecks.setEnabled(enable)
        if enable:
            self.start.setText('Start')
        else:
            self.start.setText('Stop')

    def errorReport(self, title, error):
        QMessageBox.information(self, title, error)

    def reject(self):
        self.close()

    def closeEvent(self, event):
        if not self.buildNum.isEnabled():
            QMessageBox.information(self, 'Cannot Quit',
                                    'Please wait for download finish '
                                    'or click Stop button')
            event.ignore()


class StopFetch(Exception):
    pass


class DownloadThread(QThread):
    setfilename = pyqtSignal(str)
    setrange = pyqtSignal(int, int)
    progress = pyqtSignal(int)
    enable = pyqtSignal(bool)
    error = pyqtSignal(str, str)

    def __init__(self, parent):
        super().__init__(parent)
        self.stop = False
        parent.stop.connect(self.setStop)

    def run(self):
        hasfile = False
        self.enable.emit(False)
        for ftp, filename in self.all_files():
            hasfile = True
            self.setfilename.emit(os.path.basename(filename))
            try:
                urlretrieve(ftp, filename, reporthook=self.progressHook)
            except StopFetch:
                os.remove(filename)
                break
            except URLError as e:
                self.error.emit('FTP Error', str(e))
            if os.path.isfile(filename):
                with zipfile.ZipFile(filename, 'r') as zf:
                    zf.extractall(os.path.dirname(filename))
                os.remove(filename)
        if not hasfile:
            self.error.emit('Error', ('Please select at least one module, '
                                      'and specify PDB/MAP, Win32/x64'))
        self.setfilename.emit('')
        self.setrange.emit(0, 0)
        self.enable.emit(True)

    def progressHook(self, count, blocksize, totalsize):
        if self.stop:
            raise StopFetch
        self.setrange.emit(0, totalsize-1)
        self.progress.emit(count * blocksize)

    def setStop(self):
        self.stop = True


sip.setdestroyonexit(False)
app = QApplication(sys.argv)
app.setOrganizationDomain('originlab.com')
app.setOrganizationName('originlab')
app.setApplicationName('PDBDownloader')
app.setApplicationVersion('1.0.0')
dlg = PDBDownloader()
dlg.show()
app.exec_()