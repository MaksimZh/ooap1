from enum import Enum
from abc import ABC
from typing import Any


class ParentList(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.clear()


    def head(self) -> None:
        self.__head_status = self.HeadStatus.EMPTY

    class HeadStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __head_status: HeadStatus

    def get_head_status(self) -> HeadStatus:
        return self.__head_status


    def tail(self) -> None:
        self.__tail_status = self.TailStatus.EMPTY

    class TailStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __tail_status: TailStatus

    def get_tail_status(self) -> TailStatus:
        return self.__tail_status


    def right(self) -> None:
        self.__right_status = self.RightStatus.NO_RIGHT_NEIGHBOR

    class RightStatus(Enum):
        NIL = 0,
        OK = 1,
        NO_RIGHT_NEIGHBOR = 2,
    
    __right_status: RightStatus

    def get_right_status(self) -> RightStatus:
        return self.__right_status


    def put_right(self, value: Any) -> None:
        self.__put_right_status = self.PutRightStatus.EMPTY

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
        self.__remove_status = self.RemoveStatus.EMPTY

    class RemoveStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __remove_status: RemoveStatus

    def get_remove_status(self) -> RemoveStatus:
        return self.__remove_status


    def replace(self, value: Any) -> None:
        self.__replace_status = self.ReplaceStatus.EMPTY

    class ReplaceStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __replace_status: ReplaceStatus

    def get_replace_status(self) -> ReplaceStatus:
        return self.__replace_status


    def find(self, value: Any) -> None:
        self.__find_status = self.FindStatus.NOT_FOUND

    class FindStatus(Enum):
        NIL = 0,
        OK = 1,
        NOT_FOUND = 2,

    __find_status: FindStatus

    def get_find_status(self) -> FindStatus:
        return self.__find_status


    def get(self) -> Any:
        self.__get_status = self.GetStatus.EMPTY

    class GetStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __get_status: GetStatus

    def get_get_status(self) -> GetStatus:
        return self.__get_status


    def clear(self) -> None:
        self.__head_status = self.HeadStatus.NIL
        self.__tail_status = self.TailStatus.NIL
        self.__right_status = self.RightStatus.NIL
        self.__put_right_status = self.PutRightStatus.NIL
        self.__put_left_status = self.PutLeftStatus.NIL
        self.__remove_status = self.RemoveStatus.NIL
        self.__replace_status = self.ReplaceStatus.NIL
        self.__find_status = self.FindStatus.NIL
        self.__get_status = self.GetStatus.NIL


    def is_head(self) -> bool:
        return False

    def is_tail(self) -> bool:
        return False

    def is_value(self) -> bool:
        return False

    def size(self) -> int:
        return 0


class LinkedList(ParentList):
    pass

class TwoWayList(ParentList):

    def __init__(self) -> None:
        super().__init__()
        self.__left_status = self.LeftStatus.NIL


    def left(self) -> None:
        self.__left_status = self.LeftStatus.NO_LEFT_NEIGHBOR

    class LeftStatus(Enum):
        NIL = 0,
        OK = 1,
        NO_LEFT_NEIGHBOR = 2,

    __left_status: LeftStatus

    def get_left_status(self) -> LeftStatus:
        return self.__left_status
