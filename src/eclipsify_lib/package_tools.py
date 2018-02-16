import exceptions

try:
    from catkin_pkg.packages import find_packages
    from catkin_pkg.package import parse_package
    foundCatkinPkg = True
except exceptions.ImportError:
  try:
      from catkin_pkg.package import find_packages, parse_package
      foundCatkinPkg = True
  except exceptions.ImportError as e:
      foundCatkinPkg = False
      print("Unable to import catkin_pkg (%s)." % e)
      print("Without it eclipsify won't find packages in subfolders of the 'src' folder or in other than the top level workspace.")
      print("If this is needed try:")
      print("  sudo apt-get install catkin_pkg")
      print("or use the eclipsify-gen-project cli tool.")

from tools import *



class Workspace :
    def __init__(self, develSpace):
        self._develspace = develSpace
        self._base = os.path.dirname(develSpace)
        
    def getPath(self):
        return self._base;
    def getDevelSpace(self):
        return self._develspace;
    def getBuildSpace(self):
        return os.path.join(self._base, 'build');
    def getSourceFolder(self):
        return os.path.join(self._base, 'src');

def isPackageSrc(spath):
    return os.path.exists(os.path.join(spath, "package.xml"))

class PackageCollector:
    def __init__(self, searchPackageName):
        self.cnt = 0
        self.src = None
        self.workspace = None
        self.searchPackageName = searchPackageName

    def processPackage(self, s, ws):
        verbose("Testing package candidate in folder '%s'." % s);
        if isPackageSrc(s):
            p = parse_package(s);
            verbose("Found package named '%s'." % p.name);
            if(p.name == self.searchPackageName):
                if self.cnt==0:
                    self.workspace = Workspace(ws)
                    self.src = s
                    okay('-- Found {0} in workspace {1} with source {2}'.format(self.searchPackageName, ws, s))
                elif self.workspace._develspace != ws or self.src != s:
                    error('-- Package ambiguous also in workspace {0} with source {1}'.format(ws, s))
                self.cnt+=1
        else:
            verbose("Is no package.");
