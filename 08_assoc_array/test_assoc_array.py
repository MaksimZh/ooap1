import unittest

from assoc_array import Node


class Test_Node(unittest.TestCase):

    def test_value(self):
        a = Node("a")
        b = Node("b")
        self.assertEqual(a.get_value(), "a")
        self.assertEqual(b.get_value(), "b")
        a.set_value(1)
        self.assertEqual(a.get_value(), 1)
        self.assertEqual(b.get_value(), "b")

    def test_links(self):
        a = Node("a")
        b = Node("b")
        c = Node("c")
        self.assertIsNone(a.get_parent())
        self.assertIsNone(a.get_left_child())
        self.assertIsNone(a.get_right_child())
        self.assertIsNone(b.get_parent())
        self.assertIsNone(b.get_left_child())
        self.assertIsNone(b.get_right_child())
        self.assertIsNone(c.get_parent())
        self.assertIsNone(c.get_left_child())
        self.assertIsNone(c.get_right_child())
        a.set_left_child(b)
        b.set_parent(a)
        a.set_right_child(c)
        c.set_parent(a)
        self.assertIsNone(a.get_parent())
        self.assertIs(a.get_left_child(), b)
        self.assertIs(a.get_right_child(), c)
        self.assertIs(b.get_parent(), a)
        self.assertIsNone(b.get_left_child())
        self.assertIsNone(b.get_right_child())
        self.assertIs(c.get_parent(), a)
        self.assertIsNone(c.get_left_child())
        self.assertIsNone(c.get_right_child())
        a.set_left_child(None)
        b.set_parent(None)
        a.set_right_child(None)
        c.set_parent(None)
        self.assertIsNone(a.get_parent())
        self.assertIsNone(a.get_left_child())
        self.assertIsNone(a.get_right_child())
        self.assertIsNone(b.get_parent())
        self.assertIsNone(b.get_left_child())
        self.assertIsNone(b.get_right_child())
        self.assertIsNone(c.get_parent())
        self.assertIsNone(c.get_left_child())
        self.assertIsNone(c.get_right_child())

"""
class Test_RedBlackTree(unittest.TestCase):

    def test_build(self):
        rbt = RedBlackTree()
        self.assertEqual(rbt.get_new_node_status(), RedBlackTree.NewNodeStatus.NIL)
        self.assertEqual(rbt.get_go_status(), RedBlackTree.GoStatus.NIL)
        self.assertEqual(rbt.get_size(), 0)
        self.assertTrue(rbt.node_is_empty())
        rbt.go_parent()
        self.assertEqual(rbt.get_go_status(), RedBlackTree.GoStatus.NO_WAY)
        rbt.go_left_child()
        self.assertEqual(rbt.get_go_status(), RedBlackTree.GoStatus.NO_WAY)
        rbt.go_right_child()
        self.assertEqual(rbt.get_go_status(), RedBlackTree.GoStatus.NO_WAY)
        rbt.to_root()
        self.assertTrue(rbt.node_is_empty())

        rbt.new_node("a", Node.Color.BLACK)
        self.assertEqual(rbt.get_new_node_status(), RedBlackTree.NewNodeStatus.OK)
        self.assertEqual(rbt.get_size(), 1)
        self.assertFalse(rbt.node_is_empty())
        rbt.to_root()
        self.assertFalse(rbt.node_is_empty())
        
        rbt.go_left_child()
        self.assertEqual(rbt.get_go_status(), RedBlackTree.GoStatus.OK)
        self.assertTrue(rbt.node_is_empty())
        rbt.go_parent()
        self.assertEqual(rbt.get_go_status(), RedBlackTree.GoStatus.OK)
        self.assertFalse(rbt.node_is_empty())
        rbt.go_right_child()
        self.assertEqual(rbt.get_go_status(), RedBlackTree.GoStatus.OK)
        self.assertTrue(rbt.node_is_empty())        
        rbt.to_root()
        self.assertFalse(rbt.node_is_empty())

        rbt.new_node("b", Node.Color.RED)
        self.assertEqual(rbt.get_new_node_status(), RedBlackTree.NewNodeStatus.NOT_EMPTY_NODE)
        rbt.go_left_child()
        rbt.new_node("b", Node.Color.RED)
        self.assertEqual(rbt.get_new_node_status(), RedBlackTree.NewNodeStatus.OK)
        self.assertEqual(rbt.get_size(), 2)
        self.assertFalse(rbt.node_is_empty())

        rbt.to_root()
        rbt.go_right_child()
        rbt.new_node("c", Node.Color.RED)
        self.assertEqual(rbt.get_new_node_status(), RedBlackTree.NewNodeStatus.OK)
        self.assertEqual(rbt.get_size(), 3)
        self.assertFalse(rbt.node_is_empty())


    def test_get_node_key(self):
        rbt = RedBlackTree()
        self.assertEqual(rbt.get_get_node_key_status(), RedBlackTree.GetNodeKeyStatus.NIL)
        rbt.get_node_key()
        self.assertEqual(rbt.get_get_node_key_status(), RedBlackTree.GetNodeKeyStatus.EMPTY_NODE)

    def test_get_node_value(self):
        rbt = RedBlackTree()
        self.assertEqual(rbt.get_get_node_value_status(), RedBlackTree.GetNodeValueStatus.NIL)
        rbt.get_node_value()
        self.assertEqual(rbt.get_get_node_value_status(), RedBlackTree.GetNodeValueStatus.EMPTY_NODE)
"""

if __name__ == "__main__":
    unittest.main()
