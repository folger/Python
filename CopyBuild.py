import os
import shutil
import zipfile

srcpath = r'\\fs1\NewBuilds\92\I'
despath = r'\\fs1\Builds\92\I'

for f in os.listdir(srcpath):
    if f not in os.listdir(despath):
        print(f + '...')
        srcfile = os.path.join(srcpath, f)
        shutil.copytree(srcfile, os.path.join(despath, f))
        with zipfile.ZipFile(os.path.join(r'\\fs1\Released\ZipBuilds\92', f + '.zip'), 'w') as myzip:
            for rf in os.listdir(srcfile):
                if rf.endswith('.db'):
                    continue
                myzip.write(os.path.join(srcfile, rf), rf)
