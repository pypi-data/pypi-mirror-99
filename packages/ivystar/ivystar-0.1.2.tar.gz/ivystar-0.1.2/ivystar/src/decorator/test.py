#!encoding=utf-8
import unittest
from ivystar.src.decorator import log
from ivystar.src.decorator import timer

class TestSetUp(unittest.TestCase):
    '''
    测试文件
    '''

    def setUp(self):
        print(">>> start test ivystar.src.decorator")


    def test_run(self):

        @log
        def fast(x, y):
            return x*y
        fast(3,5)

        @timer
        def fast(x, y):
            return x*y
        fast(3,5)

    def tearDown(self):
        print("<<< end test ivystar.src.decorator")

if __name__ == "__main__":
    unittest.main()
else:
    unittest.main()
