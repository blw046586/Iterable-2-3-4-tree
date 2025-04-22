# Node234 class - represents a node in a 2-3-4 tree
class Node234:
    # Constructs a Node234 object from a key and two optional child references
    def __init__(self, key0, child0 = None, child1 = None):
        self.keys = [key0, 0, 0]
        self.key_count = 1
        self.children = [child0, child1, None, None]
    
    # If child_index is >= 0 and <= key_count then the child at child_index is
    # returned. Otherwise None is returned.
    def get_child(self, child_index):
        if child_index >= 0 and child_index <= self.key_count:
            return self.children[child_index]
        return None
    
    # Returns 0, 1, 2, or 3 if the child argument is this node's child 0,
    # child 1, child 2, or child 3, respectively.
    # Returns -1 if the child argument is not a child of this node.
    def get_child_index(self, child):
        for i in range(4):
            if self.children[i] is child:
                return i
        return -1
    
    # Returns the key at key_index
    def get_key(self, key_index):
        return self.keys[key_index]
    
    # Returns the number of keys in this node, which will be 1, 2, or 3
    def get_key_count(self):
        return self.key_count
    
    # Returns the index of the key within this node, or -1 if this node does
    # not contain the key.
    def get_key_index(self, key):
        for i in range(self.key_count):
            if self.keys[i] == key:
                return i
        return -1
    
    # Returns True if this node has the specified key, False otherwise
    def has_key(self, key):
        for i in range(self.key_count):
            if self.keys[i] == key:
                return True
        return False
    
    # Inserts a new key into the proper location in this node, and assigns the
    # children on either side of the inserted key.
    # Precondition: This node's key count is <= 2.
    def insert_key_with_children(self, key, left_child, right_child):
        if key < self.keys[0]:
            self.keys[2] = self.keys[1]
            self.keys[1] = self.keys[0]
            self.keys[0] = key
            self.children[3] = self.children[2]
            self.children[2] = self.children[1]
            self.children[1] = right_child
            self.children[0] = left_child
        elif self.key_count == 1 or key < self.keys[1]:
            self.keys[2] = self.keys[1]
            self.keys[1] = key
            self.children[3] = self.children[2]
            self.children[2] = right_child
            self.children[1] = left_child
        else:
            self.keys[2] = key
            self.children[3] = right_child
            self.children[2] = left_child
        self.key_count += 1
    
    # Returns True if this node is a leaf, False otherwise
    def is_leaf(self):
        return self.children[0] is None
    
    # Returns the child of this node that must be visited next in the traversal
    # to find the specified key
    def next_node(self, key):
        i = 0
        while i < self.key_count:
            if key < self.keys[i]:
                return self.children[i]
            i += 1
        return self.children[i]
    
    # Removes key 0, 1, or 2 from this node, if key_index is 0, 1, or 2,
    # respectively. Other keys and children are shifted as needed.
    def remove_key(self, key_index):
        if key_index == 0:
            self.keys[0] = self.keys[1]
            self.keys[1] = self.keys[2]
            self.children[0] = self.children[1]
            self.children[1] = self.children[2]
            self.children[2] = self.children[3]
            self.children[3] = None
            self.key_count -= 1
        elif key_index == 1:
            self.keys[1] = self.keys[2]
            self.children[2] = self.children[3]
            self.children[3] = None
            self.key_count -= 1
        elif key_index == 2:
            self.children[3] = None
            self.key_count -= 1
    
    # Sets a child by index
    def set_child(self, child_index, child):
        self.children[child_index] = child
    
    # Sets a key by index
    def set_key(self, key_index, key_value):
        self.keys[key_index] = key_value
    
    # Sets this node's key count
    def set_key_count(self, new_key_count):
        self.key_count = new_key_count