# Assignment 6 Report: Medians, Order Statistics & Elementary Data Structures

**Course:** MSCS 532 — Algorithms and Data Structures  
**Student:** Peter Nwochie Tiewah  
**Date:** November 22, 2026

## 1. Introduction

This assignment compares two order-statistic selection algorithms and implements basic data structures from scratch. Selection returns the kth smallest value without paying for a full sort. The implementations prioritize correctness, especially on repeated keys, and use measured benchmarks to connect theoretical complexity with actual Python execution time.

## 2. Part 1: Order Statistics

### 2.1 Implementation and design

`src/selection.py` includes `deterministic_select` (Median of Medians) and `randomized_select` (Randomized Quickselect). Both accept a sequence of integers and a **1-based** rank `k`, validate the rank, and copy the sequence to avoid mutating caller-owned data. Both partition into `< pivot`, `== pivot`, and `> pivot` regions using an in-place Dutch-national-flag style loop. This is especially useful for duplicate-rich arrays: when the desired rank falls inside the equal band, the algorithm returns immediately rather than repeatedly processing equal elements.

For **Median of Medians**, the algorithm splits the active range into blocks of at most five, sorts each tiny block, finds the block medians, recursively selects the median of those medians as pivot, partitions the active range, and continues only into the region holding the target rank. The Python implementation copies the active slice for median grouping and uses a small recursive helper for selecting the pivot; its outer selection loop is iterative.

For **Randomized Quickselect**, a pseudo-random pivot is drawn uniformly from the current active region. After three-way partitioning, only the region containing the target rank is retained. The optional seeded random-number generator is useful for reproducible testing; the benchmark seeds a fresh generator on each repetition.

### 2.2 Deterministic time-complexity analysis

For groups of five, at least approximately 3n/10 elements are guaranteed to be on either side of the median-of-medians pivot, except for a constant number of leftover/group-boundary elements. Consequently, the largest recursive selection region contains at most approximately 7n/10 elements. Finding the pivot recursively costs `T(ceil(n/5))`; grouping and partitioning take O(n). The recurrence is:

\[
T(n) \leq T(\lceil n/5\rceil) + T(7n/10 + O(1)) + cn.
\]

Because `1/5 + 7/10 = 9/10 < 1`, the recurrence solves to **O(n) worst-case time**. This guarantee applies even to already sorted, reverse-sorted, or adversarial inputs. The sum of sizes of all live arrays/slices used by this implementation is O(n) auxiliary space at peak; the recursive median pivot helper adds O(log n) stack depth. Python sorting each group of at most five has constant bounded cost.

### 2.3 Randomized time-complexity analysis

Each partition scans the current subarray once, taking O(n). Random pivot choice makes the expected surviving partition a constant fraction of the input; the expected recurrence yields **E[T(n)] = O(n)**. In the pathological case where successive pivots leave `n-1`, `n-2`, ... elements to inspect, total work is **O(n²)**. Randomization makes such sequences unlikely but does not make the worst case impossible. This implementation uses an iterative selection loop and partitions its private array copy in place. It therefore uses O(n) auxiliary space for the copy and O(1) additional selection-loop state. The pseudorandom generator maintains constant-size state for this analysis.

### 2.4 Empirical experimental design

The benchmark uses Python's `time.perf_counter_ns` to time each complete selection call, including input copying, pivot selection, and partitioning. Data sets contain 100, 500, 1,000, 2,000, or 4,000 integers and four distributions: random uniform values, ascending sorted, descending sorted, and duplicates drawn from 10 distinct values. The target is the lower median (`k = (n + 1)//2`). Each algorithm/distribution/size is repeated seven times, and the **median elapsed time in milliseconds** is reported. All computed selections are checked against the sorted reference value. This is a single-run sample, not a hardware-independent performance claim; timings vary with load, interpreter, and machine.

### 2.5 Measured results

