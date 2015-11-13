import sys
import os
import re
import json
import zipfile
import traceback
from functools import partial
from subprocess import check_call, CalledProcessError, Popen
from urllib.request import urlretrieve
from urllib.error import URLError
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from folstools.qt.utils import *
import sip
try:
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
except Exception:
    pass


class PDBDownloader(QDialog):
    stop = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selfclose = False

        with open('settings.json') as fr:
            settings = json.load(fr)
            self.buildPrefix = settings['CurrentBuildPrefix']
            self.downloadPath = settings['DownloadPath']
            if not self.downloadPath:
                self.downloadPath = os.path.join(os.environ['home'], 'Desktop')
            self.buildPath = settings['BuildPath']
            self.curVer = re.match(r'Ir(\d+)', self.buildPrefix).group(1)
            self.ftp = settings['FTP']
            self.username = settings['Username']
            self.password = settings['Password']

        self.setWindowTitle('PDB Downloader({})'.
                            format(self.curVer))
        self.setFixedSize(250, 550)

        icon = QIcon()
        icon.addPixmap(QPixmap('main.png'))
        self.setWindowIcon(icon)

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
        self.buildNum = QLineEdit()
        self.checkLatest = QPushButton('&Latest')
        self.connect(self.checkLatest, SIGNAL("clicked()"), self.onCheckLatest)
        self.onCheckLatest()
        label = QLabel('B&uild Number')
        label.setBuddy(self.buildNum)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.buildNum)
        layout.addWidget(self.checkLatest)
        return layout

    @create_group('File Type')
    def createFileTypeGroup(self):
        self.pdb = QCheckBox("&PDB")
        self.pdb.setChecked(True)
        self.map = QCheckBox("&MAP")

        layout = QHBoxLayout()
        layout.addWidget(self.pdb)
        layout.addWidget(self.map)
        return layout

    @create_group('Platform')
    def createPlatformGroup(self):
        self.win32 = QCheckBox("Win&32")
        self.win32.setChecked(True)
        self.x64 = QCheckBox("x&64")
        self.x64.setChecked(True)

        layout = QHBoxLayout()
        layout.addWidget(self.win32)
        layout.addWidget(self.x64)
        return layout

    def createActionLayout(self):
        self.filename = QLabel('')
        self.start = QPushButton('&Start')
        self.start.setDefault(True)
        self.connect(self.start, SIGNAL("clicked()"), self.onStart)

        layout = QHBoxLayout()
        layout.addWidget(self.filename)
        layout.addStretch()
        layout.addWidget(self.start)
        return layout

    @create_group('Modules')
    def createModulesGroup(self):
        modules = [
                "ok9",
                "okUtil9",
                "Outl9",
                "ou9",
                "od9",
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
                "ofio9",
                "ohtmlhelp9",
                "ohttp9",
                "OIFileDlg9",
                "oimg9",
                "OImgLT9",
                "OlbtEdit9",
                "OLTmsg9",
                "omail9",
                "omat9",
                "ONAG_ex9",
                "ONAG9",
                "ONLSF9",
                "OODBC9",
                "OODR9",
                "ooff60",
                "OPack9",
                "OPattern_Utils9",
                "opencv_core",
                "opencv_highgui",
                "opencv_imgproc",
                "opfm9",
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
                "OImgProc",
                "OImage",
                "libgif",
                "ORserve9",
        ]
        modules.insert(0, 'Origin' + self.curVer)

        self.view = QListView()
        moduleItems = QStandardItemModel(self.view)
        for i, m in enumerate(modules):
            item = QStandardItem(m)
            item.setCheckState(Qt.Checked if i < 8 else Qt.Unchecked)
            item.setCheckable(True)
            moduleItems.appendRow(item)
        self.view.setModel(moduleItems)

        self.checkAll = QPushButton('&Check All')
        self.unCheckAll = QPushButton('Uncheck &All')
        self.connect(self.checkAll, SIGNAL("clicked()"), partial(self.onChecks, True))
        self.connect(self.unCheckAll, SIGNAL("clicked()"), partial(self.onChecks, False))

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.checkAll)
        layout.addWidget(self.unCheckAll)
        return layout

    def onCheckLatest(self):
        def latest_build_num():
            if not self.buildPath:
                return ''
            try:
                localBuildPath = os.path.join(self.buildPath, self.curVer, 'I')
                latestBuild = max(build for build in
                                  os.listdir(localBuildPath)
                                  if build.startswith('Ir'))
                return re.match(r'Ir\d+Sr\d_([0-9a-z]+)', latestBuild).group(1)
            except Exception:
                report_error()
        self.buildNum.setText(latest_build_num())

    def onChecks(self, checked):
        for module in self.modules():
            module.setCheckState(Qt.Checked if checked else Qt.Unchecked)

    def onStart(self):
        if not self.pdb.isEnabled():
            self.stop.emit()
            return

        if not self.buildNum.text().lstrip().rstrip():
            self.errorReport('Error', 'Please specify build number')
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
            buildFolder = self.buildPrefix + self.buildNum.text()
            localPath = os.path.join(self.downloadPath, buildFolder)
            try:
                os.makedirs(localPath)
            except FileExistsError:
                pass
            for module in self.modules():
                if module.checkState() == Qt.Checked:
                    for f in files(module.text()):
                        filename = os.path.join(localPath, f)
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
        self.checkLatest.setEnabled(enable)
        self.pdb.setEnabled(enable)
        self.map.setEnabled(enable)
        self.win32.setEnabled(enable)
        self.x64.setEnabled(enable)
        self.view.setEnabled(enable)
        self.checkAll.setEnabled(enable)
        if enable:
            self.start.setText('&Start')
            if self.selfclose:
                self.close()
        else:
            self.start.setText('S&top')

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
        folder = ''
        self.enable.emit(False)
        for ftp, filename in self.all_files():
            if not folder:
                folder = os.path.dirname(filename)
            if os.path.isfile(filename[:-4]):  # remove .zip
                continue
            self.setfilename.emit(os.path.basename(filename))
            self.setrange.emit(0, 0)
            try:
                urlretrieve(ftp, filename, reporthook=self.progressHook)
            except StopFetch:
                os.remove(filename)
                break
            except Exception:
                report_error()
                continue
            if os.path.isfile(filename):
                with zipfile.ZipFile(filename, 'r') as zf:
                    zf.extractall(os.path.dirname(filename))
                os.remove(filename)
        if folder:
            if os.listdir(folder):
                try:
                    check_call(['explorer', folder])
                except CalledProcessError:
                    pass
        else:
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


def report_error():
    error_file = 'error.txt'
    with open(error_file, 'w', encoding='utf-8-sig') as fw:
        print(traceback.format_exc(), file=fw)
    Popen(['notepad', error_file])


# somehow using QListView will crash
# when exit, that why this is needed
sip.setdestroyonexit(False)

app = QApplication([])
app.setOrganizationDomain('originlab.com')
app.setOrganizationName('originlab')
app.setApplicationName('PDBDownloader')
app.setApplicationVersion('1.0.0')
dlg = PDBDownloader()
onetime = sys.argv[1] if len(sys.argv) > 1 else 0
dlg.selfclose = onetime != 0
dlg.show()
if onetime:
    dlg.onStart()
app.exec_()
