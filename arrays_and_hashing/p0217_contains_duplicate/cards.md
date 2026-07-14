Q: Contains Duplicate (LC 217) — what is the optimal approach and its complexity?
A: A seen-set with early exit. Walk the array holding the values already seen in a set, and return True the moment the current element is already present. `O(n)` time and `O(n)` space, with an `O(1)` best case.
TAGS: solutions::arrays_and_hashing::217 pattern::seen_set
---
Q: Contains Duplicate (LC 217) — what invariant makes the seen-set pass correct?
A: `seen` holds exactly the elements at indices before the current one. If the current element is already in `seen`, it must have appeared earlier, so a duplicate exists.
TAGS: solutions::arrays_and_hashing::217 pattern::seen_set
---
Q: Contains Duplicate (LC 217) — why prefer the seen-set over `len(set(nums)) != len(nums)`?
A: Both share the same `O(n)`/`O(n)` worst case, but the seen-set early-exits on the first repeat, giving an `O(1)` best case. The set-length check materializes the entire set before it can decide.
TAGS: solutions::arrays_and_hashing::217 pattern::seen_set
---
Q: Contains Duplicate (LC 217) — the seen-set's `O(n)` time bound rests on what unstated assumption?
A: That hash-set membership and insertion are average-case `O(1)`. Hashability itself is a given, carried by the `int` type; the assumption is the average-case cost. Adversarial input can force every key into one bucket, which collapses a single operation to `O(n)`.
TAGS: solutions::arrays_and_hashing::217 pattern::seen_set
---
Q: Contains Duplicate (LC 217) — why does the brute-force `O(n^2)` approach fail the constraints?
A: Checking all unique pairs sums to exactly `n(n-1)/2`, roughly `n^2/2`. At the ceiling `n = 10**5` that is about `5 * 10**9` (5 billion) operations, which guarantees a Time Limit Exceeded. The ceiling forces a linear or log-linear approach.
TAGS: solutions::arrays_and_hashing::217
---
Q: Contains Duplicate (LC 217) — if you cannot afford `O(n)` extra space but may mutate the input, what is the pivot?
A: Sort in place with an algorithm needing no auxiliary array, such as heapsort, then scan adjacent elements. This preserves space at `O(1)` and trades time up to `O(n log n)`.
TAGS: solutions::arrays_and_hashing::217
---
Q: Contains Duplicate (LC 217) — over an unbounded stream where an `O(n)` set would OOM, what is the pivot?
A: Exact deduplication needs space proportional to every distinct value ever seen, which has no bound. Substitute a Bloom filter, which enforces a fixed memory ceiling by trading exactness for a managed false-positive rate while guaranteeing zero false negatives.
TAGS: solutions::arrays_and_hashing::217
---
Q: Contains Duplicate (LC 217) — how do you adapt the seen-set for a duplicate within index distance `k` (LC 219)?
A: Convert the set into a sliding window. As the scan advances, evict the element that falls outside the `i - k` boundary. This bounds space at `O(k)` rather than `O(n)`.
TAGS: solutions::arrays_and_hashing::217 pattern::sliding_window