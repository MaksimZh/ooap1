from math import log
from ctypes import Array, c_int, sizeof
from enum import Enum, auto

class BitArray:

    __cell_size = sizeof(c_int) * 8
    __size: int
    __cells: Array[c_int]
    
    
    # КОНСТРУКТОР
    # создан битовый массив заданного размера
    def __init__(self, size: int) -> None:
        self.__size = size
        count = size // self.__cell_size
        if count * self.__cell_size < size:
            count += 1
        self.__cells = (c_int * count)()
        self.__set_status = self.SetStatus.NIL
        self.__get_status = self.GetStatus.NIL

    
    # КОМАНДЫ

    # установить бит с заданным индексом
    # предусловие: индекс в допустимом диапазоне
    def set_on(self, index: int) -> None:
        if index < 0 or index >= self.__size:
            self.__set_status = self.SetStatus.INDEX_OUT_OF_RANGE
            return
        self.__set_status = self.SetStatus.OK
        base, offset = divmod(index, self.__cell_size)
        self.__cells[base] = self.__cells[base] | (1 << offset)
    
    # обнулить бит с заданным индексом
    # предусловие: индекс в допустимом диапазоне
    def set_off(self, index: int) -> None:
        if index < 0 or index >= self.__size:
            self.__set_status = self.SetStatus.INDEX_OUT_OF_RANGE
            return
        self.__set_status = self.SetStatus.OK
        base, offset = divmod(index, self.__cell_size)
        self.__cells[base] = self.__cells[base] & ~(1 << offset)
    
    class SetStatus(Enum):
        NIL = auto(),
        OK = auto(),
        INDEX_OUT_OF_RANGE = auto(),
    
    __set_status: SetStatus

    def get_set_status(self) -> SetStatus:
        return self.__set_status
    
    
    # ЗАПРОСЫ

    # определить состояние бита с заданным индексом
    # предусловие: индекс в допустимом диапазоне
    def get(self, index: int) -> bool:
        if index < 0 or index >= self.__size:
            self.__get_status = self.GetStatus.INDEX_OUT_OF_RANGE
            return False
        self.__get_status = self.GetStatus.OK
        base, offset = divmod(index, self.__cell_size)
        return self.__cells[base] & (1 << offset) != 0

    class GetStatus(Enum):
        NIL = auto(),
        OK = auto(),
        INDEX_OUT_OF_RANGE = auto(),

    __get_status: GetStatus

    def get_get_status(self) -> GetStatus:
        return self.__get_status

    
    # определить размер массива
    def get_size(self) -> int:
        return self.__size


class BloomFilter:
    
    def __init__(self, count: int, err_prob: float) -> None:
        alpha = 0.6931
        size = count * log(err_prob) / log(alpha)
        k = alpha * size / count
        k = k
