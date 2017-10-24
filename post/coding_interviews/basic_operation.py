from queue import Queue, LifoQueue
from random import randint

"""
关于二叉树的一些基本操作
"""


class BinTreeNode:
    """ 普通二叉数结点的定义 """

    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


"""
   10
 6   14
4 8 12 16

10 6 4 8 14 12 16
4 6 8 10 12 14 16
4 8 6 12 16 14 10
10 6 14 4 8 12 16
preorder(sorted_bin_tree_root, lambda x: print(x, end=" "))
inorder(sorted_bin_tree_root, lambda x: print(x, end=" "))
postorder(sorted_bin_tree_root, lambda x: print(x, end=" "))
widthorder(sorted_bin_tree_root, lambda x: print(x, end=" "))
"""
leafs = [BinTreeNode(i) for i in [4, 8, 12, 16]]
node1 = BinTreeNode(6, left=leafs[0], right=leafs[1])
node2 = BinTreeNode(14, left=leafs[2], right=leafs[3])
sorted_bin_tree_root = BinTreeNode(10, left=node1, right=node2)


def preorder(node, proc):  # 先根序
    s = LifoQueue()
    while node is not None or not s.empty():
        while node is not None:
            proc(node.data)
            s.put(node.right)
            node = node.left
        node = s.get()


def inorder(node, proc):  # 中根序
    s = LifoQueue()
    while node is not None or not s.empty():
        while node is not None:
            s.put(node)
            node = node.left
        if not s.empty():
            node = s.get()
            proc(node.data)
            node = node.right


def postorder(node, proc):  # 后根序	
    s = LifoQueue()
    while node is not None or not s.empty():
        while node is not None:
            s.put(node)
            node = node.left if node.left is not None else node.right

        node = s.get()
        proc(node.data)
        if not s.empty() and s.queue[-1].left == node:  # 重要思想是，如果访问的是左结点，则跳到右结点；如果是右结点，就应该通过跳过内层循环来向上处理它的父结点。
            node = s.queue[-1].right
        else:
            node = None


"""
相比之下，递归的实现方法非常简单，各种顺序也只是改变了一些操作的顺序而已
"""


def preorder_recursion(node, proc):
    if node is None:
        return
    proc(node.data)
    preorder_recursion(node.left, proc)
    preorder_recursion(node.right, proc)


def inorder_recursion(node, proc):
    if node is None:
        return
    preorder_recursion(node.left, proc)
    proc(node.data)
    preorder_recursion(node.right, proc)


def postorder_recursion(node, proc):
    if node is None:
        return
    preorder_recursion(node.left, proc)
    preorder_recursion(node.right, proc)
    proc(node.data)


def widthorder(node, proc):  # 宽度优先
    q = Queue()
    q.put(node)
    while not q.empty():
        node = q.get()
        if node is None:
            continue
        q.put(node.left)
        q.put(node.right)
        proc(node.data)


"""
常见查找算法
"""


def bisect_search(num_list, num):
    if not num_list:
        return False
    if len(num_list) == 1:
        return num_list == num

    start, end = 0, len(num_list) - 1
    while start <= end:
        mid = (start + end) // 2
        if num_list[mid] == num:
            return True
        elif num_list[mid] > num:
            end = mid
        else:
            start = mid
    return False


def binary_search_tree(node, num):
    assert isinstance(node, BinTreeNode)
    while node is not None:
        if node.data == num:
            return True
        elif node.data > num:
            node = node.left
        else:
            node = node.right
    return False


"""
常见排序算法
"""


def partition(nums, start, end):
    if start < end:
        index = randint(start, end)
        nums[start], nums[index] = nums[index], nums[start]
        i, j = start, end
        while i < j:
            if nums[j] < nums[start]:
                while i < j:
                    if nums[i] > nums[start]:
                        nums[i], nums[j] = nums[j], nums[i]
                        break
                    i += 1
            j -= 1
        nums[i], nums[start] = nums[start], nums[i]
        return i
    else:
        raise RuntimeError


def quick_sort(num_list):  # 主函数
    if len(num_list) > 1:
        def _quick_sort_core(nums, start, end):  # 递归函数
            if start >= end:
                return
            i = partition(num_list, start, end)
            _quick_sort_core(num_list, start, i - 1)
            _quick_sort_core(num_list, i + 1, end)

        _quick_sort_core(num_list, 0, len(num_list) - 1)
    else:
        return num_list


def quick_sort1(
        num_list):  # 同样也是用基准值去比较，但不是向上面那样，左右两边向中间逼近，而是大小区间都在左边，逐渐覆盖到右边。因为右边本来就是比较大的，所以只用处理较小的元素：每当找到小的元素（它现在在较大的最右），将这个元素与下标为i的对调，因为下标i就是最小的最右
    def qsort(lst, start, end):
        if start >= end:
            return
        pivot = lst[start]
        i = start
        for j in range(start + 1, end + 1):
            if lst[j] < pivot:
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
        lst[start], lst[i] = lst[i], lst[start]

        qsort(lst, start, i - 1)
        qsort(lst, i + 1, end)

    qsort(num_list, 0, len(num_list) - 1)


def bubble_sort(num_list):  # 比插入排序差
    for i in range(len(num_list)):
        flag = False
        for j in range(1, len(num_list) - i):
            if num_list[j - 1] > num_list[j]:
                num_list[j - 1], num_list[j] = num_list[j], num_list[j - 1]
                flag = True
        if not flag:
            break


def insert_sort(num_list):
    for i in range(1, len(num_list)):
        val = num_list[i]
        pos = i
        while pos > 0 and val < num_list[pos - 1]:
            num_list[pos] = num_list[pos - 1]
            pos -= 1
        num_list[pos] = val


def merge(lfrom, lto, low, mid, high):
    i, j, k = low, mid, low
    while i < mid and j < high:
        if lfrom[i] <= lfrom[j]:
            lto[k] = lfrom[i]
            i += 1
        else:
            lto[k] = lfrom[j]
            j += 1
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
        merge(lfrom, lto, i, i, i + slen)
    else:
        for j in range(i, llen):
            lto[j] = lfrom[j]


def merge_sort(lst):
    slen, llen = 1, len(lst)
    tmplst = [None] * llen
    while slen < llen:
        merge_pass(lst, tmplst, llen, slen)
        slen *= 2
        merge_pass(tmplst, lst, llen, slen)
        slen *= 2


if __name__ == '__main__':
    ll = [7, 5, 8, 11, 66, 2, 4, 33]
    bubble_sort(ll)
    print(ll)
