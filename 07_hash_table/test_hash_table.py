import unittest
from typing import Any

from hash_table import HashTable, HashIterator, Buffer
EMPTY = Buffer.CellState.EMPTY
DELETED = Buffer.CellState.DELETED
VALUE = Buffer.CellState.VALUE


class Test_Buffer(unittest.TestCase):

    def check(self, buffer: Buffer, pattern: list[Any]):
        self.assertEqual(buffer.get_capacity(), len(pattern))
        count: int = 0
        for i in range(len(pattern)):
            cell_state = buffer.get_cell_state(i)
            self.assertEqual(buffer.get_get_cell_state_status(),
                Buffer.GetCellStateStauts.OK)
            if pattern[i] == EMPTY:
                self.assertEqual(cell_state, EMPTY)
                continue
            if pattern[i] == DELETED:
                self.assertEqual(cell_state, DELETED)
                continue
            self.assertEqual(cell_state, VALUE)
            count += 1
            self.assertEqual(buffer.get(i), pattern[i])
        
    def test_empty(self):
        b = Buffer(5)
        self.assertEqual(b.get_put_status(), Buffer.PutStatus.NIL)
        self.assertEqual(b.get_delete_status(), Buffer.DeleteStatus.NIL)
        self.assertEqual(b.get_get_cell_state_status(), Buffer.GetCellStateStauts.NIL)
        self.check(b, [EMPTY] * 5)
        b.get_cell_state(-1)
        self.assertEqual(b.get_get_cell_state_status(),
            Buffer.GetCellStateStauts.INDEX_OUT_OF_RANGE)
        b.get_cell_state(5)
        self.assertEqual(b.get_get_cell_state_status(),
            Buffer.GetCellStateStauts.INDEX_OUT_OF_RANGE)
        b.get_cell_state(-42)
        self.assertEqual(b.get_get_cell_state_status(),
            Buffer.GetCellStateStauts.INDEX_OUT_OF_RANGE)
        b.get_cell_state(42)
        self.assertEqual(b.get_get_cell_state_status(),
            Buffer.GetCellStateStauts.INDEX_OUT_OF_RANGE)

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
        b.put(1, "d")
        self.assertEqual(b.get_put_status(), Buffer.PutStatus.OK)
        b.put(3, "e")
        self.assertEqual(b.get_put_status(), Buffer.PutStatus.OK)
        self.check(b, ["a", "d", "b", "e", "c"])

    def test_delete(self):
        b = Buffer(5)
        b.put(0, "a")
        b.put(2, "b")
        b.put(4, "c")
        self.check(b, ["a", EMPTY, "b", EMPTY, "c"])
        b.delete(0)
        self.assertEqual(b.get_delete_status(), Buffer.DeleteStatus.OK)
        self.check(b, [DELETED, EMPTY, "b", EMPTY, "c"])
        b.delete(2)
        self.assertEqual(b.get_delete_status(), Buffer.DeleteStatus.OK)
        self.check(b, [DELETED, EMPTY, DELETED, EMPTY, "c"])
        b.delete(4)
        self.assertEqual(b.get_delete_status(), Buffer.DeleteStatus.OK)
        self.check(b, [DELETED, EMPTY, DELETED, EMPTY, DELETED])
        b.delete(-1)
        self.assertEqual(b.get_delete_status(), Buffer.DeleteStatus.INDEX_OUT_OF_RANGE)
        b.delete(5)
        self.assertEqual(b.get_delete_status(), Buffer.DeleteStatus.INDEX_OUT_OF_RANGE)
        b.delete(-42)
        self.assertEqual(b.get_delete_status(), Buffer.DeleteStatus.INDEX_OUT_OF_RANGE)
        b.delete(42)
        self.assertEqual(b.get_delete_status(), Buffer.DeleteStatus.INDEX_OUT_OF_RANGE)
        b.delete(1)
        self.assertEqual(b.get_delete_status(), Buffer.DeleteStatus.NO_VALUE)
        b.delete(2)
        self.assertEqual(b.get_delete_status(), Buffer.DeleteStatus.NO_VALUE)


class Test_HashIterator(unittest.TestCase):

    def check_once(self):
        size = 17
        limit = 12
        hi = HashIterator(size, limit)
        self.assertEqual(hi.get_get_index_status(), HashIterator.GetIndexStatus.NIL)
        self.assertEqual(hi.get_next_status(), HashIterator.NextStatus.NIL)
        hi.next()
        self.assertEqual(hi.get_next_status(), HashIterator.NextStatus.NOT_STARTED)
        hi.get_index()
        self.assertEqual(hi.get_get_index_status(), HashIterator.GetIndexStatus.NOT_STARTED)
        hi.start("a")
        i = hi.get_index()
        self.assertEqual(hi.get_get_index_status(), HashIterator.GetIndexStatus.OK)
        self.assertGreaterEqual(i, 0)
        self.assertLess(i, size)
        indices: set[int] = set([i])
        for _ in range(limit - 1):
            hi.next()
            self.assertEqual(hi.get_next_status(), HashIterator.NextStatus.OK)
            i = hi.get_index()
            self.assertEqual(hi.get_get_index_status(), HashIterator.GetIndexStatus.OK)
            self.assertGreaterEqual(i, 0)
            self.assertLess(i, size)
            self.assertNotIn(i, indices)
            indices.add(i)
        hi.next()
        self.assertEqual(hi.get_next_status(), HashIterator.NextStatus.LIMIT_REACHED)
        hi.get_index()
        self.assertEqual(hi.get_get_index_status(), HashIterator.GetIndexStatus.LIMIT_REACHED)

    def test(self):
        for _ in range(100):
            self.check_once()


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
