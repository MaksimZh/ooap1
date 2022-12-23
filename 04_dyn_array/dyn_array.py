from typing import Any
from enum import Enum
from ctypes import py_object, Array

class DynArray:

    DEFAULT_CAPACITY: int = 16
    EXTEND_FACTOR: float = 2.0
    SHRINK_THRESHOLD_FACTOR: float = 0.5
    SHRINK_DIVISOR: float = 1.5
    
    __capacity: int
    __count: int
    __data: Array[Any]
    
    # конструктор
    # постусловие: создан новый пустой массив
    # постусловие: размер буфера равен DEFAULT_CAPACITY
    def __init__(self) -> None:
        self.__count = 0
        self.make_array(self.DEFAULT_CAPACITY)
        self.__get_item_status = self.GetItemStatus.NIL
        self.__insert_status = self.InsertStatus.NIL
        self.__remove_status = self.RemoveStatus.NIL


    # команды
    
    # предусловие: размер массива не больше нового размера буфера
    # постусловие: размер буфера равен заданному значению
    def make_array(self, new_capacity: int) -> None:
        new_data = (new_capacity * py_object)()
        if self.__count > 0:
            new_data[:self.__count] = self.__data[:self.__count]
        self.__capacity = new_capacity
        self.__data = new_data

    # постусловие: в конец массива добавлено новое значение
    # постусловие: если размер массива был меньше размера буфера
    #              размер буфера остался прежним
    #              если размер массива был равен размеру буфера
    #              то новый размер буфера в EXTEND_FACTOR раз больше длины массива
    def append(self, item: Any) -> None:
        self.insert(item, self.__count)
        assert(self.get_insert_status() == self.InsertStatus.OK)


    # предусловие: значение индекса больше либо равно нулю и меньше либо равно размеру массива
    # постусловие: в позицию с заданным индексом вставлено новое значение,
    #              все последующие элементы сдвинуты на одну позицию вверх
    # постусловие: если размер массива был меньше размера буфера
    #              размер буфера остался прежним
    #              если размер массива был равен размеру буфера
    #              то новый размер буфера в EXTEND_FACTOR раз больше длины массива
    def insert(self, item: Any, index: int) -> None:
        if index < 0 or index > self.__count:
            self.__insert_status = self.InsertStatus.INDEX_OUT_OF_RANGE
            return
        self.__extend_if_needed(self.__count + 1)
        self.__data[index + 1 : self.__count + 1] = self.__data[index : self.__count]
        self.__data[index] = item
        self.__count += 1
        self.__insert_status = self.InsertStatus.OK

    class InsertStatus(Enum):
        NIL = 0,
        OK = 1,
        INDEX_OUT_OF_RANGE = 2,

    __insert_status: InsertStatus

    def get_insert_status(self) -> InsertStatus:
        return self.__insert_status

    
    # предусловие: значение индекса больше или равно нулю и меньше размера массива
    # постусловие: из позиции с заданным индексом удалено значение,
    #              все последующие элементы сдвинуты на одну позицию вниз
    # постусловие: если новый размер массива меньше размера буфера
    #              умноженного на SHRINK_THRESHOLD_FACTOR
    #              то размер буфера уменьшается в SHRINK_DIVISOR раз
    #              если он окажется меньше DEFAULT_CAPACITY
    #              то становится равным DEFAULT_CAPACITY
    def remove(self, index: int) -> None:
        if index < 0 or index >= self.__count:
            self.__remove_status = self.RemoveStatus.INDEX_OUT_OF_RANGE
            return
        self.__data[index : self.__count - 1] = self.__data[index + 1: self.__count]
        self.__count -= 1
        self.__shrink_if_needed()
        self.__remove_status = self.RemoveStatus.OK

    class RemoveStatus(Enum):
        NIL = 0,
        OK = 1,
        INDEX_OUT_OF_RANGE = 2,

    __remove_status: RemoveStatus

    def get_remove_status(self) -> RemoveStatus:
        return self.__remove_status
    
    
    # запросы

    def get_count(self) -> int:
        return self.__count

    def get_capacity(self) -> int:
        return self.__capacity

    # предусловие: значение индекса больше или равно нулю и меньше размера массива
    def get_item(self, index: int) -> Any:
        if index < 0 or index >= self.__count:
            self.__get_item_status = self.GetItemStatus.INDEX_OUT_OF_RANGE
            return
        self.__get_item_status = self.GetItemStatus.OK
        return self.__data[index]

    class GetItemStatus(Enum):
        NIL = 0,
        OK = 1,
        INDEX_OUT_OF_RANGE = 2,

    __get_item_status: GetItemStatus

    def get_get_item_status(self) -> GetItemStatus:
        return self.__get_item_status


    def __extend_if_needed(self, count: int) -> None:
        if count <= self.__capacity:
            return
        self.make_array(int(self.__capacity * self.EXTEND_FACTOR))

    def __shrink_if_needed(self) -> None:
        if self.__count >= int(self.__capacity * self.SHRINK_THRESHOLD_FACTOR):
            return
        new_capacity = max(int(self.__capacity / self.SHRINK_DIVISOR), self.DEFAULT_CAPACITY)
        self.make_array(new_capacity)
