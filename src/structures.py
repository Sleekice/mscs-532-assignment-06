"""Basic data structures built with Python lists and linked nodes."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterator


class DynamicArray:
    """An array that grows or shrinks its storage when needed."""

    def __init__(self) -> None:
        # Reserve four slots initially; only the first _size slots are in use.
        self._storage: list[Any] = [None] * 4
        self._size = 0

    def __len__(self) -> int:
        """Return the number of stored elements, not the capacity."""
        return self._size

    def _check_index(self, index: int, allow_end: bool = False) -> None:
        """Reject positions outside the array's valid logical range."""
        # Insertion can use index == size to place an item at the end.
        if not 0 <= index < self._size + int(allow_end):
            raise IndexError("array index out of range")

    def _resize(self, capacity: int) -> None:
        """Copy active values into newly allocated storage."""
        new_storage = [None] * capacity
        for i in range(self._size):
            new_storage[i] = self._storage[i]
        self._storage = new_storage

    def get(self, index: int) -> Any:
        """Read an item directly by its position: O(1)."""
        self._check_index(index)
        return self._storage[index]

    def insert(self, index: int, value: Any) -> None:
        """Insert a value, shifting later elements one position right."""
        self._check_index(index, allow_end=True)
        if self._size == len(self._storage):
            # Doubling capacity avoids reallocating on every append.
            self._resize(2 * len(self._storage))
        for i in range(self._size, index, -1):
            self._storage[i] = self._storage[i - 1]
        self._storage[index] = value
        self._size += 1

    def append(self, value: Any) -> None:
        """Add at the end; O(1) amortized because resizing is occasional."""
        self.insert(self._size, value)

    def delete(self, index: int) -> Any:
        """Remove one item and shift later elements to fill its slot."""
        self._check_index(index)
        removed = self._storage[index]
        for i in range(index, self._size - 1):
            self._storage[i] = self._storage[i + 1]
        self._size -= 1
        # Clear the unused slot so it does not keep an object referenced.
        self._storage[self._size] = None
        if len(self._storage) > 4 and self._size <= len(self._storage) // 4:
            # Shrink only at quarter-full to avoid frequent size changes.
            self._resize(max(4, len(self._storage) // 2))
        return removed

    def to_list(self) -> list[Any]:
        """Return only active elements, hiding unused capacity slots."""
        return self._storage[:self._size]


class Matrix:
    """A rectangular collection of rows with access by row and column."""

    def __init__(self, rows: int, cols: int, fill: Any = 0) -> None:
        if rows < 0 or cols < 1:
            raise ValueError("rows must be >= 0 and cols >= 1")
        self.cols = cols
        # Create a separate inner list for every row.
        self.data = [[fill for _ in range(cols)] for _ in range(rows)]

    def _check_cell(self, row: int, col: int) -> None:
        """Make sure both matrix coordinates exist."""
        if not 0 <= row < len(self.data) or not 0 <= col < self.cols:
            raise IndexError("matrix index out of range")

    def get(self, row: int, col: int) -> Any:
        """Read a cell at a specific row and column."""
        self._check_cell(row, col)
        return self.data[row][col]

    def set(self, row: int, col: int, value: Any) -> None:
        """Replace the value in a cell without changing matrix size."""
        self._check_cell(row, col)
        self.data[row][col] = value

    def insert_row(self, index: int, row: list[Any]) -> None:
        """Insert a complete row while preserving the column count."""
        if len(row) != self.cols:
            raise ValueError("row width mismatch")
        if not 0 <= index <= len(self.data):
            raise IndexError("row index out of range")
        # Copy the row so changes to the caller's list will not affect it.
        self.data.insert(index, list(row))

    def delete_row(self, index: int) -> list[Any]:
        """Remove and return a row, shifting later rows upward."""
        if not 0 <= index < len(self.data):
            raise IndexError("row index out of range")
        return self.data.pop(index)


class ArrayStack:
    """A last-in, first-out (LIFO) structure backed by DynamicArray."""

    def __init__(self) -> None:
        self._data = DynamicArray()

    def __len__(self) -> int:
        """Return the number of items on the stack."""
        return len(self._data)

    def push(self, value: Any) -> None:
        """Place a new item on the top of the stack."""
        self._data.append(value)

    def pop(self) -> Any:
        """Remove and return the most recently pushed item."""
        if not len(self):
            raise IndexError("pop from empty stack")
        # The top is at the end, so no other elements need shifting.
        return self._data.delete(len(self) - 1)

    def peek(self) -> Any:
        """Read the top item without removing it."""
        if not len(self):
            raise IndexError("peek from empty stack")
        return self._data.get(len(self) - 1)


class ArrayQueue:
    """A first-in, first-out (FIFO) circular array queue."""

    def __init__(self) -> None:
        self._data: list[Any] = [None] * 4
        self._head = 0  # Index of the oldest item.
        self._size = 0  # Number of items currently in the queue.

    def __len__(self) -> int:
        """Return the number of items waiting in the queue."""
        return self._size

    def _grow(self) -> None:
        """Double capacity and put existing items back in FIFO order."""
        old = self._data
        self._data = [None] * (2 * len(old))
        for i in range(self._size):
            # Modulo wraps the index when it reaches the end of storage.
            self._data[i] = old[(self._head + i) % len(old)]
        self._head = 0

    def enqueue(self, value: Any) -> None:
        """Add a value behind all items already in the queue."""
        if self._size == len(self._data):
            self._grow()
        # Find the next free position without shifting existing items.
        self._data[(self._head + self._size) % len(self._data)] = value
        self._size += 1

    def dequeue(self) -> Any:
        """Remove and return the oldest item in the queue."""
        if not self._size:
            raise IndexError("dequeue from empty queue")
        value = self._data[self._head]
        self._data[self._head] = None
        # Advance the head, wrapping around if needed.
        self._head = (self._head + 1) % len(self._data)
        self._size -= 1
        return value

    def peek(self) -> Any:
        """Read the oldest item without removing it."""
        if not self._size:
            raise IndexError("peek from empty queue")
        return self._data[self._head]


@dataclass
class Node:
    """A linked-list element holding a value and its next-node reference."""

    value: Any
    next: Node | None = None


class SinglyLinkedList:
    """A chain of nodes where each node points to the next one."""

    def __init__(self) -> None:
        self.head: Node | None = None  # First node, or None when empty.
        self.tail: Node | None = None  # Last node, for constant-time append.
        self.size = 0

    def __len__(self) -> int:
        """Return the tracked number of nodes."""
        return self.size

    def prepend(self, value: Any) -> None:
        """Insert a new node before the current head: O(1)."""
        self.head = Node(value, self.head)
        if self.tail is None:
            # The first node is both head and tail.
            self.tail = self.head
        self.size += 1

    def append(self, value: Any) -> None:
        """Add a node at the end using the tail reference: O(1)."""
        node = Node(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def insert(self, index: int, value: Any) -> None:
        """Insert a node at a chosen position in the linked list."""
        if not 0 <= index <= self.size:
            raise IndexError("linked-list index out of range")
        if index == 0:
            self.prepend(value)
        elif index == self.size:
            self.append(value)
        else:
            # Walk to the node just before the insertion position.
            prev = self.head
            for _ in range(index - 1):
                assert prev is not None
                prev = prev.next
            assert prev is not None
            # Point the new node at the old successor, then link it in.
            prev.next = Node(value, prev.next)
            self.size += 1

    def delete(self, value: Any) -> bool:
        """Delete the first matching value; return False if not found."""
        prev: Node | None = None
        current = self.head
        while current is not None:
            if current.value == value:
                if prev is None:
                    # Deleting the head makes its successor the new head.
                    self.head = current.next
                else:
                    # Skip the current node by changing the previous link.
                    prev.next = current.next
                if self.tail is current:
                    self.tail = prev
                self.size -= 1
                return True
            prev, current = current, current.next
        return False

    def __iter__(self) -> Iterator[Any]:
        """Visit node values from head to tail."""
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def to_list(self) -> list[Any]:
        """Convert the linked nodes into a regular Python list."""
        return list(self)
