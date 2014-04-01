#! /usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys

import GeneratePolishedHTML
import DownloadImage


class GenerateHTMLDlg(QDialog):
    def __init__(self, parent=None):
        super(GenerateHTMLDlg, self).__init__(parent)

        self.setWindowTitle("Generate Labtalk Functions HTML")

        langLabel = QLabel("Language")
        self.langCombo = QComboBox()
        langLabel.setBuddy(self.langCombo)
        self.langCombo.addItems(["E", "G", "J"])

        generateBtn = QPushButton("Generate HTML")
        downloadImageBtn = QPushButton("Download Images")

        layout1 = QHBoxLayout()
        layout1.addWidget(langLabel)
        layout1.addWidget(self.langCombo)
        layout1.addWidget(generateBtn)
        layout1.addWidget(downloadImageBtn)

        # self.logOutput = QTextEdit(parent)
        # self.logOutput.setReadOnly(True)

        # layout = QGridLayout()
        # layout.addLayout(layout1, 0, 0)
        # layout.addWidget(self.logOutput, 1, 0)

        self.setLayout(layout1)

        self.connect(generateBtn, SIGNAL("clicked()"), self.generateHTML)
        self.connect(downloadImageBtn, SIGNAL("clicked()"), self.downloadImages)

    def generateHTML(self):
        result = GeneratePolishedHTML.generate_HTML(self.langCombo.currentText())
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

