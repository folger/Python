import sys
import os
import subprocess
from PyQt4.QtGui import *
from PyQt4.QtCore import *

VS6Path = 'C:\Program Files (x86)\Microsoft Visual Studio\COMMON\MSDev98\Bin\MSDEV.EXE'
VS2010Path = 'C:\Program Files (x86)\Microsoft Visual Studio 10.0\Common7\IDE\devenv.exe'
VS2012Path = 'D:\VS2012\Common7\IDE\devenv.exe'

class DebugOrigin(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Debug Origin')

        icon = QIcon()
        icon.addPixmap(QPixmap('main.ico'))
        self.setWindowIcon(icon)

        self.setFixedSize(200, 300)
        self.setLayout(self.createButtons())

    def createButtons(self):
        debug75 = self.createButton('Debug 7.5')
        debug81 = self.createButton('Debug 8.1')
        debug851 = self.createButton('Debug 8.5.1')
        debug86 = self.createButton('Debug 8.6')
        debug90sr1 = self.createButton('Debug 9.0 SR1')
        debug90sr2 = self.createButton('Debug 9.0 SR2')
        debug91sr0 = self.createButton('Debug 9.1 SR0')
        debug91sr2 = self.createButton('Debug 9.1 SR2')

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

    def createButton(self, text):
        btn = QPushButton(text)
        btn.setFixedHeight(30)
        return btn

    def debug75(self):
        self.debugVS6(r'E:\C_75', 'Orgmain.dsw')

    def debug81(self):
        self.debugVS6(r'E:\C_81', 'Orgmain8.dsw')

    def debug851(self):
        self.debugVS6(r'E:\C_851', 'Orgmain8.dsw')

    def debug86(self):
        self.debugVS2010(r'E:\C_86sr0_32', 'originVS2010Frequent.sln')

    def debug90sr1(self):
        self.debugVS2010(r'E:\C_90SR1', 'originVS2010All.sln')

    def debug90sr2(self):
        self.debugVS2010(r'E:\C_90SR2', 'originVS2010All.sln')

    def debug91sr0(self):
        self.debugVS2012(r'E:\C_91SR0')

    def debug91sr2(self):
        self.debugVS2012(r'E:\C_91SR2')

    def debugVS6(self, source_path, dsw):
        self.removeLinkFolder(r'C:\C')
        self.removeLinkFolder(r'C:\FlexLM')
        self.removeLinkFolder(r'D:\buildtmp')
        os.symlink(os.path.join(source_path, 'C'), r'C:\C', True)
        os.symlink(os.path.join(source_path, 'FlexLM'), r'C:\FlexLM', True)
        os.symlink(os.path.join(source_path, 'buildtmp'), r'D:\buildtmp', True)
        self.run(VS6Path, os.path.join(r'C:\C\Vc32\orgmain', dsw))

    def debugVS2010(self, source_path, sln):
        self.removeLinkFolder(r'C:\C')
        os.symlink(source_path, r'C:\C', True)
        self.run(VS2010Path, os.path.join(r'C:\C\Vc32\orgmain', sln))

    def debugVS2012(self, source_path):
        self.run(VS2012Path, os.path.join(source_path, r'vc32\orgmain\OriginAll.sln'))

    def run(self, exe, sln):
        subprocess.call([exe, sln])

    def removeLinkFolder(self, folder):
        try:
            os.rmdir(folder)
        except FileNotFoundError:
            pass

app = QApplication(sys.argv)
dlg = DebugOrigin()
dlg.show()
app.exec_()
