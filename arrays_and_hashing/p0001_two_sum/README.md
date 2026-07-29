# 0001. Two Sum

`LC 1` · `Easy` · `Arrays & Hashing` · pattern: `complement-map` · ref: `dsa/patterns/hashing/complement_map`

## 1. Requirements & Scoping

**Problem:** Given an integer array and a target, return the indices of the two distinct entries that sum to the target, smaller index first.

**Signature:** `twoSum(nums: list[int], target: int) -> list[int]`

**Clarifying questions**

- *What are the length bounds on `nums`?* — `2 <= len(nums) <= 1000`.
- *What is the value range of the elements and the target?* — `-10**7 <= nums[k], target <= 10**7`.
- *Can values repeat?* — Yes; equal values may form the pair (`[3, 3]`, target `6`), which means equal values must not be conflated with identical indices.
- *What is guaranteed about the number of solutions?* — Exactly one pair exists. Return on the first match.
- *Am I permitted to mutate the input array, or should I treat it as read-only?* — Unspecified, so I'll treat it as read-only.

**Assumptions**

- **Average-case `O(1)` hashing:** Assumes a hash function that distributes keys evenly, which gives average-case `O(1)` lookups and amortized average-case `O(1)` insertions, and an overall time bound of `O(n)`. **Degradation:** Adversarial input can force every key onto the same slot, which collapses a single operation from `O(1)` to `O(n)`. The loop performs one such operation for each of the `n` elements, which compounds the whole pass to `O(n^2)`. Unlike the randomized `hash(str)`, CPython evaluates `hash(int)` as the integer itself for values in this range, allowing an attacker who knows the table size to construct colliding keys.

**Portability:** Values lie within `-10**7 <= nums[k], target <= 10**7`, and a pair sums to at most `2 * 10**7` in magnitude, which sits well inside `int32` ($-2^{31}$ to $2^{31} - 1$). A C++ or Java port can hold each element and each pair sum in a 32-bit `int` with no overflow surface. Python's `int` is arbitrary-precision, which removes the question from this implementation.

## 2. Algorithmic Design & Trade-offs

**Brute-force nested scan**
- **Mechanics:** For each index `i`, scan the remaining subarray from `i + 1` to `n - 1` testing whether `nums[i] + nums[j] == target`.
- **Complexity:** Time: `O(n^2)`; Space: `O(1)`.
- **Analysis:** Re-evaluating the shrinking subarray for every element forces a quadratic `O(n^2)` time bound. The comparisons sum to $\frac{n(n-1)}{2}$, which at the ceiling $n = 1000$ equates to roughly $5 \times 10^5$ operations, well inside any time limit. Because it allocates no auxiliary structure, it establishes an `O(1)` space floor. This approach is therefore dominated rather than excluded.

**Sort-plus-two-pointers**
- **Mechanics:** Materialize a new array of `(value, original_index)` tuples and sort by value. Initialize pointers at both boundaries and converge them inward dynamically: increment the left pointer to increase the sum, or decrement the right pointer to decrease the sum, until the target is matched.
- **Complexity:** Time: `O(n log n)`; Space: `O(n)`.
- **Analysis:** Comparison-based sorting locks time at `O(n log n)`. While a standard two-pointer sweep maintains `O(1)` space, returning indices forces the creation of an auxiliary tuple array to preserve the original indices during the sort, which degrades space to `O(n)`, eliminating the space advantage this approach would otherwise offer on a value-only problem.

**One-pass complement map (chosen)**
- **Mechanics:** Execute a single forward traversal. For each element, compute its complement `target - nums[i]` and return `[seen[complement], i]` when the complement is already in the map. Otherwise, insert `nums[i] -> i` and continue.
- **Complexity:** Time: `O(n)`; Space: `O(n)`.
- **Analysis:** A single traversal paired with average-case `O(1)` hash lookups bounds the overall execution to `O(n)`, with each insert amortized `O(1)`. By executing the lookup *prior* to insertion, the algorithm structurally prevents an element from pairing with itself (satisfying the distinct index contract) and guarantees the returned pair inherently orders the earlier index first. Supporting this state requires dynamic memory allocation, which scales space to `O(n)` and carries the collision exposure established in §1.

