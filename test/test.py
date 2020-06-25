class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(object):
    def pathSum(self, root, sum):
        result = []
        self.help(root, sum, [], result)
        return result

    def help(self, root, sum, path, result):
        if root is None:
            return
        # 步骤类似先序遍历
        path.append(root.val)
        # 遍历根节点
        if root.left is None and root.right is None:
            if sum == root.val:
                result.append(list(path))
        # 遍历左子树
        self.help(root.left, sum - root.val, path, result)
        # 遍历右子树
        self.help(root.right, sum - root.val, path, result)
        path.pop()


root = TreeNode(5)
l1 = TreeNode(4)
r1 = TreeNode(8)
root.left = l1
root.right = r1
l2 = TreeNode(11)
r2 = TreeNode(13)
r3 = TreeNode(4)
l1.left = l2
r1.left = r2
r1.right = r3
l3 = TreeNode(7)
l4 = TreeNode(2)
r4 = TreeNode(5)
r5 = TreeNode(1)
l2.left = l3
l2.right = l4
r3.left = r4
r3.right = r5

slu = Solution()

t = slu.pathSum(root, 22)
print(t)

