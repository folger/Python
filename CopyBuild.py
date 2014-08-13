import os
from shutil import copytree
from zipfile import ZipFile
from functools import partial

srcpath = r'\\fs1\NewBuilds\92\I'
#srcpath = os.path.expanduser(r'~\Desktop\I')
despath = r'\\fs1\Builds\92\I'

pr = partial(print, end='', flush=True)
newbuild = False

try:
    for f in os.listdir(srcpath):
        if f not in os.listdir(despath):
            newbuild = True
            pr(f)
            srcfile = os.path.join(srcpath, f)
            pr('\tCopying ...')
            copytree(srcfile, os.path.join(despath, f))
            pr('\tZipping ...')
            with ZipFile(os.path.join(r'\\fs1\Released\ZipBuilds\92', f + '.zip'),
                                 'w') as myzip:
                for rf in os.listdir(srcfile):
                    if rf.endswith('.db'):
                        continue
                    myzip.write(os.path.join(srcfile, rf), rf)
            print()
except Exception as e:
    print(e)

if not newbuild:
    print('No new build')
os.system('pause')
