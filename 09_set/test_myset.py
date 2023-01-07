import unittest
from typing import Any

from myset import MySet


class Test_MySet(unittest.TestCase):

    def check(self, s: MySet, pattern: set[Any]):
        self.assertEqual(s.get_count(), len(pattern))
        for v in pattern:
            self.assertTrue(s.contains(v))

    def make(self, pattern: set[Any]):
        s = MySet()
        for v in pattern:
            s.put(v)
            self.assertEqual(s.get_put_status(), MySet.PutStatus.OK)
        return s

    def test_put(self):
        s = MySet()
        self.assertEqual(s.get_put_status(), MySet.PutStatus.NIL)
        self.check(s, set())
        s.put(1)
        self.assertEqual(s.get_put_status(), MySet.PutStatus.OK)
        self.check(s, {1})
        s.put(2)
        self.assertEqual(s.get_put_status(), MySet.PutStatus.OK)
        self.check(s, {1, 2})
        s.put(2)
        self.assertEqual(s.get_put_status(), MySet.PutStatus.ALREADY_CONTAINS)
        self.check(s, {1, 2})

    def test_remove(self):
        s = MySet()
        self.assertEqual(s.get_delete_status(), MySet.DeleteStatus.NIL)
        s.delete(1)
        self.assertEqual(s.get_delete_status(), MySet.DeleteStatus.NOT_FOUND)
        s.put(1)
        self.check(s, {1})
        s.delete(1)
        self.assertEqual(s.get_delete_status(), MySet.DeleteStatus.OK)
        self.check(s, set())
        s.put(1)
        s.put(2)
        s.put(3)
        self.check(s, {1, 2, 3})
        s.delete(4)
        self.assertEqual(s.get_delete_status(), MySet.DeleteStatus.NOT_FOUND)
        s.delete(2)
        self.assertEqual(s.get_delete_status(), MySet.DeleteStatus.OK)
        self.check(s, {1, 3})

    def test_itersection(self):
        self.check(
            self.make(set()).intersection(
                self.make(set())),
            set())
        self.check(
            self.make({1, 2}).intersection(
                self.make(set())),
            set())
        self.check(
            self.make(set()).intersection(
                self.make({1, 2})),
            set())
        self.check(
            self.make({1}).intersection(
                self.make({1})),
            {1})
        self.check(
            self.make({1}).intersection(
                self.make({2})),
            set())
        self.check(
            self.make({1, 2}).intersection(
                self.make({1, 2})),
            {1, 2})
        self.check(
            self.make({1, 2}).intersection(
                self.make({3, 2})),
            {2})
        self.check(
            self.make({1, 3}).intersection(
                self.make({2, 4})),
            set())
        self.check(
            self.make({1, 2, 3, 4}).intersection(
                self.make({2, 3})),
            {2, 3})
        self.check(
            self.make({1, 2, 3, 4}).intersection(
                self.make({3, 4, 5})),
            {3, 4})

    def test_union(self):
        self.check(
            self.make(
                set()
                ).union(self.make(
                set()
                )),
            set()
        )
        self.check(
            self.make(
                {1, 2}
                ).union(self.make(
                set()
                )),
            {1, 2}
        )
        self.check(
            self.make(
                set()
                ).union(self.make(
                {1, 2}
                )),
            {1, 2}
        )
        self.check(
            self.make(
                {1, 2, 3}
                ).union(self.make(
                {1, 2}
                )),
            {1, 2, 3}
        )
        self.check(
            self.make(
                {1, 2}
                ).union(self.make(
                {1, 2, 3}
                )),
            {1, 2, 3}
        )
        self.check(
            self.make(
                {1, 2}
                ).union(self.make(
                {3, 4}
                )),
            {1, 2, 3, 4}
        )
        self.check(
            self.make(
                {3, 4}
                ).union(self.make(
                {1, 2}
                )),
            {1, 2, 3, 4}
        )

    def test_difference(self):
        self.check(
            self.make(
                set()
                ).difference(self.make(
                set()
                )),
            set()
        )
        self.check(
            self.make(
                {1, 2}
                ).difference(self.make(
                set()
                )),
            {1, 2}
        )
        self.check(
            self.make(
                set()
                ).difference(self.make(
                {1, 2}
                )),
            set()
        )
        self.check(
            self.make(
                {1}
                ).difference(self.make(
                {1}
                )),
            set()
        )
        self.check(
            self.make(
                {1, 2}
                ).difference(self.make(
                {1, 2}
                )),
            set()
        )
        self.check(
            self.make(
                {1, 2}
                ).difference(self.make(
                {3, 4}
                )),
            {1, 2}
        )
        self.check(
            self.make(
                {1, 2, 3, 4}
                ).difference(self.make(
                {2, 3}
                )),
            {1, 4}
        )
        self.check(
            self.make(
                {1, 2, 3, 4}
                ).difference(self.make(
                {2, 3, 5, 6}
                )),
            {1, 4}
        )

    def test_is_subset(self):
        self.assertTrue(self.make(set()).is_subset(self.make(set())))
        self.assertFalse(self.make(set()).is_subset(self.make({1})))
        self.assertTrue(self.make({1}).is_subset(self.make(set())))
        self.assertTrue(self.make({1}).is_subset(self.make({1})))
        self.assertFalse(self.make({1}).is_subset(self.make({2})))
        self.assertTrue(self.make({1, 2, 3}).is_subset(self.make({1, 2})))
        self.assertFalse(self.make({1, 2}).is_subset(self.make({1, 2, 3})))
        self.assertFalse(self.make({1, 2}).is_subset(self.make({3})))


if __name__ == "__main__":
    unittest.main()
