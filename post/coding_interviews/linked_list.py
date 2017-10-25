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
    
def print_linked_list(head):
    p = head
    while p is not None:
        print(p.val, end=" ")
        p = p.next
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
    if head is None:
        return head
    try:
        p_slow = head.next
        p_fast = p_slow.next
    except AttributeError:
        raise RuntimeError('linked list hasnt loop')
    
    while p_slow or p_fast:
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
    while p_the_one != p_fast:
        p_the_one = p_the_one.next
        count += 1
        
    
    
    
            
if __name__ == '__main__':
    
    