import os
import fnmatch
import re

import inspect
currentpath = os.path.dirname(inspect.getfile(inspect.currentframe()))

def get_projects():
    path = os.path.join(os.environ["develop"], 'Source')
    projects = {}
    for dirpath, dirnames, files in os.walk(path):
        all = fnmatch.filter(files, '*.vcxproj')
        all.extend(fnmatch.filter(files, '*.sln'))
        for f in all:
            projects[f] = os.path.join(dirpath, f)
    return projects


def get_project_files(project):
    files = []
    p = re.compile('"([^"]+\.(c|cpp|cxx))"', re.I)
    with open(project, encoding='utf-8') as f:
        for line in f:
            m = p.search(line)
            if m:
                files.append(m.group(1))
    return files


def build(project, platform, configuration, extra_args = ""):
    args = []
    args.append('"%s"' % project)
    args.append('"/p:platform=%s"' % platform)
    args.append('"/p:configuration=%s"' % configuration)
    if extra_args:
        args.extend(['"%s"' % arg for arg in extra_args.split(' ')])

    cmd = "%s %s" % (os.path.join(currentpath, 'Build.bat'), ' '.join(args))
    os.system(cmd)


def compile(project, platform, configuration, file):
    build(project, platform, configuration, '/t:clcompile /p:selectedfiles=%s' % file)


if __name__ == '__main__':
    print(get_projects())
