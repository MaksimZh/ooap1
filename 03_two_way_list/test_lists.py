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
        self.assertEqual(ls.size(), len(values))
        ls.head()
        content = []
        while not ls.is_tail():
            content.append(ls.get())
            ls.right()
        content.append(ls.get())
        self.assertEqual(content, values)

    def new_list(self, values: list[Any]):
        ls = self.List()
        for v in values:
            ls.add_tail(v)
        return ls

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
        self.assertEqual(ls.get(), 1)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.OK)
        ls.tail()
        self.assertEqual(ls.get_tail_status(), self.List.TailStatus.OK)
        self.assertFalse(ls.is_head())
        self.assertTrue(ls.is_tail())
        self.assertTrue(ls.is_value())
        self.assertEqual(ls.get(), 3)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.OK)
        ls.head()
        self.assertEqual(ls.get_head_status(), self.List.HeadStatus.OK)
        self.assertTrue(ls.is_head())
        self.assertFalse(ls.is_tail())
        self.assertTrue(ls.is_value())
        self.assertEqual(ls.get(), 1)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.OK)

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
        ls = self.new_list([1, 2, 3])
        ls.head()
        ls.put_right(4)
        self.assertEqual(ls.get_put_right_status(), self.List.PutRightStatus.OK)
        self.check_content(ls, [1, 4, 2, 3])
        ls.head()
        ls.right()
        ls.put_right(5)
        self.assertEqual(ls.get_put_right_status(), self.List.PutRightStatus.OK)
        self.check_content(ls, [1, 4, 5, 2, 3])
        ls.tail()
        ls.put_right(6)
        self.assertEqual(ls.get_put_right_status(), self.List.PutRightStatus.OK)
        self.check_content(ls, [1, 4, 5, 2, 3, 6])


    def test_put_left(self):
        ls = self.new_list([1, 2, 3])
        ls.head()
        ls.put_left(4)
        self.assertEqual(ls.get_put_left_status(), self.List.PutLeftStatus.OK)
        self.check_content(ls, [4, 1, 2, 3])
        ls.head()
        ls.right()
        ls.put_left(5)
        self.assertEqual(ls.get_put_left_status(), self.List.PutLeftStatus.OK)
        self.check_content(ls, [4, 5, 1, 2, 3])
        ls.tail()
        ls.put_left(6)
        self.assertEqual(ls.get_put_left_status(), self.List.PutLeftStatus.OK)
        self.check_content(ls, [4, 5, 1, 2, 6, 3])

    
    def test_remove(self):
        ls = self.new_list([1, 2, 3, 4, 5])
        ls.head()
        ls.remove()
        self.assertEqual(ls.get(), 2)
        self.check_content(ls, [2, 3, 4, 5])
        ls.head()
        ls.right()
        ls.remove()
        self.assertEqual(ls.get(), 4)
        self.check_content(ls, [2, 4, 5])
        ls.tail()
        ls.remove()
        self.assertEqual(ls.get(), 4)
        self.check_content(ls, [2, 4])
        ls.remove()
        ls.remove()
        self.check_empty(ls)

    
    def test_find(self):
        ls = self.new_list([2, 1, 2, 3, 2, 2, 4, 2])
        ls.head()
        ls.find(6)
        self.assertEqual(ls.get_find_status(), self.List.FindStatus.NOT_FOUND)
        for _ in range(4):
            ls.find(2)
            self.assertEqual(ls.get_find_status(), self.List.FindStatus.OK)
            ls.right()
            self.assertEqual(ls.get_right_status(), self.List.RightStatus.OK)
        ls.find(2)
        self.assertEqual(ls.get_find_status(), self.List.FindStatus.OK)
        self.assertTrue(ls.is_tail())


    def test_remove_all(self):
        ls = self.new_list([2, 1, 2, 3, 2, 2, 4, 2])
        ls.remove_all(2)
        self.check_content(ls, [1, 3, 4])
        ls.remove_all(2)
        self.check_content(ls, [1, 3, 4])


    def test_replace(self):
        ls = self.new_list([1])
        ls.replace(2)
        self.assertEqual(ls.get_replace_status(), self.List.ReplaceStatus.OK)
        self.check_content(ls, [2])
        ls = self.new_list([1, 2, 3, 4, 5])
        ls.head()
        ls.replace(6)
        self.assertEqual(ls.get_replace_status(), self.List.ReplaceStatus.OK)
        self.check_content(ls, [6, 2, 3, 4, 5])
        ls.head()
        ls.right()
        ls.right()
        ls.replace(7)
        self.assertEqual(ls.get_replace_status(), self.List.ReplaceStatus.OK)
        self.check_content(ls, [6, 2, 7, 4, 5])
        ls.tail()
        ls.replace(8)
        self.assertEqual(ls.get_replace_status(), self.List.ReplaceStatus.OK)
        self.check_content(ls, [6, 2, 7, 4, 8])


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
        self.assertEqual(ls.get(), 1)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.OK)
        ls.tail()
        self.assertEqual(ls.get_tail_status(), self.List.TailStatus.OK)
        self.assertFalse(ls.is_head())
        self.assertTrue(ls.is_tail())
        self.assertTrue(ls.is_value())
        self.assertEqual(ls.get(), 3)
        self.assertEqual(ls.get_get_status(), self.List.GetStatus.OK)

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
