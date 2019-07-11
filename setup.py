
## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# fetch values from package.xml
setup_args = generate_distutils_setup(
    packages=[
        'eclipsify_lib',
        'eclipsify_lib.tools',
        'eclipsify_lib.package_tools',
        'eclipsify_lib.templates'],
    package_dir={'':'src'},
    scripts=['src/eclipsify-gen-project','src/eclipsify'],
    package_data={'eclipsify_lib.templates': ['linux2/.cproject',
                                              'linux2/.project',
                                              'darwin/.cproject',
                                              'darwin/.project',
                                              '.settings/*'
                                              ]}
)

setup(**setup_args)
