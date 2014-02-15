from urllib.request import urlretrieve

# filefmt = r"G:\OnePiece\海贼王第%s集.%03d.mp4"
filefmt = "/Users/lunbest/OnePiece/生活大爆炸第%s集.%03d.mp4"

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
            filename = filefmt % (album, part)
            urlretrieve(line, filename)
            print("%s.%03d" %(album, part))

            part += 1



