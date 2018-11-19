#!/usr/bin/env python

from __future__ import print_function
import unittest
import sys
import os
import subprocess

class EclipsifyAcceptance(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        os.environ['ECLIPSIFY_USE_RELATIVE_LOCATIONS_FOR_TESTING'] = "1"

    def _testGeneratorGeneratesSame(self, platform, inSource=False, projects=['test_project_1'], testWorkspace='testWs/devel'):
        for project in projects:
            outDir = 'expected/%s/%s/%s' % (testWorkspace if not inSource else os.path.join(os.path.dirname(testWorkspace), "src"), platform, project)
            subprocess.call(['rm', '-rf', outDir])
            subprocess.call([sys.executable,
                             '../src/eclipsify', '-v',
                             '-s' if inSource else '-v',
                             '-W', testWorkspace,
                             '-O', outDir,
                             '--platform', platform,
                             '-T', '=../src/eclipsify_lib/templates/%s:../src/eclipsify_lib/templates' % platform,
                             project]
                            )
            # TODO(HannesSommer): write eclipsify output also to file and make it join the expected output!
            pipe = os.popen('git diff ' + outDir + ' 2>&1')
            c = 0
            for l in pipe:
                print(l.strip())
                c += 1
            self.assertEqual(c, 0, "There should be no difference between HEAD and the expected output! Either fix the code or commit changed expected output.")

    def testLinux(self):
        self._testGeneratorGeneratesSame('linux2')

    def testLinuxInSource(self):
        self._testGeneratorGeneratesSame('linux2', True)

    def testDarwin(self):
        self._testGeneratorGeneratesSame('darwin')

    def testDarwinInSource(self):
        self._testGeneratorGeneratesSame('darwin', True)

if __name__ == '__main__':
    import rostest
    rostest.rosrun('eclipsify', 'acceptance', EclipsifyAcceptance)
