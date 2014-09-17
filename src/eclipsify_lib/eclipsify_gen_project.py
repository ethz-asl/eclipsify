from __future__ import print_function
import os
import sys
import tools
import eclipsify_lib
from argparse import ArgumentParser, RawDescriptionHelpFormatter

try:
    from termcolor import colored
except:
    print("Unable to import termcolor.")
    print("Try:")
    print("sudo pip install termcolor")
    def colored(X,Y):
        return X



def main(argv=None):
    if argv is None:
        argv=sys.argv

    usage="""

    This utility creates a new eclipse project."""

    parser = ArgumentParser(description=usage,formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument("package", nargs=1, help="Package to be created.")
    parser.add_argument("src_dir", nargs=1, help="The source directory.")
    parser.add_argument("out_dir", nargs=1, help="The output directory. Where to put the eclipse project.")
    parser.add_argument("build_dir", nargs=1, help="This project's build directory.")
    #parser.add_argument("bin_dir", nargs=1, help="This project's bin directory.")
    parser.add_argument("--platform", help="Platform (defaults to sys.platform).", default=sys.platform)

    options = parser.parse_args(argv)

    package     = options.package[0]
    src_dir     = options.src_dir[0]
    eclipse_dir = options.out_dir[0]
    build_dir   = options.build_dir[0]
    platform   = options.platform

    print("eclipsify!")
    print("----------")
    print("-- Creating directories")
    print("-- {0}".format(eclipse_dir))
    tools.mkdir_p( os.path.join( eclipse_dir, '.settings' ) )

    if platform == 'darwin':
        import eclipsify_lib.cproject_osx as cproject
        import eclipsify_lib.project_osx as project
        import eclipsify_lib.language_settings_osx as language_settings
    elif platform == 'linux2':
        import eclipsify_lib.cproject_linux as cproject
        import eclipsify_lib.project_linux as project
        import eclipsify_lib.language_settings_linux as language_settings
    else:
        raise RuntimeError('Someone has to fill in these templates');

    print("-- Creating .project")
    with open(os.path.join(eclipse_dir,'.project'), 'w') as outfile:
        print(project.get(package, src_dir), file=outfile)

    print("-- Creating .cproject")
    with open(os.path.join(eclipse_dir,'.cproject'), 'w') as outfile:
        print(cproject.get(package,build_dir), file=outfile)

    print("-- Creating .settings/language.settings.xml")
    with open(os.path.join(eclipse_dir,'.settings', 'language_settings.xml'), 'w') as outfile:
        print(language_settings.get(), file=outfile)
    print(colored('-- Successfully created the project {0} in directory {1}'.format(package, eclipse_dir), 'green'))
