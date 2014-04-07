import re
from GetAddress import OutputAddrs

preSrc = re.compile("(http://tv.sohuxia.com/\d+/n\d+\.shtml) (\d+)")
preDes = re.compile('http://(?:\d+\.\d+\.\d+\.\d+|sohu\.soooner\.com)[^"]+')

def polishAddress(all):
    block = 5
    return '\n'.join(all[block:2*block])

OutputAddrs(preSrc, preDes, polishAddress)
