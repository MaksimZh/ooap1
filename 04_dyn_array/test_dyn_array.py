import unittest
from typing import Any

from dyn_array import DynArray

class Test(unittest.TestCase):

    def test_empty(self):
        a = DynArray()
        self.assertEqual(a.get_count(), 0)
        self.assertEqual(a.get_capacity(), DynArray.DEFAULT_CAPACITY)
        self.assertEqual(a.get_make_array_status(), DynArray.MakeArrayStatus.NIL)
        self.assertEqual(a.get_get_item_status(), DynArray.GetItemStatus.NIL)
        self.assertEqual(a.get_insert_status(), DynArray.InsertStatus.NIL)
        self.assertEqual(a.get_remove_status(), DynArray.RemoveStatus.NIL)
        a.get_item(0)
        self.assertEqual(a.get_get_item_status(), DynArray.GetItemStatus.INDEX_OUT_OF_RANGE)
        a.remove(0)
        self.assertEqual(a.get_remove_status(), DynArray.RemoveStatus.INDEX_OUT_OF_RANGE)

    def check(self, a: DynArray, values: list[Any]):
        self.assertEqual(a.get_count(), len(values))
        for i in range(len(values)):
            self.assertEqual(a.get_item(i), values[i])
            self.assertEqual(a.get_get_item_status(), DynArray.GetItemStatus.OK)
    
    def new_array(self, values: list[Any]) -> DynArray:
        a = DynArray()
        for v in values:
            a.append(v)
        return a
    
    def test_append_get(self):
        a = DynArray()
        a.append(1)
        self.assertEqual(a.get_count(), 1)
        self.assertEqual(a.get_item(0), 1)
        self.assertEqual(a.get_get_item_status(), DynArray.GetItemStatus.OK)
        a.get_item(1)
        self.assertEqual(a.get_get_item_status(), DynArray.GetItemStatus.INDEX_OUT_OF_RANGE)
        a.append(2)
        self.assertEqual(a.get_count(), 2)
        self.assertEqual(a.get_item(0), 1)
        self.assertEqual(a.get_get_item_status(), DynArray.GetItemStatus.OK)
        self.assertEqual(a.get_item(1), 2)
        self.assertEqual(a.get_get_item_status(), DynArray.GetItemStatus.OK)
        a.get_item(3)
        self.assertEqual(a.get_get_item_status(), DynArray.GetItemStatus.INDEX_OUT_OF_RANGE)
        a.append(3)
        self.assertEqual(a.get_count(), 3)
        self.assertEqual(a.get_item(0), 1)
        self.assertEqual(a.get_get_item_status(), DynArray.GetItemStatus.OK)
        self.assertEqual(a.get_item(1), 2)
        self.assertEqual(a.get_get_item_status(), DynArray.GetItemStatus.OK)
        self.assertEqual(a.get_item(2), 3)
        self.assertEqual(a.get_get_item_status(), DynArray.GetItemStatus.OK)
        a.get_item(4)
        self.assertEqual(a.get_get_item_status(), DynArray.GetItemStatus.INDEX_OUT_OF_RANGE)
        self.check(a, [1, 2, 3])

    def test_append_overflow(self):
        values = list(range(DynArray.DEFAULT_CAPACITY))
        a = self.new_array(values)
        self.assertEqual(a.get_capacity(), DynArray.DEFAULT_CAPACITY)
        a.append(42)
        self.check(a, values + [42])
        self.assertEqual(a.get_capacity(), int(DynArray.DEFAULT_CAPACITY * DynArray.EXTEND_FACTOR))

    def test_make_array(self):
        a = DynArray()
        self.assertEqual(a.get_capacity(), DynArray.DEFAULT_CAPACITY)
        self.check(a, [])
        a.make_array(0)
        self.assertEqual(a.get_make_array_status(), DynArray.MakeArrayStatus.BUFFER_TO_SHORT)
        self.assertEqual(a.get_capacity(), DynArray.DEFAULT_CAPACITY)
        self.check(a, [])
        a.make_array(10)
        self.assertEqual(a.get_make_array_status(), DynArray.MakeArrayStatus.OK)
        self.assertEqual(a.get_capacity(), 10)
        self.check(a, [])
        a.append(1)
        a.append(2)
        a.append(3)
        self.check(a, [1, 2, 3])
        a.make_array(4)
        self.assertEqual(a.get_make_array_status(), DynArray.MakeArrayStatus.OK)
        self.assertEqual(a.get_capacity(), 4)
        self.check(a, [1, 2, 3])
        a.make_array(10)
        self.assertEqual(a.get_make_array_status(), DynArray.MakeArrayStatus.OK)
        self.assertEqual(a.get_capacity(), 10)
        self.check(a, [1, 2, 3])
        a.make_array(2)
        self.assertEqual(a.get_make_array_status(), DynArray.MakeArrayStatus.BUFFER_TO_SHORT)
        self.assertEqual(a.get_capacity(), 10)
        self.check(a, [1, 2, 3])

    def test_insert(self):
        a = self.new_array([1, 2, 3])
        a.insert(4, 0)
        self.assertEqual(a.get_insert_status(), DynArray.InsertStatus.OK)
        self.check(a, [4, 1, 2, 3])
        a.insert(5, 2)
        self.assertEqual(a.get_insert_status(), DynArray.InsertStatus.OK)
        self.check(a, [4, 1, 5, 2, 3])
        a.insert(6, 5)
        self.assertEqual(a.get_insert_status(), DynArray.InsertStatus.OK)
        self.check(a, [4, 1, 5, 2, 3, 6])
        a.insert(7, -1)
        self.assertEqual(a.get_insert_status(), DynArray.InsertStatus.INDEX_OUT_OF_RANGE)
        self.check(a, [4, 1, 5, 2, 3, 6])
        a.insert(7, 7)
        self.assertEqual(a.get_insert_status(), DynArray.InsertStatus.INDEX_OUT_OF_RANGE)
        self.check(a, [4, 1, 5, 2, 3, 6])

    def test_insert_overflow(self):
        values = list(range(DynArray.DEFAULT_CAPACITY))
        a = self.new_array(values)
        self.assertEqual(a.get_capacity(), DynArray.DEFAULT_CAPACITY)
        a.insert(42, 0)
        self.assertEqual(a.get_insert_status(), DynArray.InsertStatus.OK)
        self.check(a, [42] + values)
        self.assertEqual(a.get_capacity(), int(DynArray.DEFAULT_CAPACITY * DynArray.EXTEND_FACTOR))

    def test_remove(self):
        a = self.new_array([1, 2, 3, 4, 5, 6, 7])
        a.remove(-1)
        self.assertEqual(a.get_remove_status(), DynArray.RemoveStatus.INDEX_OUT_OF_RANGE)
        self.check(a, [1, 2, 3, 4, 5, 6, 7])
        a.remove(7)
        self.assertEqual(a.get_remove_status(), DynArray.RemoveStatus.INDEX_OUT_OF_RANGE)
        self.check(a, [1, 2, 3, 4, 5, 6, 7])
        a.remove(0)
        self.assertEqual(a.get_remove_status(), DynArray.RemoveStatus.OK)
        self.check(a, [2, 3, 4, 5, 6, 7])
        a.remove(2)
        self.assertEqual(a.get_remove_status(), DynArray.RemoveStatus.OK)
        self.check(a, [2, 3, 5, 6, 7])
        a.remove(4)
        self.assertEqual(a.get_remove_status(), DynArray.RemoveStatus.OK)
        self.check(a, [2, 3, 5, 6])

    def test_remove_underflow(self):
        values = list(range(int(DynArray.DEFAULT_CAPACITY * DynArray.EXTEND_FACTOR) + 1))
        a = self.new_array(values)
        capacity = a.get_capacity()
        num_of_removes = a.get_count() - int(capacity * DynArray.SHRINK_THRESHOLD_FACTOR) + 1
        for _ in range(num_of_removes - 1):
            a.remove(0)
            self.assertEqual(a.get_remove_status(), DynArray.RemoveStatus.OK)
        self.assertEqual(a.get_capacity(), capacity)
        a.remove(0)
        self.assertEqual(a.get_remove_status(), DynArray.RemoveStatus.OK)
        self.assertEqual(a.get_capacity(), int(capacity / DynArray.SHRINK_DIVISOR))
        self.check(a, values[num_of_removes:])
        capacity = a.get_capacity()
        num_of_removes_2 = a.get_count() - int(DynArray.DEFAULT_CAPACITY * DynArray.SHRINK_THRESHOLD_FACTOR) + 1
        for _ in range(num_of_removes_2 - 1):
            a.remove(0)
            self.assertEqual(a.get_remove_status(), DynArray.RemoveStatus.OK)
        a.remove(0)
        self.assertEqual(a.get_remove_status(), DynArray.RemoveStatus.OK)
        self.assertEqual(a.get_capacity(), DynArray.DEFAULT_CAPACITY)
        self.check(a, values[num_of_removes + num_of_removes_2 :])


if __name__ == "__main__":
    unittest.main()
