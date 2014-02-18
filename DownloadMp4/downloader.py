from urllib.request import urlretrieve
import os

path = r'G:\OnePiece'

with open('Now.txt') as f:
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
            urlretrieve(line, filename)
            print(name)

            part += 1



