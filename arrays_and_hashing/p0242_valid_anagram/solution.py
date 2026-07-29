"""LC 242. Valid Anagram.

in:  s: str, t: str
out: bool  -- True iff t is a permutation of s
constraints: 1 <= len(s), len(t) <= 5 * 10**4; s, t lowercase English letters
len(s) != len(t) -> False; the fixed domain permits a 26-slot direct-address table
approach: tally s (+1) and t (-1) over a 26-slot array; accept iff every slot is zero
complexity: O(n) time, O(1) space (fixed-width tally, direct-addressed)
"""


def is_anagram(s: str, t: str) -> bool:
    """Return True if t is a permutation of s.

    Runs in O(n) time over a single paired pass, and O(1) space since the
    tally is a fixed 26-slot array whose width never grows with the input. Both
    strings must contain only lowercase English letters. Characters outside that
    range are not validated.

    Args:
        s: A string of lowercase English letters.
        t: A string of lowercase English letters.
    """
    if len(s) != len(t):
        return False

    counts = [0] * 26
    # After k paired steps, counts[i] holds the occurrences of letter
    # i in s[:k] minus its occurrences in t[:k]. Equal lengths make the tallies
    # balance iff the two multisets of letters are equal, which makes
    # an all-zero table exactly the anagram condition.
    #
    # strict= records that equal-length invariant. It cannot fire, because the
    # guard has already established it. A bare zip() would truncate to the
    # shorter input in silence, reporting ("a", "ab") as an anagram if the guard
    # were ever removed.
    for char_s, char_t in zip(s, t, strict=True):
        counts[ord(char_s) - ord("a")] += 1
        counts[ord(char_t) - ord("a")] -= 1

    return counts == [0] * 26


def test_is_anagram() -> None:
    assert is_anagram("anagram", "nagaram") is True
    assert is_anagram("aabb", "bbaa") is True
    assert is_anagram("abc", "xyz") is False
    assert is_anagram("aacc", "ccca") is False
    assert is_anagram("a", "ab") is False
    assert is_anagram("a", "a") is True
