# Eclipsify
Create eclipse projects from catkin projects. This is a very simple template-based generator. Currently it works for OSX, Ubuntu 14.04, and Ubuntu 16.04.

### Installation
- Download [wstools](http://wiki.ros.org/wstool)

- Clone the **eclipsify** repository into your catkin workspace

- Download Dependencies  

    - CD into your workspace top level directory and run the following commands

        ```
        wstool init src
        wstool merge -t src src/eclipsify/.rosinstall
        wstool update -t src
        ```
    - The last command will download the required repositories into your workspace

- Build the eclipsify package

  ```
  catkin build eclipsify
  ```

### Usage

```    
usage: eclipsify [-h] [-v] [-f] [-T TEMPLATES] [-D DEFINE[=VALUE]] [--platform PLATFORM]
                 [-w ECLIPSE_WORKSPACE] [-s] [-O PROJECTOUTPUTDIR] [-W,--catkin-ws CATKIN_WORKSPACE]
                 package

This utility creates a new eclipse project. It assumes the package is in a workspace with the default
names for the devel/build/src spaces. If your workspace is different, try eclipsify-gen-project. If
the command is called with the optional -w option, pointing to an existing eclipse workspace, the
project is added to the eclipse workspace. You must not have this workspace open in eclipse when you
use -w. Unfortunately this can be slow; see below. The project files will go to
{devel}/share/{package}/eclipse/ unless -s or -O are used.

positional arguments:
  package               The name of the catkin package to be eclipsified.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Verbosity level.
  -f, --force           Force overwriting existing files.
  -T TEMPLATES, --templates TEMPLATES
                        Templates search path prefix; colon separated.
  -D DEFINE[=VALUE], --define DEFINE[=VALUE]
                        Add cpp (c pre-processor) definitions.
  --platform PLATFORM   Platform (defaults to sys.platform).
  -w ECLIPSE_WORKSPACE  The path to the eclipse workspace that this package should be added to.
                        WARNING: This is going to be very slow in some situations (see
                        'https://github.com/ethz-asl/eclipsify/issues/8' for more information). As an
                        alternative consider "File -> Import -> Existing Projects into Workspace"
                        from within eclipse. There you can even import multiple projects at once.
  -s                    Will enforce in source writing of the project files. Equivalent to "-O
                        '{src}' -D IN_SOURCE=1". An additionally provided "-O" will take precedence.
  -O PROJECTOUTPUTDIR   The path to the folder in which the eclipse project files should be created.
                        The substrings {devel}, {package} and {src} will be replaced appropriately.
  -W,--catkin-ws CATKIN_WORKSPACE
                        The path to the catkin workspace that this package should be. It must point
                        to the workspace's devel space! Default is to use the current catkin
                        workspace layers ("sourced").
```

### Example

In order to create eclipse project files for a ros package called **my_pkg** that lives in a 
catkin workspace then do the following:
- CD into the top level directory of your workspace

- Run eclipsify
    ```
    eclipsify my_pkg -O project/my_pkg
    ```

  This will create the eclipse project files in the **project/my_pkg**.  At this point
  you can import the project into [Eclipse CDT](https://www.eclipse.org/cdt/) by opening
  eclipse and browsing to the the directory just created using the **Import** feature. 
  Make sure select the "Existing Project into Workspace" option under the "General" category
  shown in the *Import* window.
  


