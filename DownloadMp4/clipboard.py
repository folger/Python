import re

from tkinter import Tk
r = Tk()
#r.clipboard_clear()
#r.clipboard_append('I am here')
result = r.clipboard_get()
r.destroy()

preDes = re.compile('http://(?:\d+\.\d+\.\d+\.\d+|sohu\.soooner\.com)[^"]+')
all = preDes.findall(result)


def polishAddress(all):
    block = 9
    return '\n'.join(all[block:2*block])

with open('Now.txt', 'w') as f:
    f.write(polishAddress(all))
