"""LC 217. Contains Duplicate.

in:  nums: list[int]
out: bool  -- True iff some value appears at least twice
constraints: 0 <= len(nums) <= 10**5; -10**9 <= nums[i] <= 10**9
    len < 2 -> False; treat input as read-only
approach: one pass, hash set of seen values, return True on the first repeat
complexity: O(n) time (avg-case O(1) lookup, amortized O(1) add), O(n) space
"""


def has_duplicate(nums: list[int]) -> bool:
    """Return True if any value in nums appears at least twice.

    Runs in O(n) time and O(n) space, with an O(1) best case when a duplicate
    appears near the front. Each membership test is average-case O(1) and each
    insertion amortized average-case O(1). nums is not mutated.

    Args:
        nums: The integers to scan for a repeated value.
    """
    seen: set[int] = set()
    # invariant: seen holds exactly the values at indices before the current
    # one. A hit therefore means the value already appeared earlier, which is a
    # duplicate, and the scan can exit without examining the rest.
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


def test_has_duplicate() -> None:
    assert has_duplicate([1, 2, 3, 1]) is True
    assert has_duplicate([1, 2, 3, 4]) is False
    assert has_duplicate([2, 2]) is True
    assert has_duplicate([7, 7, 7]) is True
    assert has_duplicate([-(10**9), 0, 10**9]) is False
    assert has_duplicate([]) is False
    assert has_duplicate([1]) is False
