import unittest
from typing import Any

from hash_table import HashTable, HashBuffer, HashIterator, Buffer, PrimeScales, PrimeTester
EMPTY = Buffer.CellState.EMPTY
DELETED = Buffer.CellState.DELETED
VALUE = Buffer.CellState.VALUE


class Test_Buffer(unittest.TestCase):

    def check(self, buffer: Buffer, pattern: list[Any]):
        self.assertEqual(buffer.get_capacity(), len(pattern))
        count: int = 0
        for i in range(len(pattern)):
            cell_state = buffer.get_cell_state(i)
            value = buffer.get(i)
            self.assertEqual(buffer.get_get_cell_state_status(),
                Buffer.GetCellStateStatus.OK)
            if pattern[i] == EMPTY:
                self.assertEqual(cell_state, EMPTY)
                self.assertEqual(buffer.get_get_status(), Buffer.GetStatus.NO_VALUE)
                continue
            if pattern[i] == DELETED:
                self.assertEqual(cell_state, DELETED)
                self.assertEqual(buffer.get_get_status(), Buffer.GetStatus.NO_VALUE)
                continue
            self.assertEqual(cell_state, VALUE)
            count += 1
            self.assertEqual(value, pattern[i])
            self.assertEqual(buffer.get_get_status(), Buffer.GetStatus.OK)
        
    def test_empty(self):
        b = Buffer(5)
        self.assertEqual(b.get_put_status(), Buffer.PutStatus.NIL)
        self.assertEqual(b.get_delete_status(), Buffer.DeleteStatus.NIL)
        self.assertEqual(b.get_get_cell_state_status(), Buffer.GetCellStateStatus.NIL)
        self.assertEqual(b.get_get_status(), Buffer.GetStatus.NIL)
        self.check(b, [EMPTY] * 5)
        b.get_cell_state(-1)
        self.assertEqual(b.get_get_cell_state_status(),
            Buffer.GetCellStateStatus.INDEX_OUT_OF_RANGE)
        b.get_cell_state(5)
        self.assertEqual(b.get_get_cell_state_status(),
            Buffer.GetCellStateStatus.INDEX_OUT_OF_RANGE)
        b.get_cell_state(-42)
        self.assertEqual(b.get_get_cell_state_status(),
            Buffer.GetCellStateStatus.INDEX_OUT_OF_RANGE)
        b.get_cell_state(42)
        self.assertEqual(b.get_get_cell_state_status(),
            Buffer.GetCellStateStatus.INDEX_OUT_OF_RANGE)
        b.get(-1)
        self.assertEqual(b.get_get_status(),
            Buffer.GetStatus.INDEX_OUT_OF_RANGE)
        b.get(5)
        self.assertEqual(b.get_get_status(),
            Buffer.GetStatus.INDEX_OUT_OF_RANGE)
        b.get(-42)
        self.assertEqual(b.get_get_status(),
            Buffer.GetStatus.INDEX_OUT_OF_RANGE)
        b.get(42)
        self.assertEqual(b.get_get_status(),
            Buffer.GetStatus.INDEX_OUT_OF_RANGE)

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
        self.assertEqual(hi.is_index_valid(), False)
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
            self.assertEqual(hi.is_index_valid(), True)
            hi.next()
            self.assertEqual(hi.get_next_status(), HashIterator.NextStatus.OK)
            i = hi.get_index()
            self.assertEqual(hi.get_get_index_status(), HashIterator.GetIndexStatus.OK)
            self.assertGreaterEqual(i, 0)
            self.assertLess(i, size)
            self.assertNotIn(i, indices)
            indices.add(i)
        hi.next()
        self.assertEqual(hi.is_index_valid(), False)
        self.assertEqual(hi.get_next_status(), HashIterator.NextStatus.LIMIT_REACHED)
        hi.get_index()
        self.assertEqual(hi.get_get_index_status(), HashIterator.GetIndexStatus.LIMIT_REACHED)

    def test(self):
        for _ in range(100):
            self.check_once()


class Test_HashBuffer(unittest.TestCase):

    def test(self):
        hb = HashBuffer(5, 3)
        ia = hb.find_cell("a")
        self.assertEqual(hb.get_find_cell_status(), HashBuffer.FindCellStatus.VACANCY_FOUND)
        hb.put(ia, "a")
        ib = hb.find_cell("b")
        self.assertNotEqual(ib, ia)
        self.assertEqual(hb.get_find_cell_status(), HashBuffer.FindCellStatus.VACANCY_FOUND)
        hb.put(ib, "b")
        self.assertEqual(hb.find_cell("a"), ia)
        self.assertEqual(hb.get_find_cell_status(), HashBuffer.FindCellStatus.VALUE_FOUND)
        self.assertEqual(hb.find_cell("b"), ib)
        self.assertEqual(hb.get_find_cell_status(), HashBuffer.FindCellStatus.VALUE_FOUND)
        for i in set(range(5)).difference({ia, ib}):
            hb.put(i, i)
        hb.find_cell("c")
        self.assertEqual(hb.get_find_cell_status(), HashBuffer.FindCellStatus.LIMIT_REACHED)


