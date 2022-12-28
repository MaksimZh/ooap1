import unittest
from typing import Any

from hash_table import HashTable, HashBuffer, Buffer
EMPTY = Buffer.CellState.EMPTY
DELETED = Buffer.CellState.DELETED
VALUE = Buffer.CellState.VALUE


class Test_Buffer(unittest.TestCase):

    def check(self, buffer: Buffer, pattern: list[Any]):
        self.assertEqual(buffer.get_capacity(), len(pattern))
        count: int = 0
        for i in range(len(pattern)):
            if pattern[i] == EMPTY:
                self.assertEqual(buffer.get_cell_state(i), EMPTY)
                continue
            if pattern[i] == DELETED:
                self.assertEqual(buffer.get_cell_state(i), DELETED)
                continue
            self.assertEqual(buffer.get_cell_state(i), VALUE)
            count += 1
            self.assertEqual(buffer.get(i), pattern[i])
        
    def test_empty(self):
        b = Buffer(5)
        self.assertEqual(b.get_put_status(), Buffer.PutStatus.NIL)
        self.assertEqual(b.get_get_cell_state_status(), Buffer.GetCellStateStauts.NIL)
        self.check(b, [EMPTY] * 5)

    def test_put(self):
        b = Buffer(5)
        b.put(0, "a")
        self.assertEqual(b.get_put_status(), Buffer.PutStatus.OK)
        self.check(b, ["a", EMPTY, EMPTY, EMPTY, EMPTY])
        b.put(2, "b")
        self.assertEqual(b.get_put_status(), Buffer.PutStatus.OK)
        self.check(b, ["a", EMPTY, "b", EMPTY, EMPTY])
        b.put(4, "c")
        self.assertEqual(b.get_put_status(), Buffer.PutStatus.OK)
        self.check(b, ["a", EMPTY, "b", EMPTY, "c"])
        b.put(-1, "z")
        self.assertEqual(b.get_put_status(), Buffer.PutStatus.INDEX_OUT_OF_RANGE)
        b.put(5, "z")
        self.assertEqual(b.get_put_status(), Buffer.PutStatus.INDEX_OUT_OF_RANGE)
        b.put(-42, "z")
        self.assertEqual(b.get_put_status(), Buffer.PutStatus.INDEX_OUT_OF_RANGE)
        b.put(42, "z")
        self.assertEqual(b.get_put_status(), Buffer.PutStatus.INDEX_OUT_OF_RANGE)
        b.put(2, "z")
        self.assertEqual(b.get_put_status(), Buffer.PutStatus.ALREADY_HAS_VALUE)
        self.check(b, ["a", EMPTY, "b", EMPTY, "c"])


class Test_HashBuffer(unittest.TestCase):

    def test(self):
        b = HashBuffer(5)
        self.assertEqual(b.get_count(), 0)


class Test_HashTable(unittest.TestCase):

    def check(self, table: HashTable, values: list[Any]):
        self.assertEqual(table.get_count(), len(values))
        for v in values:
            self.assertTrue(table.contains(v))

    def test_empty(self):
        h = HashTable(5)
        self.check(h, [])
        self.assertEqual(h.get_remove_status(), HashTable.RemoveStatus.NIL)
        self.assertFalse(h.contains(1))
        h.remove(1)
        self.assertEqual(h.get_remove_status(), HashTable.RemoveStatus.NOT_FOUND)

    def test_fill(self):
        h = HashTable(5)
        self.check(h, [])
        h.add(1)
        #self.check(h, [1])


if __name__ == "__main__":
    unittest.main()
