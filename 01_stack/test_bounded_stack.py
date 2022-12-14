import unittest

from bounded_stack import BoundedStack

class Test(unittest.TestCase):

    def test_init(self):
        _ = BoundedStack(16)
        _ = BoundedStack()

    def test_max_size(self):
        s = BoundedStack(3)
        for _ in range(3):
            s.push(1)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_OK)
        s.push(1)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_ERR)

        s = BoundedStack()
        for _ in range(32):
            s.push(1)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_OK)
        s.push(1)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_ERR)

    def test_empty(self):
        s = BoundedStack(3)
        self.assertEqual(s.size(), 0)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_NIL)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_NIL)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_NIL)
        v = s.peek()
        self.assertEqual(v, 0)
        self.assertEqual(s.size(), 0)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_NIL)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_NIL)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_ERR)
        s.pop()
        self.assertEqual(s.size(), 0)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_NIL)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_ERR)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_ERR)
    
    def test_one(self):
        s = BoundedStack(3)
        s.push(1)
        self.assertEqual(s.size(), 1)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_OK)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_NIL)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_NIL)
        v = s.peek()
        self.assertEqual(v, 1)
        self.assertEqual(s.size(), 1)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_OK)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_NIL)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_OK)
        s.pop()
        self.assertEqual(s.size(), 0)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_OK)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_OK)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_OK)

    def test_full(self):
        s = BoundedStack(3)
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.size(), 3)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_OK)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_NIL)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_NIL)
        v = s.peek()
        self.assertEqual(v, 3)
        self.assertEqual(s.size(), 3)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_OK)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_NIL)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_OK)
        s.pop()
        self.assertEqual(s.size(), 2)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_OK)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_OK)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_OK)

    def test_overflow(self):
        s = BoundedStack(3)
        s.push(1)
        s.push(2)
        s.push(3)
        s.push(4)
        self.assertEqual(s.size(), 3)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_ERR)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_NIL)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_NIL)
        v = s.peek()
        self.assertEqual(v, 3)
        self.assertEqual(s.size(), 3)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_ERR)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_NIL)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_OK)
        s.pop()
        self.assertEqual(s.size(), 2)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_ERR)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_OK)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_OK)

    def test_clear(self):
        s = BoundedStack()
        s.push(1)
        s.push(2)
        s.push(3)
        s.push(4)
        s.peek()
        s.pop()
        self.assertEqual(s.size(), 3)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_OK)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_OK)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_OK)
        s.clear()
        self.assertEqual(s.size(), 0)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_NIL)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_NIL)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_NIL)


if __name__ == "__main__":
    unittest.main()
