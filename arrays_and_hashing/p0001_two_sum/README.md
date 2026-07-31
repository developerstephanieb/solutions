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

**Brute-force nested scan**

- **Mechanics:** For each index `i`, scan the remaining subarray from `i + 1` to `n - 1` testing whether `nums[i] + nums[j] == target`.
- **Complexity:** Time: `O(n^2)`; Space: `O(1)`.
- **Analysis:** Re-evaluating the shrinking subarray for every element forces a quadratic `O(n^2)` time bound. The comparisons sum to $\frac{n(n-1)}{2}$, which at the ceiling $n = 1000$ equates to roughly $5 \times 10^5$ operations, well inside any time limit. Because it allocates no auxiliary structure, it establishes an `O(1)` space floor. This approach is therefore dominated rather than excluded. 
- **Pattern:** `complement-map`. The inner scan searches for `target - nums[i]`, a value the outer loop has already computed, and discards what it learned the moment `i` advances. A search for a value you already hold is a lookup, which calls for a map from value to index.

**Sort-plus-two-pointers**

- **Mechanics:** Materialize a new array of `(value, original_index)` tuples and sort by value. Initialize pointers at both boundaries and converge them inward dynamically: increment the left pointer to increase the sum, or decrement the right pointer to decrease the sum, until the target is matched.
- **Complexity:** Time: `O(n log n)`; Space: `O(n)`.
- **Analysis:** Comparison-based sorting locks time at `O(n log n)`. While a standard two-pointer sweep maintains `O(1)` space, returning indices forces the creation of an auxiliary tuple array to preserve the original indices during the sort, which degrades space to `O(n)`, eliminating the space advantage this approach would otherwise offer on a value-only problem.

**One-pass complement map (chosen)**

- **Mechanics:** Execute a single forward traversal. For each element, compute its complement `target - nums[i]` and return `[seen[complement], i]` when the complement is already in the map. Otherwise, insert `nums[i] -> i` and continue.
- **Complexity:** Time: `O(n)`; Space: `O(n)`.
- **Analysis:** A single traversal paired with average-case `O(1)` hash lookups bounds the overall execution to `O(n)`, with each insert amortized `O(1)`. Supporting the map requires dynamic allocation, which scales space to `O(n)` and carries the collision exposure established in §1.

**Selection:** The constraint ceiling is loose enough to admit every candidate, which moves the decision onto asymptotics and the index contract. Brute force is the only candidate needing no auxiliary memory, but it is the slowest. Sort-plus-two-pointers is log-linear and still needs `O(n)` space since preserving the original indices forces a `(value, index)` tuple array. The one-pass map is alone in reaching `O(n)` time while enforcing the distinct-index and ordering contracts structurally rather than through a guard.

**Invariant:** `seen` holds only values from indices strictly before `i`. Any hit is therefore a distinct earlier element, which prevents an element from pairing with itself and resolves duplicate values like `[3, 3]` to two distinct indices. The stored index is also necessarily smaller than `i`, which satisfies the smaller-index-first requirement without additional sorting. Building the map in full before querying it would break the invariant and require an explicit `i != j` guard in its place.

## 3. Follow-ups & Variations

**Value-only return:** Contract drops the requirement to map elements back to their original indices. 
- **Pivot:** Return `[complement, num]` at the match, which removes the need for the `(value, index)` tuple array and makes sort-plus-two-pointers competitive again. With mutation permitted, sorting in place with an algorithm that needs no auxiliary array, such as heapsort, then sweeping two pointers inward gives `O(n log n)` time at `O(1)` space. Under a read-only array the sort still needs an `O(n)` copy, which leaves the complement map ahead on time at equal space.

**All distinct pairs summing to target:** The caller requires every valid pair rather than the first match. 
- **Pivot:** Early termination is no longer available, which calls for sort-plus-two-pointers over the whole array. Sorting groups equal values adjacently, which means an ordinary pointer step can land on the same value and record the same pair twice. Skip the repeats by advancing before comparing: `left += 1`, followed by `while left < right and nums[left] == nums[left - 1]: left += 1`. Advancing first keeps `left - 1` non-negative, and the `left < right` bound keeps the skip from running past the opposing pointer.

**No solution guaranteed:** A valid pair is no longer guaranteed to exist?
- **Pivot:** The `-> list[int]` return type cannot be honoured on a miss. Widen the signature to `list[int] | None` and return `None` if no match is found. Under the original guarantee, reaching the end of the loop without a result meant the input was invalid, which justified a `ValueError`. A miss is now an expected outcome, which requires a `None` return rather than an exception.