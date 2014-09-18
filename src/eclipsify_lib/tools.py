import errno
import os
import sys

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: 
            raise

class FindError(Exception):
    def __init__(self, file):
        self.file = file
        
    def getFile(self):
        return self.file


def findInSearchPath(pathList, file):
    for dirname in pathList:
        candidate = os.path.join(dirname, file)
        if os.path.isfile(candidate):
            return candidate
    raise FindError(file)

def addModuleSaearchDirsAndCleanFromDanglingPycFiles(directories):
    import glob
    for d in reversed(directories):
        if os.path.isdir(d):
            for pycFile in glob.glob(os.path.join(d, "*.pyc")):
                if not os.path.isfile(pycFile[:-1]):
                    print ("Removing dangling '%s'." % pycFile)
                    os.remove(pycFile); 
            sys.path.insert(0, d)
