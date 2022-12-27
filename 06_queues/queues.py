from abc import ABC, abstractmethod
from typing import Any
from enum import Enum


class ParentQueue(ABC):

    _data: list[Any]

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        self._data = []
        self.__pop_front_status = self.PopFrontStatus.NIL
        self.__get_front_status = self.GetFrontStatus.NIL

    # команды

    # постусловие: в хвост очереди добавлен новый элемент
    def put_tail(self, value: Any) -> None:
        self._data.append(value)

    # предусловие: очередь не пуста
    # постусловие: из головы очереди удалён элемент
    def pop_front(self) -> None:
        if self.get_size() == 0:
            self.__pop_front_status = self.PopFrontStatus.EMPTY
            return
        self._data.pop(0)
        self.__pop_front_status = self.PopFrontStatus.OK

    class PopFrontStatus(Enum):
        NIL = 0,   # команда не вызывалась
        OK = 1,    # успех
        EMPTY = 2, # ошибка: очередь пуста

    __pop_front_status: PopFrontStatus

    def get_pop_front_status(self) -> PopFrontStatus:
        return self.__pop_front_status
    

    # запросы

    # получить размер очереди
    def get_size(self) -> int:
        return len(self._data)

    # получить значение из головы очереди
    # предусловие: очередь не пуста
    def get_front(self) -> Any:
        if self.get_size() == 0:
            self.__get_front_status = self.GetFrontStatus.EMPTY
            return None
        self.__get_front_status = self.GetFrontStatus.OK
        return self._data[0]

    class GetFrontStatus(Enum):
        NIL = 0,   # запрос не выполнялся
        OK = 1,    # успех
        EMPTY = 2, # ошибка: очередь пуста

    __get_front_status: GetFrontStatus

    def get_get_front_status(self) -> GetFrontStatus:
        return self.__get_front_status


class Queue(ParentQueue):

    # конструктор
    # постусловие: создана новая пустая очередь
    def __init__(self) -> None:
        super().__init__()


class Deque(ParentQueue):

    # конструктор
    # постусловие: создана новая пустая очередь
    def __init__(self) -> None:
        super().__init__()
        self.__get_tail_status = self.GetTailStatus.NIL
        self.__pop_tail_status = self.PopTailStatus.NIL


    # команды

    # постусловие: в голову очереди добавлен новый элемент
    def put_front(self, value: Any) -> None:
        self._data.insert(0, value)

    # предусловие: очередь не пуста
    # постусловие: из хвоста очереди удалён элемент
    def pop_tail(self) -> None:
        if self.get_size() == 0:
            self.__pop_tail_status = self.PopTailStatus.EMPTY
            return
        self.__pop_tail_status = self.PopTailStatus.OK
        self._data.pop()

    class PopTailStatus(Enum):
        NIL = 0,   # команда не вызывалась
        OK = 1,    # успех
        EMPTY = 2, # ошибка: очередь пуста


    __pop_tail_status: PopTailStatus

    def get_pop_tail_status(self) -> PopTailStatus:
        return self.__pop_tail_status


    # запросы

    # получить значение из хвоста очереди
    # предусловие: очередь не пуста
    def get_tail(self) -> Any:
        if self.get_size() == 0:
            self.__get_tail_status = self.GetTailStatus.EMPTY
            return None
        self.__get_tail_status = self.GetTailStatus.OK
        return self._data[-1]

    class GetTailStatus(Enum):
        NIL = 0,   # запрос не выполнялся
        OK = 1,    # успех
        EMPTY = 2, # ошибка: очередь пуста

    __get_tail_status: GetTailStatus

    def get_get_tail_status(self) -> GetTailStatus:
        return self.__get_tail_status
