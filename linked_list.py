"""Singly linked list for Assignment 6."""


class Node:
    """Store a value and a reference to the next node."""

    def __init__(self, value, next_node=None):
        self.value = value
        # This reference links the current node to the following node.
        self.next = next_node


class SinglyLinkedList:
    """Support insertion, deletion, and traversal."""

    def __init__(self):
        self.head = None
        self._size = 0

    def __len__(self):
        return self._size

    def insert(self, index, value):
        """Insert at an index.

        Head insertion is O(1). Other positions take O(n)
        because the preceding node must be located.
        """
        if not 0 <= index <= self._size:
            raise IndexError("Insertion index out of range.")

        if index == 0:
            # A new head points to the old head, keeping the rest connected.
            self.head = Node(value, self.head)
        else:
            previous = self.head

            for _ in range(index - 1):
                previous = previous.next

            # Link the new node between the previous node and its successor.
            previous.next = Node(value, previous.next)

        self._size += 1

    def delete(self, index):
        """Remove and return a value.

        Head deletion is O(1). Other positions take O(n).
        """
        if not 0 <= index < self._size:
            raise IndexError("Deletion index out of range.")

        if index == 0:
            removed = self.head
            self.head = removed.next
        else:
            previous = self.head

            for _ in range(index - 1):
                previous = previous.next

            removed = previous.next
            # Bypass the removed node to join the remaining nodes together.
            previous.next = removed.next

        self._size -= 1
        return removed.value

    def traverse(self):
        """Return all values in order in O(n) time."""
        values = []
        current = self.head

        # Traversal follows each link until the final node points to None.
        while current is not None:
            values.append(current.value)
            current = current.next

        return values


def main():
    linked = SinglyLinkedList()

    linked.insert(0, 10)
    linked.insert(1, 20)
    linked.insert(2, 30)
    print("Starting list:", linked.traverse())

    linked.insert(1, 15)
    print("After insertion:", linked.traverse())

    print("Deleted value:", linked.delete(2))
    print("Final list:", linked.traverse())
    print("Length:", len(linked))


if __name__ == "__main__":
    main()
