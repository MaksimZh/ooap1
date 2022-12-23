from typing import Any
from enum import Enum
from ctypes import py_object, Array

class DynArray:

    DEFAULT_CAPACITY: int = 16

    __capacity: int
    __count: int
    __data: Array[Any]
    
    # конструктор
    # постусловие: создан новый пустой массив
    # постусловие: размер буфера равен DEFAULT_CAPACITY
    def __init__(self) -> None:
        self.make_array(self.DEFAULT_CAPACITY)
        self.__count = 0
        self.__get_item_status = self.GetItemStatus.NIL
        self.__remove_status = self.RemoveStatus.NIL


    # команды
    
    # предусловие: размер массива не больше нового размера буфера
    # постусловие: размер буфера равен заданному значению
    def make_array(self, new_capacity: int) -> None:
        self.__capacity = new_capacity
        self.__data = (self.__capacity * py_object)()

    # постусловие: в конец массива добавлено новое значение
    # постусловие: размер буфера не меньше размера массива
    def append(self, item: Any) -> None:
        self.__data[self.__count] = item
        self.__count += 1

    
    # предусловие: значение индекса больше либо равно нулю и меньше либо равно размеру массива
    # постусловие: в позицию с заданным индексом вставлено новое значение,
    #              все последующие элементы сдвинуты на одну позицию вверх
    # постусловие: размер буфера не меньше размера массива
    def insert(self, item: Any, index: int) -> None:
        pass

    class InsertStatus(Enum):
        NIL = 0,
        OK = 1,
        INDEX_OUT_OF_RANGE = 2,

    def get_insert_status(self) -> InsertStatus:
        return self.InsertStatus.NIL

    
    # предусловие: значение индекса больше или равно нулю и меньше размера массива
    # постусловие: из позиции с заданным индексом удалено значение,
    #              все последующие элементы сдвинуты на одну позицию вниз
    # постусловие: размер буфера не превышает размер массива более чем в 2 раза
    def remove(self, index: int) -> None:
        if index < 0 or index >= self.__count:
            self.__remove_status = self.RemoveStatus.INDEX_OUT_OF_RANGE
            return

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
