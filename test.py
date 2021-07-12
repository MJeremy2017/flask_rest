from collections import defaultdict


class Node:
    def __init__(self):
        self.val = 0


class Tree:
    def __init__(self):
        self.child = defaultdict(Node)


if __name__ == '__main__':
    tree = Tree()
    n1 = tree.child.get('child1')  # get returns None
    n2 = tree.child['child1']  # [] returns an Object
    print(n1, n2)