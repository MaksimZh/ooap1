from typing import Any
from enum import Enum, auto


class Buffer:

    class __Empty:
        pass

    __empty_cell = __Empty()

    class __Deleted:
        pass

    __deleted_cell = __Deleted()

    __data: list[Any]
    __count: int
    
    # конструктор
    # постусловие: создан новый пустой буфер заданного размера
    def __init__(self, capacity: int):
        self.__data = [self.__empty_cell] * capacity
        self.__count = 0
        self.__put_status = self.PutStatus.NIL
        self.__get_cell_state_status = self.GetCellStateStauts.NIL
    
    
    # команды

    # записать значение в указанную ячейку
    # предусловие: индекс лежит в допустимом диапазоне
    # предусловие: ячейка не содержит значение
    def put(self, index: int, value: Any) -> None:
        if index < 0:
            self.__put_status = self.PutStatus.INDEX_OUT_OF_RANGE
            return
        if index >= self.get_capacity():
            self.__put_status = self.PutStatus.INDEX_OUT_OF_RANGE
            return
        if self.get_cell_state(index) == self.CellState.VALUE:
            self.__put_status = self.PutStatus.ALREADY_HAS_VALUE
            return
        self.__count += 1
        self.__data[index] = value
        self.__put_status = self.PutStatus.OK

    class PutStatus(Enum):
        NIL = auto(),
        OK = auto(),
        INDEX_OUT_OF_RANGE = auto(),
        ALREADY_HAS_VALUE = auto(),

    __put_status: PutStatus

    def get_put_status(self) -> PutStatus:
        return self.__put_status

    
    # запросы

    # размер буфера
    def get_capacity(self) -> int:
        return len(self.__data)

    # количество заполненных ячеек в буфере
    def get_count(self) -> int:
        return self.__count

    # состояние ячейки
    class CellState(Enum):
        EMPTY = auto(),   # пустая
        VALUE = auto(),   # содержит значение
        DELETED = auto(), # значение было удалено

    # получить состояние указанной ячейки
    # предусловие: индекс лежит в допустимом диапазоне
    def get_cell_state(self, index: int) -> CellState:
        if self.__data[index] is self.__empty_cell:
            return self.CellState.EMPTY
        if self.__data[index] is self.__deleted_cell:
            return self.CellState.DELETED
        return self.CellState.VALUE

    class GetCellStateStauts(Enum):
        NIL = auto(),
        OK = auto(),
        INDEX_OUT_OF_RANGE = auto(),

    __get_cell_state_status: GetCellStateStauts

    def get_get_cell_state_status(self) -> GetCellStateStauts:
        return self.__get_cell_state_status

    # получить значение из указанной ячейки
    # предусловие: индекс лежит в допустимом диапазоне
    # предусловие: ячейка содержит значение
    def get(self, index: int) -> Any:
        return self.__data[index]


class HashBuffer(Buffer):
    pass


class HashTable:

    __buffer: HashBuffer
    
    def __init__(self, capacity: int):
        self.__buffer = HashBuffer(capacity)
        self.__remove_status = self.RemoveStatus.NIL


    # команды

    def remove(self, value: Any) -> None:
        self.__remove_status = self.RemoveStatus.NOT_FOUND

    class RemoveStatus(Enum):
        NIL = 0,
        OK = 1,
        NOT_FOUND = 2,

    __remove_status: RemoveStatus

    def get_remove_status(self) -> RemoveStatus:
        return self.__remove_status


    def add(self, value: Any) -> None:
        pass


    # запросы

    def get_count(self) -> int:
        return self.__buffer.get_count()

    def contains(self, value: Any) -> bool:
        return False
