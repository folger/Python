from tkinter import Tk
r = Tk()
#r.clipboard_clear()
#r.clipboard_append('I am here')
result = r.clipboard_get()


def polishAddress(all):
    block = 9
    return '\n'.join(all[block:2*block])


import re
all = re.findall('http://(?:\d+\.\d+\.\d+\.\d+|sohu\.soooner\.com)[^"]+', result)

if len(all) > 0:
    name = input("File Name : ")
    with open('Now.txt', 'w') as f:
        f.write(name + '\n')
        f.write(polishAddress(all))
else:
    print('No addresses found!!!!!!!!!!!!!!')

r.destroy()
