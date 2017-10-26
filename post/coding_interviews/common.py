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
    from itertools import permutations
    return list(permutations(lst))
        
        
if __name__ == '__main__':
    print(push_seq_and_pop_seq([1, 2, 3, 4, 5], [4, 5, 3, 2, 1]))