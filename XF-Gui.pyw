#! /usr/bin/python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from FolsTools import XFGUI

class XFGuiUpdater(QDialog):
  def __init__(self, parent=None):
    super(XFGuiUpdater, self).__init__(parent)

    self.title = "XF ~ Gui"
    self.setWindowTitle(self.title)

    self.xf2gui = QPushButton("XF to GUI")
    self.gui2xf = QPushButton("GUI to XF")
    self.cleanxml = QPushButton("   Clean all localized XMLs   ")

    layout = QVBoxLayout()
    layout.addWidget(self.xf2gui)
    layout.addWidget(self.gui2xf)
    layout.addWidget(self.cleanxml)
    self.setLayout(layout)

    self.connect(self.xf2gui, SIGNAL("released()"), self.do_xf2gui)
    self.connect(self.gui2xf, SIGNAL("released()"), self.do_gui2xf)
    self.connect(self.cleanxml, SIGNAL("released()"), self.do_cleanxml)

    self.xfgui = XFGUI()

  def do_xf2gui(self):
    xfs = self.xfgui.XF2GUI()
    QMessageBox.about(self, self.title, '\n'.join(xfs))

  def do_gui2xf(self):
    xfs = self.xfgui.GUI2XF()
    QMessageBox.about(self, self.title, '\n'.join(xfs))

  def do_cleanxml(self):
    self.xfgui.Clear()


app = QApplication(sys.argv)
dlg = XFGuiUpdater()
dlg.show()
app.exec_()
