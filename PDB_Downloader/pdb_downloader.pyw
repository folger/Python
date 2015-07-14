import sys
import os
import json
from urllib.request import urlretrieve
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from random import randint


class PDBDownloader(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        with open('settings.json') as fr:
            settings = json.load(fr)
        self.buildPrefix = settings['CurrentBuildPrefix']

        self.setWindowTitle('PDB Downloader({})'.
                            format(settings['CurrentVersion']))
        self.setFixedSize(250, 450)

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
        self.buildnumber = QLineEdit('100')

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.buildnumber)
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
        self.filename = QLabel('ok9.pdb')
        self.start = QPushButton('Start')

        layout = QHBoxLayout()
        layout.addWidget(self.filename)
        layout.addStretch()
        layout.addWidget(self.start)
        return layout

    def createModulesGroup(self):
        modules = (
                "ok9",
                "ou9",
                "okUtil9",
                "omocavc9",
                "OCompiler9",
                "Outl9",
                "gsodbc9",
                "Lababf32",
                "libapr",
                "libsie",
                "MOCABaseTypes9",
                "nlsf9",
                "O3DGL9",
                "oc3dx9",
                "OCcontour9",
                "ocim9",
                "ocmath29",
                "ocMath9",
                "ocmathsp9",
                "OCMmLink9",
                "OCntrls9",
                "ocStatEx9",
                "octree_Utils9",
                "OCTree9",
                "ocUtils9",
                "ocuv9",
                "OCVImg",
                "OD9",
                "odbc9",
                "odcfl9",
                "oExtFile9",
                "offt9",
                "OFFTW9",
                "ofgp9",
                "OFIO9",
                "ogrid9",
                "ohtmlhelp9",
                "ohttp9",
                "OIFileDlg9",
                "oimg9",
                "OImgLT9",
                "OK3DGL9",
                "OKXF9",
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
                "Origin93.exe",
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

        self.modules = QStandardItemModel()
        for m in modules:
            item = QStandardItem(m)
            item.setCheckState(Qt.Unchecked)
            item.setCheckable(True)
            self.modules.appendRow(item)
        view = QListView()
        view.setModel(self.modules)

        self.resetChecks = QPushButton('Reset Checks')
        self.connect(self.resetChecks, SIGNAL("clicked()"), self.onResetChecks)

        layout = QVBoxLayout()
        layout.addWidget(view)
        layout.addWidget(self.resetChecks)
        group = QGroupBox('Modules')
        group.setLayout(layout)
        return group

    def onResetChecks(self):
        for i in range(self.modules.rowCount()):
            item = self.modules.item(i, 0)
            item.setCheckState(Qt.Unchecked)

    def reject(self):
        self.close()

    def closeEvent(self, event):
        pass


app = QApplication(sys.argv)
app.setOrganizationDomain('originlab.com')
app.setOrganizationName('originlab')
app.setApplicationName('BatchBuild')
app.setApplicationVersion('1.0.0')
dlg = PDBDownloader()
dlg.show()
app.exec_()
