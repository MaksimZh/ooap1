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

def _make_left_child(parent: Node, child: Optional[Node]):
    parent.set_left_child(child)
    if child is not None:
        child.set_parent(parent)

def _make_right_child(parent: Node, child: Optional[Node]):
    parent.set_right_child(child)
    if child is not None:
        child.set_parent(parent)

def _replace_child(old: Node, new: Optional[Node]):
    parent = old.get_parent()
    assert(parent is not None)
    if parent.get_left_child() is old:
        _make_left_child(parent, new)
    else:
        _make_right_child(parent, new)


class BinaryTree:

    class __Vacancy(Node):

        def __init__(self) -> None:
            super().__init__(None)


    __root_parent: Node
    __cursor: Node
    __size: int
    __saved_cursors: dict[str, Node]


    # КОНСТРУКТОР
    # постусловие: создано пустое дерево
    def __init__(self) -> None:
        self.__root_parent = self.__Vacancy()
        self.__cursor = self.__Vacancy()
        _make_left_child(self.__root_parent, self.__cursor)
        self.__size = 0
        self.__saved_cursors = dict()
        self.__go_status = self.GoStatus.NIL
        self.__get_node_value_status = self.GetNodeValueStatus.NIL
        self.__delete_status = self.DeleteStatus.NIL
        self.__rotate_status = self.RotateStatus.NIL


    # КОМАНДЫ

    # задать значение текущему узлу
    # постусловие: в положении курсора находится узел с заданным значением
    def put(self, value: Any) -> None:
        if self.is_on_node():
            self.__cursor.set_value(value)
            return
        node = Node(value)
        _replace_child(self.__cursor, node)
        _make_left_child(node, self.__cursor)
        _make_right_child(node, self.__Vacancy())
        self.__cursor = node
        self.__size += 1


    # переместить курсор на корень дерева
    # постусловие: курсор перемещён в корень дерева
    def to_root(self) -> None:
        root = self.__root_parent.get_left_child()
        assert(root is not None)
        self.__cursor = root

    # переместить курсор к родителю текущего узла
    # предусловие: у текущего узла есть родитель
    # постусловие: курсор перемещён к родителю текущего узла
    def go_parent(self) -> None:
        self.__go(self.__cursor.get_parent())


    # переместить курсор к левому потомку текущего узла
    # предусловие: у текущего узла есть левый потомок
    # постусловие: курсор перемещён к левому потомку текущего узла
    def go_left_child(self) -> None:
        self.__go(self.__cursor.get_left_child())

    # переместить курсор к правому потомку текущего узла
    # предусловие: дерево не пустое
    # предусловие: у текущего узла есть правый потомок
    # постусловие: курсор перемещён к правому потомку текущего узла
    def go_right_child(self) -> None:
        self.__go(self.__cursor.get_right_child())

    class GoStatus(Enum):
        NIL = auto(),       # команда не выполнялась
        OK = auto(),        # успех
        NO_TARGET = auto(), # нет узла в заданном направлении

    __go_status: GoStatus

    def get_go_status(self) -> GoStatus:
        return self.__go_status

    
    # удалить текущий узел
    # предусловие: курсор не установлен на вакансию
    # предусловие: хотя бы один из потомков текущего узла - вакансия
    # постусловие: текущий узел удалён
    # постусловие: курсор сохраняет положение относительно вышестоящих узлов
    def delete(self) -> None:
        if not self.is_on_node():
            self.__delete_status = self.DeleteStatus.NOT_NODE
            return
        node = self.__cursor
        left = self.__cursor.get_left_child()
        right = self.__cursor.get_right_child()
        if isinstance(right, self.__Vacancy):
            _replace_child(right, None)
            _replace_child(node, left)
            self.__forget_this_cursor()
            assert(left is not None)
            self.__cursor = left
            self.__size -= 1
            self.__delete_status = self.DeleteStatus.OK
            return
        if isinstance(left, self.__Vacancy):
            _replace_child(left, None)
            _replace_child(node, right)
            self.__forget_this_cursor()
            assert(right is not None)
            self.__cursor = right
            self.__size -= 1
            self.__delete_status = self.DeleteStatus.OK
            return
        self.__delete_status = self.DeleteStatus.TWO_CHILDREN

    class DeleteStatus(Enum):
        NIL = auto(),          # команда не выполнялась
        OK = auto(),           # успех
        NOT_NODE = auto(),     # курсор на вакансии
        TWO_CHILDREN = auto(), # у узла два потомка

    __delete_status: DeleteStatus

    def get_delete_status(self) -> DeleteStatus:
        return self.__delete_status


    # повернуть дерево вправо на текущем узле
    # предусловие: курсор не на вакансии
    # предусловие: у текущего узла есть левый потомок
    # постусловие: левый потомок занял место текущего узла
    #              текущий узел стал правым потомком своего левого потомка
    #              правый потомок левого потомка текущего узла стал левым потомком текущего узла
    def rotate_right(self) -> None:
        if not self.is_on_node():
            self.__rotate_status = self.RotateStatus.NOT_NODE
            return
        if isinstance(self.__cursor.get_left_child(), self.__Vacancy):
            self.__rotate_status = self.RotateStatus.NO_PROPER_CHILD
            return
        top = self.__cursor
        assert(top is not None)
        left = top.get_left_child()
        assert(left is not None)
        right_of_left = left.get_right_child()
        self.__cursor = left
        _replace_child(top, left)
        left.set_right_child(top)
        top.set_parent(left)
        top.set_left_child(right_of_left)
        if right_of_left is not None:
            right_of_left.set_parent(top)
        self.__rotate_status = self.RotateStatus.OK

    # повернуть дерево влево на текущем узле
    # предусловие: курсор не на вакансии
    # предусловие: у текущего узла есть правый потомок
    # постусловие: правый потомок занял место текущего узла
    #              текущий узел стал левым потомком своего правого потомка
    #              левый потомок правого потомка текущего узла стал правым потомком текущего узла
    def rotate_left(self) -> None:
        if not self.is_on_node():
            self.__rotate_status = self.RotateStatus.NOT_NODE
            return
        if isinstance(self.__cursor.get_right_child(), self.__Vacancy):
            self.__rotate_status = self.RotateStatus.NO_PROPER_CHILD
            return
        top = self.__cursor
        assert(top is not None)
        right = top.get_right_child()
        assert(right is not None)
        left_of_right = right.get_left_child()
        self.__cursor = right
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
        NOT_NODE = auto(),        # курсор на вакансии
        NO_PROPER_CHILD = auto(), # нет потомка чтобы заменить текущий узел

    __rotate_status: RotateStatus

    def get_rotate_status(self) -> RotateStatus:
        return self.__rotate_status


    # сохранить положение курсора
    # постусловие: положение курсора сохранено под заданным именем
    def save_cursor(self, name: str) -> None:
        self.__saved_cursors[name] = self.__cursor

    # переместить курсор к сохранённому положению
    # предусловие: узел сохранённого положения присутствует в дереве
    # постусловие: курсор перемещён к сохранённому положению
    def go_saved(self, name: str) -> None:
        if name not in self.__saved_cursors:
            self.__go_status = self.GoStatus.NO_TARGET
            return
        self.__cursor = self.__saved_cursors[name]
        self.__go_status = self.GoStatus.OK


    # ЗАПРОСЫ

    # получить количество узлов
    def get_size(self) -> int:
        return self.__size

    # проверить установлен ли курсор на реальный узел
    def is_on_node(self) -> bool:
        return not isinstance(self.__cursor, self.__Vacancy)

    # проверить установлен ли курсор на корень дерева
    def is_on_root(self) -> bool:
        return self.__cursor.get_parent() is self.__root_parent

    # проверить установлен ли курсор на левого потомка
    def is_on_left_child(self) -> bool:
        if self.get_size() == 0:
            return False
        if self.is_on_root():
            return False
        parent = self.__cursor.get_parent()
        assert(parent is not None)
        return parent.get_left_child() is self.__cursor

    # проверить установлен ли курсор на правого потомка
    def is_on_right_child(self) -> bool:
        if self.get_size() == 0:
            return False
        if self.is_on_root():
            return False
        parent = self.__cursor.get_parent()
        assert(parent is not None)
        return parent.get_right_child() is self.__cursor

    # получить значение текущего узла
    # предусловие: дерево не пусто
    def get_node_value(self) -> Any:
        if self.get_size() == 0:
            self.__get_node_value_status = self.GetNodeValueStatus.NOT_NODE
            return
        assert(self.__cursor is not None)
        self.__get_node_value_status = self.GetNodeValueStatus.OK
        return self.__cursor.get_value()

    class GetNodeValueStatus(Enum):
        NIL = auto(),
        OK = auto(),
        NOT_NODE = auto(),

    __get_node_value_status: GetNodeValueStatus

    def get_get_node_value_status(self) -> GetNodeValueStatus:
        return self.__get_node_value_status

    
    def __go(self, target: Optional[Node]) -> None:
        if target is None or target is self.__root_parent:
            self.__go_status = self.GoStatus.NO_TARGET
            return
        self.__cursor = target
        self.__go_status = self.GoStatus.OK

    def __forget_this_cursor(self) -> None:
        if self.__cursor in self.__saved_cursors.values():
            index = list(self.__saved_cursors.values()).index(self.__cursor)
            name = list(self.__saved_cursors.keys())[index]
            del self.__saved_cursors[name]


