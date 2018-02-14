# Eclipsify
Create eclipse projects from catkin projects. This is a very simple template-based generator. Currently it works at least for OSX, Ubuntu 14.04, and Ubuntu 16.04.
If you'd like to enjoy the colorful output of catkin on the eclipse console have a look at the  [ansi-escape-console plugin](https://marketplace.eclipse.org/content/ansi-escape-console) .

### Requirements
* [Eclipse CDT](https://www.eclipse.org/cdt/)
* [catkin tools](https://catkin-tools.readthedocs.io/)

### Installation
- Clone the **eclipsify** repository into your catkin workspace

- Retrieve dependencies by performing one of the following alternatives:
  1. Using `wstools` :
      - Install [wstools](http://wiki.ros.org/wstool)
      - CD into your workspace top level directory and run the following commands

          ```
          wstool init src
          wstool merge -t src src/eclipsify/.rosinstall
          wstool update -t src
        ```
      - The last command will download the required repositories into your workspace

  2. Manually:
      - Clone all the missing dependences listed in [.rosinstall](.rosinstall) into your catkin workspace

- Build the **eclipsify** package

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

### Examples

#### Single ROS packages
In order to create eclipse project files for a single ros package called **my_pkg** that lives in a 
catkin do the following:

- `cd` into the top level directory of your **catkin workspace**

- Run **eclipsify** to generate Eclipse project files by performing one of the following alternatives:
  1. Project files in catkin devel-space:
      ```
      eclipsify my_pkg
      ```
      The generated project files go into **\<catkin workspace>/devel/share/my_pkg/eclipse/** and the my_pkg source folder gets linked into the project.

  2. Other separate project files folder (e.g. `projects`):

      This options is useful if you'd like to keep IDE project files outside of your tracked repository directories and the catkin devel-space.
      ```
      eclipsify my_pkg -O projects/my_pkg
      ```

      This will create the eclipse project files in the **\<catkin workspace>/projects/my_pkg** and also link it to my_pkg source folder.

  3. In-source option (required by **EGit**):
      ```
      eclipsify -s my_pkg
      ```
      In this case the generated project files go into the source folder of my_pkg (e.g. src/my_pkg).
      Currently EGit (Eclipse's git plugin) requires the project files to reside within the src folder under git's version control.
      To mitigate the problem of accidentally committed project files, a [global git ignore file](https://help.github.com/articles/ignoring-files/#create-a-global-gitignore) is an interesting option. 
      For example with the following content:
      ```
      # Ignore Eclipse project files
      .project
      .settings/
      ## Eclipse CDT
      .cproject
      .csettings/
      ## Eclipse pydev
      .pydevproject
      ## TeXlipse
      .texlipse
      ```

#### Multiple Packages
The _eclipsify_ command can be used in conbitation with the catkin command to easily generate project files for all the ROS packages that  
reside in a workspace. The options are as follows:

  1. Create project files in the catkin worspace devel directory:
    ```
    catkin list -u | xargs -I pkg bash -c "eclipsify pkg"
    ```
    As in the single package example, the eclipse project files will be stored in a subdirectory in the **\<catkin workspace>/devel/share/..**  
    directory.

  2. Create project files in a separate __projects__ directory:
    Run the following command from the root directory of your catkin workspace
    ```
    catkin list -u | xargs -I pkg bash -c "eclipsify pkg -O projects/pkg"
    ```
    This will create the eclipse project files for each package in separate subdirectories in the **\<catkin workspace>/projects/** directory.


- **Import** into an Eclipse workspace through one of the following alternatives:

  1. Import the project by browsing to the project files directory just created from the **Import** window in eclipse.
  Make sure to select the "Existing Project into Workspace" option under the "General" category
  shown in the **Import** window.
  
  2. In the next window, check the boxes for all the packages you wish to import and then click **Finish**
  
  3. **EGit** option (assuming my_pkg being under git version control):
      - **Add** the my_pkg source folder as git repository to the Eclipse workspace using EGit
      - Right click on the repository and select **Improt Projects...**
