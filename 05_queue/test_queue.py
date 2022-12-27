import unittest

from my_queue import Queue

class Test(unittest.TestCase):

    def test_empty(self):
        q = Queue()
        self.assertEqual(q.get_size(), 0)
        self.assertEqual(q.get_dequeue_status(), Queue.DequeueStatus.NIL)
        self.assertEqual(q.get_get_status(), Queue.GetStatus.NIL)
        q.dequeue()
        self.assertEqual(q.get_dequeue_status(), Queue.DequeueStatus.EMPTY)
        q.get()
        self.assertEqual(q.get_get_status(), Queue.GetStatus.EMPTY)

    def test_one(self):
        q = Queue()
        q.enqueue(1)
        self.assertEqual(q.get_size(), 1)
        self.assertEqual(q.get(), 1)
        self.assertEqual(q.get_get_status(), Queue.GetStatus.OK)
        q.dequeue()
        self.assertEqual(q.get_dequeue_status(), Queue.DequeueStatus.OK)
        self.assertEqual(q.get_size(), 0)
        q.get()
        self.assertEqual(q.get_get_status(), Queue.GetStatus.EMPTY)
        q.dequeue()
        self.assertEqual(q.get_dequeue_status(), Queue.DequeueStatus.EMPTY)

    def test_multi(self):
        q = Queue()
        q.enqueue(1)
        self.assertEqual(q.get_size(), 1)
        self.assertEqual(q.get(), 1)
        self.assertEqual(q.get_get_status(), Queue.GetStatus.OK)
        q.enqueue(2)
        self.assertEqual(q.get_size(), 2)
        self.assertEqual(q.get(), 1)
        self.assertEqual(q.get_get_status(), Queue.GetStatus.OK)
        q.enqueue(3)
        self.assertEqual(q.get_size(), 3)
        self.assertEqual(q.get(), 1)
        self.assertEqual(q.get_get_status(), Queue.GetStatus.OK)
        q.dequeue()
        self.assertEqual(q.get_dequeue_status(), Queue.DequeueStatus.OK)
        self.assertEqual(q.get_size(), 2)
        self.assertEqual(q.get(), 2)
        self.assertEqual(q.get_get_status(), Queue.GetStatus.OK)
        q.dequeue()
        self.assertEqual(q.get_dequeue_status(), Queue.DequeueStatus.OK)
        self.assertEqual(q.get_size(), 1)
        self.assertEqual(q.get(), 3)
        self.assertEqual(q.get_get_status(), Queue.GetStatus.OK)
        q.dequeue()
        self.assertEqual(q.get_dequeue_status(), Queue.DequeueStatus.OK)
        self.assertEqual(q.get_size(), 0)
        q.get()
        self.assertEqual(q.get_get_status(), Queue.GetStatus.EMPTY)
        q.dequeue()
        self.assertEqual(q.get_dequeue_status(), Queue.DequeueStatus.EMPTY)



if __name__ == "__main__":
    unittest.main()
