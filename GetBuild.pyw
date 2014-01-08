#! /usr/bin/python

import os
import sys
from functools import partial
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import FolsTools
import threading

class GetOneBuild(QDialog):
  def __init__(self, parent, ftp, ver):
    super(GetOneBuild, self).__init__(parent, Qt.FramelessWindowHint)

    self.ftp = ftp
    self.ver = ver

    # self.setWindowTitle("%s build from %s" % (ver, ftp))

    self.browser = QTextBrowser()
    self.btnOK = QPushButton("OK")

    layBtn = QHBoxLayout()
    layBtn.addStretch()
    layBtn.addWidget(self.btnOK)
    layBtn.addStretch()

    layout = QVBoxLayout()
    layout.addWidget(self.browser)
    layout.addLayout(layBtn)
    self.setLayout(layout)

    self.connect(self.btnOK, SIGNAL("clicked()"), self.accept)

  def output(self, s):
    self.browser.append(s)

  def do(self):
    try:
      print(self.ver)
      print(self.ftp)

      localpath = r'D:\Builds'
               
      gb = FolsTools.GetBuildFromFTP(self.ver, self.ver,
                       'Builds/{}/I/'.format(self.ver),
                       localpath,
                       'C:/Dropbox/Windows/FlashGet/flashget.exe',
                       self.ftp
                       )
      build = gb.do(self.output)

      if build:
        cb = FolsTools.CopyBuild(self.ver, self.ver,
                         localpath,
                         r'\\fs1\Builds\{}'.format(self.ver),
                         r'\\fs1\Builds\Zip Builds\{}'.format(self.ver)
                         )
        cb.do(build, self.output)
    except Exception as e:
      self.output("Failed to download: %s" % e)
    finally:
      self.btnOK.setEnabled(True)

  def showEvent(self, event):
    super(GetOneBuild, self).showEvent(event)

    self.btnOK.setEnabled(False)
    self.my_thread = threading.Thread(None, self.do)
    self.my_thread.setDaemon(True)
    self.my_thread.start()

class GetBuild(QDialog):
  def __init__(self, parent=None):
    super(GetBuild, self).__init__(parent)

    self.setWindowTitle("Get Latest Build")

    self.label = QLabel("You clicked button 'xxxxx'")

    btn91nd1 = QPushButton("   91 From nd1   ")
    btn91nd2 = QPushButton("   91 From nd2   ")
    btn92nd1 = QPushButton("   92 From nd1   ")
    btn92nd2 = QPushButton("   92 From nd2   ")

    layout = QGridLayout()
    layout.addWidget(btn91nd1, 0, 0)
    layout.addWidget(btn91nd2, 0, 1)
    layout.addWidget(btn92nd1, 1, 0)
    layout.addWidget(btn92nd2, 1, 1)    
    self.setLayout(layout)

    nd1 = '98.118.55.12'
    nd2 = '207.180.39.173'
    self.connect(btn91nd1, SIGNAL("clicked()"), partial(self.do, nd1, '91'))
    self.connect(btn91nd2, SIGNAL("clicked()"), partial(self.do, nd2, '91'))
    self.connect(btn92nd1, SIGNAL("clicked()"), partial(self.do, nd1, '92'))
    self.connect(btn92nd2, SIGNAL("clicked()"), partial(self.do, nd2, '92'))

  def do(self, ftp, ver):
    onebuild = GetOneBuild(self, ftp, ver)
    onebuild.exec_()

app = QApplication(sys.argv)
getbuild = GetBuild()
getbuild.show()
app.exec_()

