"""
一般问题，包括但不限于栈、队列、循环递归、动态规划等。
"""

from queue import LifoQueue, Queue
from itertools import product


class MyQueue:
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


class MyStack:
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


def fibonacci(n):
    fone, ftwo = 0, 1
    for _ in range(2, n + 1):
        fi = fone + ftwo
        fone, ftwo = ftwo, fi
    return fi


def climb_stairs(n):
    fone, ftwo = 1, 2
    for _ in range(3, n + 1):
        fi = fone + ftwo
        fone, ftwo = ftwo, fi
    return fi


def sort_age1(lst):
    """    
    from random import randint

    bb = []
    for _ in range(12):
        bb.append(randint(18, 70))
    print(bb)
    print(sort_age1(bb))
    print(sort_age2(bb))
    """
    if len(lst) > 1:
        times_of_age = []
        for _ in range(18, 71):
            times_of_age.append(0)
        for i in lst:
            assert 17 < i < 70
            times_of_age[i - 18] += 1

        sorted_ages = []
        for index, times in enumerate(times_of_age):
            for _ in range(times):
                sorted_ages.append(index + 18)

        return sorted_ages
    else:
        return lst


def sort_age2(lst):  # 基数排序，时间复杂度为O(d*(n+k))，d是关键码长度，k是桶的数量，空间复杂度为O(kn)
    if len(lst) > 1:
        bucket_list = [[] for _ in range(10)]
        res = list(lst)
        for i in range(2):
            for ele in res:
                index = ele // (10 ** i) % 10
                bucket_list[index].append(ele)
            res.clear()
            for bucket in bucket_list:
                for j in bucket:
                    res.append(j)
                bucket.clear()
        return res
    else:
        return lst

def cut_the_rope(lenght):
    if lenght < 2: return 0
    if lenght == 2: return 1
    if lenght == 3: return 2
    
    factor_list = [0, 1, 2, 3]
    for i in range(4, lenght + 1):
        factor_list.append(0)
        for j in range(1, i // 2 + 1):
            factor_list[i] = max(factor_list[i], factor_list[j] * factor_list[i - j])
    return factor_list[-1]
    

def count_how_many_one1(num):
    count = 0
    while num > 0:
        num = (num - 1) & num
        count += 1
    return count
    
def count_how_many_one2(num):
    count, flag = 0, 1
    while flag < num:
        if num & flag:
            count += 1
        flag = flag << 1  # 增大比较位而不是右移输入
    return count
    
def my_pow(base, exponent):  # 只支持整数
    if base == 0 and exponent < 0:
        raise RuntimeError
    def pow_core(base, unsign_exponent):
        if unsign_exponent == 0:
            return 1
        if unsign_exponent == 1:
            return base
        res = pow_core(base, unsign_exponent >> 1)  # 划分成两部分
        res *= res  # 这两部分乘回来
        if unsign_exponent & 0b1:  # 若指数为奇数，这里补上那一次
            res *= base
        return res  
            
    if exponent < 0:
        return 1 / pow_core(base, abs(exponent))
    else:
        return pow_core(base, exponent)
        
        
def print_range_number(n):  # 就是输出全排列
    base_list = [i for i in range(10)]
    ll = []
    for _ in range(n):
        ll.append(base_list)
    for ele in product(*ll):
        print(int(''.join([str(e) for e in ele])))
            


def is_match(s, p):  # p是带有正则表达式的字符串。中心思想在于*单独出现是没有意义的，它前面必定跟着一个字符。
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

from string import digits
from re import match

def is_numeric(strings):  # A[.B][e|EC] 或者 .B[e|EC]  其中AC是可以有符号的，B不可以有
    if match('([\+-]?\d+(\.\d*)?|\.\d+)([eE][\+-]?\d+)?', strings):
        return True
    else:
        return False
        
def print_matrix_clock_wisely(matrix):
    """
    n = 1
    bb = []
    for i in range(n):
        bb.append([])
        for j in range(n):
            bb[i].append(j + i * n + 1)
    for b in bb:
        print(b)
    print_matrix_clock_wisely(bb)
    """
    if matrix is None or (not len(matrix) and not len(matrix)):
        raise RuntimeError('invalid matrix')
        
    rows, cols = len(matrix), len(matrix[0])
    start = 0
    
    while rows > start * 2 and cols > start *2:
    
        for col in range(start, cols - start):
            print(matrix[start][col], end=" ")
        if start + 1 < rows:
            for row in range(start + 1, rows - start):
                print(matrix[row][col], end=" ")
            if start + 2 < cols: 
                for col in range(cols - 2 - start, start - 1, -1):
                    print(matrix[row][col], end=" ")
                if start + 2 < rows:
                    for row in range(rows - 2 - start, start, -1):
                        print(matrix[row][col], end=" ")
                        
        start += 1

        
class MinStack:  # 用了一个辅助栈存放最小元素
    """
    ss = MinStack()
    for i in [2, 5, 1, 3, 0, 7]:
        ss.put(i)
    print(ss.min_ele)
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
    
    
def count_k_between_n(n, k=1):  #  十进制，也就是说每十个数，k就出现一次。对于个位来讲，有多少组十，就有多少个k，然后再看余数是否小于k，否则就+1。后面都是如此循环
    """
    print(count_k_between_n(2593, 5))
    """
    _digit = _count = 0
    while n > k * 10 ** _digit:
        print('{} time'.format(_digit))
        _digit += 1
        _group = n // 10 ** _digit
        _count += _group * 10 ** (_digit -  1)
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
            return _num // 10 ** (_digit - 1 - _mod)  % 10  # 等于是要求一个n位数num的第m位是多少，左边第一位为0。m = num // 10 ** (n-m) % 10
        index -= _group
        _digit += 1
        
        
def find_min_number_combine(num_lst):  # 全排之后比较需要n!，动态规划需要n^2。问题本质是，对于元素m和n，是nm小还是mn小，若是nm小，则n在m前面，相反同理。那么问题就可以转换成排序问题了，只不过这个排序的规则不再是比较元素数值的大小，而是比较它们组合成的数字的大小。可以用快排的思想，将比较规则改一下就可以了。
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
    for index, char in enumerate(strings[1:], start = 1):
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
    if n < 6 : return ugly_lst[n]
    
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
    return lst,  _count

    
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
    
    
    
            
            

if __name__ == '__main__':
    print(find_ele_equal_its_sub([-1, 1, 3, 4, 5, 6]))
    