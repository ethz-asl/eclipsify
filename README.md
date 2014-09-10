# Eclipsify
Create eclipse projects from catkin projects. This is a very simple template-based generator. Currently it works for OSX and Ubuntu 14.04.

For C++11 support in Ubuntu 14.04 & Eclipse Luna, go to Window->Preferences->C/C++->Settings->Discovery->"CDT GCC Built-in Compiler Settings" and add `-std=c++11` to the flags.

```
usage: eclipsify [-h] [-w WORKSPACE] package

This utility creates a new eclipse project. It assumes the package is
in a workspace with the default names for the devel/build/src spaces.
If your workspace is different, try eclipsify-gen-project. If the
command is called with the optional -w option, pointing to an existing
eclipse workspace, the project is added to the eclipse workspace. You 
must not have this workspace open in eclipse when you use -w.

The project files will go to devel/share/project-name/eclipse

positional arguments:
  package       The name of the catkin package to be eclipsified.

optional arguments:
  -h, --help    show this help message and exit
  -w WORKSPACE  The full path of the eclipse workspace that this package
                should be added to.
```
