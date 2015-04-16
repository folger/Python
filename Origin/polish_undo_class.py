import os
import re

setFuncUndo = re.compile(b'(\w+)::\s*Set(\w+)\s*\(')
with open(os.path.expanduser('~/Desktop/test1.txt'), 'w') as fw:
    for root, dirs, files in os.walk(os.path.join(os.environ['Develop'], r'Source\vc32')):
        for f in files:
            if f.lower().endswith('.cpp'):
                f1 = os.path.join(root, f)
                data = b''
                with open(f1, 'rb') as fr:
                    while True:
                        line = fr.readline()
                        if len(line) == 0:
                            break
                        data += line
                        m = setFuncUndo.search(line)
                        if m:
                            if line[0:2] == b'//':
                                continue
                            line = fr.readline()
                            data += line
                            if line[0:2] == b'//':
                                line = fr.readline()
                                data += line
                            if line[0:1] == b'{':
                                print(m.group(2).decode('cp1252'))
                                while True:
                                    line = fr.readline()
                                    m1 = re.search(b'^(\s+)OK_UNDO_(\w+)', line)
                                    mg2 = m1.group(2) if m1 else None
                                    if (m1 and mg2 != b'INDEX'
                                            and mg2 != b'CLASS'
                                            and mg2 != b'MASK'
                                            and mg2.find(b'THIS_SAVE') < 0
                                            and mg2.find(b'BLOCK') < 0):
                                        if mg2.find(b'_CLASS') >= 0:
                                            data += '{}OK_UNDO_CLASS({}, {});\r\n'.format(m1.group(1).decode('cp1252'), m.group(2).decode('cp1252'), m.group(1).decode('cp1252')).encode('cp1252')
                                        else:
                                            data += '{}OK_UNDO({});\r\n'.format(m1.group(1).decode('cp1252'), m.group(2).decode('cp1252')).encode('cp1252')
                                    else:
                                        data += line
                                    if line[0] == ord('}'):
                                        break;
                with open(f1, 'wb') as fw:
                    fw.write(data)
