from copy import deepcopy
from queue import LifoQueue, Queue
from itertools import product
from string import digits
from re import match

"""
一般问题，包括但不限于栈、队列、循环递归、动态规划等。
"""

"""
用两个栈实现队列
"""


class MyQueue:
    """
    画图去模拟一下实际操作就知道了。简单点说就是一个栈负责进，另外一个栈负责出，出的时候去需要与前一个栈配合。
    >>> my_queue = MyQueue()
    >>> my_queue.put(1)
    >>> my_queue.put(2)
    >>> my_queue.get()
    1
    >>> my_queue.get()
    2
    >>> my_queue.get()
    Traceback (most recent call last):
        ...
    RuntimeError: queue is empty
    """

    def __init__(self):
        self.stack1 = LifoQueue()
        self.stack2 = LifoQueue()

    def put(self, ele):
        self.stack1.put(ele)

    def get(self):
        if self.stack2.empty():
            if self.stack1.empty():
                raise RuntimeError('queue is empty')
            else:
                while not self.stack1.empty():
                    self.stack2.put(self.stack1.get())
        return self.stack2.get()


"""
用两个队列实现一个栈。
"""


class MyStack:
    """
    这个情况麻烦一点，因为不断地把最后一项摆到前面来，所以每次取的时候都要移动一整个队列。
    >>> my_stack = MyStack()
    >>> my_stack.put(1)
    >>> my_stack.put(2)
    >>> my_stack.get()
    2
    >>> my_stack.get()
    1
    >>> my_stack.get()
    Traceback (most recent call last):
        ...
    RuntimeError: stack is empty
    """

    def __init__(self):
        self.queue1 = Queue()
        self.queue2 = Queue()

    def put(self, ele):
        if self.queue1.empty():
            self.queue1.put(ele)
        else:
            self.queue2.put(ele)

    def get(self):
        if self.queue1.empty() and self.queue2.empty():
            raise RuntimeError('stack is empty')

        if self.queue2.empty():
            while self.queue1.qsize() != 1:
                self.queue2.put(self.queue1.get())
            return self.queue1.get()
        else:
            while self.queue2.qsize() != 1:
                self.queue1.put(self.queue2.get())
            return self.queue2.get()


"""
斐波那契数列
    输入n，返回斐波那契数列的第n项。
"""


def fibonacci(n):
    """
    可以用递归，也可以用循环。因为涉及到很多重复的子问题，所以用循环会好很多。
    :param n: 整数n
    :return: 斐波那契数列的第n项

    >>> fibonacci(0)
    0
    >>> fibonacci(3)
    2
    >>> fibonacci(13)
    233
    """
    if n < 0:
        raise RuntimeError
    if n == 0:
        return 0
    if n == 1:
        return 1
    fone, ftwo, fi = 0, 1, None
    for _ in range(2, n + 1):
        fi = fone + ftwo
        fone, ftwo = ftwo, fi
    return fi


"""
爬楼梯
    青蛙上楼梯，一次可以跳1级或者2级，求n级楼梯有多少中跳法。
"""


def climb_stairs(n):
    """
    由于跳法是固定的，设f(n)为n级的跳法，则有f(n) = f(n-1) + f(n-2)。
这是很符合直觉的，因为要跳到第n级，要么是我在n-1级的时候，跳一级来达到n；要
么是我在n-2级的时候，通过跳两级来达到n。所以这里跟斐波那契是一样的解决方法了。
    :param n: n级楼梯
    :return: 跳法总数

    >>> climb_stairs(2)
    2
    >>> climb_stairs(13)
    377
    """
    if n < 1:
        raise RuntimeError
    if n == 1:
        return 1
    if n == 2:
        return 2
    fone, ftwo, fi = 1, 2, None
    for _ in range(3, n + 1):
        fi = fone + ftwo
        fone, ftwo = ftwo, fi
    return fi


"""
矩阵中的路径
    设计一函数，判断矩阵中是否存在一条包含指定字符串所有字符的路径。路径可以从任意一格开始，
每一步都可以往上下左右走，每个方格只允许进入一次。
"""


