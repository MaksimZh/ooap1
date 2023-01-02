from typing import Any, Optional
from enum import Enum, auto


class Node:

    class Color(Enum):
        RED = auto(),
        BLACK = auto(),
    
    __key: str
    __value: Any
    __color: Color
    __parent: Optional["Node"]
    __left_child: Optional["Node"]
    __right_child: Optional["Node"]


    # КОНСТРУКТОР
    # постусловие: создан новый узел с заданным ключом, значением и цветом
    # постусловие: узел не связан ни с какими узлами
    def __init__(self, key: str, value: Any, color: Color) -> None:
        self.__key = key
        self.__value = value
        self.__color = color
        self.__parent = None
        self.__left_child = None
        self.__right_child = None


    # КОМАНДЫ

    # задать цвет узла
    # постусловие: цвет узла равен заданному
    def set_color(self, color: Color) -> None:
        self.__color = color

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
    
    # получить ключ узла
    def get_key(self) -> str:
        return self.__key

    # получить значение узла
    def get_value(self) -> Any:
        return self.__value

    # получить цвет узла
    def get_color(self) -> Any:
        return self.__color

    # получить родителя узла
    def get_parent(self) -> Optional["Node"]:
        return self.__parent

    # получить левого ребёнка узла
    def get_left_child(self) -> Optional["Node"]:
        return self.__left_child

    # получить правого ребёнка узла
    def get_right_child(self) -> Optional["Node"]:
        return self.__right_child


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


    class GoStatus(Enum):
        NIL = auto(),    # команда не выполнялась
        OK = auto(),     # успех
        NO_WAY = auto(), # нет узла в заданном направлении

    __go_status: GoStatus

    def get_go_status(self) -> GoStatus:
        return self.__go_status


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
