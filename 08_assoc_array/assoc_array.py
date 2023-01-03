from typing import Any, Optional
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


def _replace_child(old: Node, new: Node):
    parent = old.get_parent()
    assert(parent is not None)
    if parent.get_left_child() is old:
        parent.set_left_child(new)
    else:
        parent.set_right_child(new)
    new.set_parent(parent)


class BinaryTree:

    __root: Optional[Node]
    __current: Optional[Node]
    __size: int


    # КОНСТРУКТОР
    # постусловие: создано пустое дерево
    def __init__(self) -> None:
        self.__root = None
        self.__current = None
        self.__size = 0
        self.__add_root_status = self.AddRootStatus.NIL
        self.__add_child_status = self.AddChildStatus.NIL
        self.__go_status = self.GoStatus.NIL
        self.__get_node_value_status = self.GetNodeValueStatus.NIL
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
        self.__root = Node(value)
        self.__current = self.__root
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
        self.__go(self.__root)

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
        if top is self.__root:
            left.set_parent(None)
            self.__root = left
        else:
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
        if top is self.__root:
            right.set_parent(None)
            self.__root = right
        else:
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
        if target is None:
            self.__go_status = self.GoStatus.NO_TARGET
            return
        self.__current = target
        self.__go_status = self.GoStatus.OK


"""
class _EmptyNode(Node):
    def __init__(self) -> None:
        super().__init__("", None, Node.Color.BLACK)

def _is_empty_node(node: Node) -> bool:
    assert(node is not None)
    return isinstance(node, _EmptyNode)


class RedBlackTree:
    
    __root: Node
    __cursor: Node
    __size: int
    
    # КОНСТРУКТОР
    # постусловие: создано дерево, состоящее из единственного пустого узла
    def __init__(self) -> None:
        self.__root = _EmptyNode()
        self.__cursor = self.__root
        self.__size = 0
        self.__go_status = self.GoStatus.NIL
        self.__new_node_status = self.NewNodeStatus.NIL
        self.__get_node_key_status = self.GetNodeKeyStatus.NIL
        self.__get_node_value_status = self.GetNodeValueStatus.NIL


    # КОМАНДЫ

    # создать узел с заданным ключом и цветом
    def new_node(self, key: str, color: Node.Color) -> None:
        if not _is_empty_node(self.__cursor):
            self.__new_node_status = self.NewNodeStatus.NOT_EMPTY_NODE
            return
        self.__new_node_status = self.NewNodeStatus.OK
        if self.get_size() == 0:
            self.__new_root(key, color)
            return
        self.__new_branch(key, color)
    
    class NewNodeStatus(Enum):
        NIL = auto(),            # команда не выполнялась
        OK = auto(),             # узел создан
        NOT_EMPTY_NODE = auto(), # курсор стоит на непустом узле

    __new_node_status: NewNodeStatus

    def get_new_node_status(self) -> NewNodeStatus:
        return self.__new_node_status

    def to_root(self) -> None:
        self.__cursor = self.__root

    def go_parent(self) -> None:
        self._go(self.__cursor.get_parent())

    def go_left_child(self) -> None:
        self._go(self.__cursor.get_left_child())

    def go_right_child(self) -> None:
        self._go(self.__cursor.get_right_child())


    # ЗАПРОСЫ

    # получить количество непустых узлов
    def get_size(self) -> int:
        return self.__size

    # узнать является ли данный узел пустым
    def node_is_empty(self) -> bool:
        return _is_empty_node(self.__cursor)

    # получить ключ текущего узла
    def get_node_key(self) -> str:
        self.__get_node_key_status = self.GetNodeKeyStatus.EMPTY_NODE
        return ""

    class GetNodeKeyStatus(Enum):
        NIL = auto(),
        OK = auto(),
        EMPTY_NODE = auto(),

    __get_node_key_status: GetNodeKeyStatus

    def get_get_node_key_status(self) -> GetNodeKeyStatus:
        return self.__get_node_key_status


    # получить значение текущего узла
    def get_node_value(self) -> Any:
        self.__get_node_value_status = self.GetNodeValueStatus.EMPTY_NODE
        return None

    class GetNodeValueStatus(Enum):
        NIL = auto(),
        OK = auto(),
        EMPTY_NODE = auto(),

    __get_node_value_status: GetNodeValueStatus

    def get_get_node_value_status(self) -> GetNodeValueStatus:
        return self.__get_node_value_status


    def __new_root(self, key: str, color: Node.Color) -> None:
        assert(_is_empty_node(self.__cursor))
        assert(self.__cursor is self.__root)
        assert(self.get_size() == 0)
        left = self.__root
        right = _EmptyNode()
        node = Node(key, None, color)
        node.set_left_child(left)
        left.set_parent(node)
        node.set_right_child(right)
        right.set_parent(node)
        self.__root = node
        self.__cursor = node
        self.__size += 1

    def __new_branch(self, key: str, color: Node.Color) -> None:
        assert(_is_empty_node(self.__cursor))
        left = self.__cursor
        right = _EmptyNode()
        parent = self.__cursor.get_parent()
        assert(parent is not None)
        node = Node(key, None, color)
        if parent.get_left_child() is left:
            parent.set_left_child(node)
        else:
            parent.set_right_child(node)
        node.set_parent(parent)
        node.set_left_child(left)
        left.set_parent(node)
        node.set_right_child(right)
        right.set_parent(node)
        self.__cursor = node
        self.__size += 1

    def _go(self, target: Optional["Node"]) -> None:
        if target is None:
            self.__go_status = self.GoStatus.NO_WAY
            return
        self.__cursor = target
        self.__go_status = self.GoStatus.OK
"""