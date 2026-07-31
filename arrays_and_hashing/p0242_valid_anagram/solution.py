"""LC 242. Valid Anagram.

constraints: 1 <= len(s), len(t) <= 5 * 10**4; s, t lowercase English letters
len(s) != len(t) -> False; the fixed domain permits a 26-slot direct-address table
approach: tally s (+1) and t (-1) over a 26-slot array; accept iff every slot is zero
complexity: O(n) time, O(1) space (fixed-width tally, direct-addressed)
"""


def is_anagram(s: str, t: str) -> bool:
    """Return True if t is a permutation of s.

    Both strings must contain only lowercase English letters. Characters outside
    that range are not validated.

    Args:
        s: A string of lowercase English letters.
        t: A string of lowercase English letters.
    """
    if len(s) != len(t):
        return False

    counts = [0] * 26
    # invariant: after k paired steps, counts[i] is i's count in s[:k] minus in t[:k].
    for char_s, char_t in zip(s, t, strict=True):
        counts[ord(char_s) - ord("a")] += 1
        counts[ord(char_t) - ord("a")] -= 1

    return counts == [0] * 26


def test_is_anagram() -> None:
    assert is_anagram("anagram", "nagaram") is True  # general case
    assert is_anagram("aabb", "bbaa") is True  # repeated letters
    assert is_anagram("abc", "xyz") is False  # disjoint letters
    assert is_anagram("aacc", "ccca") is False  # multiplicity mismatch
    assert is_anagram("a", "ab") is False  # fast reject
    assert is_anagram("a", "a") is True  # minimum length
