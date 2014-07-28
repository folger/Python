import sys
import os
import BuildUtils


platform = 'win32'
configuration = 'Debug'


def main():
    if len(sys.argv) > 1:
        project_name = sys.argv[1]

        for project, project_file in BuildUtils.get_projects():
            if os.path.splitext(project)[0].lower() == project_name.lower():
                print(os.path.dirname(project_file))
                if (len(sys.argv) > 2):
                    file_name = sys.argv[2]
                    for file in BuildUtils.get_project_files(project_file):
                        if os.path.basename(file).lower() == file_name.lower():
                            print(BuildUtils.compile(True, project_file, platform, configuration, file))
                            break
                    else:
                        raise ValueError('{} cannot be found in project {}'.format(file_name, project_name))
                    return

                print(BuildUtils.build(True, project_file, platform, configuration))
                break
        else:
            raise ValueError('project file {} cannot be found'.format(project_name))


try:
    main()
except Exception as e:
    print(e)