class _ColoredValue(NamedTuple):
    value: Any
    is_red: bool


class RedBlackTree:

    __tree: BinaryTree

    # КОНСТРУКТОР
    # постусловие: создано дерево, состоящее из единственного пустого узла
    def __init__(self) -> None:
        self.__tree = BinaryTree()
        self.__get_status = self.GetStatus.NIL
        self.__delete_status = self.DeleteStatus.NIL


    # КОМАНДЫ

    # добавить или заменить узел с заданным значением
    # постусловие: если равное значение присутствовало, то оно заменено новым
    #              если равное значение отсутствует, то новое значение добавлено
    # постусловие: дерево соответствует требованиям красно-чёрного дерева
    def put(self, value: Any) -> None:
        self.__tree.to_root()
        self.__find(value)
        if self.__tree.is_on_node():
            cv = self.__tree.get_node_value()
            self.__tree.put(_ColoredValue(value, cv.is_red))
            return
        self.__insert(value)
        if __debug__:
            self.__check_tree()


    # удалить узел с заданным значением
    # предусловие: узел со значением равным заданному присутствует
    # постусловие: узел со значением равным заданному удалён
    # постусловие: дерево соответствует требованиям красно-чёрного дерева
    def delete(self, value: Any) -> None:
        self.__tree.to_root()
        self.__find(value)
        if not self.__tree.is_on_node():
            self.__delete_status = self.DeleteStatus.NOT_FOUND
            return
        self.__delete()
        self.__delete_status = self.DeleteStatus.OK
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
        return self.__tree.get_size()

    # проверить присутствует ли значение в дереве
    def has_value(self, value: Any) -> bool:
        self.__tree.to_root()
        self.__find(value)
        return self.__tree.is_on_node()

    # получить значение узла со значением равным заданному
    # предусловие: узел со значением равным заданному присутствует
    def get(self, value: Any) -> Any:
        self.__tree.to_root()
        self.__find(value)
        if not self.__tree.is_on_node():
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
        if not self.__tree.is_on_node():
            return
        cv: _ColoredValue = self.__tree.get_node_value()
        if cv.value < value:
            self.__tree.go_right_child()
            self.__find(value)
            return
        if cv.value > value:
            self.__tree.go_left_child()
            self.__find(value)
            return

    def __insert(self, value: Any) -> None:
        assert(not self.__tree.is_on_node())
        self.__tree.put(_ColoredValue(value, True))
        self.__rebalance_red()

    def __delete(self) -> None:
        if self.__node_has_two_children():
            self.__tree.save_cursor("node")
            self.__find_replacement()
            self.__tree.save_cursor("replacement")
            value = self.__tree.get_node_value().value
            self.__tree.go_saved("node")
            is_red = self.__tree.get_node_value().is_red
            self.__tree.put(_ColoredValue(value, is_red))
            self.__tree.go_saved("replacement")
            self.__delete()
            return
        if self.__is_node_red():
            self.__tree.delete()
            return
        self.__tree.delete()
        if self.__is_node_red():
            self.__set_node_red(False)
            return
        self.__rebalance_double_black()

    def __node_has_two_children(self) -> bool:
        self.__tree.go_left_child()
        if not self.__tree.is_on_node():
            self.__tree.go_parent()
            return False
        self.__tree.go_parent()
        self.__tree.go_right_child()
        if not self.__tree.is_on_node():
            self.__tree.go_parent()
            return False
        self.__tree.go_parent()
        return True

    def __find_replacement(self) -> None:
        self.__tree.go_right_child()
        self.__tree.go_left_child()
        while self.__tree.is_on_node():
            self.__tree.go_left_child()
        self.__tree.go_parent()


    def __rebalance_red(self) -> None:
        if self.__tree.is_on_root():
            self.__set_node_red(False)
            return
        self.__tree.go_parent()
        if not self.__is_node_red():
            return
        if self.__is_brother_red():
            self.__set_node_red(False)
            self.__go_brother()
            self.__set_node_red(False)
            self.__tree.go_parent()
            self.__set_node_red(True)
            self.__rebalance_red()
            return
        if self.__tree.is_on_left_child():
            self.__rebalance_red_left()
            return
        self.__rebalance_red_right()

    def __rebalance_red_left(self) -> None:
        self.__set_node_red(False)
        self.__tree.go_parent()
        self.__set_node_red(True)
        self.__tree.rotate_right()

    def __rebalance_red_right(self) -> None:
        self.__set_node_red(False)
        self.__tree.go_parent()
        self.__set_node_red(True)
        self.__tree.rotate_left()

    def __rebalance_double_black(self) -> None:
        if self.__tree.is_on_root():
            return
        if self.__is_brother_red():
            self.__rebalace_db_red_brother()
            return
        if self.__tree.is_on_left_child():
            self.__rebalace_db_black_brother_left()

    def __rebalace_db_red_brother(self) -> None:
        if self.__tree.is_on_left_child():
            self.__tree.go_parent()
            self.__set_node_red(True)
            self.__tree.go_right_child()
            self.__set_node_red(False)
            self.__tree.go_parent()
            self.__tree.rotate_left()
            return
        self.__tree.go_parent()
        self.__set_node_red(True)
        self.__tree.go_left_child()
        self.__set_node_red(False)
        self.__tree.go_parent()
        self.__tree.rotate_right()

    def __rebalace_db_black_brother_left(self) -> None:
        self.__tree.go_parent()
        self.__tree.go_right_child()
        self.__tree.go_right_child()
        if self.__is_node_red():
            self.__tree.go_parent()
            self.__tree.go_parent()
            is_red_parent = self.__is_node_red()
            self.__set_node_red(False)
            self.__tree.rotate_left()
            self.__set_node_red(is_red_parent)
            return
        self.__tree.go_parent()
        self.__tree.go_left_child()
        if self.__is_node_red():
            self.__set_node_red(False)
            self.__tree.go_parent()
            self.__set_node_red(True)
            self.__tree.rotate_right()
            return
        self.__tree.go_parent()
        self.__set_node_red(True)
        self.__tree.go_parent()
        self.__set_node_red(False)
        self.__rebalance_double_black()


    def __is_node_red(self) -> bool:
        return self.__tree.is_on_node() and self.__tree.get_node_value().is_red

    def __go_brother(self) -> None:
        if self.__tree.is_on_left_child():
            self.__tree.go_parent()
            self.__tree.go_right_child()
            return
        self.__tree.go_parent()
        self.__tree.go_left_child()

    def __set_node_red(self, is_red: bool) -> None:
        cv = self.__tree.get_node_value()
        self.__tree.put(_ColoredValue(cv.value, is_red))

    def __is_brother_red(self) -> bool:
        self.__go_brother()
        is_red = self.__is_node_red()
        self.__go_brother()
        return is_red


    def __check_tree(self) -> None:
        self.__tree.to_root()
        leaf_black_depth: list[Optional[int]] = [None]
        self.__check_black(0, leaf_black_depth)

    def __check_black(self, black_depth: int, leaf_black_depth: list[Optional[int]]) -> None:
        assert(not self.__is_node_red())
        if not self.__tree.is_on_node():
            self.__check_leaf(black_depth + 1, leaf_black_depth)
            return
        self.__tree.go_left_child()
        self.__check_node(black_depth + 1, leaf_black_depth)
        self.__tree.go_parent()
        self.__tree.go_right_child()
        self.__check_node(black_depth + 1, leaf_black_depth)
        self.__tree.go_parent()
    
    def __check_red(self, black_depth: int, leaf_black_depth: list[Optional[int]]) -> None:
        assert(self.__is_node_red())
        self.__tree.go_left_child()
        self.__check_black(black_depth, leaf_black_depth)
        self.__tree.go_parent()
        self.__tree.go_right_child()
        self.__check_black(black_depth, leaf_black_depth)
        self.__tree.go_parent()

    def __check_node(self, black_depth: int, leaf_black_depth: list[Optional[int]]) -> None:
        if self.__is_node_red():
            self.__check_red(black_depth, leaf_black_depth)
            return
        self.__check_black(black_depth, leaf_black_depth)

    def __check_leaf(self, black_depth: int, leaf_black_depth: list[Optional[int]]) -> None:
        if leaf_black_depth[0] is None:
            leaf_black_depth[0] = black_depth
            return
        assert(black_depth == leaf_black_depth[0])


