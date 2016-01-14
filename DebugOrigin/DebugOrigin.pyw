import sys
import os
import json
import subprocess
from functools import partial
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from folstools.qt.utils import *

with open('settings.json') as f:
    settings = json.load(f)
    VS6PATH = settings['VS6Path']
    VS2010PATH = settings['VS2010Path']
    VS2012PATH = settings['VS2012Path']
    BUILDS = settings["Builds"]


class DebugOrigin(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Debug Origin')

        icon = QIcon()
        icon.addPixmap(QPixmap('main.ico'))
        self.setWindowIcon(icon)

        self.setFixedWidth(200)
        self.setLayout(self.createButtons())

        load_settings((MAIN_WINDOW_GEOMETRY,
                       lambda val: self.restoreGeometry(val)))

    def createButtons(self):
        layout = QVBoxLayout()
        for build in BUILDS:
            btn = QPushButton(build['Name'])
            btn.setFixedHeight(30)
            self.connect(btn, SIGNAL('clicked()'),
                         partial(getattr(self, build['IDE']),
                                 build['Location'], build['Project']))
            layout.addWidget(btn)
        return layout

    def VS6(self, source_path, dsw):
        self.removeLinkFolder(r'C:\C')
        self.removeLinkFolder(r'C:\FlexLM')
        self.removeLinkFolder(r'D:\buildtmp')
        os.symlink(os.path.join(source_path, 'C'), r'C:\C', True)
        os.symlink(os.path.join(source_path, 'FlexLM'), r'C:\FlexLM', True)
        os.symlink(os.path.join(source_path, 'buildtmp'), r'D:\buildtmp', True)
        self.run(VS6PATH, os.path.join(r'C:\C\Vc32\orgmain', dsw))

    def VS2010(self, source_path, sln):
        self.removeLinkFolder(r'C:\C')
        os.symlink(source_path, r'C:\C', True)
        self.run(VS2010PATH, os.path.join(r'C:\C\Vc32\orgmain', sln))

    def VS2012(self, source_path, sln):
        if not sln:
            sln = "OriginAll.sln"
        self.run(VS2012PATH, os.path.join(source_path, r'vc32\orgmain', sln))

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
