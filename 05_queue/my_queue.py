from enum import Enum
from typing import Any

class Queue:

    __data: list[Any]

    # конструктор
    # постусловие: создана новая пустая очередь
    def __init__(self) -> None:
        self.__dequeue_status = self.DequeueStatus.NIL
        self.__get_status = self.GetStatus.NIL
        self.__data = []


    # команды

    # постусловие: в конец очереди добавлено новое значение
    def enqueue(self, value: Any) -> None:
        self.__data.append(value)

    # предусловие: очередь не пуста
    # постусловие: из начала очереди удалён элемент
    def dequeue(self) -> None:
        if self.get_size() == 0:
            self.__dequeue_status = self.DequeueStatus.EMPTY
            return
        self.__data.pop(0)
        self.__dequeue_status = self.DequeueStatus.OK

    class DequeueStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __dequeue_status: DequeueStatus

    def get_dequeue_status(self) -> DequeueStatus:
        return self.__dequeue_status

    
    # запросы

    # предусловие: очередь не пуста
    def get(self) -> Any:
        if self.get_size() == 0:
            self.__get_status = self.GetStatus.EMPTY
            return
        self.__get_status = self.GetStatus.OK
        return self.__data[0]

    class GetStatus(Enum):
        NIL = 0,
        OK = 1,
        EMPTY = 2,

    __get_status: GetStatus

    def get_get_status(self) -> GetStatus:
        return self.__get_status


    def get_size(self) -> int:
        return len(self.__data)
