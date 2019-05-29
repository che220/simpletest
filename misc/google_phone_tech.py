def find_path(num):
    if num == 1:
        return [1]

    path = [num]
    while num > 1:
        num = num // 2
        path.append(num)
    path.append(1)
    return path

def exists(root, path):
    if root is None:
        return False

    if len(path) == 1:
        return True

    c_node = root
    for i in range(len(path)-1, 0, -1):
        idx = path[i]
        if idx // 2 * 2 == idx:
            if c_node.left is None:
                return False
            else:
                c_node = c_node.left
        else:
            if c_node.right is None:
                return False
            else:
                c_node = c_node.right
    return True

if __name__ == '__main__':
    root = 1
    num = input()
    if num < 1:
        print(False)
    else:
        path = find_path(num)
        print(exists(root, path))
