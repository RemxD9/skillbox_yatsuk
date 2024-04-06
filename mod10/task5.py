def find_insert_position(nums, target):
    left, right = 0, len(nums) - 1
    if not nums:
        return 0
    if target < nums[0]:
        return 0
    if target > nums[-1]:
        return len(nums)

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return left


if __name__ == '__main__':
    A = [1, 2, 3, 3, 3, 5]
    x = 4
    assert find_insert_position(A, x) == 5
    print('Okay')

    A = [1, 2, 5, 5, 6]
    x = 4
    assert find_insert_position(A, x) == 2
    print('ok')
