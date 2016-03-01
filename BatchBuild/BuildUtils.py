import os
import fnmatch
import re
import subprocess
import json
import inspect


with open(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), 'settings.json')) as f:
    settings = json.load(f)
    MSBUILD = settings['MsBuild']


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


def build(return_output, project, platform, configuration, extra_args=""):
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
            s = subprocess.check_output([MSBUILD] + args, shell=True, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            s = e.output
            hasException = True

        errors = []
        lines = s.split('\n')

        def reverse_enumerate(iterable):
            return zip(reversed(range(len(iterable))), reversed(iterable))

        pCompileError = re.compile('^ +[^(]+\(\d+\): .*?error C\d+:')
        for index, line in reverse_enumerate(lines):
            line = line.rstrip()
            if line in ('Build FAILED.', '生成失败。'):
                break
            elif line in ('Build succeeded.', '已成功生成。'):
                return ''
        else:
            return ''
        # first check compile error
        for line in lines[index+1:]:
            line = line.rstrip()
            if pCompileError.search(line):
                errors.append(line)
        # if no compile error, and there is CalledProcessError
        # exception, then must be linking error
        if len(errors) == 0 and hasException:
            pLinkingError = re.compile('^ +.+? : .*?error LNK\d+:')
            for line in lines[index+1:]:
                line = line.rstrip()
                if pLinkingError.search(line):
                    errors.append(line)
        return '\n'.join(errors)
    else:
        try:
            subprocess.call([MSBUILD] + args, shell=True)
        except subprocess.CalledProcessError:
            pass


def compile(return_output, project, platform, configuration, file):
    return build(return_output, project, platform, configuration, '/t:clcompile /p:selectedfiles=%s' % file)


if __name__ == '__main__':
    print(get_projects())
