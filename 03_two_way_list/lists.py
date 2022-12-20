from enum import Enum
from abc import ABC
from typing import Any, Optional


class ParentList(ABC):
    
    class Node:
        next: Optional["ParentList.Node"]
        prev: Optional["ParentList.Node"]

        def __init__(self) -> None:
            self.next = None
            self.prev = None

        def join_right(self, node: "ParentList.Node") -> None:
            self.next = node
            node.prev = self


    class ValueNode(Node):
        value: Any

        def __init__(self, value: Any) -> None:
            super().__init__()
            self.value = value


    __pre_head: Node
    __post_tail: Node
    _cursor: Optional[ValueNode]
    __size: int

    def __init__(self) -> None:
        super().__init__()
        self.__pre_head = self.Node()
        self.__post_tail = self.Node()
        self.clear()


    def head(self) -> None:
        if self.size() == 0:
            self.__head_status = self.HeadStatus.EMPTY
            return
        assert(isinstance(self.__pre_head.next, self.ValueNode))
        self._cursor = self.__pre_head.next
        self.__head_status = self.HeadStatus.OK

    class HeadStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __head_status: HeadStatus

    def get_head_status(self) -> HeadStatus:
        return self.__head_status


    def tail(self) -> None:
        if self.size() == 0:
            self.__tail_status = self.TailStatus.EMPTY
            return
        assert(isinstance(self.__post_tail.prev, self.ValueNode))
        self._cursor = self.__post_tail.prev
        self.__tail_status = self.TailStatus.OK

    class TailStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __tail_status: TailStatus

    def get_tail_status(self) -> TailStatus:
        return self.__tail_status


    def right(self) -> None:
        if self._cursor is None:
            self.__right_status = self.RightStatus.NO_RIGHT_NEIGHBOR
            return
        assert(self._cursor.next is not None)
        if not isinstance(self._cursor.next, self.ValueNode):
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


    def put_right(self, value: Any) -> None:
        if self.size() == 0:
            self.__put_right_status = self.PutRightStatus.EMPTY
            return
        node = self.ValueNode(value)
        assert(self._cursor is not None)
        assert(self._cursor.next is not None)
        node.join_right(self._cursor.next)
        self._cursor.join_right(node)
        self.__put_right_status = self.PutRightStatus.OK

    class PutRightStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __put_right_status: PutRightStatus

    def get_put_right_status(self) -> PutRightStatus:
        return self.__put_right_status


    def put_left(self, value: Any) -> None:
        self.__put_left_status = self.PutLeftStatus.EMPTY

    class PutLeftStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __put_left_status: PutLeftStatus

    def get_put_left_status(self) -> PutLeftStatus:
        return self.__put_left_status


    def remove(self) -> None:
        if self.size() == 0:
            self.__remove_status = self.RemoveStatus.EMPTY
            return
        self.__size -= 1
        self.__remove_status = self.RemoveStatus.OK
        assert(self._cursor is not None)
        assert(self._cursor.prev is not None)
        assert(self._cursor.next is not None)
        self._cursor.prev.join_right(self._cursor.next)
        if isinstance(self._cursor.next, self.ValueNode):
            self._cursor = self._cursor.next
        elif isinstance(self._cursor.prev, self.ValueNode):
            self._cursor = self._cursor.prev
        else:
            self._cursor = None


    class RemoveStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __remove_status: RemoveStatus

    def get_remove_status(self) -> RemoveStatus:
        return self.__remove_status


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


    def find(self, value: Any) -> None:
        if self._cursor is None:
            self.__find_status = self.FindStatus.NOT_FOUND
            return
        node = self._cursor
        while isinstance(node, self.ValueNode):
            if node.value == value:
                self._cursor = node
                self.__find_status = self.FindStatus.OK
                return
            node = node.next

    class FindStatus(Enum):
        NIL = 0,
        OK = 1,
        NOT_FOUND = 2,

    __find_status: FindStatus

    def get_find_status(self) -> FindStatus:
        return self.__find_status


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


    def add_tail(self, value: Any) -> None:
        node = self.ValueNode(value)
        assert(self.__post_tail.prev is not None)
        self.__post_tail.prev.join_right(node)
        node.join_right(self.__post_tail)
        self.__size += 1
        if self._cursor is None:
            self._cursor = node


    def is_head(self) -> bool:
        return (self._cursor is not None) and (self._cursor.prev == self.__pre_head)

    def is_tail(self) -> bool:
        return (self._cursor is not None) and (self._cursor.next == self.__post_tail)

    def is_value(self) -> bool:
        return isinstance(self._cursor, self.ValueNode)

    def size(self) -> int:
        return self.__size


class LinkedList(ParentList):
    pass


class TwoWayList(ParentList):

    def __init__(self) -> None:
        super().__init__()
        self.__left_status = self.LeftStatus.NIL


    def left(self) -> None:
        if self._cursor is None:
            self.__left_status = self.LeftStatus.NO_LEFT_NEIGHBOR
            return
        assert(self._cursor.prev is not None)
        if not isinstance(self._cursor.prev, self.ValueNode):
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
