# ref-dsa

> **Synopsis:** A top-down reference for **Data Structures and Algorithms**. Content spans theoretical foundations and application. Part of the Ref-Series, a collection of high-signal technical documentation.

---

## Repository Structure

The repository is organized into thematic units, containing individual modules ordered by complexity.

```
ref-data-structures-algorithms/
├── 01-analysis-framework/
├── 02-linear-structures/
├── 03-nonlinear-structures/
├── 04-recursion/
├── 05-sorting/
├── 06-searching/
├── 07-graph-algorithms/
├── 08-dynamic-programming/
├── 09-greedy-algorithms/
├── 10-backtracking/
├── 11-bit-manipulation/
├── 12-string-algorithms/
├── 98-solutions/
├── 99-resources/
├── .gitignore
├── Makefile
└── README.md
```

* [**01-analysis-framework**](./01-analysis-framework): RAM model, Big-O notation, Master Theorem, and correctness proofs.
* [**02-linear-structures**](./02-linear-structures): Arrays, Linked Lists, Stacks, Queues, and Hash Tables.
* [**03-nonlinear-structures**](./03-nonlinear-structures): BSTs, Heaps, AVL/Red-Black Trees, Tries, Union-Find, and Graph representations.
* [**04-recursion**](./04-recursion): Stack mechanics, Tail recursion, and Divide & Conquer strategies.
* [**05-sorting**](./05-sorting): Quadratic sorts, Merge/Quick/Heap sort, and Linear sorts (Radix/Counting).
* [**06-searching**](./06-searching): Binary Search invariants and Selection algorithms (QuickSelect).
* [**07-graph-algorithms**](./07-graph-algorithms): BFS/DFS, Shortest Paths (Dijkstra/Bellman-Ford), Connectivity (SCC), and MSTs.
* [**08-dynamic-programming**](./08-dynamic-programming): Memoization/Tabulation patterns (Linear, Grid, Knapsack, Strings).
* [**09-greedy-algorithms**](./09-greedy-algorithms): Greedy choice property, Interval Scheduling, and Huffman Coding.
* [**10-backtracking**](./10-backtracking): State-space trees, Pruning, N-Queens, and Sudoku solvers.
* [**11-bit-manipulation**](./11-bit-manipulation): Two's Complement, bitwise logic, and low-level optimization hacks.
* [**12-string-algorithms**](./12-string-algorithms): Pattern matching (KMP) and Rolling Hash (Rabin-Karp).
* [**98-solutions**](./98-solutions): Python implementations of standard problems, automatically indexed by [**Company**](./98-solutions/index-by-company.md) and [**Topic**](./98-solutions/index-by-topic.md).
* [**99-resources**](./99-resources): Visualization scripts, badge assets, and complexity sheets.

---

## Module Structure

Every **topic** within a module adheres to a standardized structure.

* **Definition**: A precise, formal definition of the concept.

* **Intuition**: The logical reasoning behind the design or algorithm.

* **Formalism**: The core domain analysis.

* **Implementation**: Isolated code examples or configuration snippets.

---

## Usage

This repository includes a Makefile to automate documentation, generate assets, and audit progress.

| Command       | Description                                                                   |
| :------------ | :---------------------------------------------------------------------------- |
| `make index`  | Scans `98-solutions/` and re-generates the **Topic** and **Company** indexes. |
| `make stats`  | Displays a count of current units, modules, and solved problems.              |
| `make assets` | Generates the SVG difficulty badges for offline documentation.                |