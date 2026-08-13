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

**Brute force:** A repeated linear search over a mutable copy of `t`, deleting each character of `s` as it is matched.

- **Mechanics:** Convert `t` into a mutable list of characters. A pointer traverses `s`, and for each character scans the list from the front for the first match and deletes it. Accept if and only if the list is empty when `s` is exhausted.
- **Complexity:** Each character of `s` scans a list that shrinks by one element per match, summing to at most $\frac{n(n+1)}{2}$ comparisons and establishing an `O(n^2)` time bound. Converting the immutable string into a mutable list establishes an `O(n)` space floor.
- **Pattern:** `frequency-count`. The scan searches for a character's position when only its count matters. It passes over every non-matching character without recording what it sees, which leaves the next character of `s` scanning the list from the front again.
- **Analysis:** Exceeds the ceiling at roughly $1.25 \times 10^9$ operations, triggering a Time Limit Exceeded. The `O(n)` space floor eliminates the memory advantage a brute force usually holds. Replacing the search with a tally reduces each lookup to `O(1)` and lowers the time bound to `O(n)`.

**Sort-and-compare:** A paired scan across sorted copies of both strings comparing characters at each index for equality.

- **Mechanics:** Materialize a sorted list of characters from each of `s` and `t`. Traverse both lists simultaneously, comparing the characters at each index and rejecting on the first mismatch.
- **Complexity:** Comparison-based sorting locks time at `O(n log n)`. String immutability forces each sort to allocate a new sequence, requiring `O(n)` space.
- **Analysis:** Handles arbitrary Unicode but pays a `log n` factor to fully order the characters when the problem never asks for an ordering.

**Hash-map count:** A single paired pass tallying character frequencies into a hash map.

- **Mechanics:** Initialize an empty hash map. Traverse `s` and `t` in a single paired pass, incrementing the entry for the character drawn from `s` and decrementing the entry for the character drawn from `t`. Accept if and only if all final entries are zero.
- **Complexity:** A single paired traversal with average-case `O(1)` lookups and amortized average-case `O(1)` insertions establishes an average-case `O(n)` time bound. The map holds one entry per distinct character, scaling space to `O(k)`.
- **Analysis:** Handles arbitrary Unicode but space scales with the character set rather than staying constant.

**Fixed-count array (chosen):** A single paired pass tallying character frequencies into a fixed 26-slot direct-address table.

- **Mechanics:** Reject on a length mismatch first. Then tally over a fixed 26-slot array indexed by `ord(char) - ord("a")`, incrementing the slot for each letter of `s` and decrementing it for each letter of `t` in a single paired pass. Accept if and only if all final entries are zero.
- **Complexity:** Direct addressing via ASCII math guarantees worst-case `O(1)` index operations per character, and a single paired traversal bounds the tally at `O(n)`. A direct-address table also carries the cost of allocating and zeroing `m` slots before use, where `m` is the width of the value domain, which puts its general bound at `O(n + m)`. The restricted domain fixes `m` at 26 here, a constant independent of the input, which collapses that bound to a worst-case `O(n)` in time and holds space at a strict `O(1)`.
- **Invariant:** At the start of iteration `i`, each entry stores the character frequency difference between prefixes `s[:i]` and `t[:i]`. An initial length guard ensures the synchronized traversal consumes both strings entirely; without it, unequal strings (e.g., `("a", "ab")`) would terminate prematurely and falsely evaluate to zero. Upon termination, an all-zero table confirms a net-zero difference for every character, proving identical multisets.
- **Analysis:** Optimal on both axes, with bounds that are worst-case rather than average-case because direct addressing carries no hashing premise. What it surrenders is generality: correctness rests on the confirmed lowercase domain, and an out-of-domain character fails silently rather than loudly.

**Selection:** Between the two frequency counts, the fixed array wins under the restricted lowercase domain: direct addressing guarantees worst-case `O(1)` operations against the map's average-case, and `O(1)` space against the map's `O(k)`.

## 3. Follow-ups & Variations

**Untrusted input (contract violation):** The caller breaches the lowercase-only guarantee. 

- **Pivot:** Validation at the boundary is added, because the direct-address table fails silently rather than loudly. Python resolves negative list indices as offsets from the end, which maps characters from `G` through `` ` `` (ord 71 through 96) onto indices `-26` through `-1`, every one of them valid on a 26-slot list. `ord("G") - ord("a")` evaluates to `-26`, which Python resolves as slot 0, the slot for `a`. The function therefore reports `("G", "a")` as an anagram, and only characters below `G` fall outside the valid range and raise `IndexError`. A membership test per character holds the bounds at `O(n)` time and `O(1)` space.

**Unicode characters:** The input domain expands beyond lowercase English.

- **Pivot:** A hash-map frequency count replaces the 26-slot array, which no longer spans the domain. `Counter(s) == Counter(t)` allocates memory for the distinct characters that appear in the input stream. Time remains `O(n)`, but space expands to `O(k)` in the number of distinct characters, and the per-character lookup degrades from worst-case `O(1)` to average-case `O(1)`.

**Ransom note (LC 383):** Determine if string `t` can be constructed entirely from the characters in string `s`. 

- **Pivot:** No structural change; the acceptance condition shifts from equality to subset validation. Tally the available frequencies of `s`, then iterate `t` decrementing the corresponding slots, returning `False` the moment any slot drops below zero rather than performing a final zero-sum check. The fast reject inverts with it, from `len(s) != len(t)` to `len(t) > len(s)`. Bounds are unchanged at `O(n)` time and `O(1)` space.