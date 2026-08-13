"""LC 1. Two Sum.

constraints: 2 <= len(nums) <= 1000; -10**7 <= nums[k], target <= 10**7
exactly one pair (i != j); complement checked before insert, earlier index first
approach: one pass hash map (value -> index), lookup complement before insert,
    return the pair on first complement hit
complexity: O(n) time (avg-case O(1) lookup, amortized avg-case O(1) insert), O(n) space
"""


def two_sum(nums: list[int], target: int) -> list[int]:
    """Return the indices of the two values that sum to target, smaller index first.

    Assumes exactly one such pair exists.

    Args:
        nums: The integers to search.
        target: The sum the two chosen elements must reach.

    Raises:
        ValueError: If the sequence does not contain exactly one valid pair.
    """
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        # invariant: seen stores nums[:i], preventing self-pairing and
        # guaranteeing complement_index < i
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    # unreachable while the one-solution precondition holds
    raise ValueError("no two numbers sum to target")


def test_two_sum() -> None:
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]  # general case
    assert two_sum([3, 2, 4], 6) == [1, 2]  # no self-pairing
    assert two_sum([3, 3], 6) == [0, 1]  # distinct indices
    assert two_sum([-1, -2, -3, -4], -6) == [1, 3]  # negatives
    assert two_sum([-3, 4, 3, 90], 0) == [0, 2]  # sign crossing
    assert two_sum([1, 2], 3) == [0, 1]  # minimum length
