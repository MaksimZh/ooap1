from typing import Any, Optional, NamedTuple
from enum import Enum, auto


class Node:
    
    __value: Any
    __parent: Optional["Node"]
    __left_child: Optional["Node"]
    __right_child: Optional["Node"]


    # КОНСТРУКТОР
    # постусловие: создан новый узел с заданным значением
    # постусловие: узел не связан ни с какими узлами
    def __init__(self, value: Any) -> None:
        self.__value = value
        self.__parent = None
        self.__left_child = None
        self.__right_child = None


    # КОМАНДЫ

    # задать значение узла
    # постусловие: значение узла равно заданному
    def set_value(self, value: Any) -> None:
        self.__value = value

    # задать родителя узла
    # постусловие: родитель равен заданному узлу
    def set_parent(self, node: Optional["Node"]) -> None:
        self.__parent = node

    # задать левого ребёнка узла
    # постусловие: левый ребёнок равен заданному узлу
    def set_left_child(self, node: Optional["Node"]) -> None:
        self.__left_child = node

    # задать правого ребёнка узла
    # постусловие: правый ребёнок равен заданному узлу
    def set_right_child(self, node: Optional["Node"]) -> None:
        self.__right_child = node


    # ЗАПРОСЫ
    
    # получить значение узла
    def get_value(self) -> Any:
        return self.__value

    # получить родителя узла
    def get_parent(self) -> Optional["Node"]:
        return self.__parent

    # получить левого ребёнка узла
    def get_left_child(self) -> Optional["Node"]:
        return self.__left_child

    # получить правого ребёнка узла
    def get_right_child(self) -> Optional["Node"]:
        return self.__right_child


def _replace_child(old: Node, new: Optional[Node]):
    parent = old.get_parent()
    assert(parent is not None)
    if parent.get_left_child() is old:
        parent.set_left_child(new)
    else:
        parent.set_right_child(new)
    if new is not None:
        new.set_parent(parent)


