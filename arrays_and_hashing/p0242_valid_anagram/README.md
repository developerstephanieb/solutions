# 0242. Valid Anagram

`LC 242` · `Easy` · `Arrays & Hashing` · pattern: `frequency-count` · ref: `dsa/patterns/hashing/frequency_count`

## 1. Requirements & Scoping

**Problem** 

Given two strings `s` and `t`, return `True` if `t` is an anagram of `s` — the same letters with the same multiplicities, regardless of order — and `False` otherwise.

**Contract**

- **Signature:** `isAnagram(s: str, t: str) -> bool`
- **Length bounds:** `1 <= len(s), len(t) <= 5 * 10**4`; both are non-empty.
- **Character domain:** lowercase English letters (`a`–`z`) only, fixed to 26 symbols. The 26 letters occupy contiguous code points in ASCII and Unicode, which makes arithmetic mapping a letter onto an offset well-defined.
- **Case and whitespace:** no case to fold and no whitespace to strip.

**Ceiling** 

At $n = 5 \times 10^4$, a log-linear pass runs roughly $7.8 \times 10^5$, which is trivially affordable, where a quadratic pass runs $2.5 \times 10^9$, more than three orders of magnitude larger and beyond what any time limit absorbs. The ceiling therefore forces `O(n log n)` or better.

## 2. Algorithmic Design & Trade-offs

**Brute force (pairwise removal)**

- **Mechanics:** Convert `t` into a mutable list of characters. For each character of `s`, scan the list for the first match and delete it. Accept if and only if the list is empty at the end.
- **Complexity:** Time: `O(n^2)`; Space: `O(n)`
- **Analysis:** Converting the immutable string establishes an `O(n)` space floor. Each character of `s` scans a list that shrinks by one element per match, which in the worst case, a true anagram, sums to $\frac{n(n+1)}{2}$ comparisons. At the ceiling $n = 5 \times 10^4$ that is roughly $1.25 \times 10^9$ operations, guaranteeing a Time Limit Exceeded.
- **Pattern:** `frequency-count`. The scan locates *where* each character sits, which anagram equality never asks, and it re-searches a list the previous scans already narrowed. Only multiplicity matters, which calls for a tally keyed by character and removes the search entirely.

**Sort-and-compare**

- **Mechanics:** Sort both strings and evaluate the results for equality.
- **Complexity:** Time: `O(n log n)`; Space: `O(n)`
- **Analysis:** A comparison sort establishes the `O(n log n)` time bound. String immutability forces each sort to allocate a new sequence, requiring `O(n)` space. The approach is correct and makes no alphabet assumption, but it pays a `log n` factor to fully order the characters, which the problem does not require.

**Hash-map count**

- **Mechanics:** Tally character frequencies into a hash map, incrementing for `s` and decrementing for `t`. Accept if and only if every count is zero.
- **Complexity:** Time: `O(n)`; Space: `O(k)`
- **Analysis:** A single linear traversal paired with average-case `O(1)` hash operations bounds time at `O(n)`. Supporting these frequency counts requires dynamic memory allocation for the map structure, scaling space to `O(k)`, where `k` is the number of distinct characters. While this safely handles arbitrary Unicode, it introduces hashing overhead and space that scales with the charset rather than staying constant.

**Fixed count array (chosen)**

- **Mechanics:** Reject on a length mismatch first. Then tally over a fixed 26-slot array indexed by `ord(char) - ord("a")`, incrementing the slot for each letter of `s` and decrementing it for each letter of `t` in a single paired pass. Accept if and only if every slot is zero.
- **Complexity:** Time: `O(n)`; Space: `O(1)`
- **Analysis:** Direct addressing via ASCII math guarantees worst-case `O(1)` index operations per character, and a single paired traversal bounds the tally at `O(n)`. A direct-address table also carries the cost of allocating and zeroing `m` slots before use, where `m` is the width of the value domain, which puts its general bound at `O(n + m)`. The restricted domain fixes `m` at 26 here, a constant independent of the input, which collapses that bound to `O(n)` in time and holds space at a strict `O(1)`.

**Selection:** The constraint ceiling invalidates the brute-force approach. Sort-and-compare survives that filter but is strictly dominated, since both frequency counts reach `O(n)` while remaining correct. Between the two, the fixed array wins under the restricted lowercase domain: direct addressing guarantees worst-case `O(1)` operations against the map's average-case, and `O(1)` space against the map's `O(k)`.

**Invariant:** After `k` paired steps, `counts[i]` holds the occurrences of letter `i` in `s[:k]` minus its occurrences in `t[:k]`. The equal-length guard makes the tallies balance if and only if the two multisets of letters are equal, which makes an all-zero table exactly the anagram condition.

## 3. Follow-ups & Variations

**Untrusted input (contract violation):** The caller breaches the lowercase-only guarantee. 
- **Pivot:** Validate at the boundary, because the direct-address table fails silently rather than loudly. Python resolves negative list indices as offsets from the end, which maps characters from `G` through `` ` `` (ord 71 through 96) onto indices `-26` through `-1`, every one of them valid on a 26-slot list. `ord("G") - ord("a")` evaluates to `-26`, which Python resolves as slot 0, the slot for `a`. The function therefore reports `("G", "a")` as an anagram. Only characters below `G` fall outside the valid range and raise `IndexError`. A hash-map count suffers no such edge case, because every character hashes to its own key.

**Unicode characters:** The input domain expands beyond lowercase English. 
- **Pivot:** Abandon the 26-slot array, which no longer spans the domain. Default to a hash-map frequency count such as `Counter(s) == Counter(t)`. Time remains `O(n)`, but space expands to `O(k)`, where `k` is the number of distinct characters, and the per-character lookup degrades from worst-case `O(1)` to average-case `O(1)` due to potential hash collision resolution.

**Ransom note (LC 383):** Determine if string `t` can be constructed entirely from the characters in string `s`. 
- **Pivot:** The check shifts from strict equality to subset validation. Tally the available frequencies of `s`, then iterate `t` decrementing the corresponding slots, returning `False` the moment any slot drops below zero rather than performing a final zero-sum check.