import unittest
from typing import Any

from dyn_array import DynArray

class Test(unittest.TestCase):

    def test_empty(self):
        a = DynArray()
        self.assertEqual(a.get_count(), 0)
        self.assertEqual(a.get_capacity(), DynArray.DEFAULT_CAPACITY)
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

    def test_make_array(self):
        pass


if __name__ == "__main__":
    unittest.main()
