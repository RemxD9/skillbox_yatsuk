class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# номер узла, его потомки
def restore_tree(log_path):
    node_map = {}

    with open(log_path, 'r') as log_file:
        for line in log_file:
            node_value, left_value, right_value = map(int, line.strip().split())
            node = BinaryTreeNode(node_value)
            node_map[node_value] = node

            if left_value != -1:
                node.left = BinaryTreeNode(left_value)
            if right_value != -1:
                node.right = BinaryTreeNode(right_value)

    for node_value, node in node_map.items():
        if node.left:
            node.left = node_map[node.left.value]
        if node.right:
            node.right = node_map[node.right.value]

    root = node_map[1]
    return root


root = restore_tree('Tree.txt')
print(f'Корень дерева: {root.value}')
