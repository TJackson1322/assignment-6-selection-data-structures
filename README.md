# Assignment 6 Selection Algorithms and Elementary Data Structures

Tabbatha Jackson
Algorithms and Data Structures (MSCS-532-B01)
University of the Cumberlands

## Running the project

Use Python 3. No third-party packages are required. Open a terminal in this folder.

Run the demonstrations:

```bash
python3 selection_algorithms.py
python3 data_structures.py
python3 matrix.py
python3 stack_queue.py
python3 linked_list.py
```

Run all eight correctness tests:

```bash
python3 -m unittest -v test_assignment6.py
```

Run the selection benchmark:

```bash
python3 benchmark_selection.py
```

The benchmark writes selection_results.csv in the current directory. Save a copy of the supplied CSV before running it if you want to retain the original measurements.

## Files

| File | Purpose |
| --- | --- |
| selection_algorithms.py | Median of Medians and Randomized Quickselect |
| benchmark_selection.py | Seven trials per algorithm, size, and distribution |
| selection_results.csv | Original benchmark measurements supplied from the student's Mac |
| data_structures.py | Dynamic array with manual resizing and shifting |
| matrix.py | Matrix using custom arrays with cell access and row insertion/deletion |
| stack_queue.py | Array-based stack and resizable circular queue |
| linked_list.py | Singly linked list with insertion, deletion, and traversal |
| test_assignment6.py | Eight tests covering normal operations and edge cases |

The Python files include explanatory # comments about the implementation choices.

## Selection design and complexity

Both algorithms accept a one-based rank k and preserve the input. Inputs should contain mutually comparable finite numeric values. The three-way partition separates smaller, equal, and larger values, so duplicates count as separate ranks.

Median of Medians sorts groups of at most five, selects their middle median, and continues with the relevant partition. Its worst-case recurrence is T(n) <= T(ceil(n/5)) + T(7n/10 + O(1)) + O(n), giving O(n) worst-case time.

Randomized Quickselect chooses a random pivot on each iteration. Its expected runtime is O(n), with O(n²) worst-case time from repeatedly poor pivots. These implementations allocate partition lists and use O(n) auxiliary space. Median of Medians also uses O(log n) recursive depth to select group medians. Sorted is used for small groups, base cases, input preparation, and checking results.

For even input lengths, the benchmark selects the lower middle order statistic. It does not compute the average of the two middle values.

## Data structure costs

| Structure and operation | Time |
| --- | --- |
| Array access or replacement | O(1) |
| Array append | O(1) amortized, O(n) when growing |
| Array insertion or deletion at an arbitrary index | O(n) worst case |
| Matrix cell access or replacement | O(1) |
| Matrix row insertion or deletion | O(r + c) worst case |
| Matrix traversal | O(r × c) |
| Stack push | O(1) amortized, O(n) when growing |
| Stack pop or peek | O(1) |
| Queue enqueue | O(1) amortized, O(n) when growing |
| Queue dequeue or peek | O(1) |
| Linked list insertion or deletion at the head | O(1) |
| Linked list insertion or deletion at an arbitrary index | O(n) |
| Linked list traversal | O(n) |

Here r is the number of matrix rows and c is the column count. Arrays and queues retain their allocated capacity after deletion. Their memory usage follows allocated capacity, which may exceed the current element count.

## Benchmark method and findings

The original measurements use sizes 100, 1,000, and 10,000 across random, sorted, reverse-sorted, many-duplicate, and all-equal inputs. Each configuration uses seven trials and reports the median, minimum, and maximum runtime in milliseconds.

Dataset generation, random generator setup, reference sorting, and correctness checks occur outside the timer. The algorithms' internal input copies are included in timing. Algorithm order alternates between trials. Every measured result was checked against the sorted reference.

At 10,000 values, the supplied median runtimes were:

| Distribution | Median of Medians (ms) | Randomized Quickselect (ms) |
| --- | ---: | ---: |
| random | 2.8142 | 1.0145 |
| sorted | 2.1335 | 0.8045 |
| reverse_sorted | 2.0893 | 0.7724 |
| many_duplicates | 1.7632 | 0.7736 |
| all_equal | 0.7926 | 0.2542 |

Randomized Quickselect was faster in all supplied configurations. Median of Medians performs extra work to construct its pivot while offering a worst-case linear guarantee. On all-equal inputs, the three-way partition lets both methods return without repeatedly processing equal values.

These small experiments illustrate implementation costs and input effects. They do not prove asymptotic bounds or reproduce the worst case. Runtime varies by machine and background activity, and memory usage was analyzed theoretically rather than measured.

## Verification and report status

All eight supplied tests passed after the explanatory comments were added. Tests cover selection ranks and duplicates, input preservation, invalid ranks, empty structures, array growth, matrix validation, stack order, queue wraparound and growth, and linked list operations.

The written assignment report is being prepared separately and still needs to be added before final submission.
