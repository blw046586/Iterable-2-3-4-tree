from Node234 import Node234

class Tree234Iterator:
    def __init__(self, root):
        self.stack = []
        self._push_left_path(root)

    def _push_left_path(self, node):
        while node:
            self.stack.append((node, 0))
            node = node.get_child(0)

    def __next__(self):
        if not self.stack:
            raise StopIteration

        node, idx = self.stack.pop()
        key = node.get_key(idx)

        # If more keys in this node, push next key index to stack
        if idx + 1 < node.get_key_count():
            self.stack.append((node, idx + 1))

        # Now handle pushing the next subtree **before** returning the key
        right_child = node.get_child(idx + 1)
        if right_child:
            self._push_left_path(right_child)

        return key
