from enum import Enum
from abc import ABC

class ParentList(ABC):

    class HeadStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    def get_head_status(self) -> HeadStatus:
        return self.HeadStatus.NIL
    
    class TailStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    def get_tail_status(self) -> TailStatus:
        return self.TailStatus.NIL

    class RightStatus(Enum):
        NIL = 0,
        OK = 1,
        NO_RIGHT_NEIGHBOR = 2,

    def get_right_status(self) -> RightStatus:
        return self.RightStatus.NIL

    class PutRightStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    def get_put_right_status(self) -> PutRightStatus:
        return self.PutRightStatus.NIL

    class PutLeftStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    def get_put_left_status(self) -> PutLeftStatus:
        return self.PutLeftStatus.NIL

    class RemoveStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    def get_remove_status(self) -> RemoveStatus:
        return self.RemoveStatus.NIL

    class ReplaceStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    def get_replace_status(self) -> ReplaceStatus:
        return self.ReplaceStatus.NIL

    class FindStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    def get_find_status(self) -> FindStatus:
        return self.FindStatus.NIL

    class GetStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    def get_get_status(self) -> GetStatus:
        return self.GetStatus.NIL

    def size(self) -> int:
        return 0

    def is_head(self) -> bool:
        return False

    def is_tail(self) -> bool:
        return False

    def is_value(self) -> bool:
        return False


class LinkedList(ParentList):
    pass

class TwoWayList(ParentList):
    pass
