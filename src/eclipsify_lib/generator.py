from __future__ import print_function
import os
import tools
import sys

from tools import colored, error, verbose, okay

if sys.version_info[0] == 3:
    string_types = str
else:
    string_types = basestring

import re
commentFilter = re.compile(r'^\s*#')

import subprocess
import io
import StringIO


cppAvailable = subprocess.call(["sh", "-c", "echo | cpp > /dev/null 2>&1"]) == 0
if not cppAvailable:
    print(colored("""Warning:
    Unable to run the c pre processor (command cpp).
    Without it eclipsify won't be able to instantiate the templates relying on cpp correctly.
    On Ubuntu or Debian run 'sudo apt-get install cpp' to install it.
    """, 'red'))


def applyCppAndStripCommentsIntoFile(fileName, definitions, outfile, useCpp):
    stderr = None
    if useCpp:
        args = ''
        for key, value in definitions.iteritems():
            args += "'-D%s=%s' " % (key, value)
        pipe = subprocess.Popen("cpp -traditional-cpp %s '%s'" %(args, fileName), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        source = pipe.stdout
        stderr = pipe.stderr
    else:
        source = io.open(fileName, 'r')
    
    for line in source.readlines():
        if line != '\n' and not commentFilter.match(line):
            print(line, end='', file = outfile)
            
    if stderr:
        for line in stderr.readlines():
            print(colored(line, 'red'), end='')
        stderr.close()
    
    source.close()

def applyCppAndStripComments(fileName, definitions, useCpp):
    output = StringIO.StringIO()
    applyCppAndStripCommentsIntoFile(fileName, definitions, output, useCpp)
    value = output.getvalue()
    output.close()
    return value

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
    def __init__(self, verbose, name, srcDir, buildDir, cppMacros) :
        self._verbose = verbose
        self._name = name
        self._srcDir = srcDir
        self._buildDir = buildDir
        self._cppMacros = cppMacros

    def error(self, text):
        error(text)
        self.errors += 1
        
    def generate(self, searchDirs, projectFiles, outputDir, forceOverwrite = False):
        self.errors = 0
        
        print("-- Generating project %s in directory '%s'" % (self._name, outputDir))
        verbose("--- Using template search path '%s'" % ( ":".join(searchDirs)))
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
                    okay("--> OK")
                except tools.FindError as e:
                    self.error("--> Failed: Could not find template file '%s' in search list %s!" % (e.file, searchDirs))
            else:
                self.error("--- Skipping existing %s (use -f to overwrite)" % (projectFile))
        if self.errors == 0:
            okay('-> Successfully created the project {0} in directory {1}'.format(self._name, outputDir))
            return 0
        else:
            self.error("-> Failed: Some errors occurred while created the project {0} in directory '{1}'".format(self._name, outputDir))
            return 4

    def createDir(self, dirPath, prefix):
        if dir and not os.path.isdir(dirPath) :
            verbose(prefix + "- Creating directory '{0}'".format(dirPath))
            tools.mkdir_p(dirPath)
            okay(prefix + "> OK")

    def calcContent(self, searchDirs, fileName):
        filePath = tools.findInSearchPath(searchDirs, fileName)
        verbose("---- Instantiating template file '%s'" % filePath);
        content = applyCppAndStripComments(filePath, self._cppMacros, cppAvailable)
        return content.format(name = self._name, buildDir = self._buildDir, srcDir = self._srcDir)
