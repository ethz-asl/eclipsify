from __future__ import print_function
import os
import tools
import sys

from tools import colored

if sys.version_info[0] == 3:
    string_types = str
else:
    string_types = basestring

class ProjectFile:
    def __init__(self, name, dirPath = None):
        self._name = name;
        if isinstance(dirPath, string_types):
            self._dir = dirPath
        else:
            self._dir = os.path.join(*dirPath) if dirPath else ''
    
    def getFullDirPath(self, baseDir):
        return os.path.join(baseDir, self._dir)
        
    def getFullPath(self, baseDir = ""):
        return os.path.join(self.getFullDirPath(baseDir), self._name)

    def __str__(self):
        return self.getFullPath();

class ProjectFilesGenerator:
    def __init__(self, verbose, name, srcDir, buildDir) :
        self._verbose = verbose
        self._name = name
        self._srcDir = srcDir
        self._buildDir = buildDir

    def verbose(self, text):
        if self._verbose : print (colored(text, 'yellow'))

    def error(self, text):
        print (colored(text, 'red'))
        self.errors += 1

    def okay(self, text):
        print (colored(text, 'green'))
        
    def generate(self, searchDirs, projectFiles, outputDir, forceOverwrite = False):
        self.errors = 0
        
        print("-- Generating project %s in directory '%s'" % (self._name, outputDir))
        self.verbose("--- Using template search path '%s'" % ( ":".join(searchDirs)))
        self.createDir(outputDir, '--')
        for projectFile in projectFiles :
            projectFileFullPath = projectFile.getFullPath(outputDir)
            projectFileExists = os.path.exists(projectFileFullPath)
            if (not projectFileExists or forceOverwrite) :
                print("--- %s %s" % ("Overwriting" if projectFileExists else "Creating", projectFileFullPath))
                self.createDir(projectFile.getFullDirPath(outputDir), '---')
                try:
                    content = self.calcContent(searchDirs, projectFile.getFullPath());
                    with open(projectFileFullPath, 'w') as outfile:
                        print (content , file = outfile )
                    self.okay("--> OK")
                except tools.FindError as e:
                    self.error("--> Failed: Could not find template file '%s' in search list %s!" % (e.file, searchDirs))
            else:
                self.error("--- Skipping existing %s (use -f to overwrite)" % (projectFile))
        if self.errors == 0:
            print(colored('-> Successfully created the project {0} in directory {1}'.format(self._name, outputDir), 'green'))
        else:
            self.error("-> Failed: Some errors occurred while created the project {0} in directory '{1}'".format(self._name, outputDir))

    def createDir(self, dirPath, prefix):
        if dir and not os.path.isdir(dirPath) :
            self.verbose(prefix + "- Creating directory '{0}'".format(dirPath))
            tools.mkdir_p(dirPath)
            self.okay(prefix + "> OK")

    def calcContent(self, searchDirs, fileName):
        filePath = tools.findInSearchPath(searchDirs, fileName)
        self.verbose("---- Instantiating template file '%s'" % filePath);
        with open(filePath, 'r') as content_file:
            content = content_file.read()
            return content.format(name = self._name, buildDir = self._buildDir, srcDir = self._srcDir)
