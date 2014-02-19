from urllib.request import urlretrieve
import urllib.error
import os

import inspect
currentpath = os.path.dirname(inspect.getfile(inspect.currentframe()))

path = r'G:\OnePiece'

with open(os.path.join(currentpath, 'Now.txt')) as f:
    album = ''
    part = 0
    for line in f:
        line = line.strip()
        if not line:
            continue

        if line.isdigit():
            album = line
            part = 1
        else:
            name = "%s.%03d.mp4" %(album, part)
            filename = os.path.join(path, name)
            try:
                urlretrieve(line, filename)
                print(name)
            except urllib.error.HTTPError as e:
                print("Failed to download %s : %s" % (name, e))

            part += 1


os.system('pause')