**Selection:** At $n = 1000$, a quadratic pass runs $10^6$ operations, which is trivially affordable, and a cubic pass runs $10^9$, three orders of magnitude larger and beyond what any time limit absorbs. Therefore, the constraint ceiling permits `O(n^2)` or better. That bound is loose enough to admit every candidate, which moves the decision onto asymptotics and the index contract. Brute force is the only candidate needing no auxiliary memory, but it is the slowest. Sort-plus-two-pointers improves time to `O(n log n)` but requires `O(n)` space since preserving the original indices forces a `(value, index)` tuple array. The one-pass map achieves `O(n)` time while enforcing the distinct-index and ordering contracts through looking up before inserting rather than an explicit `i != j` guard.

Pattern: `complement-map`. Reusable note: `ref: dsa/patterns/hashing/complement_map`.

## 3. Implementation & Testing

**Execution Steps**
1. **Initialization:** Allocate an empty hash map for array values mapped to their original indices.
2. **Linear traversal & arithmetic:** Iterate through the array and for each element compute `complement = target - value`.
3. **Membership check:** Query the hash map for the complement. If it exists, return its stored index paired with the current index.
4. **Insertion:** If the complement is absent, insert the current value and index into the map and continue.
5. **Contract enforcement:** The problem constraints guarantee exactly one valid solution. A loop fall-through therefore constitutes a contract violation, which warrants a loud `ValueError` rather than a silent failure or an empty return.

**Test Vectors & Edge Cases**
- **Early termination:** `[2, 7, 11, 15], 9 -> [0, 1]` (match completes on the second element)
- **Match mid-array:** `[3, 2, 4], 6 -> [1, 2]` (complement of an interior element)
- **Duplicate values:** `[3, 3], 6 -> [0, 1]` (equal values, distinct indices)
- **Negatives:** `[-1, -2, -3, -4], -6 -> [1, 3]` (all negative)
- **Zero-sum sign crossing:** `[-3, 4, 3, 90], 0 -> [0, 2]` (zero target across a sign change)
- **Minimal length:** `[1, 2], 3 -> [0, 1]` (`n == 2`, the lower bound)

**Complexity Verification**
- **Time:** `O(n)` — a single forward traversal of `n` iterations, each an average-case `O(1)` lookup and an amortized average-case `O(1)` insertion.
- **Space:** `O(n)` — in the worst-case scenario (where the valid pair occupies the final two slots), the map holds up to `n - 1` entries before the match.

## 4. Follow-ups & Variations

**Value-only return:** contract drops the requirement to map elements back to their original indices. 
- **Pivot:** Return `[complement, num]` at the match, which removes the need for the `(value, index)` tuple array and makes sort-plus-two-pointers competitive again. With mutation permitted, sorting in place with an algorithm that needs no auxiliary array, such as heapsort, then sweeping two pointers inward gives `O(n log n)` time at `O(1)` space. Under a read-only array the sort still needs an `O(n)` copy, which leaves the complement map ahead on time at equal space.

**Pre-sorted input (LC 167):** The input arrives already sorted. 
- **Pivot:** Start a pointer at each end and converge inward, incrementing the left pointer to raise the pair sum and decrementing the right to lower it. This reaches `O(n)` time at `O(1)` space.

**All distinct pairs summing to target:** The caller requires every valid pair rather than the first match. 
- **Pivot:** Early termination is no longer available, which calls for sort-plus-two-pointers over the whole array. Sorting groups equal values adjacently, which means an ordinary pointer step can land on the same value and record the same pair twice. Skip the repeats by advancing before comparing: `left += 1`, followed by `while left < right and nums[left] == nums[left - 1]: left += 1`. Advancing first keeps `left - 1` non-negative, and the `left < right` bound keeps the skip from running past the opposing pointer.

**No solution guaranteed:** A valid pair is no longer guaranteed to exist?
- **Pivot:** The `-> list[int]` return type cannot be honoured on a miss. Widen the signature to `list[int] | None` and return `None` if no match is found. Under the original guarantee, reaching the end of the loop without a result meant the input was invalid, which justified a `ValueError`. A miss is now an expected outcome, which requires a `None` return rather than an exception.

**Three numbers summing to target (LC 15):** The target requires three distinct elements. 
- **Pivot:** Fix one element as a pivot and reduce the remainder to a two-sum on the reduced target `target - pivot`. Sort first, then for each pivot run a two-pointer sweep over the subarray to its right. An `O(n)` sweep across each of `n` pivots gives `O(n^2)` time.