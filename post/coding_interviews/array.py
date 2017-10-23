"""
数组类的问题
"""


"""
数组中重复的数字
题目一： 找出数组中的重复数字
    在一个长度为n的数组里的所有数字都在0~n-1的范围内。数组中某些数字是重复的，但不知道有
几个数字重复了，也不知道每个数字重复了几次。请找出数组中任意一个重复的数字。例如，如果输入
长度为7的数组[2, 3, 1, 0, 2, 5, 3]，那么对应的输出是重复的数字2或者3。
"""


def find_duplication_1(numbers):
    """
    对数组进行排序，然后找到重复的就返回。时间复杂度为O(nlogn)。
    用字典辅助，对数字进行计数。时间和空间复杂度均为O(n)。
    根据题目提到的特性，数组内的数字大小限定在了0~n-1，也就是说明要么这n个数都不重复，然
后这些数最终都能够与下标一一对应上；如果有重复，则说明必定有下标对应的数超过1个。现在所做的
就是从头开始，逐个把数放到它对应的位置上，怎么找呢，不断对调l[i]和l[l[i]]这两个数，总会能
找到那个数，或者重复的数。然后书上讲的每个数字最多只会交换两次就能找到它的位置，我不是很能理
解这一点。
    :param numbers: 长度为n，元素为均大于等于0，小于n的数组。
    :return: 重复的数字

    >>> find_duplication_1([2, 3, 1, 0, 2, 5, 3])
    (2, 2, 2)
    >>> find_duplication_1([2, 1, 0, 4, 5])
    >>> find_duplication_1([6, 7, 8, 7, 9])
    >>> find_duplication_1([1])
    1
    >>> find_duplication_1([])

    """
    if len(numbers) == 0:
        return None
    if len(numbers) == 1:
        return numbers[0]
    for num in numbers:  # 检验每个元素是否在规定范围内
        if num < 0 or num > len(numbers) - 1:
            return

    def find_duplication_by_sort(nums):
        nums.sort()
        for i in range(len(nums) - 1):
            if nums[i] == nums[i + 1]:
                return nums[i]

    def find_duplication_by_hash(nums):
        num_dict = {}
        for i in nums:
            if i in num_dict:
                return i
            else:
                num_dict.setdefault(i, 1)

    def find_duplication_by_sub(nums):
        for i in range(len(nums)):
            while nums[i] != i:
                if nums[i] == nums[nums[i]]:
                    return nums[i]
                # nums[i], nums[nums[i]] = nums[nums[i]], nums[i]  不可以这么写，会错误
                tmp = nums[i]
                nums[i] = nums[tmp]
                nums[tmp] = tmp

    _sort = find_duplication_by_sort(list(numbers))
    _hash = find_duplication_by_hash(list(numbers))
    _sub = find_duplication_by_sub(list(numbers))

    return _sort, _hash, _sub


"""
题目二： 不修改数组找到重复的数字
    在一个长度为n+1的数组里的所有数字都在1~n的范围内。数组至少有一个数字是重复的。请找出
数组中任意一个重复的数字。不能修改原数组。例如，如果输入长度为8的数组[2, 3, 5, 4, 3, 2, 6, 7]，
那么对应的输出是重复的数字2或者3。
"""


def find_duplication_2(numbers):
    """
    问题与上类似，不过这里不允许更改输入数组。
    利用辅助空间，可以像上面那样用哈希表，也可以从下标及元素的对应关系入手，因为限定了元素的取
值范围，所以它可以与长度为n+1的辅助数组的下标对应起来，如果某个下标对应了超过1个元素就说明它重
复了。时间和空间复杂度都为O(n)。
    这里可以采用一下二分法的思想，某个重复元素必定在[1~n/2]或者[n/2 + 1 ~ n]范围内，假如
[1~n/2]这些元素出现的次数超过[1~n/2]次，则说明那个重复的元素必定在这个区间里，反之亦然，如此
循环，最终就可以找到那个重复的元素。这里的时间复杂度为O(logn)，而具体去数元素出现的次数的时间
复杂度为O(n)，所以总的时间复杂度为O(nlogn)，不过空间复杂度只为O(1)。
    第二个方法的弊端在于无法保证找到所有的重复元素。
    :param numbers: 长度为n+1，元素为均大于等于1，小于等于n的数组。
    :return: 重复的数字

    >>> find_duplication_2([2, 3, 5, 4, 1, 2, 6, 7])
    (2, 2)
    >>> find_duplication_2([2, 3, 5, 4, 1, 2, 7, 7])
    (2, 2)
    >>> find_duplication_2([2, 3, 4, 1, 5])
    (None, None)
    >>> find_duplication_2([])

    """
    if len(numbers) == 0:
        return None
    if len(numbers) == 1:
        return numbers[0]
    for num in numbers:
        if num < 1 or num > len(numbers):
            return

    def find_duplication_by_array(nums):
        sub_array = [None] * len(nums)
        for i in nums:
            if sub_array[i - 1] is None:
                sub_array[i - 1] = i
            else:
                return sub_array[i - 1]

    def find_duplication_by_appear_times(nums):

        def count_range(ll, s, e):  # 对区间内出现的数计数
            _count = 0
            for i in ll:
                if s <= i <= e:
                    _count += 1
            return _count

        start = 1
        end = len(nums) - 1  # 这里是取值范围的上下限
        while end >= start:
            mid = ((end - start) >> 1) + start  # 从取值范围中间划分成两部分，类似二分。注意这里划分的是取值范围，而不是输入的数组。
            count = count_range(nums, start, mid)
            if end == start:  # 已经逼近到一个数了
                if count > 1:
                    return start
                else:
                    break
            if count > mid - start + 1:  # 如果某个区间内的数出现次数超过这个区间的总个数，则重复的数就在这个区间
                end = mid
            else:
                start = mid + 1

    _array = find_duplication_by_array(numbers)
    _appear_times = find_duplication_by_appear_times(numbers)
    return _array, _appear_times


"""
二维数组中的查找
    在一个二维数组中，每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。
请完成一个函数，输入这样的一个二维数组和一个整数，判断数组中是否含有该整数。
"""


def find_exist_in_matrix(matrix, num):
    """
    最简单的当然是遍历一遍。
    利用数组的特性，假如num小于某个元素matrix[i][j]，则说明它必然在j列的左边；
如果num大于某个元素matrix[i][j]，则说明它必然在i行的下方，结合这两个判断，就能
找到结果。
    :param matrix:
    :param num:
    :return: 目标num是否在二维数组中
    >>> matrix = [[1, 2, 8, 9], [2, 4, 9, 12], [4, 7, 10, 13], [6, 8, 11, 15]]
    >>> find_exist_in_matrix(matrix, 5)
    False
    >>> find_exist_in_matrix(matrix, 6)
    True

    """
    assert isinstance(num, int), 'invalid number'
    if len(matrix) and len(matrix[0]):
        rows, cols = len(matrix), len(matrix[0])
    else:
        raise RuntimeError('invalid matrix')

    row, col = 0, cols - 1
    while row < rows and col > -1:
        if matrix[row][col] == num:
            return True
        elif matrix[row][col] > num:
            col -= 1
        else:
            row += 1
    return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()
