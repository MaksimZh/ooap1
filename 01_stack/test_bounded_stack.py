import unittest

from bounded_stack import BoundedStack

class Test(unittest.TestCase):

    def test_init(self):
        _ = BoundedStack(16)
        _ = BoundedStack()

    def test_fill_3(self):
        s = BoundedStack(3)
        self.assertEqual(s.size(), 0)
        self.assertEqual(s.get_push_status(), BoundedStack.PUSH_NIL)
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_NIL)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_NIL)
        v = s.peek()
        self.assertEqual(v, 0)
        self.assertEqual(s.get_peek_status(), BoundedStack.PEEK_ERR)
        s.pop()
        self.assertEqual(s.get_pop_status(), BoundedStack.POP_ERR)


if __name__ == "__main__":
    unittest.main()
