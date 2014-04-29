import os
import fnmatch
import re

import inspect
currentpath = os.path.dirname(inspect.getfile(inspect.currentframe()))


def get_projects():
    try:
        path = os.path.join(os.environ["develop"], 'Source')
        for dirpath, dirnames, files in os.walk(path):
            for f in fnmatch.filter(files, '*.vcxproj') + fnmatch.filter(files, '*.sln'):
                yield(f, os.path.join(dirpath, f))
    except KeyError:
        yield '', ''


def get_project_files(project):
    p = re.compile('"([^"]+\.(c|cpp|cxx))"', re.I)
    with open(project, encoding='utf-8') as f:
        for line in f:
            m = p.search(line)
            if m:
                yield m.group(1)


def build(project, platform, configuration, extra_args=""):
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
