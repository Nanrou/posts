from queue import Queue, LifoQueue
from binarytree import show


class BinTreeNode:
    """ 普通二叉数结点的定义 """

    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        
    def __str__(self):
        return str(self.data)
        
    def __repr__(self):
        return self.__str__()
        


def build_bin_tree(preorder, inorder):
    """
    from basic_operation import preorder

    root = build_bin_tree([1, 2, 4, 7, 3, 5, 6, 8], [4, 7, 2, 1, 5, 3, 8, 6])
    preorder(root, lambda x: print(x, end=" "))
    """
    assert len(preorder) > 0 and len(preorder) == len(inorder)

    def build_bin_tree_core(_preorder, _inorder):
        root = BinTreeNode(_preorder[0])
        if len(_preorder) == 1:  # 递归结束的判断是到达叶结点
            if _preorder == _inorder:
                return root
            else:
                raise RuntimeError('invalid input')

        for i in range(len(_inorder)):  # 根据root的位置去划分左右子树
            if _inorder[i] == root.data:
                break
        else:
            raise RuntimeError('cant find root in inorder')

        if i > 0:
            root.left = build_bin_tree_core(_preorder[1: 1 + i], _inorder[: i])
        if i < len(_inorder) - 1:
            root.right = build_bin_tree_core(_preorder[1 + i:], _inorder[i + 1:])
        return root

    return build_bin_tree_core(preorder, inorder)
    
    
def is_subtree(root1, root2):
    """
    from basic_operation import sorted_bin_tree_root as a_root
    leafs = [BinTreeNode(i) for i in [4, 8]]
    b_root = BinTreeNode(6, *leafs)
    print(is_subtree(a_root, b_root))
    """
    res = False
    
    if root1 is not None and root2 is not None:
        if root1.data == root2.data:
            res = is_subtree_core(root1, root2)
        if not res:
            res = is_subtree(root1.left, root2)
        if not res:
            res = is_subtree(root1.right, root2)        
    return res
    
def is_subtree_core(r1, r2):
    if r2 is None:
        return True
    if r1 is None:
        return False
    if r1.data != r2.data:
        return False
    return is_subtree_core(r1.left, r2.left) and is_subtree_core(r1.right, r2.right)

    
def mirror_tree(node):
    """
    from basic_operation import sorted_bin_tree_root as eg_root
    from basic_operation import widthorder
    lst = []
    widthorder(eg_root, lambda x: lst.append(x))
    show(lst)
    mirror_tree(eg_root)
    lst = []
    widthorder(eg_root, lambda x: lst.append(x))
    show(lst)
    """
    
    if node is not None and node.left is not None and node.right is not None:
        node.left, node.right = node.right, node.left
        mirror_tree(node.left)
        mirror_tree(node.right)
        
def is_symmetrical_tree(node):  # 用中序遍历去判断，一般中序从左到中到右，定义一个新的从右到中到左，比较这两个排序就可以了，注意要处理空的字节
    """
    from basic_operation import sorted_bin_tree_root as eg_root
    print(is_symmetrical_tree(eg_root))
    """
    if node is None:
        return True
        
    _queue = Queue()
    
    pos_seq = []
    def inorder_recursion(node, proc):  # 普通的中序
        if node is None:
            proc(None)
            return
        inorder_recursion(node.left, proc)
        proc(node.data)
        inorder_recursion(node.right, proc)
    tmp = node
    inorder_recursion(tmp, pos_seq.append)
    
    
    rev_seq = []
    def rev_inorder_recursion(node, proc):  # 从右到左的中序
        if node is None:
            proc(None)
            return
        rev_inorder_recursion(node.right, proc)
        proc(node.data)
        rev_inorder_recursion(node.left, proc)
    tmp = node
    rev_inorder_recursion(tmp, rev_seq.append)
    
    return pos_seq == list(reversed(rev_seq))
 

def print_tree_row_by_row(node):  # 用两个变量维持当行与下行的结点数，初始化时，第一行肯定是只有一个
    if node is None:
        raise RuntimeError
    
    _queue = Queue()
    next_level = 0
    to_be_printed = 1
    _queue.put(node)
    while not _queue.empty():
        _node = _queue.get()
        print(_node.data, end=" ")
        to_be_printed -= 1
        
        if _node.left is not None:
            _queue.put(_node.left)
            next_level += 1
        if _node.right is not None:
            _queue.put(_node.right)
            next_level += 1
        
        if to_be_printed == 0:
            print()
            to_be_printed, next_level = next_level, 0
            
def print_tree_by_z(node):  # 用两个栈来分别存放奇数行和偶数行的结点，用两个变量来判断奇偶
    if node is None:
        raise RuntimeError
    
    _queue = [LifoQueue(), LifoQueue()]
    current, next = 0, 1  # 这个0 1的表示非常巧妙
    _queue[current].put(node)
    while not _queue[0].empty() or not _queue[1].empty():
        _node = _queue[current].get()
        print(_node.data, end=" ")
        
        if current == 0:
            if _node.left is not None:
                _queue[next].put(_node.left)
            if _node.right is not None:
                _queue[next].put(_node.right)
        else:
            if _node.right is not None:
                _queue[next].put(_node.right)
            if _node.left is not None:
                _queue[next].put(_node.left)
        
        if _queue[current].empty():
            print()
            current = 1 - current
            next = 1 - next
            
def conclude_postorder_seq(postorder_seq):  # 就是利用二叉数的特征，结点的左边都比右边小
    """
    print(conclude_postorder_seq([5, 7, 6, 9, 11, 10, 8]))
    """
    if len(postorder_seq) < 2:
        return True
    
    def conclude_core(seq):
        _root = seq[-1]
        for i in range(len(seq)):
            if seq[i] > _root:
                break
        
        for j in range(i, len(seq)):
            if seq[j] < _root:
                return False
        
        left = True
        if i > 0:
            left = conclude_core(seq[:i])        
        right = True
        if i < len(seq) - 1:
            right = conclude_core(seq[i: -1])  # 注意这里递归要把最后一位去掉
        return left & right

    return conclude_core(postorder_seq)
    
def find_path_in_tree(node, num):
    """
    r = BinTreeNode(10, BinTreeNode(5, BinTreeNode(4), BinTreeNode(7)), BinTreeNode(12))
    find_path_in_tree(r, 23)
    """
    if node is None:
        raise RuntimeError
    stack = LifoQueue()
    stack.put((node, node.data, [node]))
    flag = False
    while not stack.empty():
        _node, _sum, _path = stack.get()
        if _node.left is None and _node.right is None:
            if _sum == num:
                flag = True
                print('find one paht', _path)
            continue
        if _node.left is not None:
            _new_path = list(_path)
            _new_path.append(_node.left)  # append 是数组操作，返回的是None
            stack.put((_node.left, _sum + _node.left.data, _new_path))
        if _node.right is not None:
            _new_path = list(_path)
            _new_path.append(_node.right)
            stack.put((_node.right, _sum + _node.right.data, _new_path))
    if not flag:
        print('not found')
                
if __name__ == '__main__':
    
    
