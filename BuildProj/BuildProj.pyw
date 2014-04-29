#! /usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from functools import partial
import BuildUtils


class BuildProjDlg(QDialog):
    def __init__(self, parent=None):
        super(BuildProjDlg, self).__init__(parent)

        self.setWindowTitle("Build Origin Projects")

        self.projects = dict(BuildUtils.get_projects())
        projLabel = QLabel("Projects")

        self.projectsCombo = QComboBox()
        projLabel.setBuddy(self.projectsCombo)
        projs = sorted(self.projects.keys())

        self.originallindex = self.get_sln_index(projs, 'OriginAll.sln')
        self.orgviewerindex = self.get_sln_index(projs, 'OrgViewer.sln')

        self.projectsCombo.addItems(projs)
        self.projectsCombo.setCurrentIndex(self.originallindex)

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

        self.compileBtn = QPushButton("Compile")
        originallBtn = QPushButton("OriginAll")
        buildBtn = QPushButton("Build")
        cleanBtn = QPushButton("Clean")
        orgviewerBtn = QPushButton("OrgViewer")

        btnsLayout = QGridLayout()
        btnsLayout.addWidget(originallBtn, 0, 0)
        btnsLayout.addWidget(orgviewerBtn, 1, 0)
        btnsLayout.addWidget(self.compileBtn, 0, 1)
        btnsLayout.addWidget(buildBtn, 1, 1)
        btnsLayout.addWidget(cleanBtn, 2, 1)

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
        self.connect(originallBtn, SIGNAL("clicked()"), self.originall)
        self.connect(self.compileBtn, SIGNAL("clicked()"), self.compile)
        self.connect(buildBtn, SIGNAL("clicked()"), self.build)
        self.connect(cleanBtn, SIGNAL("clicked()"), partial(self.build, "/t:clean"))
        self.connect(orgviewerBtn, SIGNAL("clicked()"), self.orgviewer)

        self.projectChanged(-1)

    def projectChanged(self, index):
        if self.projectsCombo.currentText().lower().endswith('.vcxproj'):
            self.compileBtn.setEnabled(True)
            self.compileFilesLabel.show()
            self.compileFilesCombo.show()

            self.compileFilesCombo.clear()
            self.compileFilesCombo.addItems(list(BuildUtils.get_project_files(self.projects[self.projectsCombo.currentText()])))
        else:
            self.compileBtn.setEnabled(False)
            self.compileFilesLabel.hide()
            self.compileFilesCombo.hide()

    def originall(self):
        self.projectsCombo.setCurrentIndex(self.originallindex)

    def orgviewer(self):
        self.projectsCombo.setCurrentIndex(self.orgviewerindex)

    def build(self, extra_args = ''):
        BuildUtils.build(self.projects[self.projectsCombo.currentText()],
                         self.platformCombo.currentText(),
                         self.configCombo.currentText(),
                         extra_args
                         )

    def compile(self):
        BuildUtils.compile(self.projects[self.projectsCombo.currentText()],
                           self.platformCombo.currentText(),
                           self.configCombo.currentText(),
                           self.compileFilesCombo.currentText()
                           )

    def get_sln_index(self, projs, sln):
        try:
            return projs.index("OriginAll.sln")
        except ValueError:
            return -1

app = QApplication(sys.argv)
bp = BuildProjDlg()
bp.show()
app.exec_()

