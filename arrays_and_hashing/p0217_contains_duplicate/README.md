# 0217. Contains Duplicate

`LC 217` · `Easy` · `Arrays & Hashing` · pattern: `seen-set` · ref: `dsa/patterns/hashing/seen_set`

## 1. Requirements & Scoping

**Problem:** Given an integer array `nums`, return `True` if any value appears at least twice, and `False` if every element is distinct.

**Signature:** `hasDuplicate(nums: list[int]) -> bool`

**Clarifying questions**

- *What are the length bounds on `nums`?* — `0 <= len <= 10**5`; with fewer than two elements no duplicate can exist, which makes the answer `False`.
- *What is the value range of the integers?* — `-10**9 <= nums[i] <= 10**9`.
- *Am I permitted to mutate the input array, or should I treat it as read-only?* — Unspecified, so I'll treat it as read-only.

**Assumptions**

- **Hashing environment (uniform, not adversarial):** Non-adversarial input with a uniform hash distribution is assumed, which permits average-case `O(1)` membership tests and amortized average-case `O(1)` insertions. **Degradation:** Adversarial input can force every key into the same bucket, which collapses a lookup from `O(1)` into `O(n)` and the whole pass into `O(n^2)`.

**Portability:** Values lie within `-10**9 <= nums[i] <= 10**9`, which sits inside `int32` (roughly ±2.15 billion). A C++ or Java port can therefore hold each element in a 32-bit `int` with no overflow surface. Python's `int` is arbitrary-precision, which removes the question from this implementation.

## 2. Algorithmic Design & Trade-offs

**Brute force (pairwise comparison)**

-	**Mechanics:** Compare every element against every later element, returning `True` on the first match.
-	**Complexity:** Time: `O(n^2)`; Space: `O(1)`
-	**Analysis:** The approach is trivially correct and is the only candidate requiring no auxiliary memory. The pairwise comparisons sum to $\frac{n(n-1)}{2}$, which at the ceiling of $n = 10^5$ equates to roughly $5 \times 10^9$ operations, guaranteeing a Time Limit Exceeded.

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

**Hash seen-set with early exit (chosen)**

- **Mechanics:** Traverse the array, testing each element for membership in a set of values already seen and inserting it when absent. Return `True` on the first hit.
- **Complexity:** Time: `O(n)`; Space: `O(n)`
- **Analysis:** A duplicate-free array forces a complete traversal and retains every element, which fixes `O(n)` for both time and space in the worst case. The early exit gives an `O(1)` best case whenever a duplicate appears within a constant number of steps, as the number of operations remains independent of `n`.

**Selection:** At $n = 10^5$, a linear pass runs $10^5$ operations and a log-linear pass roughly $1.7 \times 10^6$, both trivially affordable. Therefore, the constraint ceiling permits an `O(n log n)` solution or better. By contrast, a quadratic runs $10^{10}$ operations, nearly four orders of magnitude larger and beyond what any time limit absorbs, invalidating the brute-force approach. Sort-and-scan reaches `O(n log n)`, but the read-only constraint forces an `O(n)` copy, stripping the space advantage it has over hashing. Direct addressing gives worst-case `O(1)` access, but the value domain forces an array of $m = 2 \times 10^9 + 1$ slots that must be zeroed before use, incurring a `Θ(m)` cost in both time and auxiliary space that shifts the overall time complexity to `O(n + m)` and guarantees a Memory Limit Exceeded at allocation. Set-length and the seen-set share an `O(n)`/`O(n)` worst-case but seen-set wins because it decides on the first repeat, whereas set-length materializes the entire set before it can decide at all.

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

- **Time:** `O(n)` — A single linear pass, with each membership test average-case `O(1)` and each insertion amortized average-case `O(1)`.
- **Space:** `O(n)` — The set grows to hold every element only when the array is duplicate-free.

## 4. Follow-ups & Variations

**Strict memory limit (`O(1)` auxiliary space), with mutation permitted:** The system cannot afford `O(n)` auxiliary space, but the input may be modified in place. **Pivot:** Abandon the set. Sort in place with an algorithm that needs no auxiliary array, such as heapsort, then scan adjacent elements. This holds space at `O(1)` and deliberately trades time up to `O(n log n)`.

**Unbounded data stream:** The input arrives as an endless stream rather than a static array. **Pivot:** Exact deduplication needs space proportional to every distinct value ever seen, which exhausts memory without bound. Substitute a Bloom filter, which enforces a fixed memory ceiling by trading exactness for a tunable false-positive rate while guaranteeing zero false negatives.

**Return the value or index rather than a boolean:** The caller needs to know *which* element repeats. **Pivot:** The seen-set supports this with no structural change. Return `nums[i]` or the index `i` at the point where the membership test currently returns `True`.

**Duplicate within index distance `k` (LC 219):** The repeat only counts if the two occurrences lie within `k` positions of each other. **Pivot:** Convert the set into a sliding window. As the scan advances, evict the element that falls outside the `i - k` boundary, which bounds space at `O(k)` instead of `O(n)`.

**Duplicate within index distance `k` and value difference `t` (LC 220):** The repeat must be near in both position and value. **Pivot:** A hash set is insufficient, because the query becomes a range query rather than an exact match. Pivot to an ordered structure such as a balanced BST over the window, giving `O(n log k)`, or to bucketing by value width, giving `O(n)`.