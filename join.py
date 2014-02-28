import os
from collections import defaultdict

mainfiles = defaultdict(list)
for file in os.listdir(r"."):
    if file.endswith('.mp4'):
        mainfiles[file[:-8]].append(file) # remove .000.mp4 as key

path = r"/Users/lunbest/Downloads/Naruto2"
if not os.path.exists(path):
    os.makedirs(path)

cmdpath = "MP4Box"
for key in mainfiles:
    cmd = '"%s" %s %s.mp4' % (cmdpath,
        ' '.join(['-cat %s' % file for file in sorted(mainfiles[key])]),
        os.path.join(path, key))
    # print(cmd)
    os.system(cmd)

