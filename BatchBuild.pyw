import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from time import sleep
import threading

class BatchBuilder(QDialog):
    def __init__(self, parent=None):
        super(BatchBuilder, self).__init__(parent)
        self.setWindowTitle('Batch Build')

        self.progress = QProgressBar()

        layout = QVBoxLayout()
        layout.addWidget(self.createSolutionGroup())
        layout.addWidget(self.createConfigurationGroup())
        layout.addWidget(self.createActionGroup())
        layout.addWidget(self.progress)
        self.setLayout(layout)

    def createSolutionGroup(self):
        self.slnOrigin = QRadioButton('Origin')
        self.slnViewer = QRadioButton('Viewer')
        self.slnOrglab = QRadioButton('OrgLab')
        self.slnOrigin.setChecked(True)

        layout = QHBoxLayout()
        layout.addWidget(self.slnOrigin)
        layout.addWidget(self.slnViewer)
        layout.addWidget(self.slnOrglab)
        group = QGroupBox('Soluntion')
        group.setLayout(layout)
        return group

    def createConfigurationGroup(self):
        self.check32Release = QCheckBox('32bit Release')
        self.check32Debug = QCheckBox('32bit Debug')
        self.check64Release = QCheckBox('64bit Release')
        self.check64Debug = QCheckBox('64bit Debug')
        self.check32Release.setChecked(True)

        layout = QGridLayout()
        layout.addWidget(self.check32Release, 0, 0)
        layout.addWidget(self.check64Release, 0, 1)
        layout.addWidget(self.check32Debug, 1, 0)
        layout.addWidget(self.check64Debug, 1, 1)
        group = QGroupBox('Configuration')
        group.setLayout(layout)
        return group

    def createActionGroup(self):
        self.btnBatchBuild = QPushButton('Batch Build')
        self.btnCopyToFS1 = QPushButton('Copy to fs1')
        self.btnDeleteBin = QPushButton('Delete Binaries')
        self.btnClean = QPushButton('Clean Files')
        self.btnVerifyBin = QPushButton('Verify Binary Files')
        self.checkCopyAfterBuild = QCheckBox('Copy files after Build')

        self.connect(self.btnBatchBuild, SIGNAL("clicked()"), self.batchBuild)
        self.connect(self.btnCopyToFS1, SIGNAL("clicked()"), self.copyToFS1)
        self.connect(self.btnDeleteBin, SIGNAL("clicked()"), self.deleteBin)
        self.connect(self.btnClean, SIGNAL("clicked()"), self.clean)
        self.connect(self.btnVerifyBin, SIGNAL("clicked()"), self.verifyBin)

        layout = QVBoxLayout()
        layout.addWidget(self.checkCopyAfterBuild)
        layout.addWidget(self.btnBatchBuild)
        layout.addWidget(self.btnCopyToFS1)
        layout.addWidget(self.btnDeleteBin)
        layout.addWidget(self.btnClean)
        layout.addWidget(self.btnVerifyBin)
        group = QGroupBox('Action')
        group.setLayout(layout)
        return group

    def batchBuild(self):
        print('BatchBuild')

    def copyToFS1(self):
        self.progress.setRange(0, 99)
        class MyThread(QThread):
            updated = pyqtSignal(int)
            enabled = pyqtSignal(bool)

            def run(self):
                self.enabled.emit(False)
                for i in range(self.min, self.max+1):
                    self.updated.emit(i)
                    sleep(0.05)
                self.enabled.emit(True)

        mythread = MyThread(self)
        mythread.updated.connect(self.updateProgress)
        mythread.enabled.connect(self.enableAll)
        mythread.min = self.progress.minimum()
        mythread.max = self.progress.maximum()
        mythread.start()

    def deleteBin(self):
        print('deleteBin')

    def clean(self):
        print('clean')

    def verifyBin(self):
        print('verifyBin')

    def updateProgress(self, val):
        self.progress.setValue(val)

    def enableAll(self, enable):
        self.slnOrigin.setEnabled(enable)
        self.slnViewer.setEnabled(enable)
        self.slnOrglab.setEnabled(enable)

        self.check32Release.setEnabled(enable)
        self.check32Debug.setEnabled(enable)
        self.check64Release.setEnabled(enable)
        self.check64Debug.setEnabled(enable)

        self.btnBatchBuild.setEnabled(enable)
        self.btnCopyToFS1.setEnabled(enable)
        self.btnDeleteBin.setEnabled(enable)
        self.btnClean.setEnabled(enable)
        self.btnVerifyBin.setEnabled(enable)
        self.checkCopyAfterBuild.setEnabled(enable)

app = QApplication(sys.argv)
dlg = BatchBuilder()
dlg.show()
app.exec_()
