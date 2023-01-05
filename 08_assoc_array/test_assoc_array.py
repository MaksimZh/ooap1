import unittest
from typing import Any#, NamedTuple

from assoc_array import Node, BinaryTree#, RedBlackTree


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
        if pattern == []:
            self.assertFalse(tree.is_on_node())
            return
        self.assertTrue(tree.is_on_node())
        self.assertEqual(pattern[0], tree.get_node_value())
        self.assertEqual(tree.get_get_node_value_status(), BinaryTree.GetNodeValueStatus.OK)
        count[0] += 1
        assert(len(pattern) == 3 or len(pattern) == 1)
        left: list[Any] = pattern[1] if len(pattern) == 3 else []
        right: list[Any] = pattern[2] if len(pattern) == 3 else []
        if left != []:
            tree.go_left_child()
            self.assertEqual(tree.get_go_status(), BinaryTree.GoStatus.OK)
            self.assertFalse(tree.is_on_root())
            self.assertTrue(tree.is_on_left_child())
            self.check_subtree(tree, left, count)
            tree.go_parent()
            self.assertEqual(tree.get_go_status(), BinaryTree.GoStatus.OK)
        if right != []:
            tree.go_right_child()
            self.assertEqual(tree.get_go_status(), BinaryTree.GoStatus.OK)
            self.assertFalse(tree.is_on_root())
            self.assertTrue(tree.is_on_right_child())
            self.check_subtree(tree, right, count)
            tree.go_parent()
            self.assertEqual(tree.get_go_status(), BinaryTree.GoStatus.OK)

    def check(self, tree: BinaryTree, pattern: list[Any]):
        tree.to_root()
        self.assertTrue(tree.is_on_root())
        self.assertFalse(tree.is_on_left_child())
        self.assertFalse(tree.is_on_right_child())
        count = [0]
        self.check_subtree(tree, pattern, count)
        self.assertEqual(tree.get_size(), count[0])

    def make(self, tree: BinaryTree, pattern: list[Any]):
        assert(not tree.is_on_node())
        if pattern == []:
            return
        tree.put(pattern[0])
        assert(len(pattern) == 3 or len(pattern) == 1)
        left: list[Any] = pattern[1] if len(pattern) == 3 else []
        right: list[Any] = pattern[2] if len(pattern) == 3 else []
        if left != []:
            tree.go_left_child()
            self.make(tree, left)
            tree.go_parent()
            self.assertEqual(tree.get_go_status(), BinaryTree.GoStatus.OK)
        if right != []:
            tree.go_right_child()
            self.make(tree, right)
            tree.go_parent()
    

    def test_put(self):
        bt = BinaryTree()
        self.check(bt, [])

        bt.put("a0")
        self.check(bt, ["a0"])
        bt.to_root()
        bt.put("a")
        self.check(bt, ["a"])

        bt.to_root()
        bt.go_left_child()
        bt.put("b")
        self.check(bt, ["a", ["b"], []])

        bt.to_root()
        bt.go_right_child()
        bt.put("c0")
        self.check(bt, ["a", ["b"], ["c0"]])
        bt.to_root()
        bt.go_right_child()
        bt.put("c")
        self.check(bt, ["a", ["b"], ["c"]])

        bt.to_root()
        bt.go_left_child()
        bt.go_left_child()
        bt.put("d")
        self.check(bt, ["a", ["b", ["d"], []], ["c"]])

        bt.to_root()
        bt.go_left_child()
        bt.go_right_child()
        bt.put("e")
        self.check(bt, ["a", ["b", ["d"], ["e"]], ["c"]])

    def test_make(self):
        bt = BinaryTree()
        self.make(bt, ["a", ["b", ["d"], ["e"]], ["c", ["f"], ["g"]]])
        self.check(bt, ["a", ["b", ["d"], ["e"]], ["c", ["f"], ["g"]]])
 
    def test_get(self):
        bt = BinaryTree()
        self.assertEqual(bt.get_get_node_value_status(), BinaryTree.GetNodeValueStatus.NIL)
        bt.get_node_value()
        self.assertEqual(bt.get_get_node_value_status(), BinaryTree.GetNodeValueStatus.NOT_NODE)
        bt.put("a")
        self.assertEqual(bt.get_node_value(), "a")
        self.assertEqual(bt.get_get_node_value_status(), BinaryTree.GetNodeValueStatus.OK)


    def test_go(self):
        bt = BinaryTree()
        bt.to_root()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NIL)
        bt.go_parent()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_left_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_right_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        
        bt.put("a")
        bt.to_root()
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
        bt.go_left_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_right_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)

        bt.to_root()
        bt.go_left_child()
        bt.put("b")
        bt.go_parent()
        bt.go_right_child()
        bt.put("c")
        bt.to_root()
        bt.go_parent()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_left_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.OK)
        bt.go_left_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.OK)
        bt.go_left_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_parent()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.OK)
        bt.go_right_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.OK)
        bt.go_left_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.go_right_child()
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)

    
    def test_delete(self):
        bt = BinaryTree()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.NIL)
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.NOT_NODE)

        bt.put("a")
        self.check(bt, ["a"])
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.OK)
        self.check(bt, [])

        self.make(bt, ["a", ["b", ["d"], ["e"]], ["c", ["f"], ["g"]]])
        
        bt.to_root()
        bt.go_left_child()
        bt.go_left_child()
        bt.go_left_child()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.NOT_NODE)
        self.check(bt, ["a", ["b", ["d"], ["e"]], ["c", ["f"], ["g"]]])

        bt.to_root()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.TWO_CHILDREN)
        bt.go_right_child()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.TWO_CHILDREN)

        bt.to_root()
        bt.go_right_child()
        bt.go_right_child()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.OK)
        self.check(bt, ["a", ["b", ["d"], ["e"]], ["c", ["f"], []]])

        bt.to_root()
        bt.go_right_child()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.OK)
        self.check(bt, ["a", ["b", ["d"], ["e"]], ["f"]])

        bt.to_root()
        bt.go_left_child()
        bt.go_left_child()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.OK)
        self.check(bt, ["a", ["b", [], ["e"]], ["f"]])

        bt.to_root()
        bt.go_left_child()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.OK)
        self.check(bt, ["a", ["e"], ["f"]])

        bt.to_root()
        bt.go_left_child()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.OK)
        self.check(bt, ["a", [], ["f"]])

        bt.to_root()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.OK)
        self.check(bt, ["f"])

        bt.to_root()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.OK)
        self.check(bt, [])

    
    """
    def test_rotate_right_branch(self):
        bt = BinaryTree()
        bt.put("a")
        bt.go_left_child()
        bt.put("b")
        bt.go_left_child()
        bt.put("d")
        bt.go_parent()
        bt.go_right_child()
        bt.put("e")
        bt.go_parent()
        bt.go_parent()
        bt.go_right_child()
        bt.put("c")
        bt.go_left_child()
        bt.put("f")
        bt.go_parent()
        bt.go_right_child()
        bt.put("g")

        bt.go_root()
        bt.go_left_child()
        bt.rotate_right()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.OK)
        self.assertEqual(bt.get_node_value(), "d")
        self.check(bt, ["a", ["d", ["f", [], []], ["b", ["g", [], []], ["e", [], []]]], ["c", [], []]])

    def test_rotate_left_root(self):
        bt = BinaryTree()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.NIL)
        bt.rotate_left()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.EMPTY_TREE)
        bt.add_root("a")
        bt.add_left_child("b")
        bt.rotate_left()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.NO_PROPER_CHILD)
        bt.add_right_child("c")
        bt.go_right_child()
        bt.add_left_child("d")
        bt.add_right_child("e")
        self.check(bt, ["a", ["b", [], []], ["c", ["d", [], []], ["e", [], []]]])
        bt.go_root()
        bt.rotate_left()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.OK)
        self.assertEqual(bt.get_node_value(), "c")
        self.check(bt, ["c", ["a", ["b", [], []], ["d", [], []]], ["e", [], []]])

    def test_rotate_left_branch(self):
        bt = BinaryTree()
        bt.add_root("a")
        bt.add_left_child("b")
        bt.add_right_child("c")
        bt.go_right_child()
        bt.add_left_child("d")
        bt.add_right_child("e")
        bt.go_right_child()
        bt.add_left_child("f")
        bt.add_right_child("g")
        self.check(bt, ["a", ["b", [], []], ["c", ["d", [], []], ["e", ["f", [], []], ["g", [], []]]]])
        bt.go_root()
        bt.go_right_child()
        bt.rotate_left()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.OK)
        self.assertEqual(bt.get_node_value(), "e")
        self.check(bt, ["a", ["b", [], []], ["e", ["c", ["d", [], []], ["f", [], []]], ["g", [], []]]])
    """
