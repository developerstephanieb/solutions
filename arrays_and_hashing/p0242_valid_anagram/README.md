# 0242. Valid Anagram

`LC 242` · `Easy` · `Arrays & Hashing` · pattern: `frequency-count` · ref: `dsa/patterns/hashing/frequency_count`

## 1. Requirements & Scoping

**Problem:** Given two strings `s` and `t`, return `True` if `t` is an anagram of `s` — the same letters with the same multiplicities, regardless of order — and `False` otherwise.

**Signature:** `isAnagram(s: str, t: str) -> bool`

**Clarifying questions**

- *What are the length bounds on `s` and `t`?* — `1 <= len(s), len(t) <= 5 * 10**4`; both are non-empty.
- *What is the character domain — arbitrary Unicode, or a restricted alphabet? Is the comparison case-sensitive and whitespace-sensitive?* — Lowercase English letters (`a`–`z`) only, fixed to 26 symbols. There is no case to fold and no whitespace to strip.

**Portability:** The 26 lowercase letters occupy contiguous code points in ASCII and Unicode, and Python's `str` is Unicode. Any arithmetic that maps a letter onto an offset is therefore well-defined here. A C port cannot rely on that. The C standard guarantees contiguity for the digits `0`–`9` but deliberately withholds it for the alphabet, in order to accommodate EBCDIC, which gaps between `i`/`j` and `r`/`s`.

## 2. Algorithmic Design & Trade-offs

**Brute force (pairwise removal)**

- **Mechanics:** Convert `t` into a mutable list of characters. For each character of `s`, scan the list for the first match and delete it. Accept if and only if the list is empty at the end.
- **Complexity:** Time: `O(n^2)`; Space: `O(n)`
- **Analysis:** Converting the immutable string establishes an `O(n)` space floor. Each character of `s` scans a list that shrinks by one element per match, which in the worst case, a true anagram, sums to $\frac{n(n+1)}{2}$ comparisons. At the ceiling $n = 5 \times 10^4$ that is roughly $1.25 \times 10^9$ operations, guaranteeing a Time Limit Exceeded.

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

**Selection:** At $n = 5 \times 10^4$, a linear pass runs $5 \times 10^4$ operations and a log-linear pass roughly $7.8 \times 10^5$, making both trivially affordable. Therefore, the constraint ceiling permits an `O(n log n)` solution or better. By contrast, a quadratic pass scales to $2.5 \times 10^9$ operations, more than three orders of magnitude larger and beyond what any time limit absorbs, invalidating the brute-force approach. Sort-and-compare survives that filter but is strictly dominated, since both frequency counts reach `O(n)` while remaining correct. Between the two, the fixed array wins under the restricted lowercase domain: direct addressing guarantees worst-case `O(1)` operations against the map's average-case, and `O(1)` space against the map's `O(k)`.

Pattern: `frequency-count`. Reusable note: `ref: dsa/patterns/hashing/frequency_count`.

## 3. Implementation & Testing

**Execution Steps**

1. **Length fast-reject:** If `len(s) != len(t)`, return `False`, as a length mismatch cannot be an anagram.
2. **Initialization:** Initialize a 26-slot count array of zeros.
3. **Concurrent frequency mutation:** Traverse both strings in a single paired pass. Map each character to an index using `ord(char) - ord("a")`, incrementing the slot for the character drawn from `s` and decrementing the slot for the character drawn from `t`.
4. **Zero-sum validation:** Return `True` if every slot is zero. Any non-zero slot indicates differing multiplicities and returns `False`.

**Test Vectors & Edge Cases**

- **General anagram:** `("anagram", "nagaram") -> True` (reordered, same multiplicities).
- **Same letters, same counts:** `("aabb", "bbaa") -> True` (validates multiple occurrences of the same character).
- **Disjoint alphabets:** `("abc", "xyz") -> False` (equal length, no shared characters).
- **Same letters, different counts:** `("aacc", "ccca") -> False` (the case a set-of-letters check would wrongly accept).
- **Length mismatch:** `("a", "ab") -> False` (triggers the fast reject before any tallying).
- **Single character:** `("a", "a") -> True` (the minimum permitted by the constraints).

**Complexity Verification**

- **Time:** `O(n)` — A single paired linear pass to tally, plus a constant `O(1)` validation scan of the 26-slot array.
- **Space:** `O(1)` — The direct-address table is fixed at 26 slots by the confirmed alphabet, independent of `n`.

## 4. Follow-ups & Variations

**Untrusted input (contract violation):** The caller breaches the lowercase-only guarantee. 
- **Pivot:** Validate at the boundary, because the direct-address table fails silently rather than loudly. Python resolves negative list indices as offsets from the end, which maps characters from `G` through `` ` `` (ord 71 through 96) onto indices `-26` through `-1`, every one of them valid on a 26-slot list. `ord("G") - ord("a")` evaluates to `-26`, which Python resolves as slot 0, the slot for `a`. The function therefore reports `("G", "a")` as an anagram. Only characters below `G` fall outside the valid range and raise `IndexError`. A hash-map count suffers no such edge case, because every character hashes to its own key.

**Unicode characters:** The input domain expands beyond lowercase English. 
- **Pivot:** Abandon the 26-slot array, which no longer spans the domain. Default to a hash-map frequency count such as `Counter(s) == Counter(t)`. Time remains `O(n)`, but space expands to `O(k)`, where `k` is the number of distinct characters, and the per-character lookup degrades from worst-case `O(1)` to average-case `O(1)` due to potential hash collision resolution.

**Case- or whitespace-insensitive anagrams:** Complex inputs (e.g., `"Dormitory"` vs `"Dirty Room"`) should compare equal. 
- **Pivot:** Normalize both inputs by casefolding and stripping whitespace before counting. The core frequency logic is unchanged, though normalization forces an `O(n)` space allocation to materialize the sanitized strings, since `str` is immutable.

**Group anagrams (LC 49):** Categorize a list of strings into distinct anagram buckets. 
- **Pivot:** Build a hash map whose key is a canonical signature and whose value is the list of words producing it. The signature must be deterministic and hashable so that anagrams route to the same bucket, which admits two candidates: the alphabetically sorted string, where `"eat"` and `"tea"` both become `"aet"`, or the 26-slot count array cast to a tuple.

**Ransom note (LC 383):** Determine if string `t` can be constructed entirely from the characters in string `s`. 
- **Pivot:** The check shifts from strict equality to subset validation. Tally the available frequencies of `s`, then iterate `t` decrementing the corresponding slots, returning `False` the moment any slot drops below zero rather than performing a final zero-sum check.