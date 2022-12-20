import unittest
from typing import Type, Any

from lists import ParentList, LinkedList, TwoWayList

class Test_List(unittest.TestCase):
    
    List: Type[ParentList]

    def check_nil_status(self, ls: ParentList):
        self.assertEqual(ls.get_head_status(), self.List.HeadStatus.NIL)
        self.assertEqual(ls.get_tail_status(), self.List.TailStatus.NIL)
        self.assertEqual(ls.get_right_status(), self.List.RightStatus.NIL)
        self.assertEqual(ls.get_put_right_status(), self.List.PutRightStatus.NIL)
        self.assertEqual(ls.get_put_left_status(), self.List.PutLeftStatus.NIL)
        self.assertEqual(ls.get_remove_status(), self.List.RemoveStatus.NIL)
        self.assertEqual(ls.get_replace_status(), self.List.ReplaceStatus.NIL)
        self.assertEqual(ls.get_find_status(), self.List.FindStatus.NIL)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.NIL)

    def check_empty(self, ls: ParentList):
        self.assertFalse(ls.is_head())
        self.assertFalse(ls.is_tail())
        self.assertFalse(ls.is_value())
        self.assertEqual(ls.size(), 0)
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

    def check_content(self, ls: ParentList, values: list[Any]):
        ls.head()
        content = []
        while not ls.is_tail():
            content.append(ls.get())
            ls.right()
        content.append(ls.get())
        self.assertEqual(content, values)

    def test_init(self):
        ls = self.List()
        self.check_nil_status(ls)
        self.check_empty(ls)
    
    def test_single(self):
        ls = self.List()
        ls.add_tail(1)
        self.assertTrue(ls.is_head())
        self.assertTrue(ls.is_tail())
        self.assertTrue(ls.is_value())
        self.assertEqual(ls.size(), 1)
        ls.head()
        self.assertEqual(ls.get_head_status(), self.List.HeadStatus.OK)
        ls.tail()
        self.assertEqual(ls.get_tail_status(), self.List.TailStatus.OK)
        ls.right()
        self.assertEqual(ls.get_right_status(), self.List.RightStatus.NO_RIGHT_NEIGHBOR)
        ls.replace(2)
        self.assertEqual(ls.get_replace_status(), self.List.ReplaceStatus.OK)
        ls.find(2)
        self.assertEqual(ls.get_find_status(), self.List.FindStatus.OK)
        v = ls.get()
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.OK)
        self.assertEqual(v, 2)
        ls.remove()
        self.check_empty(ls)

    def test_clear(self):
        ls = self.List()
        ls.add_tail(1)
        ls.add_tail(2)
        ls.clear()
        self.check_nil_status(ls)
        self.check_empty(ls)

    def test_multi(self):
        ls = self.List()
        ls.add_tail(1)
        ls.add_tail(2)
        ls.add_tail(3)
        self.assertEqual(ls.size(), 3)
        self.assertTrue(ls.is_head())
        self.assertFalse(ls.is_tail())
        self.assertTrue(ls.is_value())
        ls.tail()
        self.assertEqual(ls.get_tail_status(), self.List.TailStatus.OK)
        self.assertFalse(ls.is_head())
        self.assertTrue(ls.is_tail())
        self.assertTrue(ls.is_value())
        ls.head()
        self.assertEqual(ls.get_head_status(), self.List.HeadStatus.OK)
        self.assertTrue(ls.is_head())
        self.assertFalse(ls.is_tail())
        self.assertTrue(ls.is_value())

        self.assertEqual(ls.get(), 1)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.OK)
        ls.right()
        self.assertEqual(ls.get_right_status(), self.List.RightStatus.OK)
        self.assertFalse(ls.is_head())
        self.assertFalse(ls.is_tail())
        self.assertTrue(ls.is_value())
        self.assertEqual(ls.get(), 2)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.OK)
        ls.right()
        self.assertEqual(ls.get_right_status(), self.List.RightStatus.OK)
        self.assertFalse(ls.is_head())
        self.assertTrue(ls.is_tail())
        self.assertTrue(ls.is_value())
        self.assertEqual(ls.get(), 3)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.OK)
        ls.right()
        self.assertEqual(ls.get_right_status(), self.List.RightStatus.NO_RIGHT_NEIGHBOR)


    def test_put_right(self):
        ls = self.List()
        ls.add_tail(1)
        ls.add_tail(2)
        ls.add_tail(3)
        ls.head()
        ls.put_right(4)
        self.check_content(ls, [1, 4, 2, 3])
        ls.head()
        ls.right()
        ls.put_right(5)
        self.check_content(ls, [1, 4, 5, 2, 3])
        ls.tail()
        ls.put_right(6)
        self.check_content(ls, [1, 4, 5, 2, 3, 6])


class Test_LinkedList(Test_List):
    
    List: Type[LinkedList] = LinkedList


class Test_TwoWayList(Test_List):
    List: Type[TwoWayList] = TwoWayList

    def check_nil_status(self, ls: ParentList):
        super().check_nil_status(ls)
        assert(isinstance(ls, TwoWayList))
        self.assertEqual(ls.get_left_status(), self.List.LeftStatus.NIL)

    def check_empty(self, ls: ParentList):
        super().check_empty(ls)
        assert(isinstance(ls, TwoWayList))
        ls.left()
        self.assertEqual(ls.get_left_status(), self.List.LeftStatus.NO_LEFT_NEIGHBOR)

    def test_single_left(self):
        ls = self.List()
        ls.add_tail(1)
        ls.left()
        self.assertEqual(ls.get_left_status(), self.List.LeftStatus.NO_LEFT_NEIGHBOR)

    def test_multi_left(self):
        ls = self.List()
        ls.add_tail(1)
        ls.add_tail(2)
        ls.add_tail(3)
        self.assertEqual(ls.size(), 3)
        self.assertTrue(ls.is_head())
        self.assertFalse(ls.is_tail())
        self.assertTrue(ls.is_value())
        ls.tail()
        self.assertEqual(ls.get_tail_status(), self.List.TailStatus.OK)
        self.assertFalse(ls.is_head())
        self.assertTrue(ls.is_tail())
        self.assertTrue(ls.is_value())

        self.assertEqual(ls.get(), 3)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.OK)
        ls.left()
        self.assertEqual(ls.get_left_status(), self.List.LeftStatus.OK)
        self.assertFalse(ls.is_head())
        self.assertFalse(ls.is_tail())
        self.assertTrue(ls.is_value())
        self.assertEqual(ls.get(), 2)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.OK)
        ls.left()
        self.assertEqual(ls.get_left_status(), self.List.LeftStatus.OK)
        self.assertTrue(ls.is_head())
        self.assertFalse(ls.is_tail())
        self.assertTrue(ls.is_value())
        self.assertEqual(ls.get(), 1)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.OK)
        ls.right()
        self.assertEqual(ls.get_right_status(), self.List.RightStatus.OK)
        self.assertFalse(ls.is_head())
        self.assertFalse(ls.is_tail())
        self.assertTrue(ls.is_value())
        self.assertEqual(ls.get(), 2)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.OK)
        ls.left()
        self.assertEqual(ls.get_left_status(), self.List.LeftStatus.OK)
        self.assertTrue(ls.is_head())
        self.assertFalse(ls.is_tail())
        self.assertTrue(ls.is_value())
        self.assertEqual(ls.get(), 1)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.OK)
        ls.left()
        self.assertEqual(ls.get_left_status(), self.List.LeftStatus.NO_LEFT_NEIGHBOR)


del Test_List

if __name__ == "__main__":
    unittest.main()
