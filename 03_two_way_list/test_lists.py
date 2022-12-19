import unittest

from lists import LinkedList, TwoWayList

class Test_List(unittest.TestCase):
    List = None

    def test(self):
        print(self.List)


class Test_LinkedList(Test_List):
    List = LinkedList


class Test_TwoWayList(Test_List):
    List = TwoWayList


del Test_List

if __name__ == "__main__":
    unittest.main()
