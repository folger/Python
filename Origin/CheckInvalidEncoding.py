from itertools import chain
import fnmatch
import os

import os
for root, dirs, files in os.walk('H:/Dev/Source'):
    for f in chain(fnmatch.filter(files, '*.h'), fnmatch.filter(files, '*.c'), fnmatch.filter(files, '*.cpp')):
        fullpath = os.path.join(root, f)
        try:
            fr = open(fullpath, encoding='utf8')
            fr.read()
        except UnicodeDecodeError:
            print(fullpath)
        finally:
            fr.close()
