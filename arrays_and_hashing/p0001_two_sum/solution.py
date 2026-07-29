"""LC 1. Two Sum.

in:  nums: list[int], target: int
out: list[int]  -- [i, j] with i < j and nums[i] + nums[j] == target
constraints: 2 <= len(nums) <= 1000; -10**7 <= nums[k], target <= 10**7
exactly one pair (i != j); complement checked before insert, earlier index first
approach: one pass hash map (value -> index), lookup complement before insert,
    return the pair on first complement hit
complexity: O(n) time (avg-case O(1) lookup, amortized avg-case O(1) insert), O(n) space
"""


def two_sum(nums: list[int], target: int) -> list[int]:
    """Return the indices of the two values that sum to target, smaller index first.

    Assumes exactly one such pair exists. A single linear pass maps each previously
    seen value to its index, which bounds space at O(n) and average-case time at
    O(n). Checking for the complement before inserting the current value prevents an
    element from pairing with itself. The same ordering yields the smaller index
    first, which removes any need to sort.

    Args:
        nums: The integers to search.
        target: The sum the two chosen elements must reach.

    Raises:
        ValueError: If the sequence does not contain exactly one valid pair.
    """
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        # Invariant: seen holds only values from indices before i.
        # A hit is therefore a distinct earlier element, never num itself.
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    # Unreachable while the one-solution precondition holds. Raising turns a
    # contract violation into a loud failure instead of an implicit None.
    raise ValueError("no two numbers sum to target")


def test_two_sum() -> None:
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    assert two_sum([3, 3], 6) == [0, 1]
    assert two_sum([-1, -2, -3, -4], -6) == [1, 3]
    assert two_sum([-3, 4, 3, 90], 0) == [0, 2]
    assert two_sum([1, 2], 3) == [0, 1]
