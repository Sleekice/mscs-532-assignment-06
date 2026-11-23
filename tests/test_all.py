"""Checks correctness, edge cases, and basic operations for both parts."""

import random
import unittest
from src.selection import deterministic_select, randomized_select
from src.structures import DynamicArray, Matrix, ArrayStack, ArrayQueue, SinglyLinkedList


class TestSelection(unittest.TestCase):
    """Validate both kth-smallest algorithms against Python sorting."""
    def test_distributions(self):
        """Check every k across random, sorted, reverse, and equal values."""
        rng = random.Random(42)
        for n in [1, 2, 5, 6, 25, 100]:
            arr = [rng.randint(-10, 10) for _ in range(n)]
            # Small n lets us check every possible answer position.
            for sample in [arr, sorted(arr), sorted(arr, reverse=True), [7] * n]:
                for k in range(1, n + 1):
                    expected = sorted(sample)[k - 1]
                    self.assertEqual(deterministic_select(sample, k), expected)
                    self.assertEqual(randomized_select(sample, k, random.Random(k)), expected)

    def test_invalid(self):
        """Invalid positions and empty inputs should raise ValueError."""
        for func in (deterministic_select, randomized_select):
            for array, k in [([], 1), ([2], 0), ([2], 2)]:
                with self.assertRaises(ValueError):
                    func(array, k)


class TestStructures(unittest.TestCase):
    """Check insertion, removal, access, and order for each structure."""
    def test_array(self):
        """Exercise array growth, front insertion, deletion, and shrinking."""
        a = DynamicArray()
        for i in range(30):
            a.append(i)
        a.insert(0, 99)
        self.assertEqual(a.get(0), 99)
        self.assertEqual(a.delete(0), 99)
        for _ in range(28):
            a.delete(0)
        self.assertEqual(a.to_list(), [28, 29])

    def test_matrix(self):
        """Check cell updates, row changes, and invalid row widths."""
        m = Matrix(2, 3, 0)
        m.set(1, 1, 7)
        self.assertEqual(m.get(1, 1), 7)
        m.insert_row(1, [1, 2, 3])
        self.assertEqual(m.delete_row(1), [1, 2, 3])
        with self.assertRaises(ValueError):
            m.insert_row(0, [1, 2])

    def test_stack(self):
        """Verify last-in-first-out order and empty-stack errors."""
        s = ArrayStack()
        with self.assertRaises(IndexError):
            s.pop()
        for i in range(20):
            s.push(i)
        self.assertEqual(s.peek(), 19)
        self.assertEqual([s.pop() for _ in range(20)], list(reversed(range(20))))

    def test_queue_wrap_and_growth(self):
        """Check queue order even after wraparound and capacity growth."""
        q = ArrayQueue()
        with self.assertRaises(IndexError):
            q.dequeue()
        for i in range(4):
            q.enqueue(i)
        self.assertEqual([q.dequeue() for _ in range(2)], [0, 1])
        for i in range(4, 40):
            q.enqueue(i)
        self.assertEqual([q.dequeue() for _ in range(len(q))], list(range(2, 40)))

    def test_linked_list(self):
        """Check head, middle, and tail changes in a linked list."""
        ll = SinglyLinkedList()
        ll.append(2)
        ll.prepend(1)
        ll.insert(2, 4)
        ll.insert(2, 3)
        self.assertEqual(ll.to_list(), [1, 2, 3, 4])
        self.assertTrue(ll.delete(1))
        self.assertTrue(ll.delete(4))
        self.assertFalse(ll.delete(99))
        self.assertEqual(ll.to_list(), [2, 3])
        ll.append(5)
        self.assertEqual(ll.to_list(), [2, 3, 5])


if __name__ == '__main__':
    unittest.main()
