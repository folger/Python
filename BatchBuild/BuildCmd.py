import sys
import os
import subprocess
import traceback
from argparse import ArgumentParser
from datetime import datetime as DT

from folstools import dir_temp_change
import BuildUtils


parser = ArgumentParser()
parser.add_argument('project')
parser.add_argument('-f', '--file',
                    help='Source file in specified project')
parser.add_argument('-p', '--platform',
                    help='Build Platform, can be Win32 or x64, Default Win32')
parser.add_argument('-c', '--configuration',
                    help='Build Configuration, can be Debug or Release, '
                    'Debug by default')
parser.add_argument('-a', '--all-output',
                    help='Diaplay all output, not just errors',
                    action='store_true')
parser.add_argument('-e', '--error-exit',
                    help='Exit with error code',
                    action='store_true')
args = parser.parse_args()
if args.platform is None:
    args.platform = 'Win32'
if args.configuration is None:
    args.configuration = 'Debug'


class MyValueError(ValueError):
    pass

def guess_project_from_source_file(f):
    path = os.path.dirname(f)
    paths = path.split('/')
    last_folder = paths[-1].lower()
    proj_name = ''
    if last_folder == 'sdk':
        proj_name = r'vc32\okstatic\oks70'
    elif last_folder == 'modll':
        proj_name = r'MFC\OMocavc\omocavc'
    elif last_folder in ('labutil', 'labmath', 'labtext'):
        proj_name = r'vc32\outl'
    else:
        for ff in os.listdir(path):
            if ff.endswith('.vcxproj'):
                return os.path.join(path, ff)
    if proj_name:
        with dir_temp_change(path):
            dev = subprocess.check_output('git rev-parse --show-toplevel',
                                          universal_newlines=True).strip()
        return os.path.join(dev,
                            'Source',
                            proj_name) + '.vcxproj'
    raise MyValueError('Failed to guess project from source file {}'.format(f))


def find_project_file(proj):
    if os.path.isfile(proj):
        return proj
    for project, project_file in BuildUtils.get_projects():
        if os.path.splitext(project)[0].lower() == proj.lower():
            return project_file
    raise MyValueError('Failed to find project file from project name {}'
                     .format(proj))


def main():
    if args.project in ('xxx', 'zzz'):
        if not args.file:
            raise MyValueError('Source file is not specified, '
                             'cannot guess project')
        project_file = guess_project_from_source_file(args.file)
        if args.project == 'zzz':
            args.file = None
    else:
        project_file = find_project_file(args.project)
    print(os.path.dirname(project_file))
    if args.file:
        file_name = os.path.basename(args.file)
        for target, ff in BuildUtils.get_project_files(project_file):
            if os.path.basename(ff).lower() == file_name.lower():
                print(BuildUtils.compile(args.error_exit,
                                        not args.all_output,
                                         project_file,
                                         args.platform,
                                         args.configuration,
                                         (target, ff)))
                break
        else:
            raise MyValueError('{} cannot be found in project {}'
                             .format(file_name, args.project))
        return

    res = (BuildUtils.build(args.error_exit,
                            not args.all_output,
                            project_file,
                            args.platform,
                            args.configuration))
    if not args.all_output:
        print(res)
    else:
        print(DT.now().strftime("%Y-%m-%d %H:%M:%S"))

try:
    main()
    if args.all_output:
        os.system('pause')
except SystemExit:
    raise
except MyValueError as e:
    print(e)
except Exception as e:
    traceback.print_exc()
    os.system('pause')
