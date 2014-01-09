#! /usr/bin/python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
import fnmatch


class BuildProjDlg(QDialog):
  def __init__(self, parent=None):
    super(BuildProjDlg, self).__init__(parent)

    self.setWindowTitle("Build Origin Projects")

    self.projects = self.get_projects()
    
    projLabel = QLabel("Projects")
    self.projectsCombo = QComboBox()
    projLabel.setBuddy(self.projectsCombo)
    self.projectsCombo.addItems(sorted(self.projects.keys()))

    platformLabel = QLabel("Platform")
    self.platformCombo = QComboBox()
    platformLabel.setBuddy(self.platformCombo)
    self.platformCombo.addItems(["Win32", "x64"])

    configLabel = QLabel("Configuration")
    self.configCombo = QComboBox()
    configLabel.setBuddy(self.configCombo)
    self.configCombo.addItems(["Debug", "Release"])

    buildBtn = QPushButton("Build")
    cleanBtn = QPushButton("Clean")

    btnsLayout = QHBoxLayout()
    btnsLayout.addStretch()
    btnsLayout.addWidget(buildBtn)
    btnsLayout.addWidget(cleanBtn)

    layout = QGridLayout()
    layout.addWidget(projLabel, 0, 0)
    layout.addWidget(self.projectsCombo, 0, 1)
    layout.addWidget(platformLabel, 1, 0)
    layout.addWidget(self.platformCombo, 1, 1)
    layout.addWidget(configLabel, 2, 0)
    layout.addWidget(self.configCombo, 2, 1)
    layout.addLayout(btnsLayout, 3, 0, 1, -1)
    self.setLayout(layout)

    self.connect(buildBtn, SIGNAL("clicked()"), self.build)
    self.connect(cleanBtn, SIGNAL("clicked()"), self.clean)

  def get_projects(self):
    path = r'G:\Develop\Source'
    projects = {}
    for dirpath, dirnames, files in os.walk(path):
      all = fnmatch.filter(files, '*.vcxproj')
      all.extend(fnmatch.filter(files, '*.sln'))
      for f in all:
        projects[f] = os.path.join(dirpath, f)
    return projects

  def build(self):
    self.buildimpl("")

  def clean(self):
    self.buildimpl("/t:clean")

  def buildimpl(self, extra_args):
    args = []
    args.append('"%s"' % self.projects[self.projectsCombo.currentText()])
    args.append('"/p:platform=%s"' % self.platformCombo.currentText())
    args.append('"/p:configuration=%s"' % self.configCombo.currentText())
    if ( extra_args ):
      args.extend(['"%s"' % arg for arg in extra_args.split(' ')])

    cmd = "Build.bat %s" % ' '.join(args)
    # print(cmd)
    os.system(cmd)

app = QApplication(sys.argv)
bp = BuildProjDlg()
bp.show()
app.exec_()

