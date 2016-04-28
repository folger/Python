import sys
import os
from argparse import ArgumentParser
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
args = parser.parse_args()
if args.platform is None:
    args.platform = 'Win32'
if args.configuration is None:
    args.configuration = 'Debug'


def guess_project_from_source_file(f):
    path = os.path.dirname(f)
    paths = path.split('/')
    last_folder = paths[-1].lower()
    if last_folder == 'sdk':
        return 'oks70'
    if last_folder == 'labutil':
        return 'outl'
    for ff in os.listdir(path):
        if ff.endswith('.vcxproj'):
            return os.path.splitext(ff)[0]
    print('Failed to guess project from source file')
    assert(False)


def main():
    if args.project == 'xxx':
        if not args.file:
            print('Source file is not specified, cannot guess project')
            assert(False)
        args.project = guess_project_from_source_file(args.file)
    if args.file:
        args.file = os.path.basename(args.file)
    for project, project_file in BuildUtils.get_projects():
        if os.path.splitext(project)[0].lower() == args.project.lower():
            print(os.path.dirname(project_file))
            if args.file:
                file_name = args.file
                for ff in BuildUtils.get_project_files(project_file):
                    if os.path.basename(ff).lower() == file_name.lower():
                        print(BuildUtils.compile(not args.all_output,
                                                 project_file,
                                                 args.platform,
                                                 args.configuration,
                                                 ff))
                        break
                else:
                    raise ValueError('{} cannot be found in project {}'
                                     .format(file_name, args.project))
                return

            print(BuildUtils.build(not args.all_output,
                                   project_file,
                                   args.platform,
                                   args.configuration))
            break
    else:
        raise ValueError('project file {} cannot be found'
                         .format(args.project))


try:
    main()
    if args.all_output:
        os.system('pause')
except Exception as e:
    print(e)
