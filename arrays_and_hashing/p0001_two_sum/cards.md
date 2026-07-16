Q: Two Sum (LC 1) — what is the optimal approach, and its complexity?
A: A one-pass complement map. For each element, check whether its complement (`target - value`) was already seen. If found, return the stored index and current index; otherwise, insert value -> current_index. Time: `O(n)`. Space: `O(n)`.
TAGS: solutions::arrays_and_hashing::1 pattern::complement_map
---
Q: Two Sum (LC 1) — why look up the complement before inserting the current value?
A: The map holds only values at indices strictly before the current one, so a hit is always a distinct earlier element. This is what keeps an element from pairing with itself and what makes duplicate values like `[3, 3]` resolve to two different indices.
TAGS: solutions::arrays_and_hashing::1 pattern::complement_map
---
Q: Two Sum (LC 1) — why prefer the one-pass map over building the full map first, then querying it?
A: One pass supports O(1) early termination upon the first match and the lookup-before-insertion enforces the distinct-index contract, whereas a two-pass approach requires an explicit guard (`i != j`) to prevent a single element from self-pairing.
TAGS: solutions::arrays_and_hashing::1 pattern::complement_map
---
Q: Two Sum (LC 1) — the map's `O(n)` time rests on what assumption, and how does it degrade?
A: It assumes average-case `O(1)` lookups and amortized `O(1)` insertions. Adversarial hash collisions degrade a single lookup to `O(n)`. Executing this across `n` elements compounds to an `O(n^2)` ceiling.
TAGS: solutions::arrays_and_hashing::1 pattern::complement_map
---
Q: Two Sum (LC 1) — brute force is `O(n^2)`; at `n <= 1000` it passes easily, so why prefer the map?
A: With `n <= 1000`, brute force executes a trivial ~`5 * 10**5` operations, well within standard compute limits. The map is selected purely for asymptotic optimization, achieving an `O(n)` time floor while satisfying the ordered index contract without mutating the input array.
TAGS: solutions::arrays_and_hashing::1
---
Q: Two Sum (LC 1) — if the array were already sorted, what beats the map on space?
A: Opposing two pointers from both ends, moving inward by comparing the pair sum against the target: `O(n)` time, `O(1)` space (this is LC 167). Sorting a raw array is not free here, because it loses the original indices the problem asks for.
TAGS: solutions::arrays_and_hashing::1 pattern::two_pointers
---
Q: Two Sum (LC 1) — the problem wants the smaller index first; what extra work does the one-pass map need for that?
A: None. Because the algorithm dynamically builds the map as it traverses forward, any stored complement is guaranteed to originate from an earlier iteration. Returning `[seen[complement], i]` satisfies the ascending order.
TAGS: solutions::arrays_and_hashing::1 pattern::complement_map