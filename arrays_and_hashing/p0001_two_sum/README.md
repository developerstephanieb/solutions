# 0001. Two Sum

`LC 1` · `Easy` · `Arrays & Hashing` · pattern: `complement-map` · ref: `dsa/patterns/hashing/complement_map`

## 1. Requirements & Scoping

**Problem** 

Given an integer array and a target, return the indices of the two distinct entries that sum to the target, smaller index first.

**Contract**

- **Signature:** `twoSum(nums: list[int], target: int) -> list[int]`
- **Length bounds:** `2 <= len(nums) <= 1000`.
- **Value range:** `-10**7 <= nums[k], target <= 10**7`.
- **Duplicates:** Permitted, and equal values may form the pair (`[3, 3]`, target `6`), which means equal values must not be conflated with identical indices.
- **Mutability:** Unspecified, and therefore treated as read-only.
- **Cardinality:** Exactly one pair exists, which makes the first match the answer.

**Assumptions**

- **Average-case `O(1)` hashing:** Assumes a hash function that distributes keys evenly, which gives average-case `O(1)` lookups and amortized average-case `O(1)` insertions, and an overall time bound of `O(n)`. **Degradation:** Adversarial input can force every key onto the same slot, which collapses a single operation from `O(1)` to `O(n)`. The loop performs one such operation for each of the `n` elements, which compounds the whole pass to `O(n^2)`. Unlike the randomized `hash(str)`, CPython evaluates `hash(int)` as the integer itself for values in this range, allowing an attacker who knows the table size to construct colliding keys.

**Ceiling** 

At $n = 1000$, a quadratic pass runs $10^6$ operations, which is trivially affordable, and a cubic pass runs $10^9$, three orders of magnitude larger and beyond what any time limit absorbs. The ceiling therefore forces `O(n^2)` or better.

## 2. Algorithmic Design & Trade-offs

**Brute-force**: A nested loop evaluating every unique pair for the target sum.

- **Mechanics:** An outer pointer establishes a pivot index `i`, while an inner pointer `j` traverses the linearly shrinking subarray from `i + 1` to the end of the array.
- **Complexity:** The traversal yields $\frac{n(n-1)}{2}$ pair-wise comparisons, establishing an `O(n^2)` time bound. Execution is entirely in-place, yielding `O(1)` space.
- **Pattern:** `complement-map`. The inner loop scans for a complement that can be calculated (`target - nums[i]`).
- **Analysis:** Viable under the ceiling at roughly $5 \times 10^5$ operations, but asymptotically suboptimal. Trading `O(n)` auxiliary space for a hash map reduces the search to an `O(1)` average-case lookup, lowering the time bound to `O(n)`.

**Sort-plus-two-pointers:** A converging two-pointer sweep over a sorted copy that carries the value-index pairs.

- **Mechanics:** Materialize an array of `(value, original_index)` tuples and sort by value. Initialize pointers at both boundaries and converge them while `left < right`: increment the left pointer to increase the sum, or decrement the right pointer to decrease the sum, until the target is matched.
- **Complexity:** Comparison-based sorting locks time at `O(n log n)`. Space complexity is `O(n)` due to the allocation of the auxiliary structure.
- **Analysis:** Returning indices forces the creation of an auxiliary tuple array to preserve the original positions during the sort, eliminating the `O(1)` advantage this approach would offer on a value-only problem. 

**One-pass complement-map (chosen):** A single forward pass that looks up each element's complement before inserting the element itself.

- **Mechanics:** Initialize a hash map to store `(value, index)` mappings. Iterate a pointer `i` through the array, calculating the complement (`target - nums[i]`). If the complement exists in the map, return the paired indices. Otherwise, insert the current value and index into the map and continue.
- **Complexity:** A single traversal paired with average-case `O(1)` hash lookups bounds the overall execution to `O(n)`. Supporting the map requires dynamic allocation, which scales space to `O(n)`.
- **Invariant**: At the start of any iteration `i`, the map holds `nums[:i]` keyed to their indices, which guarantees any hit is a distinct earlier element, preventing self-pairing and resolving duplicate values to two distinct indices. The stored index is also smaller than `i`, which satisfies the smaller-index-first requirement. Building the map in full before querying it would break the invariant and require an explicit `i != j` guard in its place.
- **Analysis:** Asymptotically optimal at `O(n)` time. The `O(n)` auxiliary space is the price of the `O(1)` lookup, and the only property surrendered is the in-place execution brute force keeps.

**Selection:** The one-pass complement-map, alone in reaching `O(n)` time and satisfying the distinct-index and ordering contracts structurally rather than through a guard.

## 3. Follow-ups & Variations

**Value-only return, with mutation permitted:** The contract requires the integers themselves rather than their original indices, and the input may be modified in place.

- **Pivot:** An in-place sort replaces the map. Sort with an algorithm needing no auxiliary array, such as heapsort, then converge two pointers and return the pair of values. Time regresses to `O(n log n)` and space falls to `O(1)`.

**All distinct pairs summing to target:** The caller requires every distinct pair rather than the first match.

- **Pivot:** No structural change; the map extends. The termination condition shifts from an early exit to an exhaustive traversal, and upon identifying a valid complement the two values are normalized into a `(min, max)` tuple and inserted into a secondary result set, which deduplicates identical pairs at average-case `O(1)` per insertion. Time stays average-case `O(n)` and space `O(n)` across both structures.

**No solution guaranteed:** The input array may lack a valid complement pair.

- **Pivot:** No structural change; the return contract widens. Widen the signature to `list[int] | None`. Under the original guarantee, reaching the end of the loop without a result meant the input was invalid, which justified a `ValueError`. A miss is now an expected outcome, which requires a `None` return rather than an exception.
