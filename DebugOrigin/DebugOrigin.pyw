import sys
import os
import subprocess
from PyQt4.QtGui import *
from PyQt4.QtCore import *

VS6Path = (r'C:\Program Files (x86)\Microsoft Visual Studio'
           '\COMMON\MSDev98\Bin\MSDEV.EXE')
VS2010Path = (r'C:\Program Files (x86)\Microsoft Visual Studio 10.0'
              '\Common7\IDE\devenv.exe')
VS2012Path = r'D:\VS2012\Common7\IDE\devenv.exe'
MAIN_WINDOW_GEOMETRY = 'mainWindowGeometry'


class DebugOrigin(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Debug Origin')

        icon = QIcon()
        icon.addPixmap(QPixmap('main.ico'))
        self.setWindowIcon(icon)

        self.setFixedSize(200, 320)
        self.setLayout(self.createButtons())

        self.loadSetting(MAIN_WINDOW_GEOMETRY,
                         lambda val: self.restoreGeometry(val))

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
        self.run(VS2012Path,
                 os.path.join(source_path, r'vc32\orgmain\OriginAll.sln'))

    def run(self, exe, sln):
        subprocess.Popen([exe, sln],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    def removeLinkFolder(self, folder):
        try:
            os.rmdir(folder)
        except FileNotFoundError:
            pass

    def reject(self):
        self.close()

    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue(MAIN_WINDOW_GEOMETRY, self.saveGeometry())

    def loadSetting(self, key, func):
        settings = QSettings()
        value = settings.value(key)
        if value is not None:
            func(value)

app = QApplication(sys.argv)
app.setOrganizationDomain('originlab.com')
app.setOrganizationName('originlab')
app.setApplicationName('DebugOrigin')
app.setApplicationVersion('1.0.0')
dlg = DebugOrigin()
dlg.show()
app.exec_()
