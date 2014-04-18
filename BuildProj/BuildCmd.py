import sys
import os
import BuildUtils


platform = 'win32'
configuration = 'Debug'


def main():
    if len(sys.argv) > 1:
        project_name = sys.argv[1]

        projects = BuildUtils.get_projects()
        for project in projects.keys():
            if os.path.splitext(project)[0].lower() == project_name.lower():
                project_file = projects[project]

                if (len(sys.argv) > 2):
                    file_name = sys.argv[2]
                    project_files = BuildUtils.get_project_files(project_file)
                    for file in project_files:
                        if os.path.basename(file).lower() == file_name.lower():
                            BuildUtils.compile(project_file, platform, configuration, file)
                            break
                    else:
                        raise ValueError('{} cannot be found in project {}'.format(file_name, project_name))
                    return

                BuildUtils.build(project_file, platform, configuration)
                break
        else:
            raise ValueError('project file {} cannot be found'.format(project_name))


try:
    main()
except Exception as e:
    print(e)
    os.system('pause')
