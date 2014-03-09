import re
from GetAddress import OutputAddrs

preSrc = re.compile("(http://www.letvxia.com/ptv/vplay/\d+.html) (\d+)")
preDes = re.compile('http://g3.letv.cn/\d+/\d+/\d+/letv-uts/\d+/[^.]+.mp4[^"]+')

def polishAddress(all):
    s = all[0]
    return s.replace('&amp;', '&')

OutputAddrs(preSrc, preDes, polishAddress)
