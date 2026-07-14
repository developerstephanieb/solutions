# 0217. Contains Duplicate

`LC 217` · `Easy` · `Arrays & Hashing` · pattern: `seen-set` · ref: `dsa/patterns/hashing/seen_set`

## 1. Requirements & Scoping

**Problem:** Given an integer array `nums`, return `True` if any value appears at least twice, and `False` if every element is distinct.

**Signature:** `hasDuplicate(nums: list[int]) -> bool`

**Clarifying questions**

- *What are the length bounds of the array?* — `0 <= len <= 10**5`. With fewer than two elements no duplicate can exist, which makes the answer `False`.
- *What is the value range of the integers?* — `-10**9 <= nums[i] <= 10**9`.
- *Am I permitted to mutate the input array, or should I treat it as read-only?* — Unspecified, so I'll treat it as read-only.

**Assumptions**

- **Memory bound (static, not streaming):** Assumes the system can allocate up to `O(n)` auxiliary space if an approach requires trading space for time.
  - Degradation: Over an unbounded stream, exact deduplication needs space proportional to every distinct value ever seen, which exhausts memory. Pivot to bounded, probabilistic structures (e.g., Bloom Filter).
- **Hashing environment (uniform, not adversarial):** Assumes non-adversarial input with a uniform hash distribution, permitting average-case `O(1)` set operations.
  - Degradation: Adversarial inputs can exploit the hash function to map every key into the same memory bucket, which collapses a lookup from `O(1)` into a `O(n)` and the whole pass into `O(n^2)`.

**Portability:** Values lie within `-10**9 <= nums[i] <= 10**9`, which sits inside `int32` (roughly ±2.15 billion). A C++ or Java port can therefore hold each element in a 32-bit `int` with no overflow surface. Python's `int` is arbitrary-precision, which removes the question from this implementation.

## 2. Algorithmic Design & Trade-offs

**Brute force (pairwise comparison)**

-	**Mechanics:** Compare every element against every later element, returning `True` on the first match.
-	**Complexity:** Time: `O(n^2)`; Space: `O(1)`
-	**Analysis:** Comparing each element against every element after it sums to $\frac{n(n-1)}{2}$ pairs, which is roughly $\frac{n^2}{2}$. At the ceiling `n = 10**5` that is about $5 \times 10^9$ operations, which guarantees a Time Limit Exceeded. The approach is trivially correct and is the only candidate needing no auxiliary memory, but it is quadratic.

**Sort and scan adjacent elements**

- **Mechanics:** Sort the array so that equal values become adjacent, then scan once comparing `nums[i]` to `nums[i+1]`.
- **Complexity:** Time: `O(n log n)`; Space: `O(n)`
- **Analysis:** A comparison-based sort establishes an `O(n log n)` time bound. While an in-place sort (like Heapsort) could theoretically achieve `O(1)` space, the requirement to treat the input as read-only mandates an array copy, degrading space to `O(n)`. This renders the approach strictly inferior to Hashing for this specific constraint profile.

**Set length**

- **Mechanics:** Convert the array into a Hash Set and compare its size against the array's length.
- **Complexity:** Time: `O(n)`; Space: `O(n)`
- **Analysis:** Building the set traverses the array once with average-case `O(1)` insertions, which is `O(n)` time, and a duplicate-free array retains all `n` elements, which fixes `O(n)` space. The approach is the shortest to write and reads as a single expression, but it materializes the entire set before deciding, which structurally forfeits an early exit.

**Hash seen-set with early exit (chosen)**

- **Mechanics:** Traverse the array, testing each element for membership in a set of values already seen and inserting it when absent. Return `True` on the first hit.
- **Complexity:** Time: `O(n)`; Space: `O(n)`
- **Analysis:** A duplicate-free array forces a complete traversal and retains every element, which fixes `O(n)` for both time and space in the worst case. The early exit gives an `O(1)` best case whenever a duplicate appears within a constant number of steps.

**Selection**

**Selection:** The ceiling `n = 10**5` forces a linear or log-linear bound, which invalidates brute force. The immutability constraint nullifies the `O(1)` space advantage of the sort and scan approach. The direct-address table is defeated by the value domain rather than by the algorithm. Between the two hash-based approaches, both share an `O(n)`/`O(n)` worst case, but the seen-set decides as soon as evidence appears, where the set-length approach must pay for the entire set before it can decide at all.

Pattern: `seen-set`. Reusable note: `ref: dsa/patterns/hashing/seen_set`.

## 3. Implementation & Testing

**Execution Steps**

1. **Initialization:** Allocate an empty set to hold the values already seen.
2. **Traversal:** Walk the array one element at a time.
3. **Membership check:** If the current element is already in the set, a duplicate exists, and the answer is `True`.
4. **Insertion:** Otherwise insert the element and continue.
5. **Exhaustion:** If the traversal completes with no hit, every element was distinct, and the answer is `False`.

**Test Vectors & Edge Cases**

- **General case:** `[1, 2, 3, 1] -> True` (duplicate separated by distance).
- **Distinct elements:** `[1, 2, 3, 4] -> False` (forces the worst case in both time and space).
- **Immediate duplicate:** `[2, 2] -> True` (triggers the `O(1)` best-case early exit).
- **Uniform array:** `[7, 7, 7] -> True` (the scan halts on the first repeat, not the last).
- **Boundary values:** `[-10**9, 0, 10**9] -> False` (the extremes of the value range, plus zero).
- **Empty array:** `[] -> False` (fewer than two elements cannot form a pair).
- **Singleton:** `[1] -> False` (fewer than two elements cannot form a pair).

**Complexity Verification**

- **Time:** `O(n)` — a single linear pass, with each membership test and insertion average-case `O(1)`.
- **Space:** `O(n)` - the dynamically built set scales linearly only if all elements are distinct.

## 4. Follow-ups & Variations

**Strict memory limit (`O(1)` auxiliary space), with mutation permitted:** The system cannot afford `O(n)` auxiliary space, but the input may be modified in place.
- **Pivot:** Abandon the set. Sort in place with an algorithm that needs no auxiliary array, such as heapsort, then scan adjacent elements. This holds space at `O(1)` and deliberately trades time up to `O(n log n)`.

**Unbounded data stream:** The input arrives as an endless stream rather than a static array.
- **Pivot:** Exact deduplication needs space proportional to every distinct value ever seen, which exhausts memory without bound. Substitute a Bloom filter, which enforces a fixed memory ceiling by trading exactness for a tunable false-positive rate while guaranteeing zero false negatives.

**Return the value or index rather than a boolean:** The caller needs to know *which* element repeats.
- **Pivot:** The seen-set supports this with no structural change. Return `nums[i]` or the index `i` at the point where the membership test currently returns `True`.

**Duplicate within index distance `k` (LC 219):** The repeat only counts if the two occurrences lie within `k` positions of each other.
- **Pivot:** Convert the set into a sliding window. As the scan advances, evict the element that falls outside the `i - k` boundary, which bounds space at `O(k)` instead of `O(n)`.

**Duplicate within index distance `k` and value difference `t` (LC 220):** The repeat must be near in both position and value.
- **Pivot:** A hash set is insufficient, because the query becomes a range query rather than an exact match. Pivot to an ordered structure such as a balanced BST over the window, giving `O(n log k)`, or to bucketing by value width, giving `O(n)`.