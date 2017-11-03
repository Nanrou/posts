from queue import LifoQueue


class ListNode:
    """
    普通链表的定义
    """

    def __init__(self, val, next=None):
        self.val = val
        self.next = next

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return self.__str__()


class ComplexListNode(ListNode):
    """ 每个结点均多了一个指向其他结点的指针 """
    complex = None


"""
5 -> 2 -> 4 -> 0 -> 8 -> None
"""


def product_linked_list(val_list=None):  # 生成普通链表
    if val_list is None:
        val_list = [5, 2, 4, 0, 8]
    dummy = ListNode(None)
    p = dummy
    for i in val_list:
        n = ListNode(i)
        p.next = n
        p = n
    return dummy.next


def product_common_node_linked_list():  # 生成Y型链表，就是两个头部指针，指向同一个尾部
    common_node = ListNode(None)
    curr = common_node
    for i in range(5):
        n = ListNode(i)
        curr.next = n
        curr = n

    dummy1 = ListNode(None)
    curr = dummy1
    for i in range(5, 10):
        n = ListNode(i)
        curr.next = n
        curr = n

    curr.next = common_node.next

    dummy2 = ListNode(None)
    curr = dummy2
    for i in range(15, 18):
        n = ListNode(i)
        curr.next = n
        curr = n
    curr.next = common_node.next
    return dummy1.next, dummy2.next


def product_loop_linked_list(val_list=None, entry_node=3):  # 生成有环的链表
    if val_list is None:
        val_list = [5, 2, 4, 0, 8]
    dummy = ListNode(None)
    p = dummy
    loop_entry = None
    for index, i in enumerate(val_list):
        n = ListNode(i)
        if index == entry_node:
            loop_entry = n
        p.next = n
        p = n
    if loop_entry:
        p.next = loop_entry
    return dummy.next


def print_linked_list(head, t=None, proc=lambda x: print(x, end=" ")):
    """
    遍历链表并对其中元素进行操作，默认操作是打印
    :param head: 链表的头部
    :param t: 对前t个元素进行操作，默认None是对全部都进行操作
    :param proc: 对每个元素的操作，默认是打印
    :return:
    """
    p = head
    i = 0
    while p is not None:
        proc(p)
        p = p.next
        if t:
            if i > t:
                break
            else:
                i += 1
                # print()


"""
从尾到头打印链表
    输入链表的头部结点，从尾到头打印出各结点。
"""


def print_linked_list_reversed(node):
    """
    不改变原链表的前提下，需要用栈来辅助实现。
    :param node: 链表的头部结点
    :return: 从尾到头的结点列表
    >>> head = product_linked_list()
    >>> print_linked_list_reversed(head)
    [8, 0, 4, 2, 5]
    >>> print_linked_list_reversed(ListNode(1))
    [1]
    >>> print_linked_list_reversed(None)

    """
    if node is None:
        return None
    stack = LifoQueue()
    curr = node
    while curr is not None:
        stack.put(curr.val)
        curr = curr.next
    res = []
    while not stack.empty():
        res.append(stack.get())
    return res


"""
删除链表中的结点
    给定单向链表的头指针和一个结点指针，定义一个函数在O(1)时间内删除该结点。
"""


def delete_node_in_one_pass(node):
    """
    普通的想法是，从头开始遍历，然后在发现下个结点是目标结点的时候，将指针指向再下
一个结点，这就等于删除了目标结点。问题是这个的复杂度是O(n)。
    换个角度，将下一个结点复制到当前结点，然后当前结点指向下下个结点，那么也等于删
掉当前结点。这样做复杂度就仅为O(1)。
    :param node: 链表的头部指针
    :return: None
    """
    if node.next:
        node.val, node.next = node.next.val, node.next.next
    else:
        node.val = node.next = None


"""
删除链表中重复的结点
    在一个排序的链表中，删除掉重复的结点。
"""


