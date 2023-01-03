import unittest
from typing import Any

from assoc_array import Node, BinaryTree


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


class Test_BinaryTree(unittest.TestCase):

    def check_subtree(self, tree: BinaryTree, pattern: list[Any], count: list[int]):
        assert(len(pattern) == 3)
        self.assertEqual(pattern[0], tree.get_node_value())
        count[0] += 1
        if pattern[1] != []:
            tree.go_left_child()
            self.check_subtree(tree, pattern[1], count)
            tree.go_parent()
        if pattern[2] != []:
            tree.go_right_child()
            self.check_subtree(tree, pattern[2], count)
            tree.go_parent()

    def check(self, tree: BinaryTree, pattern: list[Any]):
        if pattern == []:
            self.assertEqual(tree.get_size(), 0)
            return
        tree.go_root()
        count = [0]
        self.check_subtree(tree, pattern, count)
        self.assertEqual(tree.get_size(), count[0])

    
    def test_build(self):
        bt = BinaryTree()
        self.assertEqual(bt.get_add_root_status(), BinaryTree.AddRootStatus.NIL)
        self.assertEqual(bt.get_add_child_status(), BinaryTree.AddChildStatus.NIL)
        self.check(bt, [])
        bt.add_left_child("foo")
        self.assertEqual(bt.get_add_child_status(), BinaryTree.AddChildStatus.EMPTY_TREE)
        bt.add_right_child("foo")
        self.assertEqual(bt.get_add_child_status(), BinaryTree.AddChildStatus.EMPTY_TREE)

        bt.add_root("a")
        self.check(bt, ["a", [], []])
        bt.add_root("foo")
        self.assertEqual(bt.get_add_root_status(), BinaryTree.AddRootStatus.ALREADY_EXISTS)
        self.check(bt, ["a", [], []])

        bt.go_root()
        bt.add_left_child("b")
        self.check(bt, ["a", ["b", [], []], []])
        bt.go_root()
        bt.add_right_child("c")
        self.check(bt, ["a", ["b", [], []], ["c", [], []]])
        bt.go_root()
        bt.add_left_child("foo")
        self.assertEqual(bt.get_add_child_status(), BinaryTree.AddChildStatus.ALREADY_EXISTS)
        bt.add_right_child("foo")
        self.assertEqual(bt.get_add_child_status(), BinaryTree.AddChildStatus.ALREADY_EXISTS)

        bt.go_root()
        bt.go_left_child()
        bt.add_left_child("d")
        self.check(bt, ["a", ["b", ["d", [], []], []], ["c", [], []]])

        bt.go_root()
        bt.go_left_child()
        bt.add_right_child("e")
        self.check(bt, ["a", ["b", ["d", [], []], ["e", [], []]], ["c", [], []]])

    
    def test_get(self):
        bt = BinaryTree()
        self.assertEqual(bt.get_get_node_value_status(), BinaryTree.GetNodeValueStatus.NIL)
        bt.get_node_value()
        self.assertEqual(bt.get_get_node_value_status(), BinaryTree.GetNodeValueStatus.EMPTY_TREE)
        bt.add_root("a")
        self.assertEqual(bt.get_node_value(), "a")
        self.assertEqual(bt.get_get_node_value_status(), BinaryTree.GetNodeValueStatus.OK)


    def test_go(self):
        bt = BinaryTree()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NIL)
        bt.go_root()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_parent()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_left_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_right_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        
        bt.add_root("a")
        bt.go_root()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.OK)
        bt.go_parent()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_left_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_right_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        
        bt.add_left_child("b")
        bt.add_right_child("c")
        bt.go_parent()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_left_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.OK)
        bt.go_left_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_right_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_parent()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.OK)
        bt.go_right_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.OK)
        
        bt.go_root()
        bt.go_left_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.OK)
        bt.add_left_child("d")
        bt.add_right_child("e")
        bt.go_left_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.OK)
        bt.go_left_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_right_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_parent()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.OK)
        bt.go_right_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.OK)


    def test_rotate(self):
        bt = BinaryTree()
        bt.add_root("a")
        bt.add_left_child("b")
        bt.add_right_child("c")
        bt.go_left_child()
        bt.add_left_child("d")
        bt.add_right_child("e")


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
