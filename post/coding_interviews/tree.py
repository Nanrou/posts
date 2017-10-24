class BinTreeNode:
    """ 普通二叉数结点的定义 """

    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


def build_bin_tree(preorder, inorder):
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


if __name__ == '__main__':
    from basic_operation import preorder

    root = build_bin_tree([1, 2, 4, 7, 3, 5, 6, 8], [4, 7, 2, 1, 5, 3, 8, 6])
    preorder(root, lambda x: print(x, end=" "))
