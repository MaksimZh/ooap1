from typing import Any

class BoundedStack:

    __stack: list[Any]
    __max_size: int
    __push_status: int
    __peek_status: int
    __pop_status: int

    PUSH_NIL: int = 0
    PUSH_OK: int = 1
    PUSH_ERR: int = 2
    POP_NIL: int = 0
    POP_OK: int = 1
    POP_ERR: int = 2
    PEEK_NIL: int = 0
    PEEK_OK: int = 1
    PEEK_ERR: int = 2

    def __init__(self, max_size: int = 32):
        self.clear()
        self.__max_size = max_size

    # предусловие: размер стека меньше максимального
    # постусловие: в стек добавлено новое значение
    def push(self, value: Any) -> None:
        if self.size() == self.__max_size:
            self.__push_status = self.PUSH_ERR
            return
        self.__stack.append(value)
        self.__push_status = self.PUSH_OK

    # предусловие: стек не пуст
    # постусловие: из стека удалён верхний элемент
    def pop(self) -> None:
        if self.size() == 0:
            self.__pop_status = self.POP_ERR
            return
        self.__stack.pop()
        self.__pop_status = self.POP_OK

    # постусловие: стек пуст
    def clear(self) -> None:
        self.__stack = []
        self.__push_status = self.PUSH_NIL
        self.__pop_status = self.POP_NIL
        self.__peek_status = self.PEEK_NIL
    
    # предусловие: стек не пуст
    def peek(self) -> Any:
        if self.size() == 0:
            self.__peek_status = self.PEEK_ERR
            return 0
        self.__peek_status = self.PEEK_OK
        return self.__stack[-1]

    def size(self) -> int:
        return len(self.__stack)

    def get_push_status(self) -> int:
        return self.__push_status

    def get_pop_status(self) -> int:
        return self.__pop_status

    def get_peek_status(self) -> int:
        return self.__peek_status
