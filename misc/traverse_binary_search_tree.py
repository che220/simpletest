class Node:
    def __init__(self, data):
        self.data = data
        self.left = self.right = None

def insert_data(node, data):
    if node is None:
        return Node(data)
    else:
        if data <= node.data:
            node.left = insert_data(node.left, data)
        else:
            node.right = insert_data(node.right, data)
    return node

def min_value(node):
    if node is None:
        return None

    c_node = node
    while c_node.left is not None:
        c_node = c_node.left

    return c_node.data

def max_value(node):
    if node is None:
        return None

    c_node = node
    while c_node.right is not None:
        c_node = c_node.right

    return c_node.data

if __name__ == '__main__':
    root = Node(4)
    insert_data(root, 2)
    insert_data(root, 0)
    insert_data(root, 1)
    insert_data(root, 3)
    insert_data(root, 10)
    insert_data(root, 5)

    print(min_value(root))
    print(max_value(root))
