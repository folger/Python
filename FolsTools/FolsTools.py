import re
import os
import subprocess


class XFGUI:
    def __init__(self, filepath=r"c:\xfgui", reportpath=r"d:\report.txt"):
        self.filepath = filepath
        self.reportpath = reportpath

    def GUI2XF(self):
        scripts = []
        for file in os.listdir(self.filepath):
            m = self.Match(r"(.)XFGUI_(.*)\.xml", file)
            if m:
                scripts.append("gui2xf %s l:=%s;" % (m.group(2), m.group(1)))
        self.Run(''.join(scripts))
        return scripts

    def XF2GUI(self):
        xfs = []
        with open(self.reportpath, "r") as fr:
            script = ""
            for line in fr:
                m1 = self.Match(r".*\\(.*)\.oxf", line)
                m2 = self.Match(r"(.*) changes:", line)
                m3 = self.Match(r"(.*)\.oxf", line)
                m = m1 if m1 else (m2 if m2 else m3)
                if m:
                    # print(m.group(1))
                    xfs.append(m.group(1))
                    for c in "JG":
                        script += ("xf2gui %s l:=%s;" % (m.group(1), c))
            self.Run(script)
        return xfs

    def Clear(self):
        for file in os.listdir(self.filepath):
            m = self.Match(r".XFGUI_.*\.xml", file)
            if m:
                os.remove(os.path.join(self.filepath, file))

    def Run(self, script):
        if len(script) != 0:
            os.system(r"G:\F_C_VC32\origin9 -h -rs %s;exit;" % script)
            # subprocess.check_call([r"G:\F_C_VC32\origin9.exe", "-h", "-rs", '"%s;exit;"' % script])

    def Match(self, pattern, string):
        return re.match(pattern, string, re.I)


import shutil
import zipfile

exclamination = '!!!!!!!!!!!'


class CopyBuild(object):
    def __init__(self, key1, key2, srcPath, desPath, desZipPath):
        self.key1 = key1
        self.key2 = key2
        self.srcPath = srcPath
        self.desPath = desPath
        self.desZipPath = desZipPath
        pass

    @staticmethod
    def pattern1(key1, key2):
        #return r"(IR%s-\d+\w?_%ssr\d.+?)$" % (key1, key2)
        # return r"(IR%sSr0-\d+\w?)$" % (key1)
        return r"(IR%ssr\d[-_]\d+[a-z]?(_H)?)$" % (key1)

    def pattern(self):
        return CopyBuild.pattern1(self.key1, self.key2)

    def do(self, build):
        # if len(build) == 0:
        #     for f in os.listdir(self.srcPath):
        #         file = os.path.join(self.srcPath, f)

        #         if os.path.isdir(file) and re.match(self.pattern(), f, re.I):
        #             build = f
        #             break
        file = os.path.join(self.srcPath, build)
        desfile = os.path.join(self.desPath, build)
        print("Copying {} to {} ...".format(build, self.desPath))
        try:
            shutil.copytree(file, desfile)
            print("Done{}\n".format(exclamination))

            with zipfile.ZipFile(os.path.join(self.desZipPath, build) + '.zip', 'w') as myzip:
                print("Zipping {} to {} ...".format(file, self.desZipPath))
                for ff in os.listdir(file):
                    myzip.write(os.path.join(file, ff), ff, zipfile.ZIP_DEFLATED)
                print("Done{}\n".format(exclamination))

            return True
        except FileNotFoundError:
            print("{} does not exist, fail to copy to {}".format(file, desfile))

        return False


from ftplib import FTP
from urllib.request import urlretrieve
import sys


