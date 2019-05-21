import sys
import os
import re
import json
import zipfile
import traceback
import tempfile
import urllib
from functools import partial
from subprocess import check_call, CalledProcessError, Popen
import socket
from urllib.request import urlretrieve
from urllib.error import URLError
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from folstools.qt.utils import *
import sip

from folstools.orglab.release import get_origin_binaries


BUILDPREFIX = 'BuildPrefix'
PDB = 'PDB'
MAP = 'MAP'
WIN32 = 'Win32'
X64 = 'x64'
ORIGIN = 'Origin'


class PDBDownloader(QDialog):
    stop = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selfclose = False

        with open('settings.json') as fr:
            settings = json.load(fr)
            self.downloadPath = settings['DownloadPath']
            if not self.downloadPath:
                self.downloadPath = os.path.join(os.environ['home'], 'Desktop')
            self.buildPath = settings['BuildPath']
            self.exepath = settings['ExePath']
            self.ftp = settings['FTP']
            self.username = settings['Username']
            self.password = settings['Password']

        self.build_prefix = QSettings().value(BUILDPREFIX)
        if not self.build_prefix:
            self.build_prefix = settings['DefaultBuildPrefix']

        self.setFixedWidth(250)

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

        load_settings(
            (MAIN_WINDOW_GEOMETRY, lambda val: self.restoreGeometry(val)),
            (BUILDPREFIX, self.buildPrefix.setText),
            (PDB, settings_set_checked(self.pdb)),
            (MAP, settings_set_checked(self.map)),
            (WIN32, settings_set_checked(self.win32)),
            (X64, settings_set_checked(self.x64)))

        self.updateWindowTitle()

    def createBuildNumberLayout(self):
        layout = QGridLayout()

        self.buildPrefix = QLineEdit(self.build_prefix)
        label = QLabel('Build P&refix')
        label.setBuddy(self.buildPrefix)
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.buildPrefix, 0, 1, 1, 2)

        self.buildNum = QLineEdit()
        self.checkLatest = QPushButton('&Latest')
        self.connect(self.checkLatest, SIGNAL("clicked()"), self.onCheckLatest)
        self.onCheckLatest()
        label = QLabel('B&uild Number')
        label.setBuddy(self.buildNum)
        layout.addWidget(label, 1, 0)
        layout.addWidget(self.buildNum, 1, 1)
        layout.addWidget(self.checkLatest, 1, 2)
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
        self.start.setFixedWidth(50)
        self.start.setDefault(True)
        self.connect(self.start, SIGNAL("clicked()"),
                     partial(self.onStart, False))
        self.showAddresses = QPushButton('S&how')
        self.showAddresses.setFixedWidth(50)
        self.connect(self.showAddresses, SIGNAL("clicked()"),
                     partial(self.onStart, True))

        layout = QHBoxLayout()
        layout.addWidget(self.filename)
        layout.addStretch()
        layout.addWidget(self.showAddresses)
        layout.addWidget(self.start)
        return layout

    @create_group('Modules')
    def createModulesGroup(self):
        suffix = '.dll'
        modules = []
        for c in get_origin_binaries(self.exepath, False, self.curExeVer()):
            if c.find('\\') > 0:
                continue
            if c.find(suffix) < 0:
                continue
            modules.append(c.replace(suffix, ''))

        self.view = QListView()
        moduleItems = QStandardItemModel(self.view)
        for i, m in enumerate(modules):
            item = QStandardItem(m)
            # item.setCheckState(Qt.Checked if i < 8 else Qt.Unchecked)
            item.setCheckable(True)
            moduleItems.appendRow(item)
        self.view.setModel(moduleItems)

        self.checkAll = QPushButton('&Check All')
        self.unCheckAll = QPushButton('Uncheck &All')
        self.connect(self.checkAll, SIGNAL("clicked()"),
                     partial(self.onChecks, True))
        self.connect(self.unCheckAll, SIGNAL("clicked()"),
                     partial(self.onChecks, False))

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.checkAll)
        layout.addWidget(self.unCheckAll)
        return layout

    def curVer(self):
        m = re.match(r'Ir(\d+b?)', self.buildPrefix.text())
        return m.group(1) if m else ''

    def curExeVer(self):
        return self.curVer().replace('b', '')

    def updateWindowTitle(self):
        self.setWindowTitle('PDB Downloader({})'.format(self.curVer()))

    def onCheckLatest(self):
        def latest_build_num():
            if not self.buildPath:
                return ''

            def one_build():
                for build in os.listdir(localBuildPath):
                    m = re.match(r'Ir\d+\w?Sr\d_(\d+)([a-z])?', build)
                    if m:
                        yield int(m.group(1)), m.group(2) if m.group(2) else ''

            try:
                localBuildPath = os.path.join(self.buildPath,
                                              self.curVer(), 'I')
                build_num, suffix = max(one_build())
                return ''.join([str(build_num), suffix])
            except Exception:
                report_error()
        self.buildNum.setText(latest_build_num())
        self.updateWindowTitle()

    def onChecks(self, checked):
        for module in self.modules():
            module.setCheckState(Qt.Checked if checked else Qt.Unchecked)

    def onStart(self, showaddresses):
        if not self.pdb.isEnabled():
            self.stop.emit()
            return

        if not self.buildNum.text().lstrip().rstrip():
            self.errorReport('Error', 'Please specify build number')
            return

        def files(module):
            def _format(fm):
                return fm.format(module)
            if self.pdb.isChecked():
                if self.win32.isChecked():
                    yield _format('{}_32.pdb.zip')
                if self.x64.isChecked():
                    yield _format('{}.pdb.zip')
            if self.map.isChecked():
                if self.win32.isChecked():
                    yield _format('{}_32.map.zip')
                if self.x64.isChecked():
                    yield _format('{}.map.zip')

        def all_files():
            buildFolder = self.buildPrefix.text() + self.buildNum.text()
            localPath = os.path.join(self.downloadPath, buildFolder)
            try:
                os.makedirs(localPath)
            except FileExistsError:
                pass
            for module in self.modules():
                if module.checkState() == Qt.Checked:
                    mtext = module.text()
                    if mtext == ORIGIN:
                        mtext = mtext + self.curExeVer()
                    for f in files(mtext):
                        filename = os.path.join(localPath, f)
                        ftp = ('ftp://{}:{}@{}/Builds/{}/'
                               'MAP_and_PDB/{}/{}'
                               ).format(self.username,
                                        self.password,
                                        self.ftp,
                                        self.curVer(),
                                        buildFolder,
                                        f)
                        yield ftp, filename

        if showaddresses:
            with open(os.path.join(tempfile.gettempdir(),
                      'pdb_ftps.txt'), 'w') as f:
                for ftp, __ in all_files():
                    print(ftp, file=f)
                Popen(['notepad', f.name])
            return

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
        self.buildPrefix.setEnabled(enable)
        self.buildNum.setEnabled(enable)
        self.checkLatest.setEnabled(enable)
        self.pdb.setEnabled(enable)
        self.map.setEnabled(enable)
        self.win32.setEnabled(enable)
        self.x64.setEnabled(enable)
        self.view.setEnabled(enable)
        self.checkAll.setEnabled(enable)
        self.unCheckAll.setEnabled(enable)
        self.showAddresses.setEnabled(enable)
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
        else:
            save_settings(
                (MAIN_WINDOW_GEOMETRY, self.saveGeometry()),
                (BUILDPREFIX, self.buildPrefix.text()),
                (PDB, self.pdb.isChecked()),
                (MAP, self.map.isChecked()),
                (WIN32, self.win32.isChecked()),
                (X64, self.x64.isChecked()))


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
        ftp_errors = []
        for ftp, filename in self.all_files():
            if not folder:
                folder = os.path.dirname(filename)
            if os.path.isfile(filename[:-4]):  # remove .zip
                continue
            self.setfilename.emit(os.path.basename(filename))
            self.setrange.emit(0, 0)
            try:
                socket.setdefaulttimeout(30)
                urlretrieve(ftp, filename, reporthook=self.progressHook)
            except StopFetch:
                os.remove(filename)
                break
            except urllib.error.URLError as e:
                ftp_errors.append(str(e))
                continue
            except Exception:
                report_error()
                break
            if os.path.isfile(filename):
                with zipfile.ZipFile(filename, 'r') as zf:
                    zf.extractall(os.path.dirname(filename))
                os.remove(filename)
        if ftp_errors:
            report_error('\n'.join(ftp_errors))
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
        self.setrange.emit(0, totalsize - 1)
        self.progress.emit(count * blocksize)

    def setStop(self):
        self.stop = True


def report_error(s=None):
    error_file = 'error.txt'
    with open(error_file, 'w', encoding='utf-8-sig') as fw:
        print(s if s is not None else traceback.format_exc(), file=fw)
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
