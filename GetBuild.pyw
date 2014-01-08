#! /usr/bin/python

import os
import sys
from functools import partial
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import FolsTools

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
    print(ftp)
    print(ver)

app = QApplication(sys.argv)
getbuild = GetBuild()
getbuild.show()
app.exec_()

