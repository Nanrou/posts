"""
数组类的问题
"""

"""
找出数组中的重复数字
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
                # nums[i], nums[nums[i]] = nums[nums[i]], nums[i]  不可以这么写，因为nums[nums[i]]会变
                tmp = nums[i]
                nums[i] = nums[tmp]
                nums[tmp] = tmp

    _sort = find_duplication_by_sort(list(numbers))
    _hash = find_duplication_by_hash(list(numbers))
    _sub = find_duplication_by_sub(list(numbers))

    return _sort, _hash, _sub

"""
不修改数组找到重复的数字
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
对员工年龄进行排列
    其实也就是排列，不过这里规定了元素的大小范围。
"""


def sort_age1(lst):
    """
    由于目标数组的元素都较小（可以理解为就18~70），可以用哈希表来辅助存储，用空间
换时间。这样做的话空间复杂度会下降到O(n)。
    :param lst: 待排序数组
    :return: 排序好的数组

    >>> sort_age1([25, 26, 44, 18, 54, 60, 25])
    [18, 25, 25, 26, 44, 54, 60]
    >>> sort_age1([25])
    [25]
    >>> sort_age1([])
    []

    """
    if len(lst) > 1:
        times_of_age = []  # 这个可以理解成用哈希表来存储每个年龄的人数
        for _ in range(18, 71):
            times_of_age.append(0)
        for i in lst:
            assert 17 < i < 70  # 这里根据实际情况限定了年龄范围
            times_of_age[i - 18] += 1

        sorted_ages = []
        for index, times in enumerate(times_of_age):
            for _ in range(times):
                sorted_ages.append(index + 18)  # 因为实际上是用数组的序号来代替了哈希的键值，所以返回的时候要做转换

        return sorted_ages
    else:
        return lst


def sort_age2(lst):
    """
    采用基数排序，时间复杂度为O(d*(n+k))，d是关键码长度，k是桶的数量，空间复杂度为O(kn)。
    :param lst: 待排序数组
    :return: 已排序数组

    >>> sort_age2([25, 26, 44, 18, 54, 60, 25])
    [18, 25, 25, 26, 44, 54, 60]
    >>> sort_age2([25])
    [25]
    >>> sort_age2([])
    []
    """
    if len(lst) > 1:
        bucket_list = [[] for _ in range(10)]  # 生成十个桶
        res = list(lst)
        for i in range(2):  # 因为工作年龄必定为两位数
            for ele in res:
                index = ele // (10 ** i) % 10  # 从低位开始排序，根据对应位的数值
                bucket_list[index].append(ele)  # 来将元素放到合适的桶中
            res.clear()
            for bucket in bucket_list:  # 按顺序从桶中取出元素
                for j in bucket:
                    res.append(j)
                bucket.clear()
        return res
    else:
        return lst

"""
旋转数组中最小的数字
    输入一个递增排序的数组的一个旋转，输出旋转数组中的最小元素。
"""


def find_min_in_rotate(lst):
    """
    最简单当然是重新排序就可以了。
    如果数组中元素均不重复，可以用二分的思路，去找到选择的起点，也就是最小值，其特征就是这个
元素的左边比自己大。注意二分时的区间选取，目标所在的区间，必定是左边元素大于右边的。
    如果数组中有重复元素，则只能重新排序了。
    :param lst: 旋转数组
    :return: 最小元素

    >>> find_min_in_rotate([3, 4, 5, 1, 2])
    1
    >>> find_min_in_rotate([1, 2, 3, 4, 5])
    1
    >>> find_min_in_rotate([1, 2])
    1
    >>> find_min_in_rotate([2, 1])
    1
    >>> find_min_in_rotate([3])
    3
    >>> find_min_in_rotate([1, 0, 1, 1])
    0
    """
    if len(lst) > 1:
        start, end = 0, len(lst) - 1
        while lst[start] >= lst[end]:
            if lst[start] == lst[end]:  # 针对有重复元素的情况
                lst.sort()
                return lst[0]

            if end - start == 1:
                return lst[end]
            mid = (start + end) >> 1
            if lst[mid] > lst[start]:
                start = mid
            else:
                end = mid
        return lst[start]
    elif len(lst) == 1:
        return lst[0]
    else:
        return None


"""
二维数组中的查找元素
    在一个二维数组中，每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。
