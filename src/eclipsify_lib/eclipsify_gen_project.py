from __future__ import print_function
import sys
import os
import tools
import generator as generator;
from argparse import ArgumentParser, RawDescriptionHelpFormatter

def main(argv=None):
    if argv is None:
        argv=sys.argv

    usage="""

    This utility creates a new eclipse project."""

    parser = ArgumentParser(description=usage,formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument("package", nargs=1, help="Package to be created.")
    parser.add_argument("srcDir", nargs=1, help="The source directory.")
    parser.add_argument("outDir", nargs=1, help="The output directory. Where to put the eclipse project.")
    parser.add_argument("buildDir", nargs=1, help="This project's build directory.")
    #parser.add_argument("binDir", nargs=1, help="This project's bin directory.")
    parser.add_argument("--platform", help="Platform (defaults to sys.platform).", default=sys.platform)

    options = parser.parse_args(argv)

    platform = options.platform
    outputDir = options.outDir[0]
    
    print("eclipsify!")
    print("----------")

    libDir = os.path.dirname(__file__);
    sys.path.insert(0, libDir)
    
    templatesDir = os.path.join(libDir, 'templates');
    platformTemplateDir = os.path.join(templatesDir, platform);
    templateSearchPaths = [platformTemplateDir, templatesDir];
    tools.addModuleSaearchDirsAndCleanFromDanglingPycFiles(templateSearchPaths);
    import projectFiles
    
    projectFilesGenerator = generator.ProjectFilesGenerator(options.package[0], options.srcDir[0], options.buildDir[0])
    projectFilesGenerator.generate(templateSearchPaths, projectFiles.files, outputDir);