| n | Input distribution | Deterministic (ms) | Randomized (ms) |
|---:|---|---:|---:|
| 100 | random | 0.0442 | 0.0387 |
| 100 | sorted | 0.0334 | 0.0366 |
| 100 | reverse | 0.0386 | 0.0319 |
| 100 | duplicates | 0.0271 | 0.0261 |
| 500 | random | 0.2222 | 0.1515 |
| 500 | sorted | 0.1960 | 0.2091 |
| 500 | reverse | 0.2160 | 0.2206 |
| 500 | duplicates | 0.0855 | 0.1549 |
| 1,000 | random | 0.4577 | 0.3840 |
| 1,000 | sorted | 0.4164 | 0.3622 |
| 1,000 | reverse | 0.5148 | 0.4624 |
| 1,000 | duplicates | 0.3152 | 0.2172 |
| 2,000 | random | 0.9706 | 0.6845 |
| 2,000 | sorted | 0.9389 | 0.9784 |
| 2,000 | reverse | 1.2144 | 1.0917 |
| 2,000 | duplicates | 0.3376 | 0.5099 |
| 4,000 | random | 2.0854 | 1.8200 |
| 4,000 | sorted | 1.9614 | 1.6887 |
| 4,000 | reverse | 1.8131 | 1.5049 |
| 4,000 | duplicates | 0.8666 | 1.2546 |

**Interpretation.** In this experiment, randomized selection often ran faster than the deterministic algorithm because it avoids the grouping, small-array sorting, and recursive pivot-selection work. Those are constant-factor costs even though both algorithms are linear in the appropriate theoretical sense. Ordered inputs did not force catastrophic behavior for Randomized Quickselect, because the pivot was chosen randomly rather than always taken from an array endpoint. The many-duplicates workload is efficiently handled by the equal-to-pivot band; it may improve either algorithm's runtime depending on pivot choice. At these modest sizes, Python execution overhead and timer noise can obscure smooth asymptotic trends. These measurements do not establish that randomized selection always wins; the deterministic method offers a stronger worst-case bound.

## 3. Part 2: Elementary Data Structures

### 3.1 Designs and implementations

`DynamicArray` stores elements in a Python list used as a **fixed-capacity backing buffer**, initially of length four. It manages its own logical size, shifts elements for middle insertion/deletion, doubles capacity when full, and halves capacity when at most one-quarter full (never below four). Python list allocation is used as the underlying storage primitive; resizing logic is implemented explicitly. This is a conceptual dynamic-array exercise, not a native contiguous-memory reimplementation.

`Matrix` uses a list of row lists, validates the rectangular width for inserted rows, supports indexed get/set, row insertion, and row deletion. Its public operations manipulate **entire rows** for insertion/deletion; changing the number of columns is not implemented. The initial fill value should be immutable because object-valued fills share the same reference.

`ArrayStack` wraps `DynamicArray`, with push, pop, and peek using the final logical slot (LIFO). `ArrayQueue` uses a circular-buffer Python list with a head index and logical size; it doubles the buffer only when full. This keeps dequeue O(1) by eliminating a front-of-list shift. `SinglyLinkedList` uses explicit `Node` objects and maintains both head and tail pointers, supporting prepend, append, positional insert, first-match deletion by value, and traversal.

### 3.2 Operation complexity

| Data structure | Operation | Time complexity | Notes |
|---|---|---|---|
| Dynamic array | get by index | O(1) | Direct indexed read |
| Dynamic array | append | O(1) amortized, O(n) worst-case | Resize may copy all elements |
| Dynamic array | insert/delete at arbitrary index | O(n) | Element shifts and possibly resize |
| Matrix | get/set one cell | O(1) | Two list index accesses |
| Matrix | insert/delete row | O(r + c) worst-case | r rows may shift; inserted row of width c is copied; delete returns existing row |
| Array stack | push | O(1) amortized | Underlying dynamic-array append |
| Array stack | pop/peek | O(1) amortized / O(1) | Occasional shrink on pop; peek constant |
| Circular array queue | enqueue | O(1) amortized | Occasional grow |
| Circular array queue | dequeue/peek | O(1) | No shifting; buffer is not shrunk |
| Singly linked list | prepend/append | O(1) | Head/tail pointers |
| Singly linked list | insert at index | O(n) generally | O(1) at front or end |
| Singly linked list | delete first matching value | O(n) | Must search for predecessor |
| Singly linked list | traverse | O(n) | Visit each node |

