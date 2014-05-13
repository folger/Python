from urllib.request import urlretrieve
import os
import sys

out = sys.stdout
lastpercent = ''


def progress(count, blocksize, totalsize):
    global lastpercent
    global out
    percent = count*blocksize*100.0/totalsize
    if percent > 100:
        percent = 100
    out.write('\b' * len(lastpercent))
    lastpercent = '{:.2f}%'.format(percent)
    out.write(lastpercent)
    out.flush()

import inspect
currentpath = os.path.dirname(inspect.getfile(inspect.currentframe()))

path = 'G:/OnePiece'
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
            name = "%s.%03d.mp4" % (album, part)
            filename = os.path.join(path, name)
            try:
                out.write(name + ' ... ')
                out.flush()
                lastpercent = ''
                urlretrieve(line, filename, reporthook=progress)
            except Exception as e:
                print()
                print("Failed to download %s : %s" % (name, e))

            print()
            part += 1


os.system('pause')