def delete_duplicate_node(head):
    """
    先要注意的地方有，用dummy头部，因为输入的头部有可能会被删除掉。
    因为删除重复结点的时候，连当前结点也要删掉的，所以要用双指针来解决问题。
    :param head: 待操作的链表头部结点
    :return: 操完完成后的链表头部结点

    >>> head = product_linked_list([1, 2, 3, 3, 4, 4, 5])
    >>> print_linked_list(delete_duplicate_node(head), proc=lambda x: print(x, end=','))
    1,2,5,
    >>> head = product_linked_list([1, 2, 2, 3, 3, 4, 4])
    >>> print_linked_list(delete_duplicate_node(head), proc=lambda x: print(x, end=','))
    1,
    >>> head = product_linked_list([2, 2, 3, 3, 4, 4, 5])
    >>> print_linked_list(delete_duplicate_node(head), proc=lambda x: print(x, end=','))
    5,
    >>> head = product_linked_list([1, 2, 3, 4, 5])
    >>> print_linked_list(delete_duplicate_node(head), proc=lambda x: print(x, end=','))
    1,2,3,4,5,
    >>> head = product_linked_list([2, 2, 3, 3, 4, 4])
    >>> print_linked_list(delete_duplicate_node(head), proc=lambda x: print(x, end=','))

    """

    if head is None or head.next is None:
        return head

    dummy = ListNode(None)
    pre = curr = dummy
    curr.next = head
    curr = curr.next
    while curr.next is not None:
        if curr.next and curr.val == curr.next.val:
            while curr.next and curr.val == curr.next.val:  # 跳过重复节点
                curr = curr.next
            if curr is None or curr.next is None:  # 有重复的时候要小心判断，删除完之后的情况
                pre.next = None
            else:
                curr = curr.next
                pre.next = curr
        else:
            curr = curr.next  # 没重复的时候就一起向前
            pre = pre.next

    return dummy.next


"""
链表中倒数第k个结点
    输入一个链表，输出该链表中倒数第k个结点
"""


def find_last_k_node(head, k):  # 链表问题都加一个dummy表头来做就好了
    """
    第一反应是，可以通过栈来存放所有结点，然后再出栈k个来得到结果。
    然后就是利用双指针，走在前面的指针先走k步，然后两个指针再一起走，这样的话
前面指针到尾部时，后面的指针刚好指向倒数第k个。要注意的是k比链表还要长的情况。
    链表问题尽量用dummy头来辅助求解。
    :param head: 链表的头部结点
    :param k: 倒数第几个结点
    :return: 目标结点

    >>> h = product_linked_list()  # 链表 [5, 2, 4, 0, 8]
    >>> find_last_k_node(h, 3)
    4
    >>> find_last_k_node(h, 5)
    5
    >>> find_last_k_node(h, 7)
    Traceback (most recent call last):
        ...
    RuntimeError: k must little than length of linked list

    """

    if head is None or k < 1:
        return head
    dist = k
    dummy = ListNode(None)
    curr = dummy
    curr.next = head
    while dist:
        try:
            curr = curr.next
            dist -= 1
        except AttributeError:  # k比链表长
            raise RuntimeError('k must little than length of linked list')

    pre = dummy
    while curr is not None:
        pre = pre.next
        curr = curr.next
    return pre


"""
链表中环的入口结点
    如果一个链表中包含环，请找出环的入口结点。
"""


