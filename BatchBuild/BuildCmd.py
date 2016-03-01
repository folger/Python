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
args = parser.parse_args()
if args.platform is None:
    args.platform = 'Win32'
if args.configuration is None:
    args.configuration = 'Debug'


def main():
    for project, project_file in BuildUtils.get_projects():
        if os.path.splitext(project)[0].lower() == args.project.lower():
            print(os.path.dirname(project_file))
            if args.file:
                file_name = args.file
                for ff in BuildUtils.get_project_files(project_file):
                    if os.path.basename(ff).lower() == file_name.lower():
                        print(BuildUtils.compile(True,
                                                 project_file,
                                                 args.platform,
                                                 args.configuration,
                                                 ff))
                        break
                else:
                    raise ValueError('{} cannot be found in project {}'
                                     .format(file_name, args.project))
                return

            print(BuildUtils.build(True,
                                   project_file,
                                   args.platform,
                                   args.configuration))
            break
    else:
        raise ValueError('project file {} cannot be found'
                         .format(args.project))


try:
    main()
except Exception as e:
    print(e)
