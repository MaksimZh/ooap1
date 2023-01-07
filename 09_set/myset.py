from hash_table import HashTable, Buffer

class MySet(HashTable):
    
    # КОНСТРУКТОР
    # постусловие: создано пустое множество
    def __init__(self) -> None:
        super().__init__(17, 17, 100)

    # ЗАПРОСЫ

    # вычислить пересечение множества с другим множеством
    def intersection(self, other: "MySet") -> "MySet":
        result = MySet()
        for index in range(self.get_capacity()):
            if self._buffer.get_cell_state(index) != Buffer.CellState.VALUE:
                continue
            value = self._buffer.get(index)
            if not other.contains(value):
                continue
            result.put(value)
        return result

    # вычислить объединение множества с другим множеством
    def union(self, other: "MySet") -> "MySet":
        result = self.difference(other)
        for index in range(other.get_capacity()):
            if other._buffer.get_cell_state(index) != Buffer.CellState.VALUE:
                continue
            value = other._buffer.get(index)
            result.put(value)
        return result

    # вычислить разность множества с другим множеством
    def difference(self, other: "MySet") -> "MySet":
        result = MySet()
        for index in range(self.get_capacity()):
            if self._buffer.get_cell_state(index) != Buffer.CellState.VALUE:
                continue
            value = self._buffer.get(index)
            if other.contains(value):
                continue
            result.put(value)
        return result

    # проверить является ли другое множество подмножеством данного
    def is_subset(self, other: "MySet") -> bool:
        return other.difference(self).get_count() == 0
