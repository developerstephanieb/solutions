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

**Brute force (pairwise comparison)**

- **Mechanics:** Compare every element against every later element, returning `True` on the first match.
- **Complexity:** Time: `O(n^2)`; Space: `O(1)`
- **Analysis:** The approach is trivially correct and is the only candidate requiring no auxiliary memory. The pairwise comparisons sum to $\frac{n(n-1)}{2}$, which at the ceiling of $n = 10^5$ equates to roughly $5 \times 10^9$ operations, guaranteeing a Time Limit Exceeded.

**Sort-and-scan adjacent elements**

- **Mechanics:** Sort the array so that equal values become adjacent, then scan once comparing `nums[i]` to `nums[i+1]`.
- **Complexity:** Time: `O(n log n)`; Space: `O(n)`
- **Analysis:** A comparison sort establishes the `O(n log n)` time bound. An in-place sort such as heapsort would hold auxiliary space at `O(1)`, but the read-only constraint forces an `O(n)` copy, stripping the space advantage it has over hashing.

**Direct-address count array**

- **Mechanics:** Index a fixed array by value itself, incrementing each slot and accepting on the first slot to reach two.
- **Complexity:** Time: `O(n + m)`; Space: `O(m)`, where `m` is the width of the value domain
- **Analysis:** Direct addressing computes the slot arithmetically for worst-case `O(1)` access time, meaning traversing the `n` inputs costs `O(n)` operations. However, the value domain forces an array of $m = 2 \times 10^9 + 1$ slots that must be zeroed before use, incurring a `Θ(m)` cost in both time and auxiliary space that shifts the overall time complexity to `O(n + m)`. That array demands gigabytes of memory, which guarantees a Memory Limit Exceeded at allocation.

**Set length**

- **Mechanics:** Convert the array into a hash set and compare its size against the array's length.
- **Complexity:** Time: `O(n)`; Space: `O(n)`
- **Analysis:** A single traversal with amortized average-case `O(1)` insertions yields `O(n)` time. If the array is duplicate-free, the set must store all `n` elements, dictating `O(n)` space. The approach is the shortest to write and reads as a single expression, but it materializes the entire set before it can decide.
- **Pattern:** `seen-set`. Every scan re-derives from the tail what earlier scans already established, and comparing `nums[i]` against `nums[j]` answers a comparison question where the problem asks a membership one. Membership is established once rather than recomputed per element, which calls for a structure answering it in `O(1)`.

**Hash seen-set with early exit (chosen)**

- **Mechanics:** Traverse the array, testing each element for membership in a set of values already seen and inserting it when absent. Return `True` on the first hit.
- **Complexity:** Time: `O(n)`; Space: `O(n)`
- **Analysis:** A duplicate-free array forces a complete traversal and retains every element, which fixes `O(n)` for both time and space in the worst case. The early exit gives an `O(1)` best case whenever a duplicate appears within a constant number of steps, as the number of operations remains independent of `n`.

**Selection:** The ceiling excludes brute force. Sort-and-scan is log-linear but the read-only constraint costs it the `O(1)` space advantage it has over hashing. Direct addressing is defeated by the value domain, which makes it a Memory Limit Exceeded at allocation. Set-length and the seen-set share an `O(n)`/`O(n)` worst case, and the seen-set wins because it decides on the first repeat where set-length must materialize the whole set first.

**Invariant:** `seen` holds exactly the values at indices before the current one. A hit therefore indicates an earlier occurrence, which is a duplicate, and the scan can exit without examining the rest.

## 3. Follow-ups & Variations

**Strict memory limit (`O(1)` auxiliary space), with mutation permitted:** The system cannot afford `O(n)` auxiliary space, but the input may be modified in place. 
- **Pivot:** Abandon the set. Sort in place with an algorithm that needs no auxiliary array, such as heapsort, then scan adjacent elements. This holds space at `O(1)` and deliberately trades time up to `O(n log n)`.

**Unbounded data stream:** The input arrives as an endless stream rather than a static array. 
- **Pivot:** Exact deduplication needs space proportional to every distinct value ever seen, which exhausts memory without bound. Substitute a Bloom filter, which enforces a fixed memory ceiling by trading exactness for a tunable false-positive rate while guaranteeing zero false negatives.

**Duplicate within index distance `k` (LC 219):** The repeat only counts if the two occurrences lie within `k` positions of each other. 
- **Pivot:** Convert the set into a sliding window. As the scan advances, evict the element that falls outside the `i - k` boundary, which bounds space at `O(k)` instead of `O(n)`.

**Duplicate within index distance `k` and value difference `t` (LC 220):** The repeat must be near in both position and value. 
- **Pivot:** A hash set is insufficient, because the query becomes a range query rather than an exact match. Pivot to an ordered structure such as a balanced BST over the window, giving `O(n log k)`, or to bucketing by value width, giving `O(n)`.