"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""
import itertools
import logging
import random
from collections import deque
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)

    node_right = get_tree(max_depth - 1, level=level + 1)

    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def place_node(root_node, new_node):
    if isinstance(root_node.left, int):
        if root_node.left == new_node.val:
            root_node.left = new_node
    elif root_node.left is BinaryTreeNode:
        new_root_node = BinaryTreeNode(root_node.left)
        place_node(new_root_node.left, new_node)
    if isinstance(root_node.right, int):
        if root_node.right == new_node.val:
            root_node.right = new_node
    elif root_node.right is BinaryTreeNode:
        new_root_node = BinaryTreeNode(root_node.right)
        place_node(new_root_node.right, new_node)


def formation_node(root_node, node_val, node_side, next_node_val):
    if root_node.val == node_val:
        if node_side == 'left':
            root_node.left = next_node_val
        else:
            root_node.right = next_node_val
    elif root_node.left:
        if isinstance(root_node.left, BinaryTreeNode):
            formation_node(root_node.left, node_val, node_side, next_node_val)
    elif root_node.right:
        if isinstance(root_node.right, BinaryTreeNode):
            formation_node(root_node.right, node_val, node_side, next_node_val)


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    with open(path_to_log_file, 'r') as log_file:
        records = log_file.readlines()
        start_val = records[0].find('[')
        finish_val = records[0].find(']')
        node_val = int(records[0][start_val + 1: finish_val])
        left = None
        right = None
        tree = BinaryTreeNode(node_val, left, right)
        for record in range(1, len(records)):
            if records[record].startswith('INFO'):
                start_val = records[record].find('[')
                finish_val = records[record].find(']')
                node_val = int(records[record][start_val + 1: finish_val])
                new_node = BinaryTreeNode(node_val, left, right)
                place_node(tree, new_node)
            else:
                start_val = records[record].find('[')
                finish_val = records[record].find(']')
                node_val = int(records[record][start_val + 1: finish_val])
                start_side = records[record].find('>')
                finish_side = records[record].find(' ', start_side + 2)
                node_side = records[record][start_side + 2: finish_side]
                start_val = records[record].rfind('[')
                finish_val = records[record].rfind(']')
                next_node_val = int(records[record][start_val + 1: finish_val])
                formation_node(tree, node_val, node_side, next_node_val)
    return tree


if __name__ == "__main__":
    restore_tree('hw_8_walk_log_4.txt')
    # logging.basicConfig(
    #         level=logging.DEBUG,
    #         format="%(levelname)s:%(message)s",
    #         filename="hw_8_walk_log_4.txt",
    # )
    #
    # root = get_tree(7)
    #
    # walk(root)
