import sys
import os
import json
import subprocess
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from folstools.qt.utils import *

with open('settings.json') as f:
    settings = json.load(f)
    VS6PATH = settings['VS6Path']
    VS2010PATH = settings['VS2010Path']
    VS2012PATH = settings['VS2012Path']


class DebugOrigin(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Debug Origin')

        icon = QIcon()
        icon.addPixmap(QPixmap('main.ico'))
        self.setWindowIcon(icon)

        self.setFixedSize(200, 320)
        self.setLayout(self.createButtons())

        load_settings((MAIN_WINDOW_GEOMETRY,
                       lambda val: self.restoreGeometry(val)))

    def createButtons(self):
        layout = QVBoxLayout()

        def create_button(label, func):
            btn = QPushButton(label)
            btn.setFixedHeight(30)
            self.connect(btn, SIGNAL('clicked()'), func)
            layout.addWidget(btn)

        create_button('Debug 7.5', self.debug75)
        create_button('Debug 8.1', self.debug81)
        create_button('Debug 8.5.1', self.debug851)
        create_button('Debug 8.6', self.debug86)
        create_button('Debug 9.0 SR1', self.debug90sr1)
        create_button('Debug 9.0 SR2', self.debug90sr2)
        create_button('Debug 9.1 SR0', self.debug91sr0)
        create_button('Debug 9.1 SR2', self.debug91sr2)
        create_button('Debug 9.2 SR0', self.debug92sr0)
        create_button('Debug 9.3 SR0', self.debug93sr0)
        return layout

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

    def debug92sr0(self):
        self.debugVS2012(r'E:\C_92SR0\Source')

    def debug93sr0(self):
        self.debugVS2012(r'D:\C_93SR0\Source')

    def debugVS6(self, source_path, dsw):
        self.removeLinkFolder(r'C:\C')
        self.removeLinkFolder(r'C:\FlexLM')
        self.removeLinkFolder(r'D:\buildtmp')
        os.symlink(os.path.join(source_path, 'C'), r'C:\C', True)
        os.symlink(os.path.join(source_path, 'FlexLM'), r'C:\FlexLM', True)
        os.symlink(os.path.join(source_path, 'buildtmp'), r'D:\buildtmp', True)
        self.run(VS6PATH, os.path.join(r'C:\C\Vc32\orgmain', dsw))

    def debugVS2010(self, source_path, sln):
        self.removeLinkFolder(r'C:\C')
        os.symlink(source_path, r'C:\C', True)
        self.run(VS2010PATH, os.path.join(r'C:\C\Vc32\orgmain', sln))

    def debugVS2012(self, source_path):
        self.run(VS2012PATH,
                 os.path.join(source_path, r'vc32\orgmain\OriginAll.sln'))

    def run(self, exe, sln):
        subprocess.Popen([exe, sln])

    def removeLinkFolder(self, folder):
        try:
            os.rmdir(folder)
        except FileNotFoundError:
            pass

    def reject(self):
        self.close()

    def closeEvent(self, event):
        save_settings((MAIN_WINDOW_GEOMETRY, self.saveGeometry()))

app = QApplication(sys.argv)
app.setOrganizationDomain('originlab.com')
app.setOrganizationName('originlab')
app.setApplicationName('DebugOrigin')
app.setApplicationVersion('1.0.0')
dlg = DebugOrigin()
dlg.show()
app.exec_()
