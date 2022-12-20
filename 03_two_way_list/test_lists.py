import unittest
from typing import Type

from lists import ParentList, LinkedList, TwoWayList

class Test_List(unittest.TestCase):
    List: Type[ParentList]

    def test_init(self):
        ls: ParentList = self.List()
        self.assertFalse(ls.is_head())
        self.assertFalse(ls.is_tail())
        self.assertFalse(ls.is_value())
        self.assertEqual(ls.size(), 0)
        self.assertEqual(ls.get_head_status(), self.List.HeadStatus.NIL)
        self.assertEqual(ls.get_tail_status(), self.List.TailStatus.NIL)
        self.assertEqual(ls.get_right_status(), self.List.RightStatus.NIL)
        self.assertEqual(ls.get_put_right_status(), self.List.PutRightStatus.NIL)
        self.assertEqual(ls.get_put_left_status(), self.List.PutLeftStatus.NIL)
        self.assertEqual(ls.get_remove_status(), self.List.RemoveStatus.NIL)
        self.assertEqual(ls.get_replace_status(), self.List.ReplaceStatus.NIL)
        self.assertEqual(ls.get_find_status(), self.List.FindStatus.NIL)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.NIL)


class Test_LinkedList(Test_List):
    List = LinkedList


class Test_TwoWayList(Test_List):
    List = TwoWayList


del Test_List

if __name__ == "__main__":
    unittest.main()
