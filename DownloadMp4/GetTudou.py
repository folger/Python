import re
from GetAddress import OutputAddrs

preSrc = re.compile("(http://www.tudouxia.com/albumplay/(?:-|\w)+/(?:-|\w)+.html) (\d+)")
preDes = re.compile('http://k.youku.com/player/getFlvPath/sid/\w+/st/mp4/fileid/[^"]+')


def polishAddress(all):
    ss = '\n'.join(all[-4:])
    return ss.replace('&amp;', '&')

OutputAddrs(preSrc, preDes, polishAddress)
