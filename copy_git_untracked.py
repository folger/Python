import os
import shutil
import subprocess

cwd = os.getcwd()
des = os.path.join(cwd, os.path.basename(cwd))

for line in subprocess.check_output(['git', 'clean', '-dnx']).decode().strip().split('\n'):
    line = line.replace('Would remove ', '').strip()
    copy = shutil.copytree if line[-1] == '/' else shutil.copyfile
    if line[-1] == '/':
        shutil.copytree(line, os.path.join(des, line))
    else:
        destf = os.path.join(des, line)
        os.makedirs(os.path.dirname(destf), exist_ok=True)
        shutil.copyfile(line, destf)
