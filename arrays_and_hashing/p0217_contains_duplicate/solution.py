"""LC 217. Contains Duplicate.

constraints: 0 <= len(nums) <= 10**5; -10**9 <= nums[i] <= 10**9
    len < 2 -> False; treat input as read-only
approach: one pass, hash set of seen values, return True on the first repeat
complexity: O(n) time (avg-case O(1) lookup, amortized O(1) add), O(n) space
"""


def has_duplicate(nums: list[int]) -> bool:
    """Return True if any value in nums appears at least twice.

    Args:
        nums: The integers to scan for a repeated value.
    """
    seen: set[int] = set()
    # invariant: at the start of iteration i, seen holds exactly the values in nums[:i]
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


def test_has_duplicate() -> None:
    assert has_duplicate([1, 2, 3, 1]) is True  # general case
    assert has_duplicate([1, 2, 3, 4]) is False  # worst case
    assert has_duplicate([2, 2]) is True  # early exit
    assert has_duplicate([7, 7, 7]) is True  # first repeat, not last
    assert has_duplicate([-(10**9), 0, 10**9]) is False  # value extremes
    assert has_duplicate([]) is False  # empty array
    assert has_duplicate([1]) is False  # singleton
