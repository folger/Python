from urllib.request import urlretrieve
import os
import sys


build = input('Build Number : ')


def progressHook(count, blocksize, totalsize):
    global lastlen
    percent = count * blocksize / totalsize * 100
    if percent > 100:
        percent = 100
    if lastlen > 0:
        sys.stdout.write('\b'*lastlen)
    s = '{:.2f}%'.format(percent)
    lastlen = len(s)
    sys.stdout.write(s)
    sys.stdout.flush()

while True:
    pdbs = input('PDB name : ')
    if len(pdbs) == 0:
        break
    for pdb in (pdbs, pdbs + '_64'):
        f = pdb + '.pdb.zip'
        destfile = os.path.expanduser('~/Desktop/' + f)
        if os.path.isfile(destfile):
            continue
        try:
            lastlen = 0
            print('Downloading ' + f + ' : ', end='')
            urlretrieve('ftp://gzoffice:labtalk@98.118.55.14/Builds/92/MAP_and_PDB/Ir92Sr1_' + build + '/' + f,
                    destfile, reporthook=progressHook)
            print()
        except Exception as e:
            print(e)
