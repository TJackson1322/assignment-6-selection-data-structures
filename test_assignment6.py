"""Correctness and edge-case tests for Assignment 6."""

import random
import unittest

from selection_algorithms import (
    deterministic_select,
    randomized_select,
)
from data_structures import DynamicArray
from matrix import Matrix
from stack_queue import Stack, Queue
from linked_list import SinglyLinkedList


class TestSelection(unittest.TestCase):
    def test_every_rank(self):
        datasets = [
            [5],
            [4, 4, 4, 4],
            [9, -2, 5, 5, 0, 12],
            list(range(30)),
            list(range(30, 0, -1)),
        ]

        for values in datasets:
            # I also check that both algorithms preserve the input.
            original = values.copy()

            # Check every rank in these examples, including duplicate values.
            for k, expected in enumerate(sorted(values), start=1):
                with self.subTest(values=values, k=k):
                    self.assertEqual(
                        deterministic_select(values, k), expected
                    )
                    self.assertEqual(
                        randomized_select(
                            values, k, random.Random(42)
                        ),
                        expected,
                    )
                    self.assertEqual(values, original)

    def test_invalid_inputs(self):
        for select in (deterministic_select, randomized_select):
            for values, k in [([], 1), ([1, 2], 0), ([1, 2], 3)]:
                with self.subTest(algorithm=select.__name__, k=k):
                    with self.assertRaises(ValueError):
                        select(values, k)

            with self.assertRaises(TypeError):
                select([1, 2], 1.5)


class TestStructures(unittest.TestCase):
    def test_array_resizing_and_shifting(self):
        array = DynamicArray()

        # Twenty values force growth beyond the initial four slots.
        for value in range(20):
            array.append(value)

        array.insert(0, 99)
        self.assertEqual(array.delete(1), 0)
        array.set(1, 88)

        self.assertEqual(
            array.to_list(), [99, 88] + list(range(2, 20))
        )
        self.assertEqual(array.get(1), 88)
        self.assertEqual(len(array), 20)

    def test_array_empty_and_invalid_indices(self):
        array = DynamicArray()

        with self.assertRaises(IndexError):
            array.delete(0)
        with self.assertRaises(IndexError):
            array.get(0)
        with self.assertRaises(IndexError):
            array.insert(1, 5)

        array.append(5)
        self.assertEqual(array.delete(0), 5)
        self.assertEqual(array.to_list(), [])

    def test_matrix_operations_and_validation(self):
        matrix = Matrix(2)
        matrix.insert_row(0, [1, 2])
        matrix.insert_row(1, [3, 4])
        matrix.set(0, 1, 9)

        self.assertEqual(matrix.get(0, 1), 9)
        self.assertEqual(matrix.shape(), (2, 2))

        with self.assertRaises(ValueError):
            matrix.insert_row(1, [5])
        with self.assertRaises(IndexError):
            matrix.get(0, 2)

        self.assertEqual(matrix.delete_row(0), [1, 9])
        self.assertEqual(matrix.delete_row(0), [3, 4])
        self.assertEqual(matrix.shape(), (0, 2))

    def test_stack_order_and_empty_operations(self):
        stack = Stack()

        # Twenty values force growth beyond the initial four slots.
        for value in range(20):
            stack.push(value)

        self.assertEqual(stack.peek(), 19)
        self.assertEqual(
            [stack.pop() for _ in range(20)],
            list(reversed(range(20))),
        )

        with self.assertRaises(IndexError):
            stack.pop()
        with self.assertRaises(IndexError):
            stack.peek()

    def test_queue_wraparound_resizing_and_reuse(self):
        queue = Queue()

        for value in range(4):
            queue.enqueue(value)

        self.assertEqual(queue.dequeue(), 0)
        self.assertEqual(queue.dequeue(), 1)

        # These additions exercise wraparound followed by queue resizing.
        for value in range(4, 10):
            queue.enqueue(value)

        self.assertEqual(queue.to_list(), list(range(2, 10)))
        self.assertEqual(queue.peek(), 2)
        self.assertEqual(
            [queue.dequeue() for _ in range(8)],
            list(range(2, 10)),
        )

        with self.assertRaises(IndexError):
            queue.dequeue()
        with self.assertRaises(IndexError):
            queue.peek()

        queue.enqueue(99)
        self.assertEqual(queue.dequeue(), 99)

    def test_linked_list_head_middle_tail_and_empty(self):
        linked = SinglyLinkedList()
        linked.insert(0, 10)
        linked.insert(1, 30)
        linked.insert(1, 20)

        self.assertEqual(linked.traverse(), [10, 20, 30])
        self.assertEqual(linked.delete(1), 20)
        self.assertEqual(linked.delete(1), 30)
        self.assertEqual(linked.delete(0), 10)
        self.assertEqual(linked.traverse(), [])
        self.assertEqual(len(linked), 0)

        with self.assertRaises(IndexError):
            linked.delete(0)
        with self.assertRaises(IndexError):
            linked.insert(1, 5)

        # An emptied list should work again when a new value is added.
        linked.insert(0, 99)
        self.assertEqual(linked.traverse(), [99])


if __name__ == "__main__":
    unittest.main()
