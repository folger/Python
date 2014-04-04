import re
from GetAddress import OutputAddrs

preSrc = re.compile("(http://www.tudouxia.com/albumplay/\w+/(?:-|\w)+.html) (\d+)")
preDes = re.compile('http://f.youku.com/player/getFlvPath/sid/\w+/st/mp4/fileid/[^"]+')

def polishAddress(all):
    ss = '\n'.join(all[1:])
    return ss.replace('&amp;', '&')

OutputAddrs(preSrc, preDes, polishAddress)
