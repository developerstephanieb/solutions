# 0001. Two Sum
 
`LC 1` · `Easy` · `Arrays & Hashing` · pattern: `complement-map` · ref: `dsa/patterns/hashing/complement_map`

## 1. Requirements & Scoping

**Problem:** Given an integer array and a target, return the indices of the two distinct entries that sum to the target, smaller index first.

**Signature:** `twoSum(nums: list[int], target: int) -> list[int]`

**Clarifying questions**

- *What are the length bounds on `nums`?* — `2 <= n <= 1000`.
- *What is the value range of the elements and the target?* — `-10**7 <= nums[k], target <= 10**7`.
- *Can values repeat?* — Yes; equal values may form the pair (`[3, 3]`, target `6`), which means equal values must not be conflated with identical indices.
- *What is guaranteed about the number of solutions?* — Exactly one pair exists. Return on the first match.

**Assumptions**

- **Average `O(1)` hashing:** Assumes a hash function that distributes keys evenly, giving amortized `O(1)` insertions and lookups and overall `O(n)` time.
  - Degradation: Adversarial key collisions degrade a single operation to `O(n)`. Because the main loop executes this lookup for every one of the `n` elements, the overall compute time compounds to `O(n^2)`.

## 2. Algorithmic Design & Trade-offs

**Brute-force nested scan**
- **Mechanics:** For each index `i`, scan the remaining subarray (`j` from `i + 1` to `n - 1`) to evaluate `nums[i] + nums[j] == target`.
- **Complexity:** Time: `O(n^2)`; Space: `O(1)`.
- **Analysis:** Re-evaluating the shrinking subarray for every element forces a quadratic `O(n^2)` time bound. However, because it allocates no auxiliary data structures, it establishes an `O(1)` space floor.

**Sort plus two pointers**
- **Mechanics:** Materialize a new array of `(value, original_index)` tuples and sort by value. Initialize pointers at both boundaries and converge them inward dynamically: increment the left pointer to increase the sum, or decrement the right pointer to decrease the sum, until the target is matched.
- **Complexity:** Time: `O(n log n)`; Space: `O(n)`.
- **Analysis:** Comparison-based sorting locks time at `O(n log n)`. While a standard two-pointer sweep uses `O(1)` space, returning indices forces the materialization of the tuple array which degrades space to `O(n)`, negating the space advantage this approach would hold on a value-only problem.

**One-pass complement map (chosen)**
- **Mechanics:** Execute a single forward traversal. For each element, calculate its mathematical complement (`target - nums[i]`). If this complement exists in the map, immediately return the mapped index and the current index. Otherwise, insert `nums[i] -> i` into the map and continue.
- **Complexity:** Time: `O(n)`; Space: `O(n)`.
- **Analysis:** A single traversal paired with amortized `O(1)` hash lookups bounds the overall execution to `O(n)`. By executing the lookup *prior* to insertion, the algorithm structurally prevents an element from matching against itself (satisfying the distinct index contract) and guarantees the returned pair inherently orders the earlier index first. Supporting this state requires dynamic memory allocation, scaling space to `O(n)` and exposing the system to the collision vulnerabilities established in §1.

**Selection:** The relatively small input ceiling (`n = 1000`) allows all three approaches to execute within standard time limits; therefore, the selection is driven by asymptotic optimization. The brute-force approach requires `O(1)` space but is the slowest. Sorting introduces an `O(n log n)` compute overhead and preserving the original indices forces an `O(n)` space tradeoff.  The one-pass complement map wins by achieving `O(n)` time while satisfying all index and ordering constraints in a single traversal.

Pattern: `complement-map`. Reusable note: `ref: dsa/patterns/hashing/complement_map`.

## 3. Implementation & Testing

**Execution Steps**
1. **Initialization:** Allocate an empty hash map for array values mapped to their original indices.
2. **Linear traversal & arithmetic:** Iterate through the array and for each element compute `complement = target - value`.
3. **Membership check:** Query the hash map for the complement. If it exists, return its stored index paired with the current index.
4. **Insertion:** If the complement is absent, insert the current value and index into the map and continue.
5. **Contract enforcement:** The problem constraints guarantee exactly one valid solution. A loop fall-through constitutes a strict contract violation, dictating a loud exception (ValueError) rather than a silent failure or empty return.

**Test Vectors & Edge Cases**
- **Early termination:** `[2, 7, 11, 15], 9 -> [0, 1]` (match completes on the second element)
- **Match mid-array:** `[3, 2, 4], 6 -> [1, 2]` (complement of an interior element)
- **Duplicate values:** `[3, 3], 6 -> [0, 1]` (equal values, distinct indices)
- **Negatives:** `[-1, -2, -3, -4], -6 -> [1, 3]`
- **Zero-sum sign crossing:** `[-3, 4, 3, 90], 0 -> [0, 2]`
- **Minimal length:** `[1, 2], 3 -> [0, 1]` (`n == 2`, the lower bound)

**Complexity Verification**
- **Time:** `O(n)` — A single forward traversal of `n` iterations, each doing average-case `O(1)` lookups and amortized `O(1)` insertions.
- **Space:** `O(n)` — in the worst-case scenario (where the valid pair occupies the final two slots), the map holds up to `n - 1` entries before the match.

## 4. Follow-ups & Variations

**Value-only return:** contract drops the requirement to map elements back to their original indices.
- **Pivot:** Return `[complement, num]` at the match. This relaxation structurally eliminates the need to materialize the `(value, index)` tuple array, which makes the sort-plus-two-pointer approach viable, achieving `O(n log n)` time while restoring a `O(1)` memory footprint.

**Pre-sorted input (LC 167):** The input array guarantees an increasing state.
- **Pivot:** Abandon the dynamic hash map for a two-pointer boundary sweep. By converging pointers by comparing the pair sum against the target, the system guarantees an exact match in `O(n)` time and `O(1)` space footprint.

**All distinct pairs summing to target:** The system requires all valid pairs rather than terminating on the first match.
- **Pivot:** The `O(1)` early-termination fast-reject is invalidated; use a sort-plus-two-pointer approach. Because sorting physically groups identical numbers together, a standard pointer step might land on the exact same value, causing the system to record a duplicate pair. To prevent this, use `while nums[left] == nums[left - 1]: left += 1` to fast-forward the pointer past any adjacent duplicates until it lands on a strictly new number.

**No solution guaranteed:** The problem space no longer guarantees a valid pair.
- **Pivot:** the code must fail gracefully by returning a sentinel value (e.g., an empty array `[]` or a `None`).

**Three numbers summing to target (LC 15):** The target requires three distinct elements.
- **Pivot:** Fix one element as a locked pivot and reduce the rest to a two-sum on the reduced target `target - pivot`. Sort first, then for each pivot run a two-pointer sweep over the subarray to its right. The `O(n)` sweep across each of the `n` pivots gives `O(n^2)` time.