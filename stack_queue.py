"""Array-based stack and circular queue for Assignment 6."""

from data_structures import DynamicArray


class Stack:
    """Last in, first out using the custom DynamicArray."""

    def __init__(self):
        self._items = DynamicArray()

    def __len__(self):
        return len(self._items)

    def push(self, value):
        """Add to the top in O(1) amortized time."""
        self._items.append(value)

    def pop(self):
        """Remove the top item in O(1) time."""
        if len(self) == 0:
            raise IndexError("Cannot pop from an empty stack.")

        # Removing the last item avoids shifting the other stack values.
        return self._items.delete(len(self) - 1)

    def peek(self):
        """Read the top item in O(1) time."""
        if len(self) == 0:
            raise IndexError("Cannot peek at an empty stack.")

        return self._items.get(len(self) - 1)


class Queue:
    """First in, first out using a resizable circular array."""

    def __init__(self):
        self._capacity = 4
        self._data = [None] * self._capacity
        self._front = 0
        self._size = 0

    def __len__(self):
        return self._size

    def _grow(self):
        """Copy items into a larger array in queue order."""
        new_capacity = self._capacity * 2
        new_data = [None] * new_capacity

        # Wrapped items must be copied in their logical first-in, first-out order.
        for index in range(self._size):
            old_index = (self._front + index) % self._capacity
            new_data[index] = self._data[old_index]

        self._data = new_data
        self._capacity = new_capacity
        self._front = 0

    def enqueue(self, value):
        """Add at the back in O(1) amortized time."""
        if self._size == self._capacity:
            self._grow()

        # Modulo wraps the back position to the start when it reaches the end.
        back = (self._front + self._size) % self._capacity
        self._data[back] = value
        self._size += 1

    def dequeue(self):
        """Remove from the front in O(1) time."""
        if self._size == 0:
            raise IndexError("Cannot dequeue from an empty queue.")

        value = self._data[self._front]
        self._data[self._front] = None
        # Moving the front keeps removal O(1), with no shifting of other items.
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return value

    def peek(self):
        """Read the front item in O(1) time."""
        if self._size == 0:
            raise IndexError("Cannot peek at an empty queue.")

        return self._data[self._front]

    def to_list(self):
        """Return items in queue order in O(n) time."""
        return [
            self._data[(self._front + index) % self._capacity]
            for index in range(self._size)
        ]


def main():
    stack = Stack()

    for value in [10, 20, 30]:
        stack.push(value)

    print("Stack top:", stack.peek())
    print("Stack removes:", stack.pop())
    print("New stack top:", stack.peek())

    queue = Queue()

    for value in [10, 20, 30, 40]:
        queue.enqueue(value)

    print("Queue removes:", queue.dequeue())

    # Exercise wraparound, followed by resizing.
    queue.enqueue(50)
    queue.enqueue(60)

    print("Queue front:", queue.peek())
    print("Final queue:", queue.to_list())


if __name__ == "__main__":
    main()
