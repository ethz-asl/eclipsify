from __future__ import print_function
import sys
import os
import tools
import generator as generator
from argparse import ArgumentParser, RawDescriptionHelpFormatter

def addCommonArguments(parser):
    parser.add_argument('-v', '--verbose', action='count', help="Verbosity level.", default=0)
    parser.add_argument("-f", "--force", action='count', help="Force overwriting existing files.", default=False)
    parser.add_argument('-T', '--templates', help="Templates search path prefix; colon separated.", default="")
    parser.add_argument('-D', '--define', action='append', metavar="DEFINE[=VALUE]", help="Add cpp (c pre-processor) definitions.", default=[])
    parser.add_argument("--platform", help="Platform (defaults to sys.platform).", default=sys.platform)
    parser.add_argument("package", nargs=1, help="The name of the catkin package to be eclipsified.")

def main(options = None):
    if not options:
        usage="""

        This utility creates a new eclipse project."""

        parser = ArgumentParser(description=usage,formatter_class=RawDescriptionHelpFormatter)
        addCommonArguments(parser)

        parser.add_argument("srcDir", nargs=1, help="The source directory.")
        parser.add_argument("outDir", nargs=1, help="The output directory. Where to put the eclipse project.")
        parser.add_argument("buildDir", nargs=1, help="This project's build directory.")

        options = parser.parse_args(sys.argv)

    platform = options.platform
    outputDir = options.outDir[0]
    package = options.package[0]

    cppMacroDict = dict()
    print("eclipsify package %s for platform %s" % (package, platform))
    if len(options.define) :
        print("\tactive cpp macros / defines :");
        for opt in options.define:
            print("\t\t" + opt);
            parts = opt.split('=', 2);
            cppMacroDict[parts[0]] =  parts[1] if len(parts) > 1 else '1'

    print("----------")

    libDir = os.path.dirname(__file__);
    sys.path.insert(0, libDir)

    templatesDir = os.path.join(libDir, 'templates');
    platformTemplateDir = os.path.join(templatesDir, platform);
    userTemplatesDir = os.path.expanduser("~/.eclipsify/templates");
    userPlatformTemplatesDir = os.path.join(userTemplatesDir, platform);

    extendWithDefaultTemplatePaths = True
    if options.templates.startswith('='):
        extendWithDefaultTemplatePaths = False
        options.templates = options.templates[1:]
    templateSearchPaths = options.templates.split(':')
    if extendWithDefaultTemplatePaths:
        templateSearchPaths.extend([userPlatformTemplatesDir, userTemplatesDir, platformTemplateDir, templatesDir]);

    # get rid of empty template search paths
    templateSearchPaths = [ p for p in templateSearchPaths if (p) ]

    tools.addModuleSaearchDirsAndCleanFromDanglingPycFiles(templateSearchPaths);

    import projectFiles
    projectFilesGenerator = generator.ProjectFilesGenerator(options.verbose, package, options.srcDir[0], options.buildDir[0], cppMacros = cppMacroDict)

    import precondition

    class EclipsifyConfig():
        def __init__(self):
            self.platform = platform;
            self.package = package
            self.srcDir = options.srcDir[0]
            self.outDir = outputDir
            self.options = options

    config = EclipsifyConfig();
    if precondition.fullfilled(config):
        #TODO(HannesSommer) use config object also for generator input
        projectFilesGenerator.generate(templateSearchPaths, projectFiles.files, outputDir, forceOverwrite=options.force);
