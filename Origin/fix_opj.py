import struct


with open('a.opj', 'rb') as f:
    pos_to_delete = []
    data = f.read()
    pos = 0
    pattern = b'\x8c\x00\x00\x00\x0a\x00\x00\x01'
    while True:
        pos = data.find(pattern, pos)
        if pos < 0:
            break
        begin = pos + 0x1e
        imax, i1, i2 = struct.unpack('iii', data[begin:begin+0xc])
        # print(imax, i1, i2)
        if imax == 0:
            pos_to_delete.append([pos, data.find(pattern, pos+0xc)])
        pos = begin+0xc

    data_pre1 = data[:400000000]
    data_pre2 = data[400000000:600000000]
    data = data[600000000:]
    for i, p in enumerate(reversed(pos_to_delete)):
        print(i+1, p[0], p[1])
        data1 = data[0:p[0]-600000000]
        data2 = data[p[1]-600000000:]
        data = data1 + data2
    with open('a1.opj', 'wb') as fw:
        fw.write(data_pre1)
        fw.write(data_pre2)
        fw.write(data)
