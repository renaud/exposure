import unittest
import exposure

class ObjectName(unittest.TestCase):
    def testGetObjectName(self):
        myobject = 'hello'
        self.assertEqual(exposure._find_name(myobject), 'myobject')
        mylist = ['hello', 'world']
        self.assertEqual(exposure._find_name(mylist), 'mylist')


if __name__ == "__main__":
    unittest.main()