class Test_PrimeTester(unittest.TestCase):

    def test(self):
        pt = PrimeTester()
        self.assertTrue(pt.is_prime(2))
        self.assertTrue(pt.is_prime(3))
        self.assertTrue(pt.is_prime(5))
        self.assertTrue(pt.is_prime(43))
        self.assertTrue(pt.is_prime(53))
        self.assertTrue(pt.is_prime(2017))
        self.assertFalse(pt.is_prime(6))
        self.assertFalse(pt.is_prime(14))
        self.assertFalse(pt.is_prime(56))
        self.assertFalse(pt.is_prime(128))
        self.assertFalse(pt.is_prime(4002))


class Test_PrimeScales(unittest.TestCase):

    def test(self):
        pp = PrimeScales(24, scale_factor=2, min_value=11)
        self.assertEqual(pp.get(), 29)
        pp.scale_down()
        self.assertEqual(pp.get_scale_down_status(), PrimeScales.ScaleDownStatus.OK)
        self.assertEqual(pp.get(), 17)
        pp.scale_down()
        self.assertEqual(pp.get_scale_down_status(), PrimeScales.ScaleDownStatus.OK)
        self.assertEqual(pp.get(), 11)
        pp.scale_down()
        self.assertEqual(pp.get_scale_down_status(), PrimeScales.ScaleDownStatus.MINIMAL)
        self.assertEqual(pp.get(), 11)
        pp.scale_up()
        self.assertEqual(pp.get(), 17)
        pp.scale_up()
        self.assertEqual(pp.get(), 29)
        pp.scale_up()
        self.assertEqual(pp.get(), 59)
        pp.scale_up()
        self.assertEqual(pp.get(), 127)
        pp.scale_up()
        self.assertEqual(pp.get(), 257)
        pp.scale_down()
        self.assertEqual(pp.get_scale_down_status(), PrimeScales.ScaleDownStatus.OK)
        self.assertEqual(pp.get(), 127)
        pp.scale_down()
        self.assertEqual(pp.get_scale_down_status(), PrimeScales.ScaleDownStatus.OK)
        self.assertEqual(pp.get(), 59)
        pp.scale_down()
        self.assertEqual(pp.get_scale_down_status(), PrimeScales.ScaleDownStatus.OK)
        self.assertEqual(pp.get(), 29)
        pp.scale_down()
        self.assertEqual(pp.get_scale_down_status(), PrimeScales.ScaleDownStatus.OK)
        self.assertEqual(pp.get(), 17)
        pp.scale_down()
        self.assertEqual(pp.get_scale_down_status(), PrimeScales.ScaleDownStatus.OK)
        self.assertEqual(pp.get(), 11)



class Test_HashTable(unittest.TestCase):

    def check(self, table: HashTable, values: set[Any]):
        self.assertEqual(table.get_count(), len(values))
        for v in values:
            self.assertTrue(table.contains(v))

    def test_empty(self):
        h = HashTable(5)
        self.check(h, set())
        self.assertEqual(h.get_add_status(), HashTable.AddStatus.NIL)
        self.assertEqual(h.get_remove_status(), HashTable.RemoveStatus.NIL)
        self.assertFalse(h.contains(1))
        h.remove(1)
        self.assertEqual(h.get_remove_status(), HashTable.RemoveStatus.NOT_FOUND)

    def test_fill(self):
        h = HashTable(3)
        self.check(h, set())
        h.add("a")
        self.assertEqual(h.get_add_status(), HashTable.AddStatus.OK)
        self.check(h, {"a"})
        h.add("b")
        self.assertEqual(h.get_add_status(), HashTable.AddStatus.OK)
        self.check(h, {"a", "b"})
        h.add("a")
        self.assertEqual(h.get_add_status(), HashTable.AddStatus.ALREADY_CONTAINS)
        self.check(h, {"a", "b"})
        h.add("c")
        self.assertEqual(h.get_add_status(), HashTable.AddStatus.OK)
        self.check(h, {"a", "b", "c"})
        h.add("d")
        self.assertEqual(h.get_add_status(), HashTable.AddStatus.OK)
        self.check(h, {"a", "b", "c", "d"})
        h.add("e")
        self.assertEqual(h.get_add_status(), HashTable.AddStatus.OK)
        self.check(h, {"a", "b", "c", "d", "e"})
        for i in range(10000):
            h.add(i)
            self.assertEqual(h.get_add_status(), HashTable.AddStatus.OK)
            self.assertTrue(h.contains(i))


if __name__ == "__main__":
    unittest.main()
