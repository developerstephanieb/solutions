# 0217. Contains Duplicate

`LC 217` · `Easy` · `Arrays & Hashing` · pattern: `seen-set` · ref: `dsa/patterns/hashing/seen_set`

## 1. Requirements & Scoping

**Problem** 

Given an integer array `nums`, return `True` if any value appears at least twice, and `False` if every element is distinct.

**Contract**

- **Signature:** `hasDuplicate(nums: list[int]) -> bool`
- **Length bounds:** `0 <= len(nums) <= 10**5`. Fewer than two elements cannot form a duplicate, which makes the answer `False`.
- **Value range:** `-10**9 <= nums[i] <= 10**9`.
- **Mutability:** Unspecified, and therefore treated as read-only.

**Assumptions**

- **Average-case `O(1)` hashing:** Assumes a hash function that distributes keys evenly, which gives average-case `O(1)` lookups and amortized average-case `O(1)` insertions, and an overall time bound of `O(n)`. **Degradation:** Adversarial input can force every key onto the same slot, which collapses a single operation from `O(1)` to `O(n)`. The loop performs one such operation for each of the `n` elements, which compounds the whole pass to `O(n^2)`. Unlike the randomized `hash(str)`, CPython evaluates `hash(int)` as the integer itself for values in this range, allowing an attacker who knows the table size to construct colliding keys.

**Ceiling** 

At $n = 10^5$, a log-linear pass runs roughly $1.7 \times 10^6$, which is trivially affordable, where a quadratic pass runs $10^{10}$, nearly four orders of magnitude larger and beyond what any time limit absorbs. The ceiling therefore forces `O(n log n)` or better.

## 2. Algorithmic Design & Trade-offs

**Brute force:** A nested loop evaluating every unique pair for equality.

- **Mechanics:** An outer pointer `i` traverses the array, while an inner pointer `j` initializes at `i + 1` and scans the remaining elements. The inner loop evaluates `nums[i] == nums[j]`, returning `True` on the first match.
- **Complexity:** The traversal yields $\frac{n(n-1)}{2}$ pairwise comparisons, establishing an `O(n^2)` time bound. Execution is entirely in-place, yielding `O(1)` space.
- **Pattern:** `seen-set`. The inner loop scans the remaining array for a duplicate that can be recorded during traversal.
- **Analysis:** Exceeds the ceiling at roughly $5 \times 10^9$ operations, triggering a Time Limit Exceeded. Trading `O(n)` auxiliary space for a hash-set reduces the existence check to an `O(1)` average-case lookup, lowering the time bound to `O(n)`.

**Sort-and-scan:** A sorted copy followed by a linear scan evaluating adjacent elements for equality.

- **Mechanics:** A copy of the array is sorted. A pointer `i` traverses the copy, evaluating `nums[i] == nums[i - 1]` and returning `True` on the first match.
- **Complexity:** A comparison sort establishes the `O(n log n)` time bound. The read-only constraint forces an auxiliary copy before sorting, fixing space at `O(n)`.
- **Analysis:** The copy eliminates the `O(1)` space advantage an in-place sort would hold over a hash-set.

**Set length:** A full hash-set conversion comparing the resulting size against the original array length.

- **Mechanics:** The array is passed into a hash-set constructor, discarding duplicate values. Both lengths are then compared, returning `True` on a mismatch.
- **Complexity:** The constructor performs `n` insertions, establishing an `O(n)` time bound. A duplicate-free array retains every element, scaling space to `O(n)`.
- **Analysis:** A one line implementation, but it forfeits any early exit since the set is materialized in full before the two lengths can be compared.

**Seen-set with early exit (chosen):** A linear scan testing each element for membership in a hash-set of already seen values.

- **Mechanics:** Initialize an empty hash-set. Iterate a pointer `i` through the array, querying the set for `nums[i]`. If the element is found, return `True`. Otherwise, insert `nums[i]` into the set and continue the traversal.
- **Complexity:** A single traversal paired with average-case `O(1)` lookups and amortized average-case `O(1)` insertions establishes an `O(n)` time bound, with an `O(1)` best case when a duplicate appears within a constant number of steps. A duplicate-free array retains every element, scaling space to `O(n)`.
- **Invariant:** At the start of any iteration `i`, the set holds exactly the values in `nums[:i]`. A hit therefore indicates an earlier occurrence, which is a duplicate, and the scan can exit without examining the rest.
- **Analysis:** The only candidate that decides on evidence rather than after exhausting the input.

**Selection:** Set-length and the seen-set share an `O(n)`/`O(n)` worst case, but the seen-set wins because it decides on the first repeat where set-length must materialize the whole set first.

## 3. Follow-ups & Variations

**Strict memory limit, with mutation permitted:** Auxiliary space is capped at `O(1)`, but the input may be modified in place.

- **Pivot:** An in-place sort replaces the set. Sort with an algorithm that needs no auxiliary array, such as heapsort, then perform a linear scan evaluating adjacent elements for equality. Space falls to `O(1)` but time regresses to `O(n log n)`. Note that `list.sort()` does not qualify, since Timsort needs up to `O(n)` auxiliary.

**Unbounded data stream:** The input arrives as an endless stream rather than a static array.

- **Pivot:** A Bloom filter replaces the set, because exact deduplication needs space proportional to every distinct value ever seen, which is unbounded over a stream. Hash each incoming element into a fixed-size bit array sized in advance for a target error rate. Memory is capped at `O(1)`, trading exactness for a tunable false-positive rate while guaranteeing zero false negatives.

**Duplicate within index distance `k` (LC 219):** A duplicate is only valid if the two occurrences lie at most `k` indices apart.

- **Pivot:** A sliding window replaces the set. As the scan advances, evict the element that falls outside the `i - k` boundary. Time is preserved at `O(n)` and space is bounded at `O(min(n, k))`, since the problem permits `k` to exceed the array length, in which case nothing is ever evicted.

**Duplicate within index distance `k` and value difference `t` (LC 220):** The match condition relaxes from strict equality to a bounded range, `abs(nums[i] - nums[j]) <= t`.

- **Pivot:** Bucketing by value width replaces the set, because a hash set cannot answer a range query. Index each element at `nums[i] // (t + 1)` so that a match can only lie in the same bucket or an adjacent one, and evict at the `i - k` boundary as before. Time is `O(n)` and space `O(min(n, k))`.