请完成一个函数，输入这样的一个二维数组和一个整数，判断数组中是否含有该整数。
"""


def find_exist_in_matrix(matrix, num):
    """
    最简单的当然是遍历一遍。
    利用数组的特性，假如num小于某个元素matrix[i][j]，则说明它必然在j列的左边；
如果num大于某个元素matrix[i][j]，则说明它必然在i行的下方，结合这两个判断，就能
找到结果。

    :param matrix: 一个二维数组，其中每列都是从上到下地递增，每行都是从左到右地递增
    :param num: 目标number
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


"""
调整数组顺序使奇数位于偶数前
    输入一整数数组，实现一个函数来调整改数组中数字的顺序，使得所有奇数位于数组的前半部分，所有
偶数位于数组的后半部分。
"""


def sort_odd_and_even(num_lst):
    """
    由于不是要求每个的顺序，只是简单的划分，所以直接用双指针来解决就好了。两个指针分别从头尾开
始，遇到不符合要求的就对调位置，两个指针相遇时就完成了整个数组的调整。
    :param num_lst: 目标数组
    :return: 调整后的数组

    >>> sort_odd_and_even([0, 1, 2, 3, 4, 5])
    [5, 1, 3, 2, 4, 0]
    >>> sort_odd_and_even([1, 3, 5, 0, 2, 4])
    [1, 3, 5, 0, 2, 4]
    >>> sort_odd_and_even([0])
    [0]

    """
    if num_lst is None:
        return None
    lst = list(num_lst)
    i, j = 0, len(lst) - 1
    while i < j:
        while i < j and lst[j] & 0b1 == 0:
            j -= 1
        while i < j and lst[i] & 0b1 != 0:
            i += 1
        if i < j:  # 始终要对其序号进行判断
            lst[i], lst[j] = lst[j], lst[i]
    return lst


"""
数组中出现次数超过一半的数字
    数组中有一个数字出现的次数超过数组长度的一半，请找出这个数字。
"""


def find_more_than_half_num(num_lst):
    """
    最简单的但是直接排序，然后中间那个元素就是所求。
    利用上面这个结论，就可以将问题转换为求第k个元素（求中间那个元素）。
    利用快排的划分。
    :param num_lst:
    :return:

    >>> find_more_than_half_num([1, 2, 3, 2, 2, 2, 5, 4, 2])
    2
    """
    if num_lst is None or len(num_lst) == 0:
        return None
    if len(num_lst) <= 2:
        return num_lst[0]

    def partition(lst, s, e):
        pivot = lst[s]
        i = s
        for j in range(s + 1, end + 1):
            if lst[j] < pivot:
                i += 1
                lst[i], lst[j] = lst[j], lst[i]

        lst[s], lst[i] = lst[i], lst[s]
        return i

    start, end = 0, len(num_lst) - 1
    mid = (start + end) >> 1
    index = partition(num_lst, start, end)
    while index != mid:
        if index > mid:
            end = index - 1
            index = partition(num_lst, start, end)
        else:
            start = index + 1
            index = partition(num_lst, start, end)
    return num_lst[index]


def find_more_than_half_num1(num_lst):
    """
    那个数的出现次数，至少比其他所有数的总出现次数多一次，所以遍历一次就能找出来。
    :param num_lst:
    :return:

    >>> find_more_than_half_num1([1, 2, 3, 2, 2, 2, 5, 4, 2])
    2

    """
    that_num, times = None, 0
    for i in num_lst:
        if times == 0:
            that_num = i
        elif i == that_num:
            times += 1
        else:
            times -= 1
    return that_num


"""
最小的k个数
    输入n个整数，找出其中最小的k个数。
"""


