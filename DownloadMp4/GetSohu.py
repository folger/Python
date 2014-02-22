import re
from GetAddress import OutputAddrs

preSrc = re.compile("(http://tv.sohuxia.com/\d+/n\d+\.shtml)' >第(\d+)集")
preDes = re.compile('http://\d+\.\d+\.\d+\.\d+[^"]+')

def polishAddress(all):
    block = 5
    return '\n'.join(all[block:2*block]) + '\n'

OutputAddrs(preSrc, preDes, polishAddress)