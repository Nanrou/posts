from queue import Queue, LifoQueue
# from binarytree import show
from basic_operation import preorder  # 这个是输出前序遍历的func
from basic_operation import sorted_bin_tree_root as root_node


class BinTreeNode:
    """ 普通二叉树的结点定义 """

    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()


"""
重建二叉树
    输入前序遍历和中序遍历，以此来生成对应的二叉树。
"""


def build_bin_tree(preorder, inorder):
    """
    由前序遍历可以知道根结点的位置，根据这个结点在中序遍历的位置，划分出左右子树。
    后面都是可以用递归去做了，递归结束的条件为到叶结点，也就是划分出来的数组长度为1的时候。

    :param preorder: 前序遍历
    :param inorder: 中序遍历
    :return: 二叉树的根结点

    >>> root = build_bin_tree([1, 2, 4, 7, 3, 5, 6, 8], [4, 7, 2, 1, 5, 3, 8, 6])
    >>> preorder(root, lambda x: print(x, end=","))
    1,2,4,7,3,5,6,8,
    >>> root = build_bin_tree([1], [1])
    >>> preorder(root, lambda x: print(x, end=""))
    1
    >>> root = build_bin_tree([1], [1, 2])
    Traceback (most recent call last):
        ...
    AssertionError: invalid input
    """
    assert len(preorder) > 0 and len(preorder) == len(inorder), 'invalid input'

    def build_bin_tree_core(_preorder, _inorder):  # 递归主逻辑
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


"""
树的子结构
    输入两棵二叉树A和B，判断B是不是A的子结构。
"""


def is_subtree(root1, root2):
    """
    递归去做，先判断根节点，然后判断其左右子树是否一致
    :param root1: 大的那棵树
    :param root2: 小的那棵树
    :return: bool值
    >>> b_root = BinTreeNode(6, *[BinTreeNode(i) for i in [4, 8]])
    >>> is_subtree(root_node, b_root)
    True
    >>> is_subtree(root_node, None)
    True
    """
    if root2 is None:
        return True
    if root1 is None:
        return False

    def is_subtree_core(r1, r2):
        if r2 is None:  # 到达叶节点下面的None则说明之前的比较都通过了
            return True
        if r1 is None:
            return False
        if r1.data != r2.data:
            return False
        return is_subtree_core(r1.left, r2.left) and is_subtree_core(r1.right, r2.right)

    res = False

    if root1 is not None and root2 is not None:
        if root1.data == root2.data:
            res = is_subtree_core(root1, root2)
        if not res:
            res = is_subtree(root1.left, root2)  # 注意这三个是不一样的，这里等于是前序遍历
        if not res:
            res = is_subtree(root1.right, root2)
    return res


"""
二叉树的镜像
    输入一棵二叉树，请输出它的镜像。
"""


def mirror_tree(node):
    """
    递归去处理每个节点，具体操作就是对调节点的左右子树，然后再对子树做同样操作
    :param node: 二叉树的根节点
    :return: 二叉树的镜像
    """

    if node is not None and node.left is not None and node.right is not None:
        node.left, node.right = node.right, node.left
        mirror_tree(node.left)
        mirror_tree(node.right)


"""
对称二叉树
    判断一个二叉树是否是对称的
"""


def is_symmetrical_tree(root):
    """
    无论如何，肯定是要对二叉树进行遍历，既然要遍历，则考虑中序遍历的特点，中序遍历是从左到中到右，
如果我们定义一个从右到中到左的遍历方法，再比较这两个遍历方法的结果，若相等则说明对称。
    :param root: 二叉树的根节点
    :return: bool值

    >>> is_symmetrical_tree(root_node)
    False
    >>> is_symmetrical_tree(BinTreeNode(1))
    True
    >>> is_symmetrical_tree(BinTreeNode(1, BinTreeNode(2), BinTreeNode(2)))
    True
    """
    if root is None:
        return True

    pos_seq = []

    def inorder_recursion(node, proc):  # 普通的中序
        if node is None:
            proc(None)
            return
        inorder_recursion(node.left, proc)
        proc(node.data)
        inorder_recursion(node.right, proc)

    tmp = root
    inorder_recursion(tmp, pos_seq.append)

    rev_seq = []

    def rev_inorder_recursion(node, proc):  # 从右到左的中序
        if node is None:
            proc(None)
            return
        rev_inorder_recursion(node.right, proc)
        proc(node.data)
        rev_inorder_recursion(node.left, proc)

    tmp = root
    rev_inorder_recursion(tmp, rev_seq.append)
    return pos_seq == rev_seq


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


def serialize_tree(node):  # 要模拟流输入
    if node is None:
        print('$', end=" ")  # 要用流输出
        return
    print(node.data, end=" ")
    serialize_tree(node.left)
    serialize_tree(node.right)


def find_kth_in_tree(node, k):
    """
    from basic_operation import sorted_bin_tree_root as a_root
    find_kth_in_tree(a_root, 0)
    """
    if node is None: return None
    inorde = []

    def inorder_recursion(node):
        if node is None: return
        inorder_recursion(node.left)
        inorde.append(node.data)
        inorder_recursion(node.right)

    inorder_recursion(node)
    if k <= len(inorde):
        return inorde[k - 1]
    else:
        return None


def depth_of_tree(node):  # 第一反应想到的是通过遍历去找到最深的值，但是实现起来有点复杂，用递归会简洁很多。
    if node is None:  # 空的时候深度为0
        return 0
    left = depth_of_tree(node.left)
    right = depth_of_tree(node.right)
    return max(left, right) + 1  # 每一层都会使深度加一,然后最大值就是取在这层之前的最大值


def is_balanced_tree(node):  # 也是后序遍历，在递归的时候传递flag和深度  
    """
    from basic_operation import sorted_bin_tree_root as a_root
    print(is_balanced_tree(a_root))
    """

    def is_balanced_tree_core(node):
        if node is None: return True, 0
        flag1, left = is_balanced_tree_core(node.left)
        flag2, right = is_balanced_tree_core(node.right)
        if flag1 and flag2 and abs(left - right) < 2:
            return True, max(left, right) + 1
        else:
            return False, None

    return is_balanced_tree_core(node)[0]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
