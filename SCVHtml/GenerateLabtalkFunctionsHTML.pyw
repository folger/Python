#! /usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys
import os
import re

from shutil import rmtree
from html.parser import HTMLParser
import urllib.request
import subprocess

import LTFuncsHTMLParser
import GenerateLTFuncHTML

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
        with urllib.request.urlopen("http://wikis/ltwiki/index.php?title=Script%3ALabTalk-Supported_Functions") as r:
            parser = LTFuncsHTMLParser.MyHTMLParser()
            parser.feed(r.read().decode())

            # print('\n'.join(parser.results))
            generate = GenerateLTFuncHTML.GenerateHTML(self.langCombo.currentText(), parser.results)

            with open("Default.html", encoding='utf-8-sig') as fr:
                s = fr.read()
                s = s.replace('<div style="display: none" id="labtalkFunctions"></div>', '<div style="display: none" id="labtalkFunctions">' + generate.Exec() + '</div>'). \
                    replace('/images/docwiki/math', './images')
                with open(self.htmlfile(), 'w', encoding='utf-8-sig') as fw:
                    fw.write(s)

        QMessageBox.information(self, "Attention", "%s generated" % self.htmlfile(), QMessageBox.Ok)

    def downloadImages(self):
        htmlfile = self.htmlfile()

        if not os.path.isfile(htmlfile):
            QMessageBox.critical(self, "Error", "%s is needed to download images" % htmlfile, QMessageBox.Ok)
            return

        imagefolder = 'images'
        try:
            rmtree(imagefolder)
        except FileNotFoundError:
            pass

        os.mkdir(imagefolder)

        with open(htmlfile, encoding='utf-8-sig') as fr:
            s = fr.read()
            images = re.findall('<img src="[^"]+', s)

            subprocess.Popen(r'explorer .\%s' % imagefolder)

            for image in images:
                image = image.replace('<img src="./%s/' % imagefolder, 'http://wikis/images/docwiki/math/')
                slash = image.rfind('/')
                imagename = image[slash+1:]

                try:
                    urllib.request.urlretrieve(image, os.path.join(imagefolder, imagename))
                except Exception as e:
                    QMessageBox.critical(self, "Error", "Failed to download %s : %s" % (imagename, e), QMessageBox.Ok)
                    break
            else:
                QMessageBox.information(self, "Attention", "All images downloaded", QMessageBox.Ok)

    def htmlfile(self): return 'Default%s.html' % self.langCombo.currentText()

app = QApplication(sys.argv)
bp = GenerateHTMLDlg()
bp.show()
app.exec_()

