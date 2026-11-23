"""Quick demonstration of required features."""
from src.selection import deterministic_select, randomized_select
from src.structures import DynamicArray, Matrix, ArrayStack, ArrayQueue, SinglyLinkedList


def main():
    """Show a short example of each algorithm and data structure."""
    # Both selection methods should return the same third-smallest value.
    values = [9, 2, 7, 2, 5, 1]
    print('Input:', values, '3rd smallest:', deterministic_select(values, 3), randomized_select(values, 3))
    # Insert and remove values from a resizable array.
    array = DynamicArray()
    array.append('A')
    array.insert(1, 'B')
    print('Array:', array.to_list(), 'deleted:', array.delete(0))
    # Change a matrix cell and add/remove a complete row.
    matrix = Matrix(2, 2)
    matrix.set(0, 1, 7)
    matrix.insert_row(2, [8, 9])
    print('Matrix:', matrix.data, 'removed row:', matrix.delete_row(2))
    # A stack returns the most recently added item first.
    stack = ArrayStack()
    stack.push('first')
    stack.push('last')
    print('Stack pop:', stack.pop())
    # A queue returns the oldest item first.
    queue = ArrayQueue()
    queue.enqueue('first')
    queue.enqueue('last')
    print('Queue dequeue:', queue.dequeue())
    # A linked list connects nodes instead of shifting array elements.
    linked = SinglyLinkedList()
    linked.append(1)
    linked.append(3)
    linked.insert(1, 2)
    linked.delete(3)
    print('Linked list:', linked.to_list())


# Keep the demo from running automatically when imported.
if __name__ == '__main__':
    main()
