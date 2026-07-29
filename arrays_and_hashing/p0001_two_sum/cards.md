Q: Two Sum (LC 1) — Given `2 <= len(nums) <= 1000`, what complexity class does the ceiling permit, and why?
A: `O(n^2)` or better. At `n = 1000` a quadratic pass runs `1000**2 = 10**6` operations, which is trivially affordable, and a cubic pass runs `1000**3 = 10**9`, three orders of magnitude larger and beyond what any time limit absorbs.
TAGS: solutions::arrays_and_hashing::1 slot::constraints
---
Q: Two Sum (LC 1) — With `n` bounded at `1000`, what is the brute-force approach, its complexity, and its verdict?
A: For each index `i`, scan the remaining subarray from `i + 1` to `n - 1` testing whether `nums[i] + nums[j] == target`. Time `O(n^2)`, space `O(1)`. The comparisons sum to `n(n-1) / 2`, which at the ceiling equates to roughly `5 * 10**5` operations, well inside any time limit. Because it allocates no auxiliary structure, it establishes an `O(1)` space floor. This approach is therefore dominated rather than excluded.
TAGS: solutions::arrays_and_hashing::1 slot::brute_force
---
Q: Two Sum (LC 1) — What is the chosen approach, what invariant makes it correct, and what is its complexity?
A: A one-pass complement map. For each element compute its complement `target - nums[i]`, and return `[seen[complement], i]` when the complement is already in the map. Otherwise insert `nums[i] -> i` and continue. The invariant is that `seen` holds only values from indices strictly before `i`. Any hit is therefore a distinct earlier element, which prevents self-pairing and resolves duplicate values like `[3, 3]` to two distinct indices. The stored index is also inherently smaller than `i`, satisfying the smaller-index-first requirement without additional sorting. Building the map in full first would break the invariant and require an explicit `i != j` guard in its place. `O(n)` time and `O(n)` space.
TAGS: solutions::arrays_and_hashing::1 slot::optimal pattern::complement_map
---
Q: Two Sum (LC 1) — The complement map's `O(n)` time bound rests on what unstated assumption?
A: That lookups are average-case `O(1)` and insertions amortized average-case `O(1)`, where the amortization covers the table's occasional resize. The premise is a hash function distributing keys evenly. Adversarial input can force every key onto the same slot, which collapses a single operation to `O(n)`. The loop performs one such operation for each of the `n` elements, which compounds the whole pass to `O(n^2)`.
TAGS: solutions::arrays_and_hashing::1 slot::assumption pattern::complement_map
---
Q: Two Sum (LC 1) — Given `2 <= len(nums) <= 1000`, a read-only array, and a required return of indices in ascending order, walk the elimination across the candidates.
A: 1. The ceiling excludes only cubic and worse, is loose enough to admit every candidate, which moves the decision onto asymptotics and the index contract. 2. Brute force is the only candidate needing no auxiliary memory, but it is the slowest. 3. Sort-plus-two-pointers improves time to `O(n log n)` but requires `O(n)` space since preserving the original indices forces a `(value, index)` tuple array. 4. The one-pass map achieves `O(n)` time while enforcing the distinct-index and ordering contracts through looking up before inserting rather than an explicit `i != j` guard.
TAGS: solutions::arrays_and_hashing::1 slot::selection pattern::complement_map
---
Q: Two Sum (LC 1) — Given `2 <= len(nums) <= 1000` and `-10**7 <= nums[k], target <= 10**7`, which inputs must the implementation be tested against?
A: `([2, 7, 11, 15], 9) -> [0, 1]` (match completes on the second element); `([3, 2, 4], 6) -> [1, 2]` (complement of an interior element); `([3, 3], 6) -> [0, 1]` (equal values, distinct indices); `([-1, -2, -3, -4], -6) -> [1, 3]` (all negative); `([-3, 4, 3, 90], 0) -> [0, 2]` (zero target across a sign change); `([1, 2], 3) -> [0, 1]` (`n == 2`, the lower bound).
TAGS: solutions::arrays_and_hashing::1 slot::edge_cases
---
Q: Two Sum (LC 1) — How do you adapt when the contract drops the requirement to return indices?
A: Return `[complement, num]` at the match, which removes the need for the `(value, index)` tuple array and makes sort-plus-two-pointers competitive again. With mutation permitted, sorting in place with an algorithm needing no auxiliary array, such as heapsort, then sweeping two pointers inward gives `O(n log n)` time at `O(1)` space. Under a read-only array the sort still needs an `O(n)` copy, which leaves the complement map ahead on time at equal space.
TAGS: solutions::arrays_and_hashing::1 slot::pivot pattern::two_pointers
---
Q: Two Sum (LC 1) — How do you adapt when the input arrives already sorted (LC 167)?
A: Abandon the map for a two-pointer boundary sweep. Start a pointer at each end and converge inward, incrementing the left pointer to raise the pair sum and decrementing the right to lower it. This reaches `O(n)` time at `O(1)` space. Sorting a raw array to reach this state is not free, because the sort loses the original indices the problem asks for.
TAGS: solutions::arrays_and_hashing::1 slot::pivot pattern::two_pointers
---
Q: Two Sum (LC 1) — How do you adapt to return every distinct pair summing to the target rather than the first?
A: Early termination is no longer available, which calls for sort-plus-two-pointers over the whole array. Sorting groups equal values adjacently, which means an ordinary pointer step can land on the same value and record the same pair twice. Skip the repeats by advancing before comparing: `left += 1`, followed by `while left < right and nums[left] == nums[left - 1]: left += 1`. Advancing first keeps `left - 1` non-negative, and the `left < right` bound keeps the skip from running past the opposing pointer.
TAGS: solutions::arrays_and_hashing::1 slot::pivot pattern::two_pointers
---
Q: Two Sum (LC 1) — How do you adapt when a valid pair is no longer guaranteed to exist?
A: The `-> list[int]` return type cannot be honoured on a miss. Widen the signature to `list[int] | None` and return `None` when no match is found. Under the original guarantee, reaching the end of the loop without a result meant the input was invalid, which justified a `ValueError`. A miss is now an expected outcome, which requires a `None` return rather than an exception.
TAGS: solutions::arrays_and_hashing::1 slot::pivot
---
Q: Two Sum (LC 1) — How do you adapt for three elements summing to the target (LC 15)?
A: Fix one element as a pivot and reduce the remainder to a two-sum on `target - pivot`. Sort first, then for each pivot run a two-pointer sweep over the subarray to its right. An `O(n)` sweep across each of `n` pivots gives `O(n^2)` time.
TAGS: solutions::arrays_and_hashing::1 slot::pivot pattern::two_pointers