def find_min_k_num(num_lst, k):
    """
    利用快排的思想，将问题转换成找第k个数就好了。
    :param num_lst:
    :param k:
    :return:
    """
    if len(num_lst) <= k:
        return num_lst

    from random import randint  # 引入随机数会更好的

    def partition(lst, s, e):
        if s >= e:
            return s
        _index = randint(s, e)
        lst[s], lst[_index] = lst[_index], lst[s]
        i = s
        for j in range(s + 1, e + 1):  # 注意这个范围，end要加1
            if lst[j] < lst[s]:
                i += 1  # 要先加1，因为要保证不会移动轴元素
                lst[i], lst[j] = lst[j], lst[i]
        lst[s], lst[i] = lst[i], lst[s]
        return i

    start, end = 0, len(num_lst) - 1
    index = partition(num_lst, start, end)
    while k != index:
        if index > k:
            end = index - 1
            index = partition(num_lst, start, end)
        else:
            start = index + 1
            index = partition(num_lst, start, end)
    return num_lst[: k]


def find_min_k_num1(num_lst, k):
    """
    用堆来存放最小的k项。
    :param num_lst:
    :param k:
    :return:

    >>> find_min_k_num1([i for i in range(10)], 4)
    """
    from heapq import nsmallest  # 内置的求最小k项函数
    return nsmallest(k, num_lst)


"""
在排序数组中查找数字
    统计一个数字在排序数组中出现的次数。
"""


def count_number(lst, k):
    """
    直接用内置的。
    可以尝试用二分来找到左右的边界来得到最后的结果。
    >>> count_number([1, 2, 3, 3, 3, 3, 4, 5], 3)
    4
    """
    return lst.count(k)


"""
0~n-1中缺失的数字
    一个长度为n-1的递增排序数组中的所有数字都是唯一的，并且每个数字都在范围0~n-1内。
有且只有一个数字不在该数组中，求这个数字。
"""


def find_miss_ele(lst):
    """
    可以采用求和，求0~n-1的和，与数组的和的差值就是所求了。
    或者将问题转换成，求第一个 值与下标不相等的元素。
    :param lst: 数组
    :return: 缺失的元素
    >>> find_miss_ele([1, 2, 3, 4, 5, 6])
    0
    >>> find_miss_ele([0, 1, 2, 3, 5, 6])
    4
    >>> find_miss_ele([0, 1, 2, 3, 4, 5])
    6
    """
    start, end = 0, len(lst) - 1

    while start <= end:
        mid = (start + end) >> 1
        if mid == lst[mid]:  # 边界必定是在相等元素的右边
            start = mid + 1
        else:
            if mid - 1 == lst[mid - 1] or mid == 0:
                return mid
            end = mid - 1
    return start


"""
数组中数值与下标相等的元素
    假设一个单调递增的数组里的每个元素都是整数并且唯一，请找出数组中任意一个
数值等于其下标的元素。
"""


def find_ele_equal_its_sub(lst):
    """
    在解决有序的相关问题时，应优先想到二分法。
    由于数组是单调递增的，所以可以用二分去找。
    :param lst: 数组
    :return: 数值与下标相等的元素
    >>> find_ele_equal_its_sub([-1, 1, 3, 4, 5, 6])
    1
    """
    start, end = 0, len(lst) - 1
    while start <= end:  # 二分是要有等号的
        mid = (start + end) >> 1
        if mid == lst[mid]:
            return mid
        if lst[mid] > mid:
            end = mid - 1
        else:
            start = mid + 1
    return None


"""
数组中只出现一次的两个数字
    一个整数数组里两个数字以外，其他数字都出现了两次，请找出这两个数字。
"""