def find_path_in_matrix(matrix, strings):
    """
    经典的回溯法题。
    就是用栈来辅助存储路径，需要注意的是，要一直保存好现在的位置。
    :param matrix: 目标矩阵
    :param strings: 路径
    :return: bool值

    >>> mm = [['a', 'b', 't', 'g'], ['c', 'f', 'c', 's'], ['j', 'd', 'e', 'h']]
    >>> ss = 'bfce'
    >>> find_path_in_matrix(mm, ss)
    True
    """
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def mark(m, pos):
        m[pos[0]][pos[1]] = None

    def passbile(m, pos, char):
        return m[pos[0]][pos[1]] is char

    if len(strings) <= 0:
        raise RuntimeError('invalid input')

    origins = []
    for row, col in product(range(len(matrix)), range(len(matrix[0]))):
        if matrix[row][col] == strings[0]:
            origins.append((row, col))

    if len(origins) == 0:
        return False

    for origin in origins:
        stack = LifoQueue()
        stack.put((origin, 0, 0))
        _matrix = deepcopy(matrix)

        while not stack.empty():
            _pos, _nxt, _index = stack.get()
            for i in range(_nxt, len(dirs)):
                nextp = (_pos[0] + dirs[i][0], _pos[1] + dirs[i][1])
                if -1 < nextp[0] < len(_matrix) and -1 < nextp[1] < len(_matrix[0]):
                    if _index == len(strings) - 2 and _matrix[nextp[0]][nextp[1]] == strings[_index + 1]:
                        # stack.put((_pos, 0, _index))  # 当前位置已经不在栈中了
                        # stack.put((nextp, 0, _index + 1))
                        # return stack.queue  # 栈中保存着路径
                        return True
                    if passbile(_matrix, nextp, strings[_index + 1]):
                        stack.put((_pos, i + 1, _index))  # 要把现在的位置也要塞回栈中
                        mark(_matrix, nextp)
                        stack.put((nextp, 0, _index + 1))
                        break
    return False


"""
剪绳子
    给定一段长度为n的绳子，要求将绳子剪成m段，要求这m段绳子的长度乘积最大。
"""


