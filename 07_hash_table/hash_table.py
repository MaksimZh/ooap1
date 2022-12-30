from typing import Any, Callable, Generator, Optional
from enum import Enum, auto
from random import randrange
from math import sqrt


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
        self.__get_cell_state_status = self.GetCellStateStatus.NIL
        self.__get_status = self.GetStatus.NIL
    
    
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
                self.GetCellStateStatus.INDEX_OUT_OF_RANGE
            return self.CellState.EMPTY
        self.__get_cell_state_status = self.GetCellStateStatus.OK
        if self.__data[index] is self.__empty_cell:
            return self.CellState.EMPTY
        if self.__data[index] is self.__deleted_cell:
            return self.CellState.DELETED
        return self.CellState.VALUE

    class GetCellStateStatus(Enum):
        NIL = auto(),
        OK = auto(),
        INDEX_OUT_OF_RANGE = auto(),

    __get_cell_state_status: GetCellStateStatus

    def get_get_cell_state_status(self) -> GetCellStateStatus:
        return self.__get_cell_state_status


    # получить значение из указанной ячейки
    # предусловие: индекс лежит в допустимом диапазоне
    # предусловие: ячейка содержит значение
    def get(self, index: int) -> Any:
        if self.__is_index_out_of_range(index):
            self.__get_status = \
                self.GetStatus.INDEX_OUT_OF_RANGE
            return None
        if self.get_cell_state(index) != self.CellState.VALUE:
            self.__get_status = self.GetStatus.NO_VALUE
            return None
        self.__get_status = self.GetStatus.OK
        return self.__data[index]

    class GetStatus(Enum):
        NIL = auto(),
        OK = auto(),
        INDEX_OUT_OF_RANGE = auto(),
        NO_VALUE = auto(),

    __get_status: GetStatus

    def get_get_status(self) -> GetStatus:
        return self.__get_status


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

    # проверка можно ли получить индекс
    def is_index_valid(self) -> bool:
        return self.__started and self.__count < self.__limit

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


class HashBuffer(Buffer):

    __hash_iterator: HashIterator
    
    # конструктор
    # предусловия: лимит индексов не превосходит размер
    # постусловие: создан новый пустой буфер заданного размера
    def __init__(self, capacity: int, limit: int) -> None:
        super().__init__(capacity)
        self.__hash_iterator = HashIterator(capacity, min(capacity, limit))

    # запросы

    # получить индекс ячейки со значением или для вставки значения
    def find_cell(self, value: Any) -> int:
        deleted_index: Optional[int] = None
        self.__hash_iterator.start(value)
        while self.__hash_iterator.is_index_valid():
            index = self.__hash_iterator.get_index()
            assert(self.__hash_iterator.get_get_index_status() == \
                HashIterator.GetIndexStatus.OK)
            cell_state = self.get_cell_state(index)
            if cell_state == Buffer.CellState.EMPTY:
                self.__find_cell_status = self.FindCellStatus.VACANCY_FOUND
                return index
            if cell_state == Buffer.CellState.DELETED and \
                    deleted_index is None:
                deleted_index = index
                self.__hash_iterator.next()
                continue
            assert(cell_state == Buffer.CellState.VALUE)
            cell_value = self.get(index)
            assert(self.get_get_status() == Buffer.GetStatus.OK)
            if cell_value == value:
                self.__find_cell_status = self.FindCellStatus.VALUE_FOUND
                return index
            self.__hash_iterator.next()
        if deleted_index is not None:
            self.__find_cell_status = self.FindCellStatus.VACANCY_FOUND
            return deleted_index
        self.__find_cell_status = self.FindCellStatus.LIMIT_REACHED
        return 0

    class FindCellStatus(Enum):
        NIL = auto(),           # запрос не выполнялся
        VALUE_FOUND = auto(),   # найденная ячейка содержит заданное значение
        VACANCY_FOUND = auto(), # найдена ячейка для вставки заданного значения
        LIMIT_REACHED = auto(), # достигнут лимит проверенных ячеек

    __find_cell_status: FindCellStatus

    def get_find_cell_status(self) -> FindCellStatus:
        return self.__find_cell_status    


class PrimeTester:

    __factors: list[int]
    __generator: Generator[int, None, None]

    # конструктор
    def __init__(self) -> None:
        self.__generator = _prime_candidate_gen(2)
        self.__factors = [next(self.__generator)]


    # запросы

    # проверить является ли число простым
    def is_prime(self, value: int) -> bool:
        assert(value > 1)
        max_factor = int(sqrt(value))
        self.__ensure_enough_factors(max_factor)
        i = 0
        while self.__factors[i] <= max_factor:
            if value % self.__factors[i] == 0:
                return False
            i += 1
        return True

    
    def __ensure_enough_factors(self, max_factor: int) -> None:
        while self.__factors[-1] <= max_factor:
            self.__factors.append(next(self.__generator))


