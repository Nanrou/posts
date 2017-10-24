"""
一般问题，包括但不限于栈、队列、循环递归、动态规划等。
"""

from queue import LifoQueue, Queue


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


if __name__ == '__main__':
    from random import randint

    bb = []
    for _ in range(12):
        bb.append(randint(18, 70))
    print(bb)
    print(sort_age1(bb))
    print(sort_age2(bb))
