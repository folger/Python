import os
import FolsTools

if __name__ == "__main__":
    key = '92'
    localpath = 'D:/Builds'

    dirkey = key
             
    gb = FolsTools.GetBuildFromFTP(dirkey, key, \
                     'Builds/{}/I/'.format(dirkey), \
                     localpath, \
                     'D:/FlashGet/flashget.exe', \
                     '207.180.39.173'
                     )
    build = gb.do()
    
    if build:
        cb = FolsTools.CopyBuild(dirkey, key, \
                       localpath, \
                       r'\\fs1\Builds\{}'.format(dirkey), \
                       r'\\fs1\Builds\Zip Builds\{}'.format(dirkey)
                       )
        cb.do(build)
    
    print('Finish' + FolsTools.exclamination)
    os.system('pause')
