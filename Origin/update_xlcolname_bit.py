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


# begins = [0x1b, 0x2e, 0x33, 0x18, 0x1b, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x57, 0x43, 0x1b, 0x1b, 0x57, 0x43, 0x1b, 0x17, 0x1b, 0x3c, 0x20, 0x20, 0x1b, 0x17, 0x1f, 0x20, 0x17]
# for f in otw_in_exe(''):
# begins = [0x1b, 0x1b, 0x1b, 0x1b]
# for f in otw_in_exe('Localization\\E'):
begins = [0x694d, 0xd53, 0x8dd8f, 0x88b8, 0xc16c, 0x694d, 0xd53, 0xec19, 0x4f25, 0x992b, 0x7983, 0x2c64, 0xf5c, 0xf24, 0x8875, 0x3ad4, 0x3c78, 0x864f, 0x820]
for f in ogw_in_exe():
    with open(f, 'rb') as fr:
        data = fr.read()
    length = struct.unpack('i', data[begins[i]:begins[i]+4])[0]
    if length >= 0xc3:
        pos = begins[i] + 0x8d
        with open(f, 'wb') as fw:
            fw.write(data[:pos] + bytes([data[pos]|0x40]) + data[pos+1:])
    else:
        print(f)
    i += 1
    # print(f)