class Item:
    key: str
    value: Any

    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value
    
    def __eq__(self, o: object) -> bool:
        assert(isinstance(o, Item))
        return self.key == o.key

    def __gt__(self, o: object) -> bool:
        assert(isinstance(o, Item))
        return self.key > o.key

    
class NativeDictionary:

    __tree: RedBlackTree

    
    # КОНСТРУКТОР
    # постусловие: создан пустой ассоциативный массив
    def __init__(self) -> None:
        self.__tree = RedBlackTree()
        self.__get_status = self.GetStatus.NIL
        self.__delete_status = self.DeleteStatus.NIL
    
    
    # КОМАНДЫ

    # записать значение в массив под заданным ключом
    # постусловие: если ключ уже есть в массиве - записать под ним заданное значение
    #              иначе добавить пару ключ-значение в массив 
    def put(self, key: str, value: Any) -> None:
        self.__tree.put(Item(key, value))


    # удалить элемент с заданным ключом из массива
    # предусловие: ключ содержится в массиве
    # постусловие: из массива удалён элемент с заданным ключом
    def delete(self, key: str) -> None:
        self.__tree.delete(Item(key, None))
        if self.__tree.get_delete_status() == RedBlackTree.DeleteStatus.NOT_FOUND:
            self.__delete_status = self.DeleteStatus.NOT_FOUND
            return
        self.__delete_status = self.DeleteStatus.OK

    class DeleteStatus(Enum):
        NIL = auto(),       # команда не выполнялась
        OK = auto(),        # успех
        NOT_FOUND = auto(), # ключ не найден

    __delete_status: DeleteStatus

    def get_delete_status(self) -> DeleteStatus:
        return self.__delete_status

    
    # ЗАПРОСЫ

    # получить количество записей в массиве
    def get_size(self) -> int:
        return self.__tree.get_size()

    # проверить содержится ли ключ в массиве
    def has_key(self, key: str) -> bool:
        return self.__tree.has_value(Item(key, None))

    # получить значение по заданному ключу
    # предусловие: ключ содержится в массиве
    def get(self, key: str) -> Any:
        item = self.__tree.get(Item(key, None))
        if self.__tree.get_get_status() == RedBlackTree.GetStatus.NOT_FOUND:
            self.__get_status = self.GetStatus.NOT_FOUND
            return None
        self.__get_status = self.GetStatus.OK
        return item.value

    class GetStatus(Enum):
        NIL = auto(),       # запрос не выполнялся
        OK = auto(),        # успех
        NOT_FOUND = auto(), # ключ не найден

    __get_status: GetStatus

    def get_get_status(self) -> GetStatus:
        return self.__get_status
