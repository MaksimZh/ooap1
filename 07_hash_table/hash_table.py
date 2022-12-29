from typing import Any, Callable
from enum import Enum, auto
from random import randrange


class Buffer:

    class __Empty: pass
    __empty_cell = __Empty()
    class __Deleted: pass
    __deleted_cell = __Deleted()

    __data: list[Any]
    __count: int


    # конструктор
    # постусловие: создан новый пустой буфер заданного размера
    def __init__(self, capacity: int) -> None:
        self.__data = [self.__empty_cell] * capacity
        self.__count = 0
        self.__put_status = self.PutStatus.NIL
        self.__delete_status = self.DeleteStatus.NIL
        self.__get_cell_state_status = self.GetCellStateStauts.NIL
    
    
    # команды

    # записать значение в указанную ячейку
    # предусловие: индекс лежит в допустимом диапазоне
    # предусловие: ячейка не содержит значение
    def put(self, index: int, value: Any) -> None:
        if self.__is_index_out_of_range(index):
            self.__put_status = self.PutStatus.INDEX_OUT_OF_RANGE
            return
        if self.get_cell_state(index) == self.CellState.VALUE:
            self.__put_status = self.PutStatus.ALREADY_HAS_VALUE
            return
        self.__count += 1
        self.__data[index] = value
        self.__put_status = self.PutStatus.OK

    class PutStatus(Enum):
        NIL = auto(),                # команда не вызывалась
        OK = auto(),                 # успех
        INDEX_OUT_OF_RANGE = auto(), # индекс за границами буфера
        ALREADY_HAS_VALUE = auto(),  # в ячейке уже есть значение

    __put_status: PutStatus

    def get_put_status(self) -> PutStatus:
        return self.__put_status

    
    # удалить значение из указанной ячейки
    # предусловие: индекс лежит в допустимом диапазоне
    # предусловие: ячейка содержит значение
    def delete(self, index: int) -> None:
        if self.__is_index_out_of_range(index):
            self.__delete_status = self.DeleteStatus.INDEX_OUT_OF_RANGE
            return
        if self.get_cell_state(index) != self.CellState.VALUE:
            self.__delete_status = self.DeleteStatus.NO_VALUE
            return
        self.__data[index] = self.__deleted_cell
        self.__delete_status = self.DeleteStatus.OK

    class DeleteStatus(Enum):
        NIL = auto(),                # команда не вызывалась
        OK = auto(),                 # успех
        INDEX_OUT_OF_RANGE = auto(), # индекс за границами буфера
        NO_VALUE = auto(),           # в ячейке нет значения

    __delete_status: DeleteStatus

    def get_delete_status(self) -> DeleteStatus:
        return self.__delete_status

    
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
        if self.__is_index_out_of_range(index):
            self.__get_cell_state_status = \
                self.GetCellStateStauts.INDEX_OUT_OF_RANGE
            return self.CellState.EMPTY
        self.__get_cell_state_status = self.GetCellStateStauts.OK
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


    def __is_index_out_of_range(self, index: int) -> bool:
        return index < 0 or index >= self.get_capacity()


class HashIterator:

    __size: int
    __limit: int
    __started: bool
    __index: int
    __step: int
    __count: int
    __h1: Callable[[int], int]
    __h2: Callable[[int], int]

    
    # конструктор
    # предусловия: лимит индексов не превосходит размер
    # постусловие: создан новый итератор
    def __init__(self, size: int, limit: int) -> None:
        assert(limit <= size)
        self.__size = size
        self.__limit = limit
        self.__started = False
        self.__h1 = _make_hash_func(size, size - 1)
        self.__h2 = _make_hash_func(size, size + 1)
        self.__get_index_status = self.GetIndexStatus.NIL
        self.__next_status = self.NextStatus.NIL

    
    # команды

    # сгенерировать первый индекс для заданного значения
    # постусловия: итератор готов генерировать следующие индексы
    # постусловия: счётчик индексов сброшен до единицы
    def start(self, value: Any) -> None:
        x = hash(value)
        if x < 0:
            x = -x
        self.__started = True
        self.__index = self.__h1(x)
        self.__step = self.__h2(x)
        self.__count = 0
        if self.__step == 0:
            self.__step = 1

    # сгенерировать следующий индекс
    # предусловия: первый индекс был сгенерирован
    # предусловия: счётчик индексов не достиг лимита
    # постусловия: сгенерирован новый индекс
    def next(self) -> None:
        if not self.__started:
            self.__next_status = self.NextStatus.NOT_STARTED
            return
        self.__count += 1
        if self.__count >= self.__limit:
            self.__next_status = self.NextStatus.LIMIT_REACHED
            return
        self.__index = (self.__index + self.__step) % self.__size
        self.__next_status = self.NextStatus.OK
    
    class NextStatus(Enum):
        NIL = auto(),           # запрос не вызывался
        OK = auto(),            # успех
        NOT_STARTED = auto(),   # генерация индексов не начата
        LIMIT_REACHED = auto(), # счётчик индексов достиг лимита

    __next_status: NextStatus

    def get_next_status(self) -> NextStatus:
        return self.__next_status
    
    
    # запросы

    # получить текущий индекс
    # предусловие: индекс был сгенерирован
    # предусловия: счётчик индексов не достиг лимита
    def get_index(self) -> int:
        if not self.__started:
            self.__get_index_status = self.GetIndexStatus.NOT_STARTED
            return 0
        if self.__count >= self.__limit:
            self.__get_index_status = self.GetIndexStatus.LIMIT_REACHED
            return 0
        self.__get_index_status = self.GetIndexStatus.OK
        return self.__index

    class GetIndexStatus(Enum):
        NIL = auto(),           # запрос не вызывался
        OK = auto(),            # успех
        NOT_STARTED = auto(),   # генерация индексов не начата
        LIMIT_REACHED = auto(), # счётчик индексов достиг лимита

    __get_index_status: GetIndexStatus

    def get_get_index_status(self) -> GetIndexStatus:
        return self.__get_index_status


def _make_hash_func(size: int, p: int) -> Callable[[int], int]:
    a = randrange(1, p)
    b = randrange(0, p)
    return lambda x: ((a * x + b) % p) % size    


class HashTable:

    __buffer: Buffer
    
    def __init__(self, capacity: int) -> None:
        self.__buffer = Buffer(capacity)
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
