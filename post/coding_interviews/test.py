def find_min_in_rotate(lst):
    if len(lst) > 1:
        start, end = 0, len(lst) - 1
        while lst[start] >= lst[end]:
            if end - start == 1:
                return lst[end]
            mid = (start + end) // 2
            if lst[mid] > lst[start]:
                start = mid
            else:
                end = mid
        return lst[start]
    else:
        return lst


from queue import LifoQueue
from itertools import product


def find_path_in_matrix(matrix, strings):
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def mark(m, pos):
        m[pos[0]][pos[1]] = None

    def passbile(m, pos, char):
        return m[pos[0]][pos[1]] is char

    stack = LifoQueue()

    if len(strings) <= 0:
        raise RuntimeError

    for row, col in product(range(len(matrix)), range(len(matrix[0]))):
        if matrix[row][col] == strings[0]:
            origin = (row, col)
            break
    else:
        raise RuntimeError('cant find the origin')

    stack.put((origin, 0, 0))

    while not stack.empty():
        _pos, _nxt, _index = stack.get()
        for i in range(_nxt, len(dirs)):
            nextp = (_pos[0] + dirs[i][0], _pos[1] + dirs[i][1])
            if -1 < nextp[0] < len(matrix) and -1 < nextp[1] < len(matrix[0]):
                if _index == len(strings) - 2 and matrix[nextp[0]][nextp[1]] == strings[_index + 1]:
                    stack.put((_pos, 0, _index))  # 当前位置已经不在栈中了
                    stack.put((nextp, 0, _index + 1))
                    return stack.queue  # 栈中保存着路径
                if passbile(matrix, nextp, strings[_index + 1]):
                    stack.put((_pos, i + 1, _index))
                    mark(matrix, nextp)
                    stack.put((nextp, 0, _index + 1))
                    break
    return False


def robot_move_range(rows, cols, k):
    """
    mm = [['a', 'b', 't', 'g'], ['c', 'f', 'c', 's'], ['j', 'd', 'e', 'h']]
    ss = 'bfce'
    print(find_path_in_matrix(mm, ss))
    """
    if rows <= 0 or cols <= 0 or k < 0:
        raise RuntimeError

    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def check(row, col):
        _sum = 0
        for i in [row, col]:
            while i > 0:
                _sum += i % 10
                i //= 10
        if _sum > k:
            return False
        return True

    def passbile(row, col, visited_lst):
        if -1 < row < rows and -1 < col < cols and check(row, col) and visited[row, col] is None:
            return True
        return False

    def move_core(row, col, visited_lst):
        _count = 0
        if passible(row, col, visited_lst):
            visited_lst[row * cols + col] = True
            _count = 1 + sum([move_core(row + dirs[i][0], col + dirs[i][1], visited_lst) for i in range(4)])
        return _count

    visited = []
    for _ in range(rows * cols):
        visited.append(False)

    count = move_core(0, 0, visited)

    return count


def sort_odd_and_even(lst):
    i, j = 0, len(lst) - 1
    while i < j:
        while i < j and lst[j] & 0b1 == 0:
            j -= 1
        while i < j and lst[i] & 0b1 != 0:
            i += 1
        if i < j:
            lst[i], lst[j] = lst[j], lst[i]


def conclude_even(ele):
    if ele & 0b1 == 0:
        return True
    return False


def sort_by_some_rule(lst, func):
    i, j = 0, len(lst) - 1
    while i < j:
        while i < j and func(lst[j]):
            j -= 1
        while i < j and not func(lst[i]):
            i += 1
        if i < j:
            lst[i], lst[j] = lst[j], lst[i]


def find_more_than_half_num(num_lst):
    """
    print(find_more_than_half_num([1, 2, 3, 2, 2, 2, 5, 4, 2]))
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


def find_more_than_half_num1(num_lst):  # 那个数的出现次数，至少比其他所有数的总出现次数多一次
    that_num, times = None, 0
    for i in num_lst:
        if times == 0:
            that_num = i
        elif i == that_num:
            times += 1
        else:
            times -= 1
    return that_num


def find_min_k_num(num_lst, k):
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
    print(num_lst)
    return num_lst[: k]


def find_min_k_num1(num_lst, k):  # 用堆来存放最小的k项
    """
    ll = [i for i in range(10)]
    print(find_min_k_num1(ll, 4))
    """
    from heapq import nsmallest
    return nsmallest(k, num_lst)


def find_two_num_appear_once(num_lst):  # 考察位运算，利用了一个数异或本身为0的性质
    assert len(num_lst) > 3
    from functools import reduce
    flag = reduce(lambda x, y: x ^ y, num_lst)  # 因为有两个数不同，所以最终得出来的数肯定不为1
    a = reduce(lambda x, y: x ^ y, [num for num in num_lst if num & 1])  # 所以可以根据上面那个数将数组分为两个部分，再分别异或就会剩下那个单独的数了
    b = reduce(lambda x, y: x ^ y, [num for num in num_lst if not num & 1])
    return a, b


def find_one_num_appear_once(num_lst):
    """

    print(find_one_num_appear_once([1, 2, 1, 1]))
    :param num_lst:
    :return:
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


def find_two_num_with_sum(num_lst, k):
    """
    print(find_two_num_with_sum([1, 2, 4, 7, 11, 15], 15))
    :param num_lst:
    :param k:
    :return:
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


def find_seq_with_sum(num_lst, k):
    """
    print(find_seq_with_sum([i for i in range(1, 9)], 15))
    :param num_lst:
    :param k:
    :return:
    """
    assert len(num_lst) > 2
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



if __name__ == '__main__':