class GetBuildFromFTP(object):
    def __init__(self, key1, key2, srcpath, despath, flashget, ftpsite=''):
        self.key1 = key1
        self.key2 = key2
        self.srcpath = srcpath
        self.despath = despath
        self.flashget = flashget
        if len(ftpsite) == 0:
            ftpsite = '207.180.39.173'  # nd2
            #self.fptsite = '98.118.55.12' # nd1
        self.ftpsite = ftpsite

    def pattern(self):
        return CopyBuild.pattern1(self.key1, self.key2)

    def username(self):
        return 'gzoffice'

    def password(self):
        return 'labtalk'

    def fetch(self):
        print("Connecting %s ..." % self.ftpsite)
        try:
            with FTP(self.ftpsite, self.username(), self.password()) as ftp:
                try:
                    ftp.set_pasv(False)
                    ftp.cwd(self.srcpath)
                except:
                    print("Build directory changed{}\n".format(exclamination))
                    return None

                build = []

                def get(s):
                    match = re.search(self.pattern(), s, re.I)
                    if match:
                        build.append(match.group(0))

                def build_comp(build):
                    #print(build, end='\t')
                    extra = 0
                    while build[-1].isalpha() or build[-1] == '_':
                        extra = ord(build[-1].lower()) - ord('a')
                        build = build[:-1]

                    n = build.find('-')
                    if n < 0:
                        n = build.find('_')
                    num = int(build[n-1]) * 10000 + int(build[n+1:]) * 100 + extra
                    #print(num)
                    return num

                ftp.dir(get)
                if build:
                    build.sort(reverse=True, key=build_comp)
                    return build[0]
        except Exception as e:
            print('Failed to connect {} : {}'.format(self.ftpsite, e))

    def do(self):
        f = self.fetch()
        if f:
            return self.get_build_direct(f) if self.flashget is None else self.get_build_flashget(f)

    def get_build_flashget(self, f):
        # cmd = r'"D:\FlashGet\flashget.exe" ftp://{}:{}@{}/"{}"{} {}'\
        #        .format(self.username(), self.password(), self.ftpsite, self.srcpath, file, os.path.join(self.despath, file))
        # print(cmd)
        # print()
        print('Downloading {}'.format(f))
        # os.system(cmd)
        subprocess.check_call([self.flashget,
                               'ftp://{}:{}@{}/{}{}'.format(self.username(), self.password(), self.ftpsite, self.srcpath, f),
                               os.path.join(self.despath, f)])
        print('Downloaded{}\n'.format(exclamination))
        return f

    def get_build_direct(self, f):
        files = []
        try:
            with FTP(self.ftpsite, self.username(), self.password()) as ftp:
                ftp.set_pasv(False)
                ftp.cwd(os.path.join(self.srcpath, f))

                def get(s):
                    files.append(s.split()[-1])
                ftp.dir(get)
        except Exception as e:
            print('Failed to connect {} : {}'.format(self.ftpsite, e))

        print('Downloading {}'.format(f))
        try:
            os.mkdir(os.path.join(self.despath, f))
        except Exception:
            pass

        for f1 in files:
            sys.stdout.write(f1 + ' ... ')
            sys.stdout.flush()

            self.lastpercent = ''
            urlretrieve('ftp://{}:{}@{}/{}{}/{}'.format(self.username(),
                                                        self.password(),
                                                        self.ftpsite,
                                                        self.srcpath,
                                                        f,
                                                        f1),
                        os.path.join(self.despath, os.path.join(f, f1)),
                        reporthook=self.progress
                        )
            print()

        print('Downloaded{}\n'.format(exclamination))
        return f

    def progress(self, count, blocksize, totalsize):
        sys.stdout.write('\b' * len(self.lastpercent))
        percent = count*blocksize*100.0/totalsize
        if percent > 100:
            percent = 100
        self.lastpercent = '{:.2f}%'.format(percent)
        sys.stdout.write(self.lastpercent)
        sys.stdout.flush()


import stat


class CopySourceFiles(object):
    def __init__(self, filetype):
        self.filetype = filetype

    def stat_time(self, file):
        return int(os.stat(file).st_mtime)

    def make_file_writable(self, myfile):
        os.chmod(myfile, stat.S_IWRITE)

    def copy_files(self, desPath, srcPath, recursive=False, files_except=()):
        p = re.compile('.*\.({})$'.format(self.filetype), re.I)
        for file in os.listdir(srcPath):
            filepath = os.path.join(srcPath, file)
            if os.path.isfile(filepath):
                if p.match(file) and file not in files_except:
                    desfile = os.path.join(desPath, file)
                    if not os.path.isfile(desfile):
                        shutil.copyfile(filepath, desfile)
                    elif self.stat_time(filepath) != self.stat_time(desfile):
                        self.make_file_writable(desfile)
                        shutil.copy2(filepath, desfile)
                    else:
                        continue
                    print(filepath)
            elif recursive:
                desFilePath = os.path.join(desPath, file)
                if not os.path.isdir(desFilePath):
                    os.mkdir(desFilePath)
                self.copy_files(desFilePath, filepath, recursive, files_except)
