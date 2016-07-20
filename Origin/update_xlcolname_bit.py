import os
import struct


i = 0
# otw EXE folder
# path = os.path.join(os.environ['Develop'], 'Origin')

# otw Localization folder
# path = os.path.join(os.environ['Develop'], 'Origin/Localization/E')


def otw_in_exe(sub):
    path = os.path.join(os.environ['Develop'], 'Origin', sub)
    for f in os.listdir(path):
        if f.lower().endswith('.otw'):
            yield os.path.join(path, f)


def ogw_in_exe():
    for root, dirs, files in os.walk(os.path.join(os.environ['Develop'], 'Origin')):
        for f in files:
            if f.lower().endswith('.ogw'):
                yield os.path.join(root, f)


ORIGIN = os.path.join(os.environ['Develop'], 'Origin', 'Origin94d.exe')
LOAD_OTW = 'win -t d '
LOAD_OGW = 'doc -a '

# for f in otw_in_exe(''):
# for f in otw_in_exe('Localization\\J'):
for f in ogw_in_exe():
    # os.system('{} -rs {}"{}";doc -ss;exit'.format(ORIGIN, LOAD_OTW, f))
    os.system('{} -rs {}"{}";doc -ss;exit'.format(ORIGIN, LOAD_OGW, f))
    with open(os.path.expanduser('~/Desktop/offset.txt')) as fr:
        offset = int(fr.read().strip())
    with open(f, 'rb') as fr:
        data = fr.read()
    length = struct.unpack('i', data[offset:offset+4])[0]
    if length >= 0xc3:
        pos = offset + 0x8d
        with open(f, 'wb') as fw:
            fw.write(data[:pos] + bytes([data[pos]&~0x40]) + data[pos+1:])
        print(f)
    else:
        print('Fail ~~~~~~~~ ' + f)
