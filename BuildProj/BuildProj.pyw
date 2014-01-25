#! /usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
import re
import fnmatch
from functools import partial

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

        self.compileFilesLabel = QLabel("Files")
        self.compileFilesCombo = QComboBox()
        self.compileFilesLabel.setBuddy(self.compileFilesCombo)

        compileBtn = QPushButton("Compile")
        buildBtn = QPushButton("Build")
        cleanBtn = QPushButton("Clean")

        btnsLayout = QHBoxLayout()
        btnsLayout.addStretch()
        btnsLayout.addWidget(compileBtn)
        btnsLayout.addWidget(buildBtn)
        btnsLayout.addWidget(cleanBtn)

        layout = QGridLayout()
        layout.addWidget(projLabel, 0, 0)
        layout.addWidget(self.projectsCombo, 0, 1)
        layout.addWidget(self.compileFilesLabel, 1, 0)
        layout.addWidget(self.compileFilesCombo, 1, 1)
        layout.addWidget(platformLabel, 2, 0)
        layout.addWidget(self.platformCombo, 2, 1)
        layout.addWidget(configLabel, 3, 0)
        layout.addWidget(self.configCombo, 3, 1)
        layout.addLayout(btnsLayout, 4, 0, 1, -1)
        self.setLayout(layout)

        self.connect(self.projectsCombo, SIGNAL("currentIndexChanged(int)"), self.projectChanged)
        self.connect(compileBtn, SIGNAL("clicked()"), self.compile)
        self.connect(buildBtn, SIGNAL("clicked()"), self.build)
        self.connect(cleanBtn, SIGNAL("clicked()"), partial(self.build, "/t:clean"))

        self.projectChanged(-1)

    def get_projects(self):
        path = os.path.join(os.environ["develop"], 'Source')
        projects = {}
        for dirpath, dirnames, files in os.walk(path):
            all = fnmatch.filter(files, '*.vcxproj')
            all.extend(fnmatch.filter(files, '*.sln'))
            for f in all:
                projects[f] = os.path.join(dirpath, f)
        return projects

    def get_project_files(self):
        files = []
        p = re.compile('"([^"]+\.(c|cpp|cxx))"', re.I)
        with open(self.projects[self.projectsCombo.currentText()], encoding='utf-8') as f:
            for line in f:
                m = p.search(line)
                if m:
                    files.append(m.group(1))
        return files

    def projectChanged(self, index):
        if self.projectsCombo.currentText().lower().endswith('.vcxproj'):
            self.compileFilesLabel.show()
            self.compileFilesCombo.show()

            self.compileFilesCombo.clear()
            self.compileFilesCombo.addItems(self.get_project_files())
        else:
            self.compileFilesLabel.hide()
            self.compileFilesCombo.hide()

    def build(self, extra_args = ""):
        args = []
        args.append('"%s"' % self.projects[self.projectsCombo.currentText()])
        args.append('"/p:platform=%s"' % self.platformCombo.currentText())
        args.append('"/p:configuration=%s"' % self.configCombo.currentText())
        if extra_args:
            args.extend(['"%s"' % arg for arg in extra_args.split(' ')])

        cmd = "Build.bat %s" % ' '.join(args)
        # print(cmd)
        os.system(cmd)

    def compile(self):
        self.build('/t:clcompile /p:selectedfiles=%s' % self.compileFilesCombo.currentText())

app = QApplication(sys.argv)
bp = BuildProjDlg()
bp.show()
app.exec_()

