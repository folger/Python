import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

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
        projOrigin = QRadioButton('Origin')
        projViewer = QRadioButton('Viewer')
        projOrglab = QRadioButton('OrgLab')
        projOrigin.setChecked(True)

        layout = QHBoxLayout()
        layout.addWidget(projOrigin)
        layout.addWidget(projViewer)
        layout.addWidget(projOrglab)
        group = QGroupBox('Soluntion')
        group.setLayout(layout)
        return group

    def createConfigurationGroup(self):
        check32Release = QCheckBox('32bit Release')
        check32Debug = QCheckBox('32bit Debug')
        check64Release = QCheckBox('64bit Release')
        check64Debug = QCheckBox('64bit Debug')
        check32Release.setChecked(True)

        layout = QGridLayout()
        layout.addWidget(check32Release, 0, 0)
        layout.addWidget(check64Release, 0, 1)
        layout.addWidget(check32Debug, 1, 0)
        layout.addWidget(check64Debug, 1, 1)
        group = QGroupBox('Configuration')
        group.setLayout(layout)
        return group

    def createActionGroup(self):
        btnBatchBuild = QPushButton('Batch Build')
        btnCopyToFS1 = QPushButton('Copy to fs1')
        btnDeleteBin = QPushButton('Delete Binaries')
        btnClean = QPushButton('Clean Files')
        btnVerifyBin = QPushButton('Verify Binary Files')
        checkCopyAfterBuild = QCheckBox('Copy files after Build')

        layout = QVBoxLayout()
        layout.addWidget(checkCopyAfterBuild)
        layout.addWidget(btnBatchBuild)
        layout.addWidget(btnCopyToFS1)
        layout.addWidget(btnDeleteBin)
        layout.addWidget(btnClean)
        layout.addWidget(btnVerifyBin)
        group = QGroupBox('Action')
        group.setLayout(layout)
        return group


app = QApplication(sys.argv)
dlg = BatchBuilder()
dlg.show()
app.exec_()
