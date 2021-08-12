import os
import glob
import shutil

def make_chinese():
    for xml in glob.glob('*_E.html'):
        shutil.copyfile(xml, xml.replace('_E', '_C'))

def make_SF():
    for xml in glob.glob('SCV_*.html'):
        with open(xml, 'rb') as f:
            data = f.read()
        data = data.replace(b'jquery-ui.js', b'jquery-ui2.js')
        with open(xml.replace('SCV', 'SF'), 'wb') as f:
            f.write(data)

make_chinese()
make_SF()
