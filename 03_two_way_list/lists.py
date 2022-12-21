from enum import Enum
from abc import ABC
from typing import Any, Optional


class ParentList(ABC):
    
    class _Node:
        next: Optional["ParentList._Node"]
        prev: Optional["ParentList._Node"]

        def __init__(self) -> None:
            self.next = None
            self.prev = None

        def join_right(self, node: "ParentList._Node") -> None:
            self.next = node
            node.prev = self


    class _ValueNode(_Node):
        value: Any

        def __init__(self, value: Any) -> None:
            super().__init__()
            self.value = value


    __pre_head: _Node
    __post_tail: _Node
    _cursor: Optional[_ValueNode]
    __size: int

    # конструктор:
    # постусловие: создан новый пустой список
    def __init__(self) -> None:
        super().__init__()
        self.__pre_head = self._Node()
        self.__post_tail = self._Node()
        self.clear()


    # Команды и запросы статусов:

    # предусловие: список не пуст
    # постусловие: курсор установлен на первый узел в списке
    def head(self) -> None:
        if self.size() == 0:
            self.__head_status = self.HeadStatus.EMPTY
            return
        assert(isinstance(self.__pre_head.next, self._ValueNode))
        self._cursor = self.__pre_head.next
        self.__head_status = self.HeadStatus.OK

    class HeadStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __head_status: HeadStatus

    def get_head_status(self) -> HeadStatus:
        return self.__head_status

    # предусловие: список не пуст
    # постусловие: курсор установлен на последний узел в списке
    def tail(self) -> None:
        if self.size() == 0:
            self.__tail_status = self.TailStatus.EMPTY
            return
        assert(isinstance(self.__post_tail.prev, self._ValueNode))
        self._cursor = self.__post_tail.prev
        self.__tail_status = self.TailStatus.OK

    class TailStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __tail_status: TailStatus

    def get_tail_status(self) -> TailStatus:
        return self.__tail_status


    # предусловие: список не пуст
    # предусловие: правее курсора есть элемент
    # постусловие: курсор сдвинут на один узел вправо
    def right(self) -> None:
        if self._cursor is None:
            self.__right_status = self.RightStatus.NO_RIGHT_NEIGHBOR
            return
        assert(self._cursor.next is not None)
        if not isinstance(self._cursor.next, self._ValueNode):
            self.__right_status = self.RightStatus.NO_RIGHT_NEIGHBOR
            return
        self._cursor = self._cursor.next
        self.__right_status = self.RightStatus.OK

    class RightStatus(Enum):
        NIL = 0,
        OK = 1,
        NO_RIGHT_NEIGHBOR = 2,
    
    __right_status: RightStatus

    def get_right_status(self) -> RightStatus:
        return self.__right_status

    # предусловие: список не пуст
    # постусловие: справа от текущего узла добавлен новый узел с заданным значением
    def put_right(self, value: Any) -> None:
        if self.size() == 0:
            self.__put_right_status = self.PutRightStatus.EMPTY
            return
        node = self._ValueNode(value)
        assert(self._cursor is not None)
        assert(self._cursor.next is not None)
        node.join_right(self._cursor.next)
        self._cursor.join_right(node)
        self.__size += 1
        self.__put_right_status = self.PutRightStatus.OK

    class PutRightStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __put_right_status: PutRightStatus

    def get_put_right_status(self) -> PutRightStatus:
        return self.__put_right_status


    # предусловие: список не пуст
    # постусловие: слева от текущего узла добавлен новый узел с заданным значением
    def put_left(self, value: Any) -> None:
        if self.size() == 0:
            self.__put_left_status = self.PutLeftStatus.EMPTY
            return
        node = self._ValueNode(value)
        assert(self._cursor is not None)
        assert(self._cursor.prev is not None)
        self._cursor.prev.join_right(node)
        node.join_right(self._cursor)
        self.__size += 1
        self.__put_left_status = self.PutLeftStatus.OK

    class PutLeftStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __put_left_status: PutLeftStatus

    def get_put_left_status(self) -> PutLeftStatus:
        return self.__put_left_status

    # предусловие: список не пуст
    # постусловие: текущий узел удалён
    #              если есть правый сосед - курсор смещён к нему
    #              иначе если есть левый сосед - курсор смещён к нему
    def remove(self) -> None:
        if self.size() == 0:
            self.__remove_status = self.RemoveStatus.EMPTY
            return
        assert(self._cursor is not None)
        assert(self._cursor.prev is not None)
        assert(self._cursor.next is not None)
        self._cursor.prev.join_right(self._cursor.next)
        if isinstance(self._cursor.next, self._ValueNode):
            self._cursor = self._cursor.next
        elif isinstance(self._cursor.prev, self._ValueNode):
            self._cursor = self._cursor.prev
        else:
            self._cursor = None
        self.__size -= 1
        self.__remove_status = self.RemoveStatus.OK


    class RemoveStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __remove_status: RemoveStatus

    def get_remove_status(self) -> RemoveStatus:
        return self.__remove_status

    # предусловие: список не пуст
    # постусловие: значение текущего узла заменено на заданное
    def replace(self, value: Any) -> None:
        if self.size() == 0:
            self.__replace_status = self.ReplaceStatus.EMPTY
            return
        assert(self._cursor is not None)
        self._cursor.value = value
        self.__replace_status = self.ReplaceStatus.OK

    class ReplaceStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __replace_status: ReplaceStatus

    def get_replace_status(self) -> ReplaceStatus:
        return self.__replace_status


    # постусловие: курсор установлен на следующий узел с заданным значением
    #              если такой узел найден
    def find(self, value: Any) -> None:
        if self.size() == 0:
            self.__find_status = self.FindStatus.NOT_FOUND
            return
        node = self._cursor
        while isinstance(node, self._ValueNode):
            if node.value == value:
                self._cursor = node
                self.__find_status = self.FindStatus.OK
                return
            node = node.next
        self.__find_status = self.FindStatus.NOT_FOUND

    class FindStatus(Enum):
        NIL = 0,
        OK = 1,
        NOT_FOUND = 2,

    __find_status: FindStatus

    def get_find_status(self) -> FindStatus:
        return self.__find_status


    # постусловие: из списка удалены все элементы
    def clear(self) -> None:
        self.__pre_head.join_right(self.__post_tail)
        self._cursor = None
        self.__size = 0
        self.__head_status = self.HeadStatus.NIL
        self.__tail_status = self.TailStatus.NIL
        self.__right_status = self.RightStatus.NIL
        self.__put_right_status = self.PutRightStatus.NIL
        self.__put_left_status = self.PutLeftStatus.NIL
        self.__remove_status = self.RemoveStatus.NIL
        self.__replace_status = self.ReplaceStatus.NIL
        self.__find_status = self.FindStatus.NIL
        self.__get_status = self.GetStatus.NIL


    # постусловие: в конец списка добавлен элемент с заданным значением
    def add_tail(self, value: Any) -> None:
        node = self._ValueNode(value)
        assert(self.__post_tail.prev is not None)
        self.__post_tail.prev.join_right(node)
        node.join_right(self.__post_tail)
        self.__size += 1
        if self._cursor is None:
            self._cursor = node

    # постусловие: в списке удалены все элементы с заданным значением
    def remove_all(self, value: Any) -> None:
        if self.size() == 0:
            return
        self.head()
        self.find(value)
        while self.get_find_status() == self.FindStatus.OK:
            self.remove()
            assert(self.get_remove_status() == self.RemoveStatus.OK)
            self.find(value)

    # Запросы:
    
    # предусловие: список не пуст
    def get(self) -> Any:
        if self._cursor is None:
            self.__get_status = self.GetStatus.EMPTY
            return None
        self.__get_status = self.GetStatus.OK
        return self._cursor.value

    class GetStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __get_status: GetStatus

    def get_get_status(self) -> GetStatus:
        return self.__get_status


    def is_head(self) -> bool:
        return (self._cursor is not None) and (self._cursor.prev == self.__pre_head)

    def is_tail(self) -> bool:
        return (self._cursor is not None) and (self._cursor.next == self.__post_tail)

    def is_value(self) -> bool:
        return isinstance(self._cursor, self._ValueNode)

    def size(self) -> int:
        return self.__size


class LinkedList(ParentList):
    pass


class TwoWayList(ParentList):

    def __init__(self) -> None:
        super().__init__()
        self.__left_status = self.LeftStatus.NIL


    # предусловие: список не пуст
    # предусловие: левее курсора есть элемент
    # постусловие: курсор сдвинут на один узел влево
    def left(self) -> None:
        if self._cursor is None:
            self.__left_status = self.LeftStatus.NO_LEFT_NEIGHBOR
            return
        assert(self._cursor.prev is not None)
        if not isinstance(self._cursor.prev, self._ValueNode):
            self.__left_status = self.LeftStatus.NO_LEFT_NEIGHBOR
            return
        self._cursor = self._cursor.prev
        self.__left_status = self.LeftStatus.OK
    
    class LeftStatus(Enum):
        NIL = 0,
        OK = 1,
        NO_LEFT_NEIGHBOR = 2,

    __left_status: LeftStatus

    def get_left_status(self) -> LeftStatus:
        return self.__left_status
