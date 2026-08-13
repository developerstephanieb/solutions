Q: Contains Duplicate (LC 217) — With `n` bounded at `10**5`, what is the brute-force approach, its complexity, and its verdict?
A: A nested loop evaluating every unique pair for equality. Time `O(n^2)`, space `O(1)`. Exceeds the ceiling at roughly `5 * 10**9` operations, triggering a Time Limit Exceeded.
TAGS: solutions::arrays_and_hashing::217 slot::brute_force
---
Q: Contains Duplicate (LC 217) — What does the brute force waste, and what pattern does that force?
A: The inner loop scans the remaining array for a duplicate that could have been recorded during traversal, which calls for a `seen-set`.
TAGS: solutions::arrays_and_hashing::217 slot::pattern pattern::seen_set
---
Q: Contains Duplicate (LC 217) — What is the objective, chosen approach, what invariant makes it correct, and what is its complexity?
A: To optimize time to `O(n)`, trade auxiliary space for a linear scan testing each element for membership in a hash-set of already seen values. At the start of any iteration `i`, the set holds exactly the values in `nums[:i]`. A hit therefore indicates an earlier occurrence, which is a duplicate, and the scan can exit without examining the rest. Average-case `O(n)` time with an `O(1)` best case, space `O(n)`.
TAGS: solutions::arrays_and_hashing::217 slot::pattern pattern::seen_set
