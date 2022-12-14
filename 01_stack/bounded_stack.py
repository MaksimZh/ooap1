from typing import Any

class BoundedStack:

    __peek_status: int
    __pop_status: int

    PUSH_NIL: int = 0
    POP_NIL: int = 0
    POP_ERR: int = 2
    PEEK_NIL: int = 0
    PEEK_ERR: int = 2

    def __init__(self, max_size: int = 32):
        self.__pop_status = self.POP_NIL
        self.__peek_status = self.PEEK_NIL

    def pop(self) -> None:
        self.__pop_status = self.POP_ERR

    def peek(self) -> Any:
        self.__peek_status = self.PEEK_ERR
        return 0

    def size(self) -> int:
        return 0

    def get_push_status(self) -> int:
        return self.PUSH_NIL

    def get_pop_status(self) -> int:
        return self.__pop_status

    def get_peek_status(self) -> int:
        return self.__peek_status
