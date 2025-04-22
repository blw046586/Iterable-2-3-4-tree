from Node234 import Node234
from Tree234Iterator import Tree234Iterator

class Tree234:
    # Initializes the tree by assigning the root node reference with None
    def __init__(self):
        self.root = None
    
    def __len__(self):
        return self.get_length()
    
    def alloc_full_node(self, key0, key1, key2, child0, child1, child2, child3):
        new_node = self.alloc_node(key0, child0, child1)
        new_node.set_key(1, key1)
        new_node.set_key(2, key2)
        new_node.set_child(2, child2)
        new_node.set_child(3, child3)
        return new_node
    
    def alloc_node(self, key, child0 = None, child1 = None):
        return Node234(key, child0, child1)
    
    # Returns True if this tree contains the key, False otherwise
    def contains_key(self, key):
        return self.search_recursive(key, self.root) != None
        
    # Fuses a parent node and two children into one node.
    # Precondition: left_node and right_node must have one key each.
    def fuse(self, parent, left_node, right_node):
        if parent is self.root and parent.get_key_count() == 1:
            return self.fuse_root()
        
        left_node_index = parent.get_child_index(left_node)
        middle_key = parent.get_key(left_node_index)
        fused_node = self.alloc_full_node(
            # Keys:
            left_node.get_key(0), middle_key, right_node.get_key(0),
            
            # Children:
            left_node.get_child(0), left_node.get_child(1),
            right_node.get_child(0), right_node.get_child(1)
        )
        key_index = parent.get_key_index(middle_key)
        parent.remove_key(key_index)
        parent.set_child(key_index, fused_node)
        return fused_node
    
    # Fuses the tree's root node with the root's two children.
    # Precondition: Each of the three nodes must have one key each.
    def fuse_root(self):
        old_child0 = self.root.get_child(0)
        old_child1 = self.root.get_child(1)
        self.root.set_key(1, self.root.get_key(0))
        self.root.set_key(0, old_child0.get_key(0))
        self.root.set_key(2, old_child1.get_key(0))
        self.root.set_key_count(3)
        self.root.set_child(0, old_child0.get_child(0))
        self.root.set_child(1, old_child0.get_child(1))
        self.root.set_child(2, old_child1.get_child(0))
        self.root.set_child(3, old_child1.get_child(1))
        return self.root
    
    # Returns the height of this tree
    def get_height(self):
        return Tree234.get_height_recursive(self.root)
    
    @staticmethod
    def get_height_recursive(node):
        if node.get_child(0) is None:
            return 0
        return 1 + Tree234.get_height_recursive(node.get_child(0))
    
    # Searches for, and returns, the minimum key in a subtree. The node
    # argument must not be None.
    @staticmethod
    def get_min_key(node):
        current = node
        while current.get_child(0) != None:
            current = current.get_child(0)
        return current.get_key(0)
    
    # Returns the number of keys in this tree
    def get_length(self):
        count = 0
        nodes = [self.root]
        
        while len(nodes) > 0:
            node = nodes.pop()
            if node != None:
                # Add the number of keys in the node to the count
                count = count + node.get_key_count()
                
                # Push children
                for i in range(4):
                    nodes.append(node.get_child(i))
        
        return count
    
    # Inserts a new key into this tree, provided the tree doesn't already
    # contain the same key. Returns True if the key was inserted successfully,
    # False if the key already exists and so was not inserted.
    def insert(self, key):
        return self.insert_recursive(key, self.root, None)
    
    # Inserts a new key into this tree, provided the tree doesn't already
    # contain the same key. Returns True if the key was inserted successfully,
    # False if the key already exists and so was not inserted.
    def insert_recursive(self, key, node, node_parent):
        # Special case for empty tree
        if self.root == None:
            self.root = self.alloc_node(key)
            return True
        
        # Check for duplicate key
        if node.has_key(key):
            # Duplicate keys are not allowed
            return False
        
        # Preemptively split full nodes
        if node.get_key_count() == 3:
            node = self.split(node, node_parent)
        
        # If node is not a leaf, recursively insert into child subtree
        if not node.is_leaf():
            return self.insert_recursive(key, node.next_node(key), node)
        
        # key can be inserted into leaf node
        node.insert_key_with_children(key, None, None)
        return True
    
    # Finds and replaces one key with another. The replacement key must be
    # a key that can be used as a replacement without violating any of the
    # 2-3-4 tree rules.
    def key_swap(self, node, existing_key, replacement_key):
        if node == None:
            return False
        
        key_index = node.get_key_index(existing_key)
        if key_index == -1:
            next = node.next_node(existing_key)
            return self.key_swap(next, existing_key, replacement_key)
        
        node.set_key(key_index, replacement_key)
        return True
    
    # Rotates or fuses to add 1 or 2 additional keys to a node with 1 key
    def merge(self, node, node_parent):
        # Get references to node's siblings
        node_index = node_parent.get_child_index(node)
        left_sibling = node_parent.get_child(node_index - 1)
        right_sibling = node_parent.get_child(node_index + 1)
        
        # Check siblings for a key that can be transferred
        if left_sibling != None and left_sibling.get_key_count() >= 2:
            self.rotate_right(left_sibling, node_parent)
        elif right_sibling != None and right_sibling.get_key_count() >= 2:
            self.rotate_left(right_sibling, node_parent)
        else: # fuse
            if left_sibling == None:
                node = self.fuse(node_parent, node, right_sibling)
            else:
                node = self.fuse(node_parent, left_sibling, node)
        
        return node
    
    def print_keys(self, separator = ","):
        self.print_recursive(self.root, separator, False)
    
    # Prints all keys in the tree rooted at node in ascending order
    @staticmethod
    def print_recursive(node, separator, printed_first):
        if node == None:
            return printed_first
        
        for i in range(node.get_key_count()):
            # First print the child subtree to the left of the key
            printed_first = Tree234.print_recursive(node.get_child(i), separator, printed_first)
         
            # If the first key was already printed then print the separator
            if printed_first:
                print(separator, end="")
            else:
                printed_first = True
            
            # Print the key at index i
            print(node.get_key(i), end="")
        
        # Print the final subtree to the right of the node's last key
        Tree234.print_recursive(node.get_child(node.get_key_count()),
            separator, printed_first)
        
        return printed_first
    
    # Finds and removes the specified key from this tree
    def remove(self, key):
        # Special case for tree with 1 key
        if self.root.is_leaf() and self.root.get_key_count() == 1:
            if self.root.get_key(0) == key:
                self.root = None
                return True
            return False
        
        current_parent = None
        current = self.root
        while current != None:
            # Merge any non-root node with 1 key
            if current.get_key_count() == 1 and current is not self.root:
                current = self.merge(current, current_parent)
            
            # Check if current node contains key
            key_index = current.get_key_index(key)
            if key_index != -1:
                if current.is_leaf():
                    current.remove_key(key_index)
                    return True
                # The node contains the key and is not a leaf, so the key is
                # replaced with the successor
                tmp_child = current.get_child(key_index + 1)
                tmp_key = Tree234.get_min_key(tmp_child)
                self.remove(tmp_key)
                self.key_swap(self.root, key, tmp_key)
                return True
            
            # Current node does not contain key, so continue down tree
            current_parent = current
            current = current.next_node(key)
        
        # key not found
        return False
    
    def rotate_left(self, node, node_parent):
        # Get the node's left sibling
        node_index = node_parent.get_child_index(node)
        left_sibling = node_parent.get_child(node_index - 1)
        
        # Append the key to the left sibling
        left_sibling.insert_key_with_children(
            node_parent.get_key(node_index - 1),
            left_sibling.get_child(left_sibling.get_key_count()),
            node.get_child(0))
        
        # Replace the parent's key that was appended to the left sibling
        node_parent.set_key(node_index - 1, node.get_key(0))
        
        # Remove key 0 and child 0 from node
        node.remove_key(0)
    
    def rotate_right(self, node, node_parent):
        # Get the node's right sibling
        node_index = node_parent.get_child_index(node)
        right_sibling = node_parent.get_child(node_index + 1)
        
        # Get the child from the node that will move to the sibling
        node_rightmost_child = node.get_child(node.get_key_count())
        
        # Get the key from the parent that move into the right sibling
        key_for_right_sibling = node_parent.get_key(node_index)
        
        # Insert new key and child into right sibling
        right_sibling.insert_key_with_children(key_for_right_sibling,
            node_rightmost_child, right_sibling.get_child(0))
        
        # Replace the parent's key that moved to the right sibling
        node_parent.set_key(node_index, node.get_key(node.get_key_count() - 1))
        
        # Remove node's rightmost key and child
        node.set_child(node.get_key_count(), None)
        node.set_key_count(node.get_key_count() - 1)
    
    # Searches this tree for the specified key. If found, the node containing
    # the key is returned. Otherwise None is returned.
    def search(self, key):
        return self.search_recursive(key, self.root)
    
    # Recursive helper method for search
    def search_recursive(self, key, node):
        if node == None:
            return None
        
        # Check if the node contains the key
        if node.has_key(key):
            return node
        
        # Recursively search the appropriate subtree
        return self.search_recursive(key, node.next_node(key))
    
    # Splits a full node, moving the middle key up into the parent node.
    # Precondition: node_parent has one or two keys.
    def split(self, node, node_parent):
        split_left = self.alloc_node(node.get_key(0), node.get_child(0), node.get_child(1))
        split_right = self.alloc_node(node.get_key(2), node.get_child(2), node.get_child(3))
        
        if node_parent != None:
            # Split non-root node
            node_parent.insert_key_with_children(node.get_key(1), split_left, split_right)
        else:
            # Split root node
            node_parent = self.alloc_node(node.get_key(1), split_left, split_right)
            self.root = node_parent
        
        return node_parent
    
    # Added to support iteration through the trees keys with a for loop
    def __iter__(self):
        return Tree234Iterator(self.root)