def _prime_candidate_gen(start: int) -> Generator[int, None, None]:
    window = 30
    low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    offsets = [1, 7, 11, 13, 17, 19, 23, 29]
    if start < window:
        i = 0
        while low_primes[i] < start:
            i += 1
        for v in low_primes[i:]:
            yield v
        base = 0
    else:
        base = window * (start // window)
        i = 0
        while base + offsets[i] < start:
            i += 1
        for offset in offsets[i:]:
            yield base + offset
    while True:
        base += window
        for offset in offsets:
            yield base + offset


class PrimeScales:

    __tester: PrimeTester
    __scale_factor: int
    __min_value: int
    __values: list[int]
    __index: int

    # конструктор
    # постусловие: текущее простое число - первое больше заданного значения
    def __init__(self, start: int, scale_factor: int, min_value: int) -> None:
        assert(scale_factor > 1.5)
        self.__tester = PrimeTester()
        self.__min_value = self.__nearest_prime(min_value)
        if start < self.__min_value:
            start = self.__min_value
        self.__scale_factor = scale_factor
        size = self.__nearest_prime(start)
        self.__values = [size]
        self.__index = 0


    # команды

    # уменьшить текущее простое число
    # предусловие: текущее простое число больше минимума
    # постусловие: текущее простое число уменьшено
    def scale_down(self) -> None:
        if self.get() == self.__min_value:
            self.__scale_down_status = self.ScaleDownStatus.MINIMAL
            return
        self.__scale_down_status = self.ScaleDownStatus.OK
        if self.__index > 0:
            self.__index -= 1
            return
        new_start = int(self.__values[0] / self.__scale_factor)
        self.__values.insert(0, self.__nearest_prime(new_start))
        if self.__values[0] < self.__min_value:
            self.__values[0] = self.__min_value

    class ScaleDownStatus(Enum):
        NIL = auto(),
        OK = auto(),
        MINIMAL = auto(),

    __scale_down_status: ScaleDownStatus

    def get_scale_down_status(self) -> ScaleDownStatus:
        return self.__scale_down_status

    
    # увеличить текущее простое число
    # постусловие: текущее простое число увеличено
    def scale_up(self) -> None:
        if self.__index == len(self.__values) - 1:
            next_start = int(self.get() * self.__scale_factor)
            self.__values.append(self.__nearest_prime(next_start))
        self.__index += 1


    # запросы

    # получить текущее простое число
    def get(self) -> int:
        return self.__values[self.__index]


    def __nearest_prime(self, start: int) -> int:
        generator = _prime_candidate_gen(start)
        value = next(generator)
        while not self.__tester.is_prime(value):
            value = next(generator)
        return value


class HashTable:

    MAX_COLLISIONS = 100
    SCALE_FACTOR = 2
    MIN_FILL_FACTOR = 0.1

    __buffer: HashBuffer
    __scales: PrimeScales
    
    # конструктор
    # постусловие: создана пустая таблица с ёмкостью не ниже заданной
    def __init__(self, capacity: int, min_capacity: Optional[int] = None) -> None:
        if min_capacity is None:
            min_capacity = capacity
        assert(min_capacity <= capacity)
        self.__scales = PrimeScales(capacity, self.SCALE_FACTOR, min_capacity)
        size = self.__scales.get()
        self.__buffer = HashBuffer(size, self.MAX_COLLISIONS)
        self.__add_status = self.AddStatus.NIL
        self.__remove_status = self.RemoveStatus.NIL


    # команды

    # удалить указанное значение из таблицы
    # предусловие: указанное значение содержится в таблице
    # постусловие: из таблицы удалено указанное значение
    def remove(self, value: Any) -> None:
        self.__remove_status = self.RemoveStatus.NOT_FOUND

    class RemoveStatus(Enum):
        NIL = 0,
        OK = 1,
        NOT_FOUND = 2,

    __remove_status: RemoveStatus

    def get_remove_status(self) -> RemoveStatus:
        return self.__remove_status


    # добавить указанное значение в таблицу
    # предусловие: указанное значение отсутствует в таблице
    # постусловие: в таблицу добавлено указанное значение
    def add(self, value: Any) -> None:
        index = self.__buffer.find_cell(value)
        if self.__buffer.get_find_cell_status() == \
                HashBuffer.FindCellStatus.VACANCY_FOUND:
            self.__buffer.put(index, value)
            assert(self.__buffer.get_put_status() == Buffer.PutStatus.OK)
            self.__add_status = self.AddStatus.OK
            return
        if self.__buffer.get_find_cell_status() == \
                HashBuffer.FindCellStatus.VALUE_FOUND:
            self.__add_status = self.AddStatus.ALREADY_CONTAINS
            return
        assert(self.__buffer.get_find_cell_status() == \
            HashBuffer.FindCellStatus.LIMIT_REACHED)
        self.__scale_up()
        self.add(value)

    class AddStatus(Enum):
        NIL = auto(),
        OK = auto(),
        ALREADY_CONTAINS = auto(),

    __add_status: AddStatus

    def get_add_status(self) -> AddStatus:
        return self.__add_status


    # запросы

    # получить количество значений в таблице
    def get_count(self) -> int:
        return self.__buffer.get_count()

    # проверить содержит ли таблица указанное значение
    def contains(self, value: Any) -> bool:
        self.__buffer.find_cell(value)
        return self.__buffer.get_find_cell_status() == \
            HashBuffer.FindCellStatus.VALUE_FOUND


    def __scale_up(self) -> None:
        self.__scales.scale_up()
        while True:
            new_buffer = HashBuffer(self.__scales.get(), self.MAX_COLLISIONS)
            if _try_copy_hash_buffer(self.__buffer, new_buffer):
                self.__buffer = new_buffer
                return


def _try_copy_hash_buffer(source: HashBuffer, dest: HashBuffer) -> bool:
    for index in range(source.get_capacity()):
        if source.get_cell_state(index) == Buffer.CellState.VALUE:
            value = source.get(index)
            new_index = dest.find_cell(value)
            if dest.get_find_cell_status() != \
                    HashBuffer.FindCellStatus.VACANCY_FOUND:
                return False
            dest.put(new_index, value)
    return True
