# 0217. Contains Duplicate

`LC 217` · `Easy` · `Arrays & Hashing` · pattern: `seen-set` · ref: `dsa/patterns/hashing/seen_set`

## 1. Requirements & Scoping

**Problem:** Given an integer array `nums`, return `True` if any value appears at least twice,
and `False` if every element is distinct.

**Signature:** `hasDuplicate(nums: list[int]) -> bool`

**Clarifying questions**

- *What is the maximum length of the array? Can it be empty or a single element?* - `0 <= len <= 10**5`.
- *What is the value range of the integers, and are negative values permitted?* — `-10**9 <= nums[i] <= 10**9`.
- *Am I permitted to mutate the input array, or should I treat it as read-only?* — Unspecified, so I'll treat it as read-only.

**Assumptions**

- **Memory bound (static vs streaming):** Assumes the system has sufficient RAM to allocate up to `O(n)` auxiliary space if an approach requires trading space for time.
  - Degradation: Over an unbounded stream, exact `O(n)` deduplication fails via Out of Memory (OOM) exhaustion, requiring a pivot to bounded, probabilistic structures (e.g., Bloom Filter).
- **Hashing environment (uniform vs. adversarial):** Assumes non-adversarial input with a uniform hash distribution, permitting average `O(1)` operations for hash-based structures.
  - Degradation: Adversarial inputs engineered to force mass collisions degrade hash operations to worst-case `O(n)`.

## 2. Algorithmic Design & Trade-offs

**Brute force (pairwise comparison)**

-	**Mechanics:** Iterate through all possible pairs to check for equality.
-	**Complexity:** Time: `O(n^2)`; Space: `O(1)`
-	**Analysis:** Comparing each element sequentially against the shrinking pool of remaining elements yields an arithmetic progression summing to $\frac{n(n-1)}{2}$ comparisons, which simplifies to approximately $\frac{n^2}{2}$ pairs. At `n = 10**5`, this results in roughly $\frac{(10^5)^2}{2} = \frac{10^{10}}{2} = 5 \times 10^9$ (5 billion) operations. This guarantees a Time Limit Exceeded (TLE) error on standard hardware. Trivially correct but far too slow.

To check every pair without repeating, the first element is compared to $n-1$ elements, the second to $n-2$, and so on. The sum of these comparisons is exactly $\frac{n(n-1)}{2}$, which simplifies to $\frac{n^2}{2}$ pairs. At the maximum constraint of `n = 10**5`, the algorithm executes roughly $\frac{(10^5)^2}{2} = 5 \times 10^9$ (5 billion) operations. This guarantees a Time Limit Exceeded (TLE) error on standard hardware. Trivially correct but far too slow.

**Sort and scan adjacent elements**

- **Mechanics:** Sort the array to group duplicates adjacently, followed by a linear scan comparing `nums[i]` to `nums[i+1]`.
- **Complexity:** Time: `O(n log n)`; Space: `O(n)`
- **Analysis:** A comparison-based sort establishes an `O(n log n)` time bound. While an in-place sort (like Heapsort) could theoretically achieve `O(1)` space, the requirement to treat the input as read-only mandates an array copy, degrading space to `O(n)`. This renders the approach strictly inferior to Hashing for this specific constraint profile.

**Set length**

- **Mechanics:** Convert the entire array into a Hash Set and compare its length to the original array's length.
- **Complexity:** Time: `O(n)`; Space: `O(n)`
- **Analysis:** While this achieves linear time and space, it materializes the entire set in memory. This structurally eliminates the early-exit optimization, forcing a full `O(n)` traversal and worst-case memory allocation even if a duplicate exists at index 1.

**Hash seen-set with early exit**

- **Mechanics:** Iterate the array, evaluating membership against a dynamically built Hash Set. Terminate execution and return `True` immediately upon a successful lookup.
- **Complexity:** Time: `O(n)` average; Space: `O(n)` worst-case
- **Analysis:** The "early exit" optimizes best-case time complexity to `O(1)` (if the duplicate is at index 1). Average time remains `O(n)` because evaluating a randomly distributed duplicate requires scanning an expected `n/2` elements, and evaluating a duplicate-free array requires scanning all n elements. Both scenarios scale linearly and mathematically reduce to `O(n)`.

