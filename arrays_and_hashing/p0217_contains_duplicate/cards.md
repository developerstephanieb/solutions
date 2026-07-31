Q: Contains Duplicate (LC 217) — With `n` bounded at `10**5`, what is the brute-force approach, its complexity, and its verdict?
A: Compare every element against every later element, returning `True` on the first match. Time `O(n^2)`, space `O(1)`. It is trivially correct and the only candidate needing no auxiliary memory, but the pairwise comparisons sum to `n(n-1) / 2`, roughly `5 * 10**9` at the ceiling, guaranteeing a Time Limit Exceeded.
TAGS: solutions::arrays_and_hashing::217 slot::brute_force
---
Q: Contains Duplicate (LC 217) — What does the brute force waste, and what pattern does that force?
A: Every scan re-derives from the tail what earlier scans already established. Comparing `nums[i]` against `nums[j]` answers a comparison question where the problem asks a membership one. Membership is established once rather than recomputed per element, which calls for a structure answering it in `O(1)`: the `seen-set`.
TAGS: solutions::arrays_and_hashing::217 slot::pattern pattern::seen_set
---
Q: Contains Duplicate (LC 217) — What is the chosen approach, what invariant makes it correct, and what is its complexity?
A: A seen-set with early exit. Walk the array holding the values already seen in a set, and return `True` the moment the current element is already present. The invariant is that `seen` holds exactly the values at indices before the current one, so a hit indicates an earlier occurrence, which is a duplicate. `O(n)` time and `O(n)` space, with an `O(1)` best case.
TAGS: solutions::arrays_and_hashing::217 slot::optimal pattern::seen_set