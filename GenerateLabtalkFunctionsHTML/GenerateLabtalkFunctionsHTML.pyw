#! /usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys

import GeneratePolishedHTML
import DownloadImage
from GenerateLTFuncHTML import HTMLType


class GenerateHTMLDlg(QDialog):
    def __init__(self, parent=None):
        super(GenerateHTMLDlg, self).__init__(parent)

        self.setWindowTitle("Generate Labtalk Functions HTML")

        generateBtn = QPushButton("Generate HTML")
        downloadImageBtn = QPushButton("Download Images")

        layout = QVBoxLayout()
        layout.addLayout(self.createLanguageGroup())
        layout.addWidget(self.createHTMLGroup())
        layout.addWidget(generateBtn)
        layout.addWidget(downloadImageBtn)

        self.setLayout(layout)

        self.connect(generateBtn, SIGNAL("clicked()"), self.generateHTML)
        self.connect(downloadImageBtn, SIGNAL("clicked()"), self.downloadImages)

    def createLanguageGroup(self):
        langLabel = QLabel("Language")
        self.langCombo = QComboBox()
        self.langCombo.addItems(["E", "G", "J"])

        layout = QHBoxLayout()
        layout.addWidget(langLabel)
        layout.addWidget(self.langCombo)
        return layout

    def createHTMLGroup(self):
        self.radioGeneral = QRadioButton('General')
        self.radioFO = QRadioButton('FO')
        self.radioNLFIT = QRadioButton('NLFIT')
        self.radioGeneral.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(self.radioGeneral)
        layout.addWidget(self.radioFO)
        layout.addWidget(self.radioNLFIT)
        group = QGroupBox('HTML Type')
        group.setLayout(layout)
        return group

    def generateHTML(self):
        htmlType = HTMLType()
        if self.radioFO.isChecked():
            htmlType.val = HTMLType.FO
        elif self.radioNLFIT.isChecked():
            htmlType.val = HTMLType.NLFIT
        result = GeneratePolishedHTML.generate_HTML(self.langCombo.currentText(), htmlType)
        self.reportResult(result)

    def downloadImages(self):
        result = DownloadImage.download_images(self.langCombo.currentText())
        self.reportResult(result)

    def reportResult(self, result):
        if result[0]:
            QMessageBox.information(self, "Attention", result[1], QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Error", result[1], QMessageBox.Ok)

app = QApplication(sys.argv)
bp = GenerateHTMLDlg()
bp.show()
app.exec_()