def find_entry_of_loop(head):
    """
    先要判断链表是否有环，用双指针去判断，一个指针一次循环前进两次，一个指针一次循环前进一次，
若能够相遇，则说明有环，且相遇的点必定在环内。
    然后要求出环的长度，就从刚才相遇的点出发，计数重新回到这个点的循环次数，则为环的长度。
    最后采用双指针的方法，这个用法很符合直觉的，环内的点完走环的长度会回到这个点，双指针的就是
前面那个指针先走环的长度，然后后面的再开始走，则两个指针会在环的入口处相遇。
    :param head: 链表头部
    :return: 环的入口节点

    # 5 -> 2 -> 4 -> 0 ->8
    #           ^--------|
    >>> h = product_loop_linked_list()
    >>> find_entry_of_loop(h)
    0

    # 5 -> 2 -> 4 -> 0 ->8
    # ^------------------|
    >>> h = product_loop_linked_list(entry_node=0)
    >>> find_entry_of_loop(h)
    5

    # 5 -> 2 -> 4 -> 0 ->8
    #                    ^
    >>> h = product_loop_linked_list(entry_node=4)
    >>> find_entry_of_loop(h)
    8

    """
    if head is None:
        return head
    try:
        p_slow = head.next
        p_fast = p_slow.next
    except AttributeError:
        raise RuntimeError('this linked list hasnt loop.')

    while p_slow or p_fast:  # 判断是否有环
        if p_fast == p_slow:
            p_the_one = p_fast
            break
        p_slow = p_slow.next
        p_fast = p_fast.next
        if p_fast.next:
            p_fast = p_fast.next
    else:
        raise RuntimeError('this linked list hasnt loop')

    count = 1
    p_the_one = p_the_one.next
    while p_the_one is not p_fast:  # 判断环的长度
        p_the_one = p_the_one.next
        count += 1

    p_node1 = head
    for i in range(count):  # 类似双指针来求倒数第k个结点的解法，前面的指针先走那么多步，后面的再出发
        p_node1 = p_node1.next

    p_node2 = head
    while p_node1 is not p_node2:  # 两者相遇的地方就是入口
        p_node1 = p_node1.next
        p_node2 = p_node2.next
    return p_node2


"""
反转链表
    定义一个函数，输入一个链表的头节点，反转该链表并输出反转后链表的头节点。
"""


def reverse_linked_list(head):
    """
    也是使用多指针去解决问题，具体操作为：保存下一节点，将当前节点指向上一节点，然后curr指针
移到下一节点上，prev指针移到当前节点。
    :param head: 需要反转的链表头部
    :return: 已经反转后的链表头部
    h = product_linked_list()
    print_linked_list(h)
    print_linked_list(reverse_linked_list(h))
    >>> head = product_linked_list()  # [5, 2, 4, 0, 8]
    >>> print_linked_list(reverse_linked_list(head), proc=lambda x: print(x, end=','))
    8,0,4,2,5,
    >>> head = product_linked_list([5])
    >>> print_linked_list(reverse_linked_list(head), proc=lambda x: print(x, end=','))
    5,
    """
    if head is None or head.next is None:
        return head
    pre = None
    curr = head
    reverse_head = None
    while curr:
        nextp = curr.next
        if nextp is None:
            reverse_head = curr
        curr.next = pre  # 三个节点依次换位
        pre = curr
        curr = nextp
    return reverse_head


"""
合并两个排序的链表
    输入两个递增排序的链表，合并这两个链表并使新链表中的节点仍然是递增排序。
"""


def merge_two_sorted_linked_list(a, b):  # TODO 合并同一链表
    """
    先比较头部节点，决定出新链表的头部，后面就是逐个排序然后链接起来
    :param a: 一链表头部
    :param b: 另一链表头部
    :return: 合并排序后的新链表头部

    >>> a = product_linked_list([i for i in range(10) if i % 2])
    >>> b = product_linked_list([i for i in range(10) if i % 2 == 0])
    >>> head = merge_two_sorted_linked_list(a, b)
    >>> print_linked_list(head, proc=lambda x: print(x, end=','))
    0,1,2,3,4,5,6,7,8,9,
    """
    if a is None:
        return b
    elif b is None:
        return a

    curr_a, curr_b = a, b

    dummy = ListNode(None)
    curr = dummy

    while curr_a is not None and curr_b is not None:
        if curr_a.val < curr_b.val:
            curr.next = curr_a
            curr_a = curr_a.next
        else:
            curr.next = curr_b
            curr_b = curr_b.next
        curr = curr.next
    if curr_a is not None:
        curr.next = curr_a
    else:
        curr.next = curr_b
    return dummy.next