class BinaryTree:

    __root_parent: Node
    __current: Node
    __size: int


    # КОНСТРУКТОР
    # постусловие: создано пустое дерево
    def __init__(self) -> None:
        self.__root_parent = Node(None)
        self.__current = self.__root_parent
        self.__size = 0
        self.__add_root_status = self.AddRootStatus.NIL
        self.__add_child_status = self.AddChildStatus.NIL
        self.__go_status = self.GoStatus.NIL
        self.__set_node_value_status = self.SetNodeValueStatus.NIL
        self.__get_node_value_status = self.GetNodeValueStatus.NIL
        self.__delete_status = self.DeleteStatus.NIL
        self.__rotate_status = self.RotateStatus.NIL


    # КОМАНДЫ

    # создать корень дерева с заданным значением
    # предусловие: дерево пустое
    # постусловие: дерево содержит один элемент с заданным значением
    # постусловие: текущим элементом является корень
    def add_root(self, value: Any) -> None:
        if self.get_size() != 0:
            self.__add_root_status = self.AddRootStatus.ALREADY_EXISTS
            return
        node = Node(value)
        self.__root_parent.set_left_child(node)
        node.set_parent(self.__root_parent)
        self.__current = node
        self.__size += 1
        self.__add_root_status = self.AddRootStatus.OK

    class AddRootStatus(Enum):
        NIL = auto(),            # команда не выполнялась
        OK = auto(),             # успех
        ALREADY_EXISTS = auto(), # корень уже существует

    __add_root_status: AddRootStatus

    def get_add_root_status(self) -> AddRootStatus:
        return self.__add_root_status

    
    # создать левого потомка текущего элемента с заданным значением
    # предусловие: дерево не пустое
    # предусловие: текущий элемент не имеет левого потомка
    # постусловие: в дерево добавлен левый потомок для текущего элемента с заданным значением
    def add_left_child(self, value: Any) -> None:
        if self.get_size() == 0:
            self.__add_child_status = self.AddChildStatus.EMPTY_TREE
            return
        assert(self.__current is not None)
        if self.__current.get_left_child() is not None:
            self.__add_child_status = self.AddChildStatus.ALREADY_EXISTS
            return
        node = Node(value)
        node.set_parent(self.__current)
        self.__current.set_left_child(node)
        self.__size += 1

    # создать правого потомка текущего элемента с заданным значением
    # предусловие: дерево не пустое
    # предусловие: текущий элемент не имеет правого потомка
    # постусловие: в дерево добавлен правый потомок для текущего элемента с заданным значением
    def add_right_child(self, value: Any) -> None:
        if self.get_size() == 0:
            self.__add_child_status = self.AddChildStatus.EMPTY_TREE
            return
        assert(self.__current is not None)
        if self.__current.get_right_child() is not None:
            self.__add_child_status = self.AddChildStatus.ALREADY_EXISTS
            return
        node = Node(value)
        node.set_parent(self.__current)
        self.__current.set_right_child(node)
        self.__size += 1

    class AddChildStatus(Enum):
        NIL = auto(),            # команда не выполнялась
        OK = auto(),             # успех
        EMPTY_TREE = auto(),     # дерево пусто
        ALREADY_EXISTS = auto(), # потомок уже существует

    __add_child_status: AddChildStatus

    def get_add_child_status(self) -> AddChildStatus:
        return self.__add_child_status


    # переместить курсор на корень дерева
    # предусловие: дерево не пустое
    # постусловие: курсор перемещён в корень дерева
    def go_root(self) -> None:
        if self.get_size() == 0:
            self.__go_status = self.GoStatus.NO_TARGET
            return
        self.__go(self.__root_parent.get_left_child())

    # переместить курсор к родителю текущего узла
    # предусловие: дерево не пустое
    # предусловие: у текущего узла есть родитель
    # постусловие: курсор перемещён к родителю текущего узла
    def go_parent(self) -> None:
        if self.get_size() == 0:
            self.__go_status = self.GoStatus.NO_TARGET
            return
        assert(self.__current is not None)
        self.__go(self.__current.get_parent())


    # переместить курсор к левому потомку текущего узла
    # предусловие: дерево не пустое
    # предусловие: у текущего узла есть левый потомок
    # постусловие: курсор перемещён к левому потомку текущего узла
    def go_left_child(self) -> None:
        if self.get_size() == 0:
            self.__go_status = self.GoStatus.NO_TARGET
            return
        assert(self.__current is not None)
        self.__go(self.__current.get_left_child())

    # переместить курсор к правому потомку текущего узла
    # предусловие: дерево не пустое
    # предусловие: у текущего узла есть правый потомок
    # постусловие: курсор перемещён к правому потомку текущего узла
    def go_right_child(self) -> None:
        if self.get_size() == 0:
            self.__go_status = self.GoStatus.NO_TARGET
            return
        assert(self.__current is not None)
        self.__go(self.__current.get_right_child())

    class GoStatus(Enum):
        NIL = auto(),       # команда не выполнялась
        OK = auto(),        # успех
        NO_TARGET = auto(), # нет узла в заданном направлении

    __go_status: GoStatus

    def get_go_status(self) -> GoStatus:
        return self.__go_status


    # задать значение текущего узла
    def set_node_value(self, value: Any) -> None:
        if self.get_size() == 0:
            self.__set_node_value_status = self.SetNodeValueStatus.EMPTY_TREE
            return
        self.__current.set_value(value)
        self.__set_node_value_status = self.SetNodeValueStatus.OK

    class SetNodeValueStatus(Enum):
        NIL = auto(),
        OK = auto(),
        EMPTY_TREE = auto(),

    __set_node_value_status: SetNodeValueStatus

    def get_set_node_value_status(self) -> SetNodeValueStatus:
        return self.__set_node_value_status
    
    
    # удалить текущий узел
    # предусловие: дерево не пустое
    # постусловие: текущий узел удалён и заменён самым левым из его правых потомков
    def delete(self) -> None:
        if self.get_size() == 0:
            self.__delete_status = self.DeleteStatus.EMPTY_TREE
            return
        assert(self.__current is not None)
        if self.__current.get_right_child() is not None:
            replacement = self.__current.get_right_child()
            while True:
                assert(replacement is not None)
                if replacement.get_left_child() is None:
                    break
                replacement = replacement.get_left_child()
            assert(replacement is not None)
            self.__current.set_value(replacement.get_value())
            stored_current = self.__current
            self.__current = replacement
            self.delete()
            assert(self.get_delete_status() == self.DeleteStatus.OK)
            self.__current = stored_current
            self.__size += 1
        else:
            parent = self.__current.get_parent()
            assert(parent is not None)
            left = self.__current.get_left_child()
            _replace_child(self.__current, left)
            if left is not None:
                self.__current = left
            else:
                self.__current = parent

        self.__size -= 1
        self.__delete_status = self.DeleteStatus.OK

    class DeleteStatus(Enum):
        NIL = auto(),        # команда не выполнялась
        OK = auto(),         # успех
        EMPTY_TREE = auto(), # дерево пусто

    __delete_status: DeleteStatus

    def get_delete_status(self) -> DeleteStatus:
        return self.__delete_status


    # повернуть дерево вправо на текущем узле
    # предусловие: дерево не пусто
    # предусловие: у текущего узла есть левый потомок
    # постусловие: левый потомок занял место текущего узла
    #              текущий узел стал правым потомком своего левого потомка
    #              правый потомок левого потомка текущего узла стал левым потомком текущего узла
    def rotate_right(self) -> None:
        if self.get_size() == 0:
            self.__rotate_status = self.RotateStatus.EMPTY_TREE
            return
        assert(self.__current is not None)
        if self.__current.get_left_child() is None:
            self.__rotate_status = self.RotateStatus.NO_PROPER_CHILD
            return
        top = self.__current
        assert(top is not None)
        left = top.get_left_child()
        assert(left is not None)
        right_of_left = left.get_right_child()
        self.__current = left
        _replace_child(top, left)
        left.set_right_child(top)
        top.set_parent(left)
        top.set_left_child(right_of_left)
        if right_of_left is not None:
            right_of_left.set_parent(top)
        self.__rotate_status = self.RotateStatus.OK

    # повернуть дерево влево на текущем узле
    # предусловие: дерево не пусто
    # предусловие: у текущего узла есть правый потомок
    # постусловие: правый потомок занял место текущего узла
    #              текущий узел стал левым потомком своего правого потомка
    #              левый потомок правого потомка текущего узла стал правым потомком текущего узла
    def rotate_left(self) -> None:
        if self.get_size() == 0:
            self.__rotate_status = self.RotateStatus.EMPTY_TREE
            return
        assert(self.__current is not None)
        if self.__current.get_right_child() is None:
            self.__rotate_status = self.RotateStatus.NO_PROPER_CHILD
            return
        top = self.__current
        assert(top is not None)
        right = top.get_right_child()
        assert(right is not None)
        left_of_right = right.get_left_child()
        self.__current = right
        _replace_child(top, right)
        right.set_left_child(top)
        top.set_parent(right)
        top.set_right_child(left_of_right)
        if left_of_right is not None:
            left_of_right.set_parent(top)
        self.__rotate_status = self.RotateStatus.OK

    class RotateStatus(Enum):
        NIL = auto(),             # команда не выполнялась
        OK = auto(),              # успех
        EMPTY_TREE = auto(),      # дерево пусто
        NO_PROPER_CHILD = auto(), # нет потомка чтобы заменить текущий узел

    __rotate_status: RotateStatus

    def get_rotate_status(self) -> RotateStatus:
        return self.__rotate_status


    # ЗАПРОСЫ

    # получить количество узлов
    def get_size(self) -> int:
        return self.__size

    # проверить установлен ли курсор на корень дерева
    def is_node_root(self) -> bool:
        if self.get_size() == 0:
            return False
        return self.__current.get_parent() is self.__root_parent

    # проверить установлен ли курсор на левого потомка
    def is_node_left_child(self) -> bool:
        if self.get_size() == 0:
            return False
        if self.is_node_root():
            return False
        parent = self.__current.get_parent()
        assert(parent is not None)
        return parent.get_left_child() is self.__current

    # проверить установлен ли курсор на правого потомка
    def is_node_right_child(self) -> bool:
        if self.get_size() == 0:
            return False
        if self.is_node_root():
            return False
        parent = self.__current.get_parent()
        assert(parent is not None)
        return parent.get_right_child() is self.__current

    # получить значение текущего узла
    # предусловие: дерево не пусто
    def get_node_value(self) -> Any:
        if self.get_size() == 0:
            self.__get_node_value_status = self.GetNodeValueStatus.EMPTY_TREE
            return
        assert(self.__current is not None)
        self.__get_node_value_status = self.GetNodeValueStatus.OK
        return self.__current.get_value()

    class GetNodeValueStatus(Enum):
        NIL = auto(),
        OK = auto(),
        EMPTY_TREE = auto(),

    __get_node_value_status: GetNodeValueStatus

    def get_get_node_value_status(self) -> GetNodeValueStatus:
        return self.__get_node_value_status

    
    def __go(self, target: Optional[Node]) -> None:
        if target is None or target is self.__root_parent:
            self.__go_status = self.GoStatus.NO_TARGET
            return
        self.__current = target
        self.__go_status = self.GoStatus.OK