Here `r` is current number of matrix rows and `c` is column count. A matrix with `r` rows and `c` columns uses O(rc) storage. Dynamic arrays, queues, and singly linked lists each use O(n) overall storage for n stored elements, although linked lists also allocate a separate node/reference per entry. Each linked-list insertion creates an O(1)-space node; linked-list traversal's iterator holds O(1) state.

### 3.3 Arrays versus linked lists for stacks and queues

An array-backed stack has compact storage, fast indexing, good spatial locality, and amortized O(1) push/pop. A head-insertion linked-list stack can guarantee O(1) push/pop without resizing, but uses per-node references/allocation and poorer cache locality. An array-backed queue must use a circular buffer (as in this project) to avoid O(n) front-deletion shifts. A linked queue using both head and tail nodes provides O(1) enqueue/dequeue, but costs additional memory per item. In a practical high-throughput implementation, cache behavior and memory allocator overhead matter alongside asymptotic complexity. The Python-standard `collections.deque` would usually be the production choice for a queue, but this assignment intentionally implements the mechanism from scratch.

### 3.4 Real-world applications and trade-offs

**Arrays and matrices:** fixed-index tables, pixel grids, scientific measurements, dynamic lists and dense numerical data. Choose arrays when indexed access, compact representation, or data locality is important. For large numerical matrices, numerical libraries are preferable to nested Python lists because they can use compact numeric storage and optimized operations.

**Stacks:** undo histories, expression parsing, depth-first search, and nested function-call tracking. LIFO behavior makes the most recent operation available first; array-backed stacks are typically straightforward when occasional resize is acceptable.

**Queues:** customer-service lines, print jobs, task scheduling, and breadth-first search. FIFO behavior preserves arrival order. Circular arrays avoid shifting, while linked queues can expand one node at a time without contiguous-buffer resizing.

**Singly linked lists:** workloads that frequently insert at the head or at a **known node position**, and teaching pointer/reference manipulation. They are less suited to frequent random-index access because reaching position `i` takes O(i) time. Although inserting after a known node can be O(1), locating that node generally costs O(n).

## 4. Testing and limitations

Automated unit tests cover small and duplicate-heavy selection inputs, ascending/descending order, all possible ranks on several array sizes, invalid ranks, dynamic-array resizing, matrix row edits, empty stack/queue exceptions, circular queue wrap/growth, and linked-list head/tail deletion. The benchmark performs an independent correctness check on every timed result. Seven test methods passed in the run associated with this report.

The benchmark reports wall-clock timings from one execution and should be rerun on the student's final machine if the interpreter or host differs. It measures selection algorithms only, as requested for the empirical section of Part 1. Optional rooted-tree implementation was omitted because the assignment describes it as optional. The matrix API supports row-level insertion/deletion rather than arbitrary column restructuring.

## 5. Conclusion

Both order-statistic methods avoid the O(n log n) work of full comparison sorting when only one rank is needed. Randomized Quickselect has low pivot-selection overhead and expected linear performance; Median of Medians guarantees linear worst-case performance at the cost of more pivot preparation. For elementary data structures, the choice between contiguous array storage and linked nodes affects not just big-O complexity, but also memory overhead, cache locality, resizing, and implementation complexity. Selecting the appropriate structure depends on the mix of indexed access, insertion, deletion, and FIFO/LIFO operations.

## References

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Blum, M., Floyd, R. W., Pratt, V., Rivest, R. L., & Tarjan, R. E. (1973). Time bounds for selection. *Journal of Computer and System Sciences, 7*(4), 448–461. https://doi.org/10.1016/S0022-0000(73)80033-9
- Python Software Foundation. (n.d.). *time — Time access and conversions*. https://docs.python.org/3/library/time.html
