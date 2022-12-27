import unittest
from typing import Any

import queues


class Test(unittest.TestCase):

    Queue = queues.Queue

    def check_empty(self, q: queues.ParentQueue):
        self.assertEqual(q.get_size(), 0)
        q.get_front()
        self.assertEqual(q.get_get_front_status(), self.Queue.GetFrontStatus.EMPTY)
        q.pop_front()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.EMPTY)

    def check_full(self, q: queues.ParentQueue, values: list[Any]):
        self.assertEqual(q.get_size(), len(values))
        self.assertEqual(q.get_front(), values[0])
        self.assertEqual(q.get_get_front_status(), self.Queue.GetFrontStatus.OK)

    def test_empty(self):
        q = self.Queue()
        self.assertEqual(q.get_get_front_status(), self.Queue.GetFrontStatus.NIL)
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.NIL)
        self.check_empty(q)

    def test_one(self):
        q = self.Queue()
        q.put_tail(1)
        self.check_full(q, [1])
        q.pop_front()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_empty(q)

    def test_multi(self):
        q = self.Queue()
        q.put_tail(1)
        self.check_full(q, [1])
        q.put_tail(2)
        self.check_full(q, [1, 2])
        q.put_tail(3)
        self.check_full(q, [1, 2, 3])
        q.pop_front()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_full(q, [2, 3])
        q.pop_front()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_full(q, [3])
        q.pop_front()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_empty(q)


class Test_Deque(Test):

    Queue = queues.Deque

    def check_empty(self, q: queues.ParentQueue):
        assert(isinstance(q, queues.Deque))
        super().check_empty(q)
        q.get_tail()
        self.assertEqual(q.get_get_tail_status(), self.Queue.GetTailStatus.EMPTY)
        q.pop_tail()
        self.assertEqual(q.get_pop_tail_status(), self.Queue.PopTailStatus.EMPTY)

    def check_full(self, q: queues.ParentQueue, values: list[Any]):
        assert(isinstance(q, queues.Deque))
        super().check_full(q, values)
        self.assertEqual(q.get_tail(), values[-1])
        self.assertEqual(q.get_get_tail_status(), self.Queue.GetTailStatus.OK)

    def test_empty_ext(self):
        q = self.Queue()
        self.assertEqual(q.get_get_tail_status(), self.Queue.GetTailStatus.NIL)
        self.assertEqual(q.get_pop_tail_status(), self.Queue.PopTailStatus.NIL)
        self.check_empty(q)

    def test_one_ext(self):
        q = self.Queue()
        q.put_front(1)
        self.assertEqual(q.get_size(), 1)
        self.check_full(q, [1])
        q.pop_tail()
        self.assertEqual(q.get_pop_tail_status(), self.Queue.PopTailStatus.OK)
        self.check_empty(q)
        q.put_front(1)
        q.pop_front()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_empty(q)
        q.put_tail(1)
        q.pop_tail()
        self.assertEqual(q.get_pop_tail_status(), self.Queue.PopTailStatus.OK)
        self.check_empty(q)

    def test_multi_back(self):
        q = self.Queue()
        q.put_front(1)
        self.check_full(q, [1])
        q.put_front(2)
        self.check_full(q, [2, 1])
        q.put_front(3)
        self.check_full(q, [3, 2, 1])
        q.pop_tail()
        self.assertEqual(q.get_pop_tail_status(), self.Queue.PopTailStatus.OK)
        self.check_full(q, [3, 2])
        q.pop_tail()
        self.assertEqual(q.get_pop_tail_status(), self.Queue.PopTailStatus.OK)
        self.check_full(q, [3])
        q.pop_tail()
        self.assertEqual(q.get_pop_tail_status(), self.Queue.PopTailStatus.OK)
        self.check_empty(q)

    def test_multi_stack(self):
        q = self.Queue()
        q.put_tail(1)
        self.check_full(q, [1])
        q.put_tail(2)
        self.check_full(q, [1, 2])
        q.put_tail(3)
        self.check_full(q, [1, 2, 3])
        q.pop_tail()
        self.assertEqual(q.get_pop_tail_status(), self.Queue.PopTailStatus.OK)
        self.check_full(q, [1, 2])
        q.pop_tail()
        self.assertEqual(q.get_pop_tail_status(), self.Queue.PopTailStatus.OK)
        self.check_full(q, [1])
        q.pop_tail()
        self.assertEqual(q.get_pop_tail_status(), self.Queue.PopTailStatus.OK)
        self.check_empty(q)

    def test_multi_back_stack(self):
        q = self.Queue()
        q.put_front(1)
        q.put_front(2)
        q.put_front(3)
        q.pop_front()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_full(q, [2, 1])
        q.pop_front()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_full(q, [1])
        q.pop_front()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_empty(q)

    def test_mix(self):
        q = self.Queue()
        q.put_front(1)
        self.check_full(q, [1])
        q.put_tail(2)
        self.check_full(q, [1, 2])
        q.put_tail(3)
        self.check_full(q, [1, 2, 3])
        q.put_front(4)
        self.check_full(q, [4, 1, 2, 3])
        q.put_front(5)
        self.check_full(q, [5, 4, 1, 2, 3])
        q.pop_front()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_full(q, [4, 1, 2, 3])
        q.pop_tail()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_full(q, [4, 1, 2])
        q.put_front(6)
        self.check_full(q, [6, 4, 1, 2])
        q.put_tail(7)
        self.check_full(q, [6, 4, 1, 2, 7])
        q.pop_front()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_full(q, [4, 1, 2, 7])
        q.pop_tail()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_full(q, [4, 1, 2])
        q.pop_front()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_full(q, [1, 2])
        q.pop_tail()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_full(q, [1])
        q.pop_tail()
        self.assertEqual(q.get_pop_front_status(), self.Queue.PopFrontStatus.OK)
        self.check_empty(q)


if __name__ == "__main__":
    unittest.main()