class _ColoredValue(NamedTuple):
    value: Any
    is_red: bool

_leaf = _ColoredValue(None, False)


class RedBlackTree:

    __size: int
    __tree: BinaryTree

    # КОНСТРУКТОР
    # постусловие: создано дерево, состоящее из единственного пустого узла
    def __init__(self) -> None:
        self.__size = 0
        self.__tree = BinaryTree()
        self.__tree.add_root(_leaf)
        self.__get_status = self.GetStatus.NIL


    # КОМАНДЫ

    # добавить или заменить узел с заданным значением
    # постусловие: если равное значение присутствовало, то оно заменено новым
    #              если равное значение отсутствует, то новое значение добавлено
    # постусловие: дерево соответствует требованиям красно-чёрного дерева
    def put(self, value: Any) -> None:
        self.__tree.go_root()
        self.__find(value)
        cv: _ColoredValue = self.__tree.get_node_value()
        if cv is _leaf:
            self.__insert(value)
            self.__size += 1
        else:
            self.__tree.set_node_value(_ColoredValue(value, cv.is_red))
        if __debug__:
            self.__check_tree()


    # удалить узел с заданным значением
    # предусловие: узел со значением равным заданному присутствует
    # постусловие: узел со значением равным заданному удалён
    # постусловие: дерево соответствует требованиям красно-чёрного дерева
    def delete(self, value: Any) -> None:
        self.__tree.go_root()
        self.__find(value)
        if self.__is_node_red():
            self.__tree.delete()
            self.__size -= 1
            return
        self.__size -= 1
        if __debug__:
            self.__check_tree()

    class DeleteStatus(Enum):
        NIL = auto(),       # команда не выполнялась 
        OK = auto(),        # успех
        NOT_FOUND = auto(), # значение не найдено

    __delete_status: DeleteStatus

    def get_delete_status(self) -> DeleteStatus:
        return self.__delete_status

    
    # ЗАПРОСЫ

    # получить количество непустых узлов
    def get_size(self) -> int:
        return self.__size

    # проверить присутствует ли значение в дереве
    def has_value(self, value: Any) -> bool:
        self.__tree.go_root()
        self.__find(value)
        return self.__tree.get_node_value() is not _leaf

    # получить ключ текущего узла
    # предусловие: узел со значением равным заданному присутствует
    def get(self, value: Any) -> Any:
        self.__tree.go_root()
        self.__find(value)
        if self.__tree.get_node_value() is _leaf:
            self.__get_status = self.GetStatus.NOT_FOUND
            return None
        self.__get_status = self.GetStatus.OK
        return self.__tree.get_node_value().value

    class GetStatus(Enum):
        NIL = auto(),       # запрос не выполнялся 
        OK = auto(),        # успех
        NOT_FOUND = auto(), # значение не найдено

    __get_status: GetStatus

    def get_get_status(self) -> GetStatus:
        return self.__get_status

    def __find(self, value: Any) -> None:
        cv: _ColoredValue = self.__tree.get_node_value()
        if cv is _leaf:
            return
        if cv.value < value:
            self.__tree.go_right_child()
            self.__find(value)
            return
        if cv.value > value:
            self.__tree.go_left_child()
            self.__find(value)
            return

    def __insert(self, value: Any) -> None:
        assert(self.__tree.get_node_value() is _leaf)
        self.__tree.add_left_child(_ColoredValue(value, True))
        self.__tree.go_left_child()
        self.__tree.add_left_child(_leaf)
        self.__tree.go_parent()
        self.__tree.rotate_right()
        self.__rebalance_red()

    def __rebalance_red(self) -> None:
        self.__tree.go_parent()
        if self.__tree.get_go_status() == BinaryTree.GoStatus.NO_TARGET:
            self.__set_node_black()
            return
        if not self.__is_node_red():
            return
        assert(not self.__tree.is_node_root())
        if self.__is_uncle_red():
            self.__set_node_black()
            self.__go_brother()
            self.__set_node_black()
            self.__tree.go_parent()
            self.__set_node_red()
            self.__rebalance_red()
            return
        self.__tree.go_parent()
        self.__tree.rotate_right()

    def __is_node_red(self) -> bool:
        return self.__tree.get_node_value().is_red

    def __go_brother(self) -> None:
        if self.__tree.is_node_left_child():
            self.__tree.go_parent()
            self.__tree.go_right_child()
            return
        self.__tree.go_parent()
        self.__tree.go_left_child()

    def __set_node_black(self) -> None:
        cv = self.__tree.get_node_value()
        self.__tree.set_node_value(_ColoredValue(cv.value, False))

    def __set_node_red(self) -> None:
        cv = self.__tree.get_node_value()
        self.__tree.set_node_value(_ColoredValue(cv.value, True))

    def __is_uncle_red(self) -> bool:
        assert(not self.__tree.is_node_root())
        if self.__tree.is_node_left_child():
            self.__tree.go_parent()
            self.__tree.go_right_child()
            is_red = self.__is_node_red()
            self.__tree.go_parent()
            self.__tree.go_left_child()
            return is_red
        self.__tree.go_parent()
        self.__tree.go_left_child()
        is_red = self.__is_node_red()
        self.__tree.go_parent()
        self.__tree.go_right_child()
        return is_red


    def __check_tree(self) -> None:
        self.__tree.go_root()
        leaf_black_depth: list[Optional[int]] = [None]
        self.__check_black(0, leaf_black_depth)

    def __check_black(self, black_depth: int, leaf_black_depth: list[Optional[int]]) -> None:
        assert(not self.__tree.get_node_value().is_red)
        if self.__tree.get_node_value() is _leaf:
            self.__check_leaf(black_depth + 1, leaf_black_depth)
            return
        self.__tree.go_left_child()
        self.__check_node(black_depth + 1, leaf_black_depth)
        self.__tree.go_parent()
        self.__tree.go_right_child()
        self.__check_node(black_depth + 1, leaf_black_depth)
        self.__tree.go_parent()
    
    def __check_red(self, black_depth: int, leaf_black_depth: list[Optional[int]]) -> None:
        assert(self.__tree.get_node_value().is_red)
        self.__tree.go_left_child()
        self.__check_black(black_depth, leaf_black_depth)
        self.__tree.go_parent()
        self.__tree.go_right_child()
        self.__check_black(black_depth, leaf_black_depth)
        self.__tree.go_parent()

    def __check_node(self, black_depth: int, leaf_black_depth: list[Optional[int]]) -> None:
        if self.__tree.get_node_value().is_red:
            self.__check_red(black_depth, leaf_black_depth)
            return
        self.__check_black(black_depth, leaf_black_depth)

    def __check_leaf(self, black_depth: int, leaf_black_depth: list[Optional[int]]) -> None:
        if leaf_black_depth[0] is None:
            leaf_black_depth[0] = black_depth
            return
        assert(black_depth == leaf_black_depth[0])