def cut_the_rope(length):
    """
    动态规划。当前最优解依靠前一个最优解。状态转移方程为f(n) = max(f(i) * f(n-i)) 0 < i < n，i指剪的长度
    :param length: 绳子长度
    :return: 所剪绳子能得到的最大乘积

    >>> cut_the_rope(1)
    0
    >>> cut_the_rope(16)
    324
    """
    if length < 2:
        return 0
    if length == 2:
        return 1
    if length == 3:
        return 2

    factor_list = [0, 1, 2, 3]
    for i in range(4, length + 1):  # 获得每个长度的最优解
        factor_list.append(0)
        for j in range(1, i // 2 + 1):  # 遍历所有的剪法，来更新得到最大的值。等于是一直填表，供后面使用。
            factor_list[i] = max(factor_list[i], factor_list[j] * factor_list[i - j])
    return factor_list[-1]


"""
二进制中1的个数
    输入一个整数，输出这个整数二进制中1出现的次数。
"""


def count_how_many_one(num):
    """
    不直接对输入做处理，而是改变比较值，逐步增大比较值，和输入的每一位做与操作。
    :param num: 输入number
    :return: 1出现的次数
    >>> count_how_many_one(0)
    0
    >>> count_how_many_one(3)
    2
    >>> count_how_many_one(16)
    1
    >>> count_how_many_one(0x7fffffff)
    31
    """
    count, flag = 0, 1
    while flag <= num:
        if num & flag:
            count += 1
        flag <<= 1  # 增大比较位而不是右移输入
    return count


"""
数值的整数次方
    输入一个数n，和整数e，求n的e次方
"""


def my_pow(base, exponent):
    """
    要考虑数的范围，如正负会有不同的处理方式。其次要有优化的意识，分而治之。如16次方，
可以是0->2->4->8->16，只用4次，如果只是循环乘，则需要16次
    :param base: 底数
    :param exponent: 次方数
    :return: 底数的次方

    >>> my_pow(2, 0)
    1
    >>> my_pow(2, 4)
    16
    >>> my_pow(0, 3)
    0
    >>> my_pow(0, -1)
    Traceback (most recent call last):
        ...
    RuntimeError
    """
    if base == 0 and exponent < 0:
        raise RuntimeError()

    def pow_core(base_, unsigned_exponent):  # 分而治之，递归处理相同的次方数。
        if unsigned_exponent == 0:
            return 1
        if unsigned_exponent == 1:
            return base_
        res = pow_core(base_, unsigned_exponent >> 1)  # 划分成两部分去处理
        res *= res  # 这两部分乘回来
        if unsigned_exponent & 0b1:  # 若指数为奇数，这里补上那一次
            res *= base_
        return res

    if exponent < 0:
        return 1 / pow_core(base, abs(exponent))
    else:
        return pow_core(base, exponent)


"""
打印从1到最大的n位数
    输入数字n，按顺序打印出从1到n最大的n位十进制数。
"""


def print_range_number(n):  # 就是输出全排列
    """
    其实就是输出这n位数的全排列，n为多少，就嵌套n层0~9的循环
    :param n: number
    :return: 输出1~n位数的所有
    >>> print_range_number(0)
    >>> print_range_number(2)  # doctest: +ELLIPSIS
    [0, 1, ..., 98, 99]
    """
    if n == 0:
        return None
    base_list = [i for i in range(10)]
    ll = []
    res = []
    for _ in range(n):
        ll.append(base_list)
    for ele in product(*ll):
        res.append(int(''.join([str(e) for e in ele])))
    return res


"""
正则表达式匹配
    实现能够匹配'.'和'*'的函数。
"""


def is_match(s, p):
    """
    中心思想在于*单独出现是没有意义的，它前面必定跟着一个字符。需要跳过这两个字符去
对后面判断。主要是用递归，从最后判断回头。
    :param s: 普通字符串
    :param p: 模式串，也就是带有正则表达式的字符串
    :return: bool值
    """
    if len(p) is 0:  # 临界条件
        return len(s) is 0

    if len(p) is 1:  # 临界条件
        return len(s) is 1 and (p is '.' or p is s)

    if p[1] is '*':  # 若p[1]位置为*
        if is_match(s, p[2:]):  # 看现在剩下的匹配规则部分与字符串的是否相等，这是假设*所带的字符没出现
            return True
        else:
            return len(s) > 0 and \
                   (p[0] is '.' or p[0] is s[0]) and \
                   is_match(s[1:], p)  # 第二行是要比较那个s的字符是否符合规则， s逐渐向右边靠，也就是逐渐减掉*所带的字符
    else:  # 一般情况，逐个比较字符，然后逐渐缩小问题的规模
        return len(s) > 0 and \
               (p[0] is '.' or p[0] is s[0]) and \
               is_match(s[1:], p[1:])


"""
表示数值的字符串
    实现一个函数来判断字符串是否能转换成数值。
"""


def is_numeric(strings):
    """
    有效的数值形式为 A[.B][e|EC] 或者 .B[e|EC]，其中AC是可以有符号的，B不可以有。
    知道了匹配模式后，直接用re就好了。
    :param strings: 需判断的字符串
    :return: bool值
    """
    if match('([+-]?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', strings):
        return True
    else:
        return False


"""
顺时针打印矩阵
    输入一矩阵，按照从外向里以顺时针的顺序依次打印出每一个数字。
"""


def matrix_clock_wisely(matrix):
    """
    就是要对矩阵进行分析，先要分析出每次循环的前提，然后是每个方向是否可以打印的判断
    :param matrix: 矩阵
    :return: 顺时针打印的结果

    >>> matrix_clock_wisely([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
    [1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10]
    >>> matrix_clock_wisely([[1]])
    [1]
    >>> matrix_clock_wisely([1])
    Traceback (most recent call last):
        ...
    RuntimeError: invalid matrix
    """
    if matrix is None or not isinstance(matrix, list) or not isinstance(matrix[0], list):
        raise RuntimeError('invalid matrix')

    rows, cols = len(matrix), len(matrix[0])
    start = 0
    res = []
    while rows > start * 2 and cols > start * 2:  # 每次循环的必要条件是左上角坐标相乘小于矩阵边长

        for col in range(start, cols - start):
            res.append(matrix[start][col])
        if start + 1 < rows:
            for row in range(start + 1, rows - start):
                res.append(matrix[row][col])
            if start + 2 < cols:
                for col in range(cols - 2 - start, start - 1, -1):
                    res.append(matrix[row][col])
                if start + 2 < rows:
                    for row in range(rows - 2 - start, start, -1):
                        res.append(matrix[row][col])

        start += 1
    return res


"""
包含min函数的栈
    实现一个栈，其中调用min会得到栈中最小值，时间复杂度要为O(1)。
"""


class MinStack:
    """
    显然是要用辅助空间来存放最小值才可以在常数时间得到最小值，那么解决问题的关键在于
如何协调这两个部分。实现方法是，每次push的时候，更新min值，pop的时候也对min处理。就
是用了一个辅助栈存放最小元素

    >>> ss = MinStack()
    >>> for i in [2, 5, 1, 3, 0, 7]: ss.put(i)
    >>> ss.min_ele
    0

    """

    def __init__(self):
        self.stack = LifoQueue()
        self.min_stack = LifoQueue()

    def put(self, ele):
        if self.min_stack.empty():
            self.min_stack.put(ele)
        else:
            self.min_stack.put(min(self.min_stack.queue[-1], ele))
        self.stack.put(ele)

    def get(self):
        if self.stack.empty():
            raise RuntimeError('stack is empty')
        self.min_stack.get()
        return self.stack.get()

    @property
    def min_ele(self):
        if self.min_stack.empty():
            raise RuntimeError('stack is empty')
        return self.min_stack.queue[-1]


def push_seq_and_pop_seq(push_seq, pop_seq):  # 用一个栈来模拟出入栈，一直比较栈顶元素是否能对应上弹出元素就可以了
    if len(push_seq) == 0 or len(push_seq) != len(pop_seq):
        raise RuntimeError

    stack = LifoQueue()
    push_index = pop_index = 0
    while push_index <= len(push_seq):
        if not stack.empty() and stack.queue[-1] == pop_seq[pop_index]:
            pop_index += 1
            stack.get()
            if push_index == pop_index == len(push_seq):
                return True
            continue
        stack.put(push_seq[push_index])
        push_index += 1
    return False


def permutations_chr(lst):  # 直接用内置的排列生成器
    """
    print(push_seq_and_pop_seq([1, 2, 3, 4, 5], [4, 5, 3, 2, 1]))
    """
    from itertools import permutations
    return list(permutations(lst))


def greatest_sum_of_subarry(num_lst):  # 动态规划，这里的判断不是取不取当前这个，而是要不要之前那些。如果之前那些为负数，则从现在重新开始（因为会让和比现在这个数还要小，跟我们想要的最大和不符），否则就叠加之前的。这里又要维持一个最大值的变量，因为最大值不一定出现在最后。
    """
    print(greatest_sum_of_subarry([1, -2, 3, 10, -4, 7, 2, -5]))
    """
    curr = sum = 0
    for i in range(len(num_lst)):
        if i == 0:  # 初始情况
            curr = num_lst[i]
            continue
        if curr < 0:  # 之前的和为负数的话，就重新开始累加
            curr = num_lst[i]
        else:
            curr += num_lst[i]
            sum = max(curr, sum)
    return sum


def count_k_between_n(n, k=1):  # 十进制，也就是说每十个数，k就出现一次。对于个位来讲，有多少组十，就有多少个k，然后再看余数是否小于k，否则就+1。后面都是如此循环
    """
    print(count_k_between_n(2593, 5))
    """
    _digit = _count = 0
    while n > k * 10 ** _digit:
        print('{} time'.format(_digit))
        _digit += 1
        _group = n // 10 ** _digit
        _count += _group * 10 ** (_digit - 1)
        _mod = n % 10 ** _digit // 10 ** (_digit - 1)
        if _mod > k:
            _count += 10 ** (_digit - 1)
        elif _mod == k:
            _count += n % 10 ** (_digit - 1) + 1
    return _count


def digit_at_index(index):  # 找到内在规律，就是前十位是个位数，之后的180位里都是两位数，如此类推。
    """
    print(digit_at_index(1001))
    """
    if index < 0:
        return None
    if index < 10:
        return index

    _digit = 2
    index -= 10
    while True:
        print(index)
        _group = _digit * 9 * 10 ** (_digit - 1)
        if index <= _group:
            _i = index // _digit  # 得出是这个区间的第几个数字
            _mod = index % 10  # 看是这个数字的第几位
            _num = 10 ** (_digit - 1) + _i  # 拿到这个数字
            return _num // 10 ** (_digit - 1 - _mod) % 10  # 等于是要求一个n位数num的第m位是多少，左边第一位为0。m = num // 10 ** (n-m) % 10
        index -= _group
        _digit += 1


def find_min_number_combine(
        num_lst):  # 全排之后比较需要n!，动态规划需要n^2。问题本质是，对于元素m和n，是nm小还是mn小，若是nm小，则n在m前面，相反同理。那么问题就可以转换成排序问题了，只不过这个排序的规则不再是比较元素数值的大小，而是比较它们组合成的数字的大小。可以用快排的思想，将比较规则改一下就可以了。
    """
    print(find_min_number_combine([3, 32, 321]))
    """
    if num_lst is None or len(num_lst) == 0: return None
    if len(num_lst) == 1: return num_lst[0]

    from random import randint
    def sort_core(lst, s, e):
        if s >= e:
            return
        _index = randint(s, e)
        lst[s], lst[_index] = lst[_index], lst[s]
        i = s
        for j in range(s + 1, e + 1):
            a = int(''.join([str(lst[s]), str(lst[j])]))
            b = int(''.join([str(lst[j]), str(lst[s])]))
            if b < a:
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
        lst[s], lst[i] = lst[i], lst[s]
        sort_core(lst, s, i - 1)
        sort_core(lst, i + 1, e)

    sort_core(num_lst, 0, len(num_lst) - 1)
    return int(''.join([str(i) for i in num_lst]))


def transform_num_to_str(num):  # 用了f2 = f0 + f1 的递归思想，注意深拷贝的应用
    """
    print(transform_num_to_str(12258))
    """
    if num < 0:
        raise RuntimeError

    from string import ascii_lowercase
    map_dict = {str(index): char for index, char in enumerate(ascii_lowercase)}

    from copy import deepcopy
    num_str = str(num)
    f0 = [[]]
    for index, _num in enumerate(num_str):
        if index == 0:
            f1 = [[_num]]
            continue
        _f1 = deepcopy(f1)
        for f in f1:
            f.append(_num)
        if 9 < int(num_str[index - 1] + num_str[index]) < 26:
            for f in f0:
                f.append(num_str[index - 1] + num_str[index])
            f2 = f1 + f0
        else:
            f2 = f1
        f0, f1 = deepcopy(_f1), deepcopy(f2)

    return [''.join([map_dict[i] for i in s]) for s in f2]


def get_max_value_in_chessboard(matrix):  # 类似背包问题，可以做出一个最优表，也就是可以用一维数组来保存。
    """
    mm = [[1, 10, 3, 8], [12, 2, 9, 6], [5, 7, 4, 11], [3, 7, 16, 5]] 
    get_max_value_in_chessboard(mm)
    """
    if len(matrix) == 0 or len(matrix[0]) == 0:
        raise RuntimeError
    rows, cols = len(matrix), len(matrix[0])
    res = [None] * cols  # 用一维数组来存放结果

    for row in range(rows):
        for col in range(cols):
            _left = res[col - 1] if col > 0 else 0
            _up = res[col] if row > 0 else 0
            res[col] = max(_left, _up) + matrix[row][col]

    print(res[col])


def get_longest_unique_strings(strings):  # 用一个hash表来存放出现过的字符的位置，方便出现重复的时候更新当前字符串。curr保存着现阶段的不重复字符串，有更长的话就更新到max_中去
    """
    print(get_longest_unique_strings('arabcacfr'))
    """

    if len(strings) < 2:
        return strings

    from string import ascii_lowercase
    map_dict = {char: -1 for char in ascii_lowercase}

    s, e = 0, 1
    max_ = curr = strings[s: e]
    map_dict[strings[0]] = 0
    for index, char in enumerate(strings[1:], start=1):
        if char in curr:
            s = map_dict[char] + 1
        e = index
        curr = strings[s: e + 1]
        map_dict[char] = index

        if len(curr) >= len(max_):  # 若有相同长度，则优先返回后面的
            max_ = curr
    return max_


def find_nth_ugly_num(n):  # 取巧了，第i个数，必定是由前面某个数乘2或3或5得出来的。
    """
    print(find_nth_ugly_num(15))
    """
    from itertools import cycle
    assert n > 0
    ugly_lst = [0, 1, 2, 3, 4, 5]
    if n < 6: return ugly_lst[n]

    tt_list = [3, 3, 3]
    cc = cycle((0, 1, 2))
    while len(ugly_lst) != n + 1:
        tmp = []
        for t in (ugly_lst[tt_list[0]] * 2, ugly_lst[tt_list[1]] * 3, ugly_lst[tt_list[2]] * 5):
            if t > ugly_lst[-1]:  # 取比最后一项大的数中的最小
                tmp.append(t)
        if tmp:
            next_num = min(tmp)
            ugly_lst.append(next_num)
            if next_num % 2 == 0:
                tt_list[0] += 1
            elif next_num % 3 == 0:
                tt_list[1] += 1
            else:
                tt_list[2] += 1
        else:
            i = next(cc)
            tt_list[i] += 1
    return ugly_lst[-1]


def find_first_char_appear_once(strings):  # 直接哈希表来记录出现次数
    """
    print(find_first_char_appear_one_time('google'))
    """
    from collections import OrderedDict
    _map = OrderedDict()
    for char in strings:
        _map.setdefault(char, 0)
        _map[char] += 1

    for k, v in _map.items():
        if v == 1:
            return k


def inverse_pairs(lst):
    """
    print(inverse_pairs([7, 5, 6, 4]))
    """
    if not lst: return None
    if len(lst) == 1: return 0

    _count = 0

    def merge(lfrom, lto, low, mid, high):
        nonlocal _count
        i, j, k = low, mid, low
        while i < mid and j < high:
            if lfrom[i] > lfrom[j]:
                _count += high - j  # 注意理解这一步，因为左右都是已经排序的了，若左边i的比右边j大，则意味着，j的左边都是比i小的，所以逆序对数为high - j
                lto[k] = lfrom[j]
                j += 1
            else:
                lto[k] = lfrom[i]
                i += 1
            k += 1

        while i < mid:
            lto[k] = lfrom[i]
            i += 1
            k += 1
        while j < high:
            lto[k] = lfrom[j]
            j += 1
            k += 1

    def merge_pass(lfrom, lto, llen, slen):
        i = 0
        while i + 2 * slen < llen:
            merge(lfrom, lto, i, i + slen, i + 2 * slen)
            i += 2 * slen
        if i + slen < llen:
            merge(lfrom, lto, i, i + slen, llen)
        else:
            for j in range(i, len(llen)):
                lto[j] = lfrom[j]

    def merge_main(lst):
        _assist = [None] * len(lst)
        slen, llen = 1, len(lst)
        while slen < llen:
            merge_pass(lst, _assist, llen, slen)
            slen *= 2
            merge_pass(_assist, lst, llen, slen)
            slen *= 2

    merge_main(lst)
    return lst, _count


def count_number(lst, k):
    """
    print(count_number([1, 2, 3, 3, 3, 3, 4, 5], 3))
    """
    return lst.count(k)


def find_miss_ele(lst):  # 注意是要看左边
    """
    print(find_miss_ele([1, 2, 3, 4, 5, 6]))
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
    return None


def find_ele_equal_its_sub(lst):
    """
    print(find_ele_equal_its_sub([-1, 1, 3, 4, 5, 6]))
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


def min_heater_range(house_lst, heater_lst):
    """
    print(min_heater_range([1, 2, 3], [2]))
    """
    min_lst = []
    for house in house_lst:
        start, end = 0, len(heater_lst) - 1
        min_range = float('inf')  # 最小距离初始化为正无穷大
        while start <= end:
            mid = (start + end) >> 1
            if heater_lst[mid] == house:
                min_range = 0
                break
            if heater_lst[mid] < house:
                start = mid + 1
            else:
                end = mid - 1
            min_range = min(abs(heater_lst[mid] - house), min_range)
        min_lst.append(min_range)

    return max(min_lst)


def max_in_window(num_lst, width):
    """
    print(max_in_window([2, 3, 4, 2, 6, 2, 5, 1], 3))   
    """
    if width > 0 and len(num_lst) < width:
        raise RuntimeError
    res_lst = []
    for i in range(len(num_lst) - width + 1):
        print(num_lst[i: i + width])
        res_lst.append(max(num_lst[i: i + width]))
    return res_lst


def print_property(n):
    if n < 1:
        raise RuntimeError
    tmp1 = [0] * (6 * n + 1)
    tmp2 = [0] * (6 * n + 1)
    tmp = [tmp1, tmp2]

    flag = 0
    for i in range(1, 6 + 1):
        tmp[flag][i] = 1

    for i in range(2, n + 1):  # 某个点数和n出现的次数等于上一次n-1, n-2, n-3, n-4, n-5, n-6的总和。两个数组来回错位取值。
        for j in range(i, 6 * i + 1):
            tmp[1 - flag][j] = 0
            if j >= i:
                for k in range(j - 6, j):
                    if k > 0:
                        tmp[1 - flag][j] += tmp[flag][k]
        flag = 1 - flag

    if n & 1:
        return (tmp[0])
    else:
        return (tmp[1])


from random import sample


class Deck:
    def __init__(self):
        _ranks = [i for _ in range(4) for i in range(1, 13)]
        _ranks.extend([0, 0])
        self._deck = _ranks

    @property
    def five(self):
        return sample(self._deck, 5)


def is_seq(lst):
    """
    dd = Deck()
    f = dd.five
    print(f)
    print(is_seq([1, 0, 2, 0, 5]))
    """
    assert len(lst) == 5
    lst.sort()
    times = 0
    for i in range(1, 4):
        if lst[i] == lst[i - 1] and lst[i] != 0:
            return False
        if lst[i] - lst[i - 1] == 1:
            continue
        else:
            times += lst[i] - lst[i - 1]

    return True if lst.count(0) >= times else False


def max_diff(num_lst):
    """
    print(max_diff([9, 11, 8, 5, 7, 12, 16, 14]))
    """
    assert len(num_lst) > 1
    _max = float('-inf')
    for i in range(len(num_lst)):
        if i == 0:
            _min_price = num_lst[i]
        else:
            _min_price = min(_min_price, num_lst[i - 1])
            _max = max(num_lst[i] - _min_price, _max)
    return _max


def add_two_num_without_opt(a, b):
    sum, carry = 0, 1
    while carry:
        sum = a ^ b
        carry = (a & b) << 1
        a, b = sum, carry
    return sum


if __name__ == '__main__':
    print(add_two_num_without_opt(7, 11))
