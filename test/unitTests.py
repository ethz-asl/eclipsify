#!/usr/bin/env python
import unittest
import StringIO

import eclipsify_lib.generator as generator

class GeneratorTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def runCppAndStrip(self, defs, useCpp):
        return generator.applyCppAndStripComments('testCPP.txt', defs, useCpp)

    def testGeneratorGenerate(self):
        self.assertEqual(self.runCppAndStrip({ }, False), "BLA\nTEST_DEF\nIfContent\nEND\n")
        self.assertEqual(self.runCppAndStrip({ }, True), "BLA\nBLADEF\nEND\n")
        self.assertEqual(self.runCppAndStrip({ 'COND': 1 }, True), "BLA\nBLADEF\nIfContent\nEND\n")
        self.assertEqual(self.runCppAndStrip({ 'BLA': 'NOT_BLA' }, True), "NOT_BLA\nBLADEF\nEND\n")
        
if __name__ == '__main__':
    import rostest
    rostest.rosrun('eclipsify', 'generator', GeneratorTest)
