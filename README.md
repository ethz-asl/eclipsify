# Eclipsify
Create eclipse projects from catkin projects. This is a very simple template-based generator. Currently it works for OSX and Ubuntu 14.04.

For C++11 support in Ubuntu 14.04 & Eclipse Luna, go to Window->Preferences->C/C++->Settings->Discovery->"CDT GCC Built-in Compiler Settings" and add `-std=c++11` to the flags.

```
usage: eclipsify [-h] [-v] [-f] [-T TEMPLATES] [--platform PLATFORM]
                 [-w ECLIPSE_WORKSPACE] [-s] [-O PROJECTOUTPUTDIR]
                 [-W,--catkin-ws CATKIN_WORKSPACE]
                 package

This utility creates a new eclipse project. It assumes the package is
in a workspace with the default names for the devel/build/src spaces.
If your workspace is different, try eclipsify-gen-project. If the
command is called with the optional -w option, pointing to an existing
eclipse workspace, the project is added to the eclipse workspace. You 
must not have this workspace open in eclipse when you use -w.

The project files will go to devel/share/project-name/eclipse

positional arguments:
  package               The name of the catkin package to be eclipsified.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Verbosity level.
  -f, --force           Force overwriting existing files.
  -T TEMPLATES, --templates TEMPLATES
                        Templates search path prefix; colon separated.
  --platform PLATFORM   Platform (defaults to sys.platform).
  -w ECLIPSE_WORKSPACE  The path to the eclipse workspace that this package
                        should be added to.
  -s                    Will enforce in source writing of the project files.
                        Equivalent to "-O '{src}'". Any "-O" will be ignored!
  -O PROJECTOUTPUTDIR   The path to the folder in which the eclipse project
                        files should be created. The substrings {devel},
                        {package} and {src} will be replaced appropriately.
  -W,--catkin-ws CATKIN_WORKSPACE
                        The path to the catkin workspace that this package
                        should be. It must point to the workspace's devel
                        space! Default is to use the current catkin workspace
                        layers ("sourced").
```
