import os
import re

setFuncUndo = re.compile(b'::\s*(Set\w+)\s*\(')
with open(os.path.expanduser('~/Desktop/test1.txt'), 'w') as fw:
    for root, dirs, files in os.walk(os.path.join(os.environ['Develop'], r'Source\vc32')):
        for f in files:
            #if f.lower().endswith('.cpp'):
            if f == 'OKPLTOBJ.CPP':
                f1 = os.path.join(root, f)
                with open(f1, 'rb') as fr:
                    while True:
                        line = fr.readline()
                        if len(line) == 0:
                            break
                        m = setFuncUndo.search(line)
                        if m:
                            line = fr.readline()
                            if line[0] == ord('{'):
                                line = fr.readline()
                                if line.find(b'OK_UNDO_BLOCK') >= 0:
                                    line = fr.readline()
                                if line.find(b'OK_UNDO_') >= 0:# and line.find(m.group(1)) < 0:
                                    print(f1, m.group(1).decode('cp1252'), sep='\t', file=fw)
