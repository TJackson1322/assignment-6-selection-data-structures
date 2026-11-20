"""Elementary data structures for Assignment 6."""


class DynamicArray:
    """An array with manual resizing and element shifting."""

    def __init__(self):
        # Capacity counts available slots. Size counts stored values.
        self._capacity = 4
        self._size = 0
        self._data = [None] * self._capacity

    def __len__(self):
        return self._size

    def _check_index(self, index):
        if not 0 <= index < self._size:
            raise IndexError("Array index out of range.")

    def _grow(self):
        """Double capacity and copy the existing elements."""
        # Doubling leaves room for future appends and spreads out copying costs.
        new_capacity = self._capacity * 2
        new_data = [None] * new_capacity

        for index in range(self._size):
            new_data[index] = self._data[index]

        self._data = new_data
        self._capacity = new_capacity

    def get(self, index):
        """Access an element in O(1) time."""
        self._check_index(index)
        return self._data[index]

    def set(self, index, value):
        """Replace an element in O(1) time."""
        self._check_index(index)
        self._data[index] = value

    def insert(self, index, value):
        """Insert at an index, shifting later elements right."""
        if not 0 <= index <= self._size:
            raise IndexError("Insertion index out of range.")

        if self._size == self._capacity:
            self._grow()

        # I shift right from the end so existing values are not overwritten.
        for position in range(self._size, index, -1):
            self._data[position] = self._data[position - 1]

        self._data[index] = value
        self._size += 1

    def append(self, value):
        """Add at the end in O(1) amortized time."""
        self.insert(self._size, value)

    def delete(self, index):
        """Remove an element and shift later elements left."""
        self._check_index(index)
        removed = self._data[index]

        # Closing the gap preserves the order of the remaining values.
        for position in range(index, self._size - 1):
            self._data[position] = self._data[position + 1]

        self._size -= 1
        # Clear the unused slot so it stops holding the removed reference.
        self._data[self._size] = None
        return removed

    def to_list(self):
        """Return the stored elements in O(n) time."""
        return [
            self._data[index]
            for index in range(self._size)
        ]


def main():
    array = DynamicArray()

    for value in [10, 20, 30, 40, 50]:
        array.append(value)

    print("Starting array:", array.to_list())

    array.insert(1, 15)
    print("After inserting 15:", array.to_list())
    print("Value at index 2:", array.get(2))

    removed = array.delete(3)
    print("Deleted value:", removed)
    print("Final array:", array.to_list())


if __name__ == "__main__":
    main()
