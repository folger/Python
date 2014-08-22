import sys
import os
import subprocess
import shutil
import winreg
from PyQt4.QtGui import *
from PyQt4.QtCore import *

VS6Path = 'C:\Program Files (x86)\Microsoft Visual Studio\COMMON\MSDev98\Bin\MSDEV.EXE'
VS2010Path = 'C:\Program Files (x86)\Microsoft Visual Studio 10.0\Common7\IDE\devenv.exe'
VS2012Path = 'D:\VS2012\Common7\IDE\devenv.exe'

class DebugOrigin(QDialog):
    def __init__(self, parent=None):
        super(DebugOrigin, self).__init__(parent)
        self.setWindowTitle('Debug Origin')

        self.resize(200, 200)
        self.setLayout(self.createButtons())

    def createButtons(self):
        debug75 = QPushButton('Debug 7.5')
        debug81 = QPushButton('Debug 8.1')
        debug851 = QPushButton('Debug 8.5.1')
        debug86 = QPushButton('Debug 8.6')
        debug90sr1 = QPushButton('Debug 9.0 SR1')
        debug90sr2 = QPushButton('Debug 9.0 SR2')
        debug91sr0 = QPushButton('Debug 9.1 SR0')
        debug91sr2 = QPushButton('Debug 9.1 SR2')

        self.connect(debug75, SIGNAL('clicked()'), self.debug75)
        self.connect(debug81, SIGNAL('clicked()'), self.debug81)
        self.connect(debug851, SIGNAL('clicked()'), self.debug851)
        self.connect(debug86, SIGNAL('clicked()'), self.debug86)
        self.connect(debug90sr1, SIGNAL('clicked()'), self.debug90sr1)
        self.connect(debug90sr2, SIGNAL('clicked()'), self.debug90sr2)
        self.connect(debug91sr0, SIGNAL('clicked()'), self.debug91sr0)
        self.connect(debug91sr2, SIGNAL('clicked()'), self.debug91sr2)

        layout = QVBoxLayout()
        layout.addWidget(debug75)
        layout.addWidget(debug81)
        layout.addWidget(debug851)
        layout.addWidget(debug86)
        layout.addWidget(debug90sr1)
        layout.addWidget(debug90sr2)
        layout.addWidget(debug91sr0)
        layout.addWidget(debug91sr2)
        return layout

    def debug75(self):
        self.run([''])

    def debug81(self):
        print('debug81')

    def debug851(self):
        print('debug851')

    def debug86(self):
        print('debug86')

    def debug86(self):
        print('debug86')

    def debug90sr1(self):
        print('debug90sr1')

    def debug90sr2(self):
        print('debug90sr2')

    def debug91sr0(self):
        print('debug91sr0')

    def debug91sr2(self):
        print('debug91sr2')

    def debugVS6(self, source_path, dsw):
        os.rmdir(r'C:\C')
        os.rmdir(r'C:\FlexLM')
        os.rmdir(r'D:\buildtmp')

        os.symlink(r'C:\C', os.path.join(source_path, 'C'), True)
        os.symlink(r'C:\FlexLM', os.path.join(source_path, 'FlexLM'), True)
        os.symlink(r'D:\buildtmp', os.path.join(source_path, 'buildtmp'), True)

        self.run(VS6Path, os.path.join(r'C:\C\Vc32\orgmain', dsw))

    def run(self, exe, dsw):
        subprocess.call(['start', exe, dsw])

app = QApplication(sys.argv)
dlg = DebugOrigin()
dlg.show()
app.exec_()
