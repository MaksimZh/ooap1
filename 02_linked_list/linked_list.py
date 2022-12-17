from typing import Any
from enum import Enum
from abc import ABC, abstractmethod

# 2.1
class LinkedList(ABC):

    # Результат работы команд управления курсором: head, tail, right
    class CursorStatus(Enum):
        NIL = 0, # команда не вызывалась
        OK  = 1, # последняя команда отработала нормально
        ERR = 2, # список пуст

    # Результат работы команды remove
    class RemoveStatus(Enum):
        NIL = 0, # команда не вызывалась
        OK  = 1, # последняя команда отработала нормально
        ERR = 2, # список пуст

    # Результат работы команды replace
    class ReplaceStatus(Enum):
        NIL = 0, # команда не вызывалась
        OK  = 1, # последняя команда отработала нормально
        ERR = 2, # список пуст

    # Результат работы команды find
    class FindStatus(Enum):
        NIL = 0, # команда не вызывалась
        OK  = 1, # последняя команда отработала нормально
        ERR = 2, # значение не найдено

    # Результат работы команды get
    class GetStatus(Enum):
        NIL = 0, # команда не вызывалась
        OK  = 1, # последняя команда отработала нормально
        ERR = 2, # список пуст


    # конструктор
    # постусловие: список пуст
    @abstractmethod
    def __init__(self):
        pass


    # команды
    
    # предусловие: список не пуст
    @abstractmethod
    def head(self) -> None:
        pass

    # предусловие: список не пуст
    @abstractmethod
    def tail(self) -> None:
        pass

    # предусловие: список не пуст
    # предусловие: курсор указывает не на последний элемент
    @abstractmethod
    def right(self) -> None:
        pass

    # постусловие: в список добавлено новое значение
    @abstractmethod
    def put_right(self, value: Any) -> None:
        pass

    # постусловие: в список добавлено новое значение
    @abstractmethod
    def put_left(self, value: Any) -> None:
        pass

    # предусловие: список не пуст
    @abstractmethod
    def remove(self) -> None:
        pass

    # постусловие: список пуст
    @abstractmethod
    def clear(self) -> None:
        pass

    # постусловие: в список добавлено новое значение
    @abstractmethod
    def add_tail(self, value: Any) -> None:
        pass

    # предусловие: список не пуст
    @abstractmethod
    def replace(self, value: Any) -> None:
        pass

    @abstractmethod
    def find(self, value: Any) -> None:
        pass

    @abstractmethod
    def remove_all(self, value: Any) -> None:
        pass


    # запросы
    
    # предусловие: список не пуст
    @abstractmethod
    def get(self) -> Any:
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def is_head(self) -> bool:
        pass

    @abstractmethod
    def is_tail(self) -> bool:
        pass

    @abstractmethod
    def is_value(self) -> bool:
        pass

    
    # дополнительные запросы

    @abstractmethod
    def get_cursor_status(self) -> CursorStatus:
        pass

    @abstractmethod
    def get_remove_status(self) -> RemoveStatus:
        pass

    @abstractmethod
    def get_replace_status(self) -> ReplaceStatus:
        pass

    @abstractmethod
    def get_find_status(self) -> FindStatus:
        pass

    @abstractmethod
    def get_get_status(self) -> GetStatus:
        pass


# 2.2. Почему операция tail не сводима к другим операциям (если исходить из эффективной реализации)?
# Для установки курсора в конец списка можно вызвать команду head
# и затем вызывать команду right пока не дойдём до конца (size - 1 раз).
# Этот подход имеет сложность O(N).
# В то же время, при эффективной реализации списка (хранится ссылка на конец)
# сложность команды tail будет O(1).


# 2.3. Операция поиска всех узлов с заданным значением, выдающая список таких узлов, уже не нужна. Почему?
# Теперь команда find сканирует список не с начала, а с текущей позиции курсора.
# Поэтому можно перебрать все узлы с заданным значением, вызывая find несколько раз.
