from __future__ import print_function
import os
import tools
import collections
import sys

try:
    from termcolor import colored
except:
    print("Unable to import termcolor.")
    print("Try:")
    print("sudo pip install termcolor")
    def colored(X,Y):
        return X

if sys.version_info[0] == 3:
    string_types = str
else:
    string_types = basestring

class ProjectFile:
    def __init__(self, name, dir = None):
        self._name = name;
        if isinstance(dir, string_types):
            self._dir = dir
        else:
            self._dir = os.path.join(*dir) if dir else ''
    
    def getFullDirPath(self, baseDir):
        return os.path.join(baseDir, self._dir)
        
    def getFullPath(self, baseDir = ""):
        return os.path.join(self.getFullDirPath(baseDir), self._name)

    def __str__(self):
        return self.getFullPath();

class ProjectFilesGenerator:
    def __init__(self, name, srcDir, buildDir) :
        self._name = name
        self._srcDir = srcDir
        self._buildDir = buildDir

    def generate(self, searchDirs, projectFiles, outputDir):
        errors = 0
        print("-- Generating project %s in directory '%s'" % (self._name, outputDir))
        self.createDir(outputDir, '--')
        for projectFile in projectFiles :
            print("--- Creating %s" % projectFile)
            self.createDir(projectFile.getFullDirPath(outputDir), '---')
            try:
                content = self.calcContent(searchDirs, projectFile.getFullPath());
                with open(projectFile.getFullPath(outputDir), 'w') as outfile:
                    print (content , file = outfile )
                print (colored("--> OK", 'green'))
            except tools.FindError as e:
                print (colored("--> Failed: Could not find template file '%s' in search list %s!" % (e.file, searchDirs), 'red'))
                errors += 1;
        if errors == 0:
            print(colored('-> Successfully created the project {0} in directory {1}'.format(self._name, outputDir), 'green'))
        else:
            print(colored("-> Failed: Some errors occurred while created the project {0} in directory '{1}'".format(self._name, outputDir), 'red'))

    def createDir(self, dir, prefix):
        if dir and not os.path.isdir(dir) :
            print(prefix + "- Creating directory '{0}'".format(dir))
            tools.mkdir_p(dir)
            print (colored(prefix + "> OK", 'green'))

    def calcContent(self, searchDirs, file):
        file = tools.findInSearchPath(searchDirs, file)
        with open(file, 'r') as content_file:
            content = content_file.read()
            return content.format(name = self._name, buildDir = self._buildDir, srcDir = self._srcDir)
