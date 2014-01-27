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
            filename = r"G:\OnePiece\海贼王第%s集.%03d.mp4" % (album, part)
            urlretrieve(line, filename)
            print("Got %s" % filename)

            part += 1



