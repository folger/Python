import sys
import os
import re
from time import sleep
from urllib.request import urlretrieve
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from selenium import webdriver

class Fetcher(QThread):
    re_title = re.compile('<h4 class="media-heading">(\D+(\d+)\D+)</h4>')
    title = pyqtSignal(str)
    setrange = pyqtSignal(int, int)
    progress = pyqtSignal(int)
    enable = pyqtSignal(bool)
    def run(self):
        self.driver.get(self.url)
        sleep(3)
        self.page_source = self.driver.page_source

        m = self.re_title.search(self.page_source)

        path = 'F:/OnePiece'
        for i, f in enumerate(self.files()):
            name = '{}.{:03d}.mp4'.format(m.group(2), i+1)
            filename = os.path.join(path, name)
            if not os.path.exists(filename):
                self.title.emit(m.group(1) + '.{}'.format(i+1))
                try:
                    urlretrieve(f, filename, reporthook=self.progressHook)
                except Exception as e:
                    print("Failed to download %s : %s" % (name, e))

    def files(self): pass
    def progressHook(self, count, blocksize, totalsize):
        self.setrange.emit(0, totalsize)
        self.progress.emit(count * blocksize)

class FetchTudou(Fetcher):
    pre = re.compile('http://k.youku.com/player/getFlvPath/sid/\w+/st/mp4/fileid/[^"]+')
    def files(self):
        ss = self.pre.findall(self.page_source)[-4:]
        return [s.replace('&amp;', '&') for s in ss]

class MP4Fetcher(QDialog):
    def __init__(self, parent=None):
        super(MP4Fetcher, self).__init__(parent)
        self.setWindowTitle('MP4 Fetcher')

        self.resize(400, 200)

        layout = QVBoxLayout()
        layout.addLayout(self.createInputEdit())
        layout.addLayout(self.createProgressBar())
        #layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)

        self.driver = webdriver.Chrome('D:/BoxSync/Windows/chromedriver.exe')

    def createInputEdit(self):
        label = QLabel('URLs')
        self.edit = QTextEdit()
        self.btnFetch = QPushButton('Fetch')
        self.connect(self.btnFetch, SIGNAL('clicked()'), self.fetch)
        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.btnFetch, 0, 1, Qt.AlignRight)
        layout.addWidget(self.edit, 1, 0, 1, -1)
        return layout

    def createProgressBar(self):
        self.title = QLabel('')
        self.progress = QProgressBar()
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.progress)
        return layout

    def fetch(self):
        def make_url(url):
            if url.find('.tudou.') > 0:
                return FetchTudou(self), url.replace('.tudou.', '.tudouxia.')

        for url in self.edit.toPlainText().split('\n'):
            if len(url) == 0:
                break
            fetcher, url = make_url(url)
            fetcher.title.connect(self.updateTitle)
            fetcher.setrange.connect(self.setProgressRange)
            fetcher.progress.connect(self.updateProgress)
            fetcher.driver = self.driver
            fetcher.url = url
            fetcher.start()

    def updateTitle(self, text):
        self.title.setText(text)

    def updateProgress(self, val):
        self.progress.setValue(val)

    def setProgressRange(self, min, max):
        self.progress.setRange(min, max)


app = QApplication(sys.argv)
dlg = MP4Fetcher()
dlg.show()
app.exec_()