**Selection**

The constraint `n = 10**5` forces a strict linear or log-linear time requirement, invalidating Brute Force. The immutability constraint nullifies the `O(1)` space advantage of the Sort and Scan approach. Between the two hashing strategies, the iterative Hash Set with early exit is selected over the Set Length approach. While both share the same worst-case complexity, the iterative approach leverages dynamic memory allocation and early termination, providing strictly superior time and space efficiency in the best and average execution paths.

Pattern: `seen-set`. Reusable note: `ref: dsa/patterns/hashing/seen_set`.

## 3. Implementation & Testing

**Execution Steps**

1. Initialize an empty, dynamically built Hash seen-Set.
2. Iterate through each element in the input array.
3. **Membership Check:** If the current element exists in the set, terminate execution and return `True`.
4. **Insertion:** If the element is not found, insert it into the set and proceed to the next iteration.
5. **Fallback:** If the loop exhausts with no successful lookups, return `False`.

**Test Vectors & Edge Cases**

- **General Case:** `[1, 2, 3, 1] -> True` (Duplicate separated by distance).
- **Distinct Elements:** `[1, 2, 3, 4] -> False` (Forces worst-case `O(n)` space and time).
- **Immediate Duplicates:** `[2, 2] -> True` (Triggers `O(1)` best-case early exit).
- **Uniform Array:** `[7, 7, 7] -> True` (Validates logic safely halts on multiple identical elements).
- **Boundary Constraints:** `[-10**9, 0, 10**9] -> False` (Validates handling of extreme negative/positive constraint limits and zero).
- **Guard Clauses:** `[] -> False`, `[1] -> False` (Empty and singleton arrays mathematically cannot contain pairs).

**Complexity Verification**

- **Time:** `O(n)` average. A single linear pass bounded by `O(1)` average hash operations.
- **Space:** `O(n)` worst-case. The dynamically built set scales linearly only if all elements are distinct.

## 4. Follow-ups & Variations

**Strict Memory Constraints (`O(1)` Space Limit):** The system cannot afford `O(n)` auxiliary space, but modifying the input array is permitted.
- **Pivot:** Abandon the Hash Set. Utilize an in-place sort (e.g., Heapsort) followed by an adjacent element scan. This preserves `O(1)` space while intentionally degrading time complexity to `O(n log n)`.

**Unbounded Data Stream:** The input `nums` is an infinite stream rather than a static array (meaning $n \to \infty$).
- **Pivot:** Exact deduplication requires space proportional to all distinct values seen, which mathematically guarantees an Out of Memory (OOM) crash. To maintain a strict memory ceiling, abandon the Hash Set for a Bloom Filter. This trades exactness for bounded space, yielding a manageable false-positive rate but mathematically guaranteeing zero false negatives.

**Information Extraction (Return the Value/Index):** The function must return the duplicate element itself (or its index) rather than a boolean.
- **Pivot:** The iterative Hash Set natively supports this without architectural changes. Instead of returning `True` upon a successful membership check, return `nums[i]` or the index pointer `i`.

**Bounded Index Proximity:** The duplicate must exist within a specific index distance `k`.
- **Pivot:** Modify the Hash Set to operate as a sliding window. As the iteration pointer advances, delete elements from the set that fall outside the `current_index - k` boundary. This optimizes space complexity from `O(n)` down to `O(k)`.

**Value & Index Proximity:** The duplicate must be within index distance `k` AND value difference `t`.
- **Pivot:** A standard Hash Set becomes insufficient because we need to query ranges, not just exact matches. The architecture must pivot to an ordered structure (like a Balanced Binary Search Tree for `O(n log k)` time) or a Bucket Sort mechanism (for `O(n)` time) to efficiently evaluate the value differences.