import sys
import os
import fnmatch
import re
import subprocess
import json
import inspect
from contextlib import contextmanager

import BatchBuildUtils

current_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))

with open(os.path.join(current_dir, 'settings.json')) as f:
    settings = json.load(f)
    MSBUILD = settings['MsBuild']
    UNLOAD_PROJECTS = settings.get('UnloadProjects', [])


@contextmanager
def unload_proj_from_sln(sln, projs):
    try:
        path = os.path.dirname(sln)
        sln_new = os.path.join(path, 'new.sln')
        sln_old = os.path.join(path, 'old.sln')
        if sln.lower().endswith('.sln'):
            _projs = ['"{}"'.format(p) for p in projs]
            with open(sln_new, 'w', encoding='utf-8') as fw:
                remove_next = False
                with open(sln, encoding='utf-8') as f:
                    for line in f:
                        if remove_next:
                            remove_next = False
                            continue
                        line = line.rstrip('\n')
                        for i, proj in enumerate(_projs):
                            if line.find(proj) > 0:
                                remove_next = True
                                _projs.pop(i)
                                break
                        else:
                            print(line, file=fw)
            if len(_projs) != len(projs):
                os.rename(sln, sln_old)
                os.rename(sln_new, sln)
            else:
                os.remove(sln_new)
        yield
    finally:
        if os.path.isfile(sln_old):
            os.remove(sln)
            os.rename(sln_old, sln)


def get_projects():
    try:
        path = os.path.join(os.environ["develop"], 'Source')
        for dirpath, dirnames, files in os.walk(path):
            for f in (fnmatch.filter(files, '*.vcxproj') +
                      fnmatch.filter(files, '*.sln')):
                yield(f, os.path.join(dirpath, f))
    except KeyError:
        yield '', ''


def get_project_files(project):
    p = re.compile('<(\w+) Include="([^"]+\.(c|cpp|cxx|rc))"', re.I)
    with open(project, encoding='utf-8') as f:
        for line in f:
            m = p.search(line)
            if m:
                yield (m.group(1), m.group(2))


def build(error_exit, return_output, project, platform, configuration, extra_args=""):
    os.environ['VisualStudioVersion'] = '11.0'

    args = ['/m']
    args.append('%s' % project)
    args.append('/p:platform=%s' % platform)
    args.append('/p:configuration=%s' % configuration)
    if extra_args:
        args.extend(['%s' % arg for arg in extra_args.split(' ')])

    if return_output:
        s = ''
        hasException = False
        try:
            s = subprocess.check_output([MSBUILD] + args, shell=True,
                                        universal_newlines=True)
        except subprocess.CalledProcessError as e:
            s = e.output
            hasException = True

        errors = []
        lines = s.split('\n')

        def reverse_enumerate(iterable):
            return zip(reversed(range(len(iterable))), reversed(iterable))

        pCompileError = re.compile('^ +[^(]+\(\d+\): .*?error R?C\d+:')
        for index, line in reverse_enumerate(lines):
            line = line.rstrip()
            if line in ('Build FAILED.', '生成失败。'):
                break
            elif line in ('Build succeeded.', '已成功生成。'):
                return ''
        else:
            return ''
        # first check compile error
        for line in lines[index + 1:]:
            line = line.rstrip()
            if pCompileError.search(line):
                errors.append(line)
        # if no compile error, and there is CalledProcessError
        # exception, then must be linking error
        if len(errors) == 0 and hasException:
            pLinkingError = re.compile('^ +.+? : .*?error LNK\d+:')
            for line in lines[index + 1:]:
                line = line.rstrip()
                if pLinkingError.search(line):
                    errors.append(line)
        return '\n'.join(errors)
    else:
        try:
            os.system('title ' + ' ^| '.join([BatchBuildUtils.get_current_branch(os.path.dirname(project))] + args[1:]))
            with unload_proj_from_sln(project, UNLOAD_PROJECTS):
                ret = subprocess.call([MSBUILD] + args, shell=True)
                if ret != 0 and error_exit:
                    sys.exit(1)
        except subprocess.CalledProcessError:
            pass


def compile(error_exit, return_output, project, platform, configuration, f):
    return build(error_exit, return_output, project, platform, configuration,
                 '/t:{} /p:selectedfiles={}'.format(*f))


if __name__ == '__main__':
    print(get_projects())
