import errno
import os
import sys

try:
    from termcolor import colored
except:
    print("Unable to import termcolor.")
    print("Try:")
    print("sudo pip install termcolor")
    def colored(X,Y):
        return X

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: 
            raise

class FindError(Exception):
    def __init__(self, fileName):
        self.file = fileName
        
    def getFile(self):
        return self.fileName


def findInSearchPath(pathList, fileName):
    for dirname in pathList:
        candidate = os.path.join(dirname, fileName)
        if os.path.isfile(candidate):
            return candidate
    raise FindError(fileName)

def addModuleSaearchDirsAndCleanFromDanglingPycFiles(directories):
    import glob
    for d in reversed(directories):
        if os.path.isdir(d):
            for pycFile in glob.glob(os.path.join(d, "*.pyc")):
                if not os.path.isfile(pycFile[:-1]):
                    print ("Removing dangling '%s'." % pycFile)
                    os.remove(pycFile); 
            sys.path.insert(0, d)