# 注意分析复杂度
def clone_complex_linked_list(head):  # 分三步走: 1在每个结点后面复制出副本，2根据原来的指向，复制原来指向的next就等于复制了原来的关系，3将链表拆分
    def clone(_head):
        """
        a = product_linked_list([i for i in range(10) if i % 2])
            h = clone(a)
            print_linked_list(h)
            p, n = split_duplicate(h)
            print_linked_list(p)
            print_linked_list(n)
        """
        dummy = ListNode(None)
        curr = dummy
        curr.next = _head
        curr = curr.next
        while curr is not None:
            nextp = curr.next
            copy_node = ListNode(curr.val, curr.next)
            curr.next = copy_node
            curr = nextp
        return dummy.next

    def copy_complex(_head):
        dummy = ListNode(None)
        curr = dummy
        curr.next = _head
        curr = curr.next
        while curr is not None:
            copy_node = curr.next
            copy_node.complex = curr.complex.next
            curr = curr.next.next
        return dummy.next

    def split_duplicate(_head):
        dummy = ListNode(None)
        clone_head = ListNode(None)  # 这里不能用连等

        curr = dummy
        clone_curr = clone_head

        curr.next = _head
        curr = curr.next
        print('head', id(curr))
        while curr is not None:
            clone_curr.next = curr.next
            clone_curr = clone_curr.next

            curr.next = curr.next.next
            curr = curr.next

        return dummy.next, clone_head.next


def transform_tree_to_bothway_linked_list(node):  # 这题不理解。用辅助空间会简单很多，求出中序，然后利用中序来构建双向链表就可以了。
    def transform_core(node, pre_node):
        if node is None:
            return
        curr = node
        if curr.left is not None:
            transform_core(node.left, pre_node)

        curr.left = pre_node
        if pre_node is not None:
            pre_node.right = curr
        pre_node = curr

        if curr.right is not None:
            transform_core(node.right, pre_node)

    dummy = ListNode(None)
    curr = dummy
    curr.next = ListNode(None)
    curr = curr.next
    transform_core(node, curr)
    return dummy.next.next


def find_first_common_node(node1, node2):  # 利用了两个辅助栈来分别记录两个链表，然后从后往回找
    """
    d1, d2 = product_common_node_linked_list()
    print_linked_list(d1)
    print_linked_list(d2)
    d = find_first_common_node(d1, d2)
    print_linked_list(d)
    """
    if node1 is None or node2 is None:
        return None

    _stack1 = LifoQueue()
    _stack2 = LifoQueue()

    curr1, curr2 = node1, node2

    for curr, stack in zip([curr1, curr2], [_stack1, _stack2]):
        while curr is not None:
            stack.put(curr)
            curr = curr.next
    pre1 = pre2 = None
    while not _stack1.empty() and not _stack2.empty():
        _n1, _n2 = _stack1.get(), _stack2.get()
        if _n1 is not _n2:
            return pre1
        pre1, pre2 = _n1, _n2


def find_first_common_node1(node1, node2):  # 对两个链表进行遍历，找到各自的长度，较长的先出发，往前走n步，n为长度之差，然后较短的也出发，遇到相同的就是公共结点
    """
    d1, d2 = product_common_node_linked_list()
    print_linked_list(d1)
    print_linked_list(d2)
    d = find_first_common_node1(d1, d2)
    print_linked_list(d)
    """

    curr1, curr2 = node1, node2
    llen = [0, 0]

    for i, curr in enumerate([curr1, curr2]):
        while curr is not None:
            llen[i] += 1
            curr = curr.next

    curr1, curr2 = node1, node2
    length1, length2 = llen

    if length1 > length2:
        ll = length1 - length2
        while ll:
            curr1 = curr1.next
            ll -= 1
    else:
        ll = length2 - length1
        while ll:
            curr2 = curr2.next
            ll -= 1

    while curr1 and curr2:
        if curr1 is curr2:
            return curr1
        curr1, curr2 = curr1.next, curr2.next


def last_remaining(node, k):
    """
    nn = product_loop_linked_list([0, 1, 2, 3, 4], 0)
    last_remaining(nn, 3)
    """
    curr = ListNode(None)
    curr.next = node
    i = 1
    while curr != curr.next:
        if i < k:
            i += 1
            curr = curr.next
        else:
            curr.next = curr.next.next
            i = 1
    else:
        print(curr)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
