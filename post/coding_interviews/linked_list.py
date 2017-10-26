class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next
        
    def __str__(self):
        return str(self.val)

"""
5 -> 2 -> 4 -> 0 -> 8 -> None
"""

def product_linked_list(val_list=[5, 2, 4, 0, 8]):
    dummy = ListNode(None)
    p = dummy
    for i in val_list:
        n = ListNode(i)
        p.next = n
        p = n
    return dummy.next
    
def product_loop_linked_list(val_list=[5, 2, 4, 0, 8]):
    dummy = ListNode(None)
    p = dummy
    for i in val_list:
        n = ListNode(i)
        if i == 4:
            loop_entry = n
        p.next = n
        p = n
    p.next = loop_entry
    return dummy.next
    
def print_linked_list(head, t=0, proc=lambda x: print(x, end=" ")):
    p = head
    i = 0
    while p is not None:
        proc(id(p))
        p = p.next
        if t:
            if i > t:
                break
            else:
                i += 1
    print()
    
    
def delete_node_in_O1(node):  # 将下一个结点复制到当前结点，然后当前结点指向下下个结点，那么也等于删掉当前结点
    if node.next:
        node.val, node.next = node.next.val, node.next.next
    else:
        node.val = node.next = None
        
def delete_duplicate_node(head):
    """
    ll = [[1, 2, 3, 3, 4, 4, 5], [1, 2, 3, 3, 4, 4,], [2, 2, 3, 3, 4, 4, 5], [1, 2, 3, 4, 5]]
    for l in ll:
        print('----------')
        head = product_linked_list(l)
        print_linked_list(head)
        print() 
        print_linked_list(delete_duplicate_node(head))
        print() 
    """

    if head is None or head.next is None:
        return head
        
    dummy = ListNode(None)
    pre = curr = dummy
    curr.next = head
    curr = curr.next
    while curr.next is not None: 
        if curr.next and curr.val == curr.next.val:
            while curr.next and curr.val == curr.next.val:
                curr = curr.next
            if curr is None or curr.next is None:
                pre.next = None
            else:
                curr = curr.next
                pre.next = curr
        else:
            curr = curr.next
            pre = pre.next
 
    return dummy.next
        

def find_last_k_node(head, k):  # 链表问题都加一个dummy表头来做就好了
    """
    h = product_linked_list()
    print_linked_list(h)
    k = find_last_k_node(h, 7)
    print_linked_list(k)
    
    """
    
    if head is None or k == 0:
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
            return dummy.next
        
    pre = dummy
    while curr is not None:
        pre = pre.next
        curr = curr.next
    return pre

def find_entry_of_loop(head):
    """
    h = product_loop_linked_list()
    print_linked_list(h, 10)
    print(find_entry_of_loop(h).val)
    """
    if head is None:
        return head
    try:
        p_slow = head.next
        p_fast = p_slow.next
    except AttributeError:
        raise RuntimeError('linked list hasnt loop')
    
    while p_slow or p_fast:  # 判断是否有环
        if p_fast == p_slow:
            p_the_one = p_fast
            break
        p_slow = p_slow.next
        p_fast = p_fast.next
        if p_fast.next:
            p_fast = p_fast.next
    else:
        raise RuntimeError('linked list hasnt loop')
    
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
    
def reverse_linked_list(head):
    """
    h = product_linked_list()
    print_linked_list(h)
    print_linked_list(reverse_linked_list(h))
    """
    if head is None or head.next is None:
        return head
    pre = None
    curr = head    
    while curr:
        nextp = curr.next    
        if nextp is None:
            reverse_head = curr
        curr.next = pre
        pre = curr
        curr = nextp
    return reverse_head     

def merge_two_sorted_linked_list(a, b):
    """
    a = product_linked_list([i for i in range(10) if i % 2])
    b = product_linked_list([i for i in range(10) if i % 2 == 0])
    print_linked_list(a)
    print_linked_list(b)
    print_linked_list(merge_two_sorted_linked_list(a, b))
    """
    if a is None:
        return b
    elif b is None:
        return a
        
    dummy = ListNode(None)
    curr = dummy
    
    while a is not None and b is not None:
        if a.val < b.val:
            curr.next = a
            a = a.next
        else:
            curr.next = b
            b = b.next
        curr = curr.next
    if a is not None:
        curr.next = a
    else:
        curr.next = b
    return dummy.next
    
class ComplexListNode(ListNode):
    complex = None
        
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
        
        
def serialize_tree(node):  # 要模拟流输入
    if node is None:
        print('$', end=" ")  # 要用流输出
        return
    print(node.data, end=" ")
    serialize_tree(node.left)
    serialize_tree(node.right)
    
if __name__ == '__main__':
    
    
    