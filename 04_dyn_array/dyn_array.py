from typing import Any
from enum import Enum

class DynArray:
    
    # конструктор
    # постусловие: создан новый пустой массив
    # постусловие: размер буфера равен 16
    def __init__(self) -> None:
        pass


    # команды
    
    # предусловие: размер массива не больше нового размера буфера
    # постусловие: размер буфера равен заданному значению
    def make_array(self, new_capacity: int) -> None:
        pass

    # постусловие: в конец массива добавлено новое значение
    # постусловие: размер буфера не меньше размера массива
    def append(self, item: Any) -> None:
        pass

    
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
        pass

    class RemoveStatus(Enum):
        NIL = 0,
        OK = 1,
        INDEX_OUT_OF_RANGE = 2,

    def get_remove_status(self) -> RemoveStatus:
        return self.RemoveStatus.NIL
    
    
    # запросы

    def get_count(self) -> int:
        return 0

    def get_capacity(self) -> int:
        return 0

    # предусловие: значение индекса больше или равно нулю и меньше размера массива
    def get_item(self, index: int) -> Any:
        pass
