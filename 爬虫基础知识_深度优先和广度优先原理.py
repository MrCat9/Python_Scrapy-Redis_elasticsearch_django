深度优先和广度优先
1. 网站的树结构
2. 深度优先算法和实现-->递归
3. 广度优先算法和实现(按层次遍历)-->队列

网站的url可能会有环路

#coding:gb18030
#深度优先遍历  #递归
def depth_tree(tree_node):
    if tree_node is not None:
        print(tree_node._data)
        if tree_node._left is not None:
            return depth_tree(tree_node._left)
        if tree_node._right is not None:
            return depth_tree(tree_node._right)



list = [1,2,3,4,5,6,7]
print(list)  #[1, 2, 3, 4, 5, 6, 7]
list.append(8)
print(list)  #[1, 2, 3, 4, 5, 6, 7, 8]
print(list.pop(0))  #1
print(list.pop(1))  #3



#coding:gb18030
#广度优先遍历  #队列
def level_queue(root):
    if root is None:
        return
    my_queue = []
    node = root
    my_queue.append(node)
    while my_queue:
        node = my_queue.pop(0)
        print(node.elem)
        if node.lchild is not None:
            my_queue.append(node.lchild)
        if node.rchild is not None:
            my_queue.append(node.rchild)