def find_two_num_appear_once(num_lst):  # 考察位运算，利用了一个数异或本身为0的性质
    """
    位运算，两个相同的数异或会得到0。利用这个特点。
    对整个数组做异或运算，最后一定会得到一个不为0的数。利用这个数将数组划分成两部分，
然后分别对各部分又做一次异或，就可以得到结果了。
    :param num_lst: 数组
    :return: 那两个数字
    >>> find_two_num_appear_once([2, 4, 3, 6, 3, 2, 5, 5])
    (6, 4)
    """
    assert len(num_lst) > 3
    from functools import reduce
    tmp, one = reduce(lambda x, y: x ^ y, num_lst), 1  # 因为有两个数不同，所以最终得出来的数肯定不为1
    while not tmp & one:
        one <<= 1  # tmp的二进制表示中，必然最少有一个1，现在去找那一个1的位置
    a = reduce(lambda x, y: x ^ y, [num for num in num_lst if num & one])  # 所以可以根据上面那个数将数组分为两个部分，再分别异或就会剩下那个单独的数了
    b = reduce(lambda x, y: x ^ y, [num for num in num_lst if not num & one])
    return a, b


"""
数组中唯一只出现一次的数字
    在一个数组中除一个数字只出现一次以外，其他数字都出现了三次，找到那个只出现一次的数字。
"""


def find_one_num_appear_once(num_lst):
    """
    往位运算方面去靠。换成二进制表示，在每一位上面相加，最后再对所有位整除3，如果某位不能
整除3，则说明它是所求的其中一位。
    :param num_lst: 数组
    :return: 所求那个数

    >>> find_one_num_appear_once([1, 2, 1, 1])
    2
    """
    assert len(num_lst) > 3
    bit_lst = [0] * 32
    for num in num_lst:
        num_in_bit = bin(num).lstrip('0b').zfill(32)
        for index, char in enumerate(num_in_bit):
            bit_lst[index] += int(char)
    for i in range(len(bit_lst)):
        bit_lst[i] %= 3
    return int(''.join([str(bit) for bit in bit_lst]), 2)


"""
和为s的两个数字
    输入一个递增排序的数组和一个数字s，在数组中查找两个数，使它们的和正好是s。
"""


def find_two_num_with_sum(num_lst, k):
    """
    直接用双指针，一个指头一个指尾就可以了。因为是有序的。
    :param num_lst: 有序的数组
    :param k: 目标和
    :return: 达到要求的两个元素

    >>> find_two_num_with_sum([1, 2, 4, 7, 11, 15], 15)
    (4, 11)
    """
    assert len(num_lst) > 2
    p1, p2 = 0, len(num_lst) - 1
    while p1 < p2:
        if num_lst[p1] + num_lst[p2] == k:
            return num_lst[p1], num_lst[p2]
        elif num_lst[p1] + num_lst[p2] < k:
            p1 += 1
        else:
            p2 -= 1
    return None


"""
和为s的连续正数序列
    输入一个正数s，打印出所有和为s的连续正整数序列。
"""


def find_seq_with_sum(k):
    """
    还是用双指针，不过这次是用双指针来包住序列的。
    :param k: 某正整数
    :return: 和为k的连续序列
    >>> find_seq_with_sum(15)
    [[1, 2, 3, 4, 5], [4, 5, 6], [7, 8]]
    """
    num_lst = [i for i in range(1, k // 2 + 2)]  # 序列的取值范围
    p1, p2 = 0, 1
    res = []
    while num_lst[p1] < k / 2 and p2 < len(num_lst):
        curr_sum = sum(num_lst[p1: p2 + 1])
        if curr_sum == k:
            res.append(num_lst[p1: p2 + 1])
            p2 += 1
        if curr_sum < k:
            p2 += 1
        else:
            p1 += 1
    return res


"""
滑动窗口的最大值
    给定一个数组和滑动窗口的大小，请找出所有滑动窗口里的最大值。
"""


def max_in_window(num_lst, width):
    """
    用最直观的方法来做，就是直接比较每个窗口。
    >>> max_in_window([2, 3, 4, 2, 6, 2, 5, 1], 3)
    [4, 4, 6, 6, 6, 5]
    """
    if width > 0 and len(num_lst) < width:
        raise RuntimeError
    res_lst = []
    for i in range(len(num_lst) - width + 1):
        res_lst.append(max(num_lst[i: i + width]))
    return res_lst


if __name__ == '__main__':
    import doctest

    doctest.testmod()