"""
class Val(NamedTuple):
    a: str

class Test_RedBlackTree(unittest.TestCase):

    def test_put_distinct(self):
        rbt = RedBlackTree()
        a = Val("a")
        a1 = Val("a")
        assert(a is not a1)
        b = Val("b")
        self.assertEqual(rbt.get_size(), 0)
        self.assertFalse(rbt.has_value(Val("a")))
        rbt.put(a)
        self.assertEqual(rbt.get_size(), 1)
        self.assertTrue(rbt.has_value(Val("a")))
        self.assertIs(rbt.get(Val("a")), a)
        rbt.put(a1)
        self.assertEqual(rbt.get_size(), 1)
        self.assertTrue(rbt.has_value(Val("a")))
        self.assertIs(rbt.get(Val("a")), a1)
        rbt.put(b)
        self.assertEqual(rbt.get_size(), 2)
        self.assertTrue(rbt.has_value(Val("a")))
        self.assertTrue(rbt.has_value(Val("b")))
        self.assertIs(rbt.get(Val("a")), a1)
        self.assertIs(rbt.get(Val("b")), b)

    def test_put(self):
        rbt = RedBlackTree()
        rbt.put("d")
        rbt.put("b")
        rbt.put("f")
        rbt.put("a")
        rbt.put("c")
        rbt.put("e")
        rbt.put("g")
        self.assertEqual(rbt.get_size(), 7)
        self.assertTrue(rbt.has_value("a"))
        self.assertTrue(rbt.has_value("b"))
        self.assertTrue(rbt.has_value("c"))
        self.assertTrue(rbt.has_value("d"))
        self.assertTrue(rbt.has_value("e"))
        self.assertTrue(rbt.has_value("f"))
        self.assertTrue(rbt.has_value("g"))
        self.assertEqual(rbt.get("a"), "a")
        self.assertEqual(rbt.get("b"), "b")
        self.assertEqual(rbt.get("c"), "c")
        self.assertEqual(rbt.get("d"), "d")
        self.assertEqual(rbt.get("e"), "e")
        self.assertEqual(rbt.get("f"), "f")
        self.assertEqual(rbt.get("g"), "g")

    def test_get(self):
        rbt = RedBlackTree()
        self.assertEqual(rbt.get_get_status(), RedBlackTree.GetStatus.NIL)
        rbt.get("a")
        self.assertEqual(rbt.get_get_status(), RedBlackTree.GetStatus.NOT_FOUND)
        rbt.put("a")
        self.assertEqual(rbt.get("a"), "a")
        self.assertEqual(rbt.get_get_status(), RedBlackTree.GetStatus.OK)

    def test_delete(self):
        rbt = RedBlackTree()
        rbt.put("d")
        rbt.put("b")
        rbt.put("f")
        rbt.put("a")
        rbt.put("c")
        rbt.put("e")
        rbt.put("g")
        self.assertEqual(rbt.get_size(), 7)
        rbt.delete("a")
        self.assertEqual(rbt.get_size(), 6)
"""

if __name__ == "__main__":
    unittest.main()
