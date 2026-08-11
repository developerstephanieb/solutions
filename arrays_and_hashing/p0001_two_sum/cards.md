Q: Two Sum (LC 1) — With `n` bounded at `1000`, what is the brute-force approach, its complexity, and its verdict?
A: A nested loop evaluating every unique pair for the target sum. Time `O(n^2)`, space `O(1)`. Operationally viable under the ceiling, peaking at roughly `5 * 10**5` operations, but asymptotically suboptimal.
TAGS: solutions::arrays_and_hashing::1 slot::brute_force
---
Q: Two Sum (LC 1) — What does the brute force waste, and what pattern does that force?
A: The inner loop scans for a complement that can be calculated (`target - nums[i]`), which calls for a `complement-map`.
TAGS: solutions::arrays_and_hashing::1 slot::pattern pattern::complement_map
---
Q: Two Sum (LC 1) — What is the objective, chosen approach, what invariant makes it correct, and what is its complexity?
A: To optimize time to `O(n)`, trade auxiliary space for a single forward pass that looks up each element's complement before inserting the element itself. At the start of any iteration `i`, the map holds `nums[:i]` keyed to their indices, which guarantees any hit is a distinct earlier element, preventing self-pairing and resolving duplicate values to two distinct indices. The stored index is also smaller than `i`, which satisfies the smaller-index-first requirement. Average-case `O(n)` time with an `O(1)` best case, space `O(n)`.
TAGS: solutions::arrays_and_hashing::1 slot::optimal pattern::complement_map