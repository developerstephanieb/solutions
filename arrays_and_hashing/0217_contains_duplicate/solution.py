"""LC 217. Contains Duplicate.

in:  nums: list[int]   out: bool  -- True iff some value appears at least twice
constraints: 0 <= len <= 10**5; -10**9 <= nums[i] <= 10**9
empty -> False; negatives allowed; treat input as read-only
approach: one pass, hash set of seen values, return True on the first repeat
complexity: O(n) time (avg O(1) set ops), O(n) space
"""


def seen_set(nums: list[int]) -> bool:
    """Seen-set with early exit. O(n) time, O(n) space.

    Invariant: ``seen`` holds exactly the elements at indices before the
    current one. If the current element is already in ``seen``, a duplicate
    exists and we exit early.
    """
    seen: set[int] = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


def test_seen_set() -> None:
    assert seen_set([1, 2, 3, 1]) is True
    assert seen_set([1, 2, 3, 4]) is False
    assert seen_set([2, 2]) is True
    assert seen_set([7, 7, 7]) is True
    assert seen_set([-(10**9), 0, 10**9]) is False
    assert seen_set([1]) is False
    assert seen_set([]) is False
