#! /usr/bin/python

import sys
import os
import re
import subprocess
from time import sleep
from urllib.request import urlretrieve
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from selenium import webdriver

fetchPath = os.environ['MP4_FETCH_PATH']
mp4Path = os.environ['MP4_PATH']
driver = webdriver.Chrome('./chromedriver')

class Fetcher(QThread):
    title = pyqtSignal(str)
    setrange = pyqtSignal(int, int)
    progress = pyqtSignal(int)
    enable = pyqtSignal(bool)
    error = pyqtSignal(str)

    def __init__(self, parent):
        super(Fetcher, self).__init__(parent)
        self.stop = False
        parent.stop.connect(self.setStop)

    def run(self):
        fails = []
        urls = self.text.split('\n')

        self.enable.emit(False)
        for index, url in enumerate(urls):
            url = url.lstrip()
            if len(url) == 0:
                continue

            self.title.emit('Fetching download addresses')
            getter = self.makeGetter(url)
            driver.get('http://www.flvxz.com/?url=' + url)
            for i in range(50):
                sleep(0.1)
                if self.stop:
                    break
            if self.stop:
                break
            page_source = driver.page_source

            files = getter(page_source)
            if len(files) == 0:
                fails.append('Failed to fectch ' + url)
                continue

            titles = []
            https = []
            for i, f in enumerate(files):
                print(f.split('">'))
                http, title = f.split('">')
                titles.append(title)
                https.append(http)
            print(titles[0])
            mtitle = re.search(r'\D+(\d+)', titles[0])
            if not mtitle:
                continue
            episode = mtitle.group(1)

            names = []
            for subindex, http in enumerate(https):
                name = '{}.{:03d}.mp4'.format(episode, subindex+1)
                filename = os.path.join(fetchPath, name)
                if not os.path.exists(filename):
                    self.title.emit('({}/{}) {} ({}/{})'.format(index+1,
                                    len(urls),
                                    title,
                                    subindex+1,
                                    len(https)))
                    try:
                        urlretrieve(http, filename, reporthook=self.progressHook)
                        names.append(filename)
                    except Exception as e:
                        fails.append(name + ' ' + str(e))
                        names.clear()
                else:
                    names.append(filename)
                if self.stop:
                    break

            self.setrange.emit(0, 0)
            if self.stop:
                break

            if len(names) > 0:
                self.title.emit('Joining ...')
                cmd = ['MP4Box']
                for name in names:
                    cmd += ['-force-cat', '-cat', name]
                cmd.append('-new')
                cmd.append(os.path.join(mp4Path, '{}.mp4'.format(episode)))
                subprocess.call(cmd)

        if len(fails) > 0:
            self.error.emit('\n'.join(fails))
        self.enable.emit(True)
        self.title.emit('Stopped' if self.stop else 'All Done')

    def makeGetter(self, url):
        if url.find('www.tudou.com') > 0:
            return self.getTudou
        if url.find('v.qq.com') > 0:
            return self.getQQ
        if url.find('tv.cntv.cn') > 0:
            return self.getCNTV

    def progressHook(self, count, blocksize, totalsize):
        self.setrange.emit(0, totalsize-1)
        self.progress.emit(count * blocksize)

    def setStop(self):
        self.stop = True

    def getTudou(self, page_source):
        ss = re.findall(r'http://k.youku.com/player/getFlvPath/sid/\w+/st/mp4/fileid/[^<]+',
                        page_source)[-4:]
        return [s.replace('&amp;', '&') for s in ss]

    def getQQ(self, page_source):
        return re.findall(r'http://[\w.]+qq\.com/flv/\d+/\d+/\w+\.p201\.\d+\.mp4\?vkey=[^<]+',
                          page_source)

    def getCNTV(self, page_source):
        return re.findall(r'http://vod\.cntv\.lxdns\.com/flash/mp4video\d+/TMS/\d+/\d+/\d+/\w+?h2642000000nero_aac16-\d+\.mp4[^<]+',
                          page_source)

class MP4Fetcher(QDialog):
    stop = pyqtSignal()

    def __init__(self, parent=None):
        super(MP4Fetcher, self).__init__(parent)
        self.setWindowTitle('MP4 Fetcher')

        self.resize(600, 300)

        layout = QVBoxLayout()
        layout.addLayout(self.createFetchGroup())
        layout.addLayout(self.createProgressBar())
        self.setLayout(layout)

        self.isFetch = True

    def createFetchGroup(self):
        label = QLabel('Paste url line by line into box, then press Fetch')
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
        if self.isFetch:
            fetcher = Fetcher(self)
            fetcher.title.connect(self.updateTitle)
            fetcher.setrange.connect(self.setProgressRange)
            fetcher.progress.connect(self.updateProgress)
            fetcher.enable.connect(self.enableAll)
            fetcher.error.connect(self.errorReport)
            fetcher.text = self.edit.toPlainText()
            fetcher.start()
        else:
            self.btnFetch.setEnabled(False)
            self.stop.emit()

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
        self.edit.setEnabled(enable)
        if enable:
            self.isFetch = True
            self.btnFetch.setEnabled(True)
            self.btnFetch.setText('Fetch')
        else:
            self.isFetch = False
            self.btnFetch.setText('Stop')

    def errorReport(self, error):
        QMessageBox.information(self, "Files that fail", error)

app = QApplication(sys.argv)
dlg = MP4Fetcher()
dlg.show()
app.exec_()
