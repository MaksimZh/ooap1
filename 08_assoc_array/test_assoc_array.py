import unittest
from typing import Any, NamedTuple

from assoc_array import Node, BinaryTree, RedBlackTree, NativeDictionary


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
        self.assertFalse(bt.is_on_node())
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
        self.assertFalse(bt.is_on_node())
        self.check(bt, ["a", ["b", ["d"], ["e"]], ["c", ["f"], []]])

        bt.to_root()
        bt.go_right_child()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.OK)
        self.assertTrue(bt.is_on_node())
        self.assertEqual(bt.get_node_value(), "f")
        self.check(bt, ["a", ["b", ["d"], ["e"]], ["f"]])

        bt.to_root()
        bt.go_left_child()
        bt.go_left_child()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.OK)
        self.assertFalse(bt.is_on_node())
        self.check(bt, ["a", ["b", [], ["e"]], ["f"]])

        bt.to_root()
        bt.go_left_child()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.OK)
        self.assertTrue(bt.is_on_node())
        self.assertEqual(bt.get_node_value(), "e")
        self.check(bt, ["a", ["e"], ["f"]])

        bt.to_root()
        bt.go_left_child()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.OK)
        self.assertFalse(bt.is_on_node())
        self.check(bt, ["a", [], ["f"]])

        bt.to_root()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.OK)
        self.check(bt, ["f"])
        self.assertTrue(bt.is_on_node())
        self.assertEqual(bt.get_node_value(), "f")

        bt.to_root()
        bt.delete()
        self.assertEqual(bt.get_delete_status(), BinaryTree.DeleteStatus.OK)
        self.assertFalse(bt.is_on_node())
        self.check(bt, [])

    
    def test_rotate_small(self):
        bt = BinaryTree()
        bt.rotate_right()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.NOT_NODE)
        bt.rotate_left()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.NOT_NODE)
        
        self.make(bt, ["a"])
        bt.rotate_right()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.NO_PROPER_CHILD)
        bt.rotate_left()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.NO_PROPER_CHILD)
        
    def test_rotate_medium(self):
        bt = BinaryTree()
        self.make(bt, ["a", ["b", ["d"], []], ["c", [], ["g"]]])

        bt.to_root()
        bt.go_left_child()
        bt.rotate_left()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.NO_PROPER_CHILD)
        bt.rotate_right()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.OK)
        self.check(bt, ["a", ["d", [], ["b"]], ["c", [], ["g"]]])

        bt.to_root()
        bt.go_right_child()
        bt.rotate_right()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.NO_PROPER_CHILD)
        bt.rotate_left()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.OK)
        self.check(bt, ["a", ["d", [], ["b"]], ["g", ["c"], []]])


    def test_rotate_big(self):
        bt = BinaryTree()
        self.make(bt, ["a", ["b", ["d"], ["e"]], ["c", ["f"], ["g"]]])

        bt.to_root()
        bt.go_left_child()
        bt.rotate_right()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.OK)
        self.assertEqual(bt.get_node_value(), "d")
        self.check(bt, ["a", ["d", [], ["b", [], ["e"]]], ["c", ["f"], ["g"]]])
        
        bt.to_root()
        bt.go_left_child()
        bt.rotate_left()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.OK)
        self.assertEqual(bt.get_node_value(), "b")
        self.check(bt, ["a", ["b", ["d"], ["e"]], ["c", ["f"], ["g"]]])
        
        bt.to_root()
        bt.go_left_child()
        bt.rotate_left()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.OK)
        self.assertEqual(bt.get_node_value(), "e")
        self.check(bt, ["a", ["e", ["b", ["d"], []], []], ["c", ["f"], ["g"]]])

        bt.to_root()
        bt.go_left_child()
        bt.rotate_right()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.OK)
        self.assertEqual(bt.get_node_value(), "b")
        self.check(bt, ["a", ["b", ["d"], ["e"]], ["c", ["f"], ["g"]]])

        bt.to_root()
        bt.rotate_right()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.OK)
        self.assertEqual(bt.get_node_value(), "b")
        self.check(bt, ["b", ["d"], ["a", ["e"], ["c", ["f"], ["g"]]]])

        bt.to_root()
        bt.rotate_left()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.OK)
        self.assertEqual(bt.get_node_value(), "a")
        self.check(bt, ["a", ["b", ["d"], ["e"]], ["c", ["f"], ["g"]]])

        bt.to_root()
        bt.rotate_left()
        self.assertEqual(bt.get_rotate_status(), bt.RotateStatus.OK)
        self.assertEqual(bt.get_node_value(), "c")
        self.check(bt, ["c", ["a", ["b", ["d"], ["e"]], ["f"]], ["g"]])

    
    def test_save(self):
        bt = BinaryTree()
        self.make(bt, ["a", ["b", ["d"], ["e"]], ["c", ["f"], ["g"]]])
        bt.go_saved("s-c")
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)
        bt.to_root()
        bt.go_left_child()
        bt.go_right_child()
        bt.save_cursor("s-e")
        bt.to_root()
        bt.go_right_child()
        bt.go_left_child()
        bt.save_cursor("s-f")
        bt.to_root()
        bt.go_saved("s-e")
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.OK)
        self.assertEqual(bt.get_node_value(), "e")
        bt.go_saved("s-f")
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.OK)
        self.assertEqual(bt.get_node_value(), "f")
        bt.delete()
        bt.to_root()
        bt.go_saved("s-f")
        self.assertEqual(bt.get_go_status(), BinaryTree.GoStatus.NO_TARGET)


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

    def test_put_2(self):
        rbt = RedBlackTree()
        rbt.put("a")
        rbt.put("b")
        rbt.put("c")
        rbt.put("d")
        rbt.put("e")
        rbt.put("f")
        rbt.put("g")

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
        self.assertEqual(rbt.get_delete_status(), RedBlackTree.DeleteStatus.NIL)
        rbt.delete("a")
        self.assertEqual(rbt.get_delete_status(), RedBlackTree.DeleteStatus.NOT_FOUND)
        rbt.put("d")
        rbt.put("b")
        rbt.put("f")
        rbt.put("a")
        rbt.put("c")
        rbt.put("e")
        rbt.put("g")
        self.assertEqual(rbt.get_size(), 7)
        rbt.delete("a")
        self.assertEqual(rbt.get_delete_status(), RedBlackTree.DeleteStatus.OK)
        self.assertFalse(rbt.has_value("a"))
        self.assertEqual(rbt.get_size(), 6)
        rbt.delete("b")
        self.assertEqual(rbt.get_delete_status(), RedBlackTree.DeleteStatus.OK)
        self.assertFalse(rbt.has_value("b"))
        self.assertEqual(rbt.get_size(), 5)
        rbt.delete("f")
        self.assertEqual(rbt.get_delete_status(), RedBlackTree.DeleteStatus.OK)
        self.assertFalse(rbt.has_value("f"))
        self.assertEqual(rbt.get_size(), 4)

    def test_delete_2(self):
        rbt = RedBlackTree()
        rbt.put("a")
        rbt.put("b")
        rbt.put("c")
        rbt.put("d")
        rbt.put("e")
        rbt.put("f")
        self.assertEqual(rbt.get_size(), 6)
        rbt.delete("d")
        self.assertEqual(rbt.get_delete_status(), RedBlackTree.DeleteStatus.OK)
        self.assertFalse(rbt.has_value("d"))
        self.assertEqual(rbt.get_size(), 5)


