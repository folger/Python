from urllib.request import urlretrieve

with open('OnePiece_2.txt') as f:
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
            # print("%s %s_%d.mp4" % (line, album, part))
            urlretrieve(line, r"G:\OnePiece\%s_%d.mp4" % (album, part))
            part += 1



