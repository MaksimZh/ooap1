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
        ls.head()
        self.assertEqual(ls.get_head_status(), self.List.HeadStatus.EMPTY)
        ls.tail()
        self.assertEqual(ls.get_tail_status(), self.List.TailStatus.EMPTY)
        ls.right()
        self.assertEqual(ls.get_right_status(), self.List.RightStatus.NO_RIGHT_NEIGHBOR)
        ls.put_right(1)
        self.assertEqual(ls.get_put_right_status(), self.List.PutRightStatus.EMPTY)
        ls.put_left(1)
        self.assertEqual(ls.get_put_left_status(), self.List.PutLeftStatus.EMPTY)
        ls.remove()
        self.assertEqual(ls.get_remove_status(), self.List.RemoveStatus.EMPTY)
        ls.replace(1)
        self.assertEqual(ls.get_replace_status(), self.List.ReplaceStatus.EMPTY)
        ls.find(1)
        self.assertEqual(ls.get_find_status(), self.List.FindStatus.NOT_FOUND)
        _ = ls.get()
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.EMPTY)


class Test_LinkedList(Test_List):
    List: Type[LinkedList] = LinkedList


class Test_TwoWayList(Test_List):
    List: Type[TwoWayList] = TwoWayList

    def test_init_ext(self):
        ls: TwoWayList = self.List()
        self.assertEqual(ls.get_left_status(), self.List.LeftStatus.NIL)
        ls.left()
        self.assertEqual(ls.get_left_status(), self.List.LeftStatus.NO_LEFT_NEIGHBOR)


del Test_List

if __name__ == "__main__":
    unittest.main()