class Test_NativeDictionary(unittest.TestCase):

    def check(self, a: NativeDictionary, pattern: dict[str, Any]):
        self.assertEqual(a.get_size(), len(pattern))
        for key, value in pattern.items():
            self.assertTrue(a.has_key(key))
            self.assertEqual(a.get(key), value)

    def test_put(self):
        a = NativeDictionary()
        self.check(a, dict())
        a.put("a", 0)
        self.check(a, {"a": 0})
        a.put("a", 1)
        self.check(a, {"a": 1})
        a.put("b", 2)
        self.check(a, {"a": 1, "b": 2})

    def test_get(self):
        a = NativeDictionary()
        self.assertEqual(a.get_get_status(), NativeDictionary.GetStatus.NIL)
        a.put("a", 1)
        a.put("b", 2)
        a.put("c", 3)
        self.assertEqual(a.get("b"), 2)
        self.assertEqual(a.get_get_status(), NativeDictionary.GetStatus.OK)
        a.get("foo")
        self.assertEqual(a.get_get_status(), NativeDictionary.GetStatus.NOT_FOUND)

    def test_delete(self):
        a = NativeDictionary()
        self.assertEqual(a.get_delete_status(), NativeDictionary.DeleteStatus.NIL)
        a.put("a", 1)
        a.put("b", 2)
        a.put("c", 3)
        self.check(a, {"a": 1, "b": 2, "c": 3})
        a.delete("b")
        self.assertEqual(a.get_delete_status(), NativeDictionary.DeleteStatus.OK)
        self.check(a, {"a": 1, "c": 3})
        a.delete("foo")
        self.assertEqual(a.get_delete_status(), NativeDictionary.DeleteStatus.NOT_FOUND)
        a.delete("b")
        self.assertEqual(a.get_delete_status(), NativeDictionary.DeleteStatus.NOT_FOUND)


if __name__ == "__main__":
    unittest.main()
