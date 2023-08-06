#!encoding=utf-8
import unittest
import ivystar
from ivystar import src
import ivystar.src.decorator
import ivystar.src.decorator
from ivystar.src.decorator import log
from ivystar.src.decorator import timer

class TestSetUp(unittest.TestCase):

    def setUp(self):
        print("start test")

    def test_run(self):
        fast(3,5)
        print('test_run')

    @log
    @timer
    def fast(x, y):
        return x*y

    def tearDown(self):
        print("test end")

if __name__ == "__main__":
    unittest.main()
else:
    unittest.main()
