Q: Contains Duplicate (LC 217) — Given `0 <= len(nums) <= 10**5`, what complexity class does the ceiling permit, and why?
A: `O(n log n)` or better. At `n = 10**5` a linear pass runs `10**5` operations and a log-linear pass `10**5 * log2(10**5) ≈ 1.7 * 10**6`, both trivially affordable. A quadratic pass runs `(10**5)**2 = 10**10`, nearly four orders of magnitude larger and beyond what any time limit absorbs.
TAGS: solutions::arrays_and_hashing::217 slot::constraints
---
Q: Contains Duplicate (LC 217) — With `n` bounded at `10**5`, what is the brute-force approach, its complexity, and its verdict?
A: Compare every element against every later element, returning `True` on the first match. Time `O(n^2)`, space `O(1)`. The approach is trivially correct and is the only candidate needing no auxiliary memory. The pairwise comparisons sum to `n(n-1) / 2`, which at the ceiling equates to roughly `5 * 10**9` operations, guaranteeing a Time Limit Exceeded.
TAGS: solutions::arrays_and_hashing::217 slot::brute_force
---
Q: Contains Duplicate (LC 217) — What is the chosen approach, what invariant makes it correct, and what is its complexity?
A: A seen-set with early exit. Walk the array holding the values already seen in a set, and return `True` the moment the current element is already present. The invariant is that `seen` holds exactly the values at indices before the current one, which means a hit can only indicate an earlier occurrence, and that is a duplicate. `O(n)` time and `O(n)` space, with an `O(1)` best case.
TAGS: solutions::arrays_and_hashing::217 slot::optimal pattern::seen_set
---
Q: Contains Duplicate (LC 217) — The seen-set's `O(n)` time bound rests on what unstated assumption?
A: That lookups are average-case `O(1)` and insertions amortized average-case `O(1)`, where the amortization covers the table's occasional resize. The premise is a hash function distributing keys evenly. Adversarial input can force every key onto the same slot, which collapses a single operation to `O(n)`. The loop performs one such operation for each of the `n` elements, which compounds the whole pass to `O(n^2)`.
TAGS: solutions::arrays_and_hashing::217 slot::assumption pattern::seen_set
---
Q: Contains Duplicate (LC 217) — Given `0 <= len(nums) <= 10**5`, `-10**9 <= nums[i] <= 10**9`, and a read-only array, walk the full elimination across all candidates.
A: 1. The ceiling permits `O(n log n)` or better, which invalidates the `O(n^2)` brute force approach. 2. Sort-and-scan reaches `O(n log n)`, but the read-only constraint forces an `O(n)` copy, stripping the space advantage it has over hashing. 3. Direct addressing gives worst-case `O(1)` access, but the value domain forces an array of `m = 2 * 10**9 + 1` slots that must be zeroed before use, incurring a `Θ(m)` cost in both time and auxiliary space that shifts the overall time complexity to `O(n + m)` and guarantees a Memory Limit Exceeded at allocation. 4-5. Set-length and the seen-set share an `O(n)`/`O(n)` worst-case but seen-set wins because it decides on the first repeat, whereas set-length materializes the entire set before it can decide at all.
TAGS: solutions::arrays_and_hashing::217 slot::selection pattern::seen_set
---
Q: Contains Duplicate (LC 217) — Given `0 <= len(nums) <= 10**5` and `-10**9 <= nums[i] <= 10**9`, which inputs must the implementation be tested against?
A: `[1, 2, 3, 1] -> True` (duplicate separated by distance); `[1, 2, 3, 4] -> False` (forces the worst case in both time and space); `[2, 2] -> True` (triggers the `O(1)` early exit); `[7, 7, 7] -> True` (halts on the first repeat, not the last); `[-10**9, 0, 10**9] -> False` (the value extremes plus zero); `[] -> False` and `[1] -> False` (fewer than two elements cannot form a pair).
TAGS: solutions::arrays_and_hashing::217 slot::edge_cases
---
Q: Contains Duplicate (LC 217) — How do you adapt if you cannot afford `O(n)` extra space but may mutate the input?
A: Abandon the set. Sort in place with an algorithm needing no auxiliary array, such as heapsort, then scan adjacent elements. This holds space at `O(1)` and deliberately trades time up to `O(n log n)`.
TAGS: solutions::arrays_and_hashing::217 slot::pivot
---
Q: Contains Duplicate (LC 217) — How do you adapt for an unbounded stream?
A: Exact deduplication needs space proportional to every distinct value ever seen, which has no bound. Substitute a Bloom filter, which enforces a fixed memory ceiling by trading exactness for a tunable false-positive rate while guaranteeing zero false negatives.
TAGS: solutions::arrays_and_hashing::217 slot::pivot
---
Q: Contains Duplicate (LC 217) — How do you adapt the seen-set for a duplicate within index distance `k` (LC 219)?
A: Convert the set into a sliding window. As the scan advances, evict the element that falls outside the `i - k` boundary. This bounds space at `O(k)` rather than `O(n)`.
TAGS: solutions::arrays_and_hashing::217 slot::pivot pattern::sliding_window
---
Q: Contains Duplicate (LC 217) — How do you adapt for a duplicate within index distance `k` and value difference `t` (LC 220)?
A: A hash set is insufficient, because the query becomes a range query rather than an exact match. Pivot to an ordered structure such as a balanced BST over the window, giving `O(n log k)`, or to bucketing by value width, giving `O(n)`.
TAGS: solutions::arrays_and_hashing::217 slot::pivot pattern::bucketing