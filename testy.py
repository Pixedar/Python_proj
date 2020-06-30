import main
import unittest
import game

class Basic_tests(unittest.TestCase):
    def mianTest(self):
        self.assertTrue(main.test)
    def mainTest2(self):
        self.assertFalse(main.test1(10))

class Positon_class_tests(unittest.TestCase):
    def setUp(self):
        self.cell = game.Pos(x=5, y=6)
    def testPosX(self):
         self.assertEqual(self.cell.x,5)
    def testPosY(self):
         self.assertEqual(self.cell.y,5)




