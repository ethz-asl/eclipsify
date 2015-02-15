#!/usr/bin/env python
import unittest
import sys
import os
import subprocess


class EclipsifyAcceptance(unittest.TestCase):
    def _testGeneratorGeneratesSame(self, platform, projects = ['test_project_1'], testWorkspace = 'testWs/devel'):
        for project in projects:
            outDir = 'expected/%s/%s/%s' % (testWorkspace, platform, project)
            subprocess.call(['rm', '-rf', outDir])
            subprocess.call([sys.executable, 
                             '../src/eclipsify', '-v', 
                             '-W', testWorkspace, 
                             '-O', outDir, 
                             '--platform', platform, 
                             '-T', '=../src/eclipsify_lib/templates/%s:../src/eclipsify_lib/templates' % platform, 
                             project])
            #TODO write eclipsify output also to file and make it join the expected output! 
            pipe = os.popen('git diff '+ outDir + ' 2>&1')
            c = 0
            for l in pipe:
                print l.strip()
                c += 1
            self.assertEqual(c, 0, "There should be no difference between HEAD and the expected output! Either fix the code or commit changed expected output.")
    def testLinux(self):
        self._testGeneratorGeneratesSame('linux2')
    def testDarwin(self):
        self._testGeneratorGeneratesSame('darwin')
if __name__ == '__main__':
    import rostest
    rostest.rosrun('eclipsify', 'acceptance', EclipsifyAcceptance)
