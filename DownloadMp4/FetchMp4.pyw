import sys
import os
import re
from time import sleep
from urllib.request import urlretrieve
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from selenium import webdriver

path = 'F:/OnePiece'
driver = webdriver.Chrome('D:/BoxSync/Windows/chromedriver.exe')

class Fetcher(QThread):
    title = pyqtSignal(str)
    setrange = pyqtSignal(int, int)
    progress = pyqtSignal(int)
    enable = pyqtSignal(bool)

    def __init__(self, parent):
        super(Fetcher, self).__init__(parent)
        self.parent = parent

    def run(self):
        def make_getter(url):
            if url.find('.tudou.') > 0:
                return self.getTudou
            if url.find('v.qq.com') > 0:
                return self.getQQ

        fails = []
        urls = self.text.split('\n')
        self.enable.emit(False)
        for index, url in enumerate(urls):
            if len(url) == 0:
                break
            getter = make_getter(url)
            url = 'http://www.flvxz.com/?url=' + url
            driver.get(url)
            sleep(5)
            page_source = driver.page_source
            mtitle = re.search('<h4 class="media-heading">(\D+(\d+)\D+)</h4>', page_source)
            title = mtitle.group(1) if mtitle else 'Unknown'
            episode = mtitle.group(2) if mtitle else 10000
            files = getter(page_source)
            for subindex, f in enumerate(files):
                name = '{}.{:03d}.mp4'.format(episode, subindex+1)
                filename = os.path.join(path, name)
                if not os.path.exists(filename):
                    self.title.emit('({}/{}) {}.({}/{})'.format(index+1,
                                    len(urls),
                                    title,
                                    subindex+1,
                                    len(files)))
                    try:
                        urlretrieve(f, filename, reporthook=self.progressHook)
                    except Exception:
                        fails.append(name)
        if len(fails) > 0:
            QMessageBox.information(self.parent, "Files that fail", '\n'.join(fails))
        self.enable.emit(True)
        self.setrange.emit(0, 0)
        self.title.emit('All Done')

    def progressHook(self, count, blocksize, totalsize):
        self.setrange.emit(0, totalsize-1)
        self.progress.emit(count * blocksize)

    def getTudou(self, page_source):
        ss = re.findall('http://k.youku.com/player/getFlvPath/sid/\w+/st/mp4/fileid/[^"]+',
                        page_source)[-4:]
        return [s.replace('&amp;', '&') for s in ss]

    def getQQ(self, page_source):
        return re.findall('http://[\w.]+qq.com/flv/\d+/\d+/\w+\.p201\.\d+\.mp4\?vkey=\w+',
                          page_source)

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
        fetcher = Fetcher(self)
        fetcher.title.connect(self.updateTitle)
        fetcher.setrange.connect(self.setProgressRange)
        fetcher.progress.connect(self.updateProgress)
        fetcher.enable.connect(self.enableAll)
        fetcher.text = self.edit.toPlainText()
        fetcher.start()

    def updateTitle(self, text):
        self.title.setText(text)

    def updateProgress(self, val):
        self.progress.setValue(val)

    def setProgressRange(self, min, max):
        if min == 0 and max == 0:
            self.progress.reset()
        else:
            self.progress.setRange(min, max)

    def enableAll(self, enable):
        self.btnFetch.setEnabled(enable)
        self.edit.setEnabled(enable)

app = QApplication(sys.argv)
dlg = MP4Fetcher()
dlg.show()
app.exec_()
