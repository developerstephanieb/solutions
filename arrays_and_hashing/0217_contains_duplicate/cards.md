Q: Contains Duplicate (LC 217) — what is the optimal approach and its complexity?
A: A seen-set with early exit: walk the array holding seen elements in a set, return True the moment the current element is already present. `O(n)` time, `O(n)` space.
TAGS: solutions::arrays_and_hashing::217 pattern::seen_set
---
Q: Contains Duplicate (LC 217) — what invariant makes the seen-set pass correct?
A: `seen` holds exactly the elements at indices before the current one. If the current element is already in `seen`, it must have appeared earlier, so a duplicate exists.
TAGS: solutions::arrays_and_hashing::217 pattern::seen_set
---
Q: Contains Duplicate (LC 217) — why prefer the seen-set over `len(set(nums)) != len(nums)`?
A: Same `O(n)`/`O(n)` worst case, but the seen-set early-exits on the first repeat (`O(1)` best case), whereas the set-length always materialises the entire set before deciding.
TAGS: solutions::arrays_and_hashing::217 pattern::seen_set
---
Q: Contains Duplicate (LC 217) — the seen-set's `O(n)` time bound rests on what unstated assumption?
A: That hash-set membership and insertion are average `O(1)`. Element hashability itself is a given by the `int` type; the assumption is the average-case cost — adversarial collisions make a single op `O(n)`.
TAGS: solutions::arrays_and_hashing::217 pattern::seen_set
---
Q: Contains Duplicate (LC 217) — why does the brute-force `O(n^2)` approach fail the constraints?
A: Checking all unique pairs sums to exactly `n(n-1)/2`, simplifying to roughly `n^2/2` comparisons. At the ceiling `n = 10**5`, this results in `5 * 10**9` (5 billion) operations - far too slow. This guarantees a Time Limit Exceeded (TLE) error on standard hardware. The constraint ceiling forces a linear or log-linear approach.
TAGS: solutions::arrays_and_hashing::217
---
Q: Contains Duplicate (LC 217) — if you cannot afford `O(n)` extra space but may mutate the input, what is the pivot?
A: Sort in place and scan adjacent elements. This preserves `O(1)` space at the cost of degrading time to `O(n log n)` and mutating the input.
TAGS: solutions::arrays_and_hashing::217
---
Q: Contains Duplicate (LC 217) — over an unbounded stream where an `O(n)` set would OOM, what is the pivot?
A: Exact deduplication requires infinite space, guaranteeing an OOM crash. Pivot to a Bloom Filter: it enforces a strict memory ceiling by trading exactness for a managed false-positive rate, while mathematically guaranteeing zero false negatives.
TAGS: solutions::arrays_and_hashing::217
---
Q: Contains Duplicate (LC 217) — how do you adapt the seen-set for a duplicate within index distance `k` (LC 219)?
A: Convert the set into a sliding window. As the iteration pointer advances, explicitly evict elements that fall behind the `i - k` index boundary. This bounds space complexity strictly to `O(k)`.
TAGS: solutions::arrays_and_hashing::217 pattern::sliding_window