# Iterable-2-3-4-tree
Overview
In this lab, the Tree234 class is extended to support iteration with a range-based for loop. Iteration support is provided via the implementation of an iterator that can iterate through the tree's keys in ascending order.

An iterator is an object that maintains a pointer to a specific element in a collection and can move to the next element. Ex: A Tree234 iterator points to the tree's minimum key upon construction. The iterator can then move to the second to minimum key, then the third to minimum, and so on. After moving past the tree's last key, the iterator can move no further.


Overview of iterable objects in Python
This lab requires implementation of a Tree234Iterator class that can iterate through all the tree's keys in ascending order via calls to the __next__() method. __next__() returns the tree's next key, or raises a StopIteration exception if no more keys exist.

Python for loops work on any class that implements the __iter__() method to return an iterator. Tree234's __iter__() method has already been implemented to return a Tree234Iterator instance. The returned Tree234Iterator object represents the inclusive starting point of iteration: the tree's minimum key. Tree234's __iter__() method passes the tree's root, a Node234 object, to Tree234Iterator's __init__() method.


Step 1: Inspect the Node234.py file
Inspect the Node234.py file. Node234.py is read-only and has a complete implementation of a Node234 class for a 2-3-4 tree node. Member variables are protected and so must be accessed through the provided getter and setter methods.


Step 2: Inspect the Tree234Iterator.py file
Inspect the Tree234Iterator.py file. The Tree234Iterator class is declared, but required methods are not implemented. The implementation must satisfy the following requirements:

Iteration never changes the tree in any way.
Iteration starts at the tree's minimum key and ends at the maximum.
__init__() executes in worst-case O(log N) time.
__next__() executes in worst-case O(log N) time.
Space complexity is worst-case O(log N).
For simplicity, assume the tree is not changed by an outside source during the iterator's lifetime.


Step 3: Understand requirement implications
To satisfy the requirements, the iterator must maintain a collection of node references. A node exists in the collection only if that node must be revisited at some point in time.

The iterator must visit only the necessary nodes to deliver a key when __next__() is called. "Visiting" a node means calling any of that node's methods. Ex: Suppose an iterator is built for the tree below. Then the iterator's __next__() method is called to return key 5, then again to return key 10, then again to return key 15. The iterator should have only visited the highlighted nodes.

2-3-4 tree with 14 nodes and 19 keys. Root node's keys are 30 and 70. Root's child 0 has keys 10 and 20. Root's child 1 has keys 40, 50, and 60. Root's child 2 has keys 80 and 90. Node (10, 20) has 3 single-keyed children: 5, 15, and 25. Node (40, 50, 60) has 4 single-keyed children: 25, 45, 55, and 65. Node (80, 90) has 3 single-keyed children: 75, 85, and 95.

Step 4: Implement the Tree234Iterator class
Implement the Tree234Iterator to satisfy the complexity requirements mentioned above. Code in main.py adds random keys to a Tree234 object, then tests that the iterator properly iterates through all keys in ascending order. But time and space complexity aren't tested by code in main.py. Rather, main.py only ensures that the iterator properly iterates through all keys.

Most unit tests will fail if the iterator does not properly iterate through all the tree's keys in the correct order. So run code and ensure that the test in main.py passes before submitting code for grading.


Hints
The conceptual description of an iterator mentions that the iterator "references" a key. In the actual implementation, the "reference" to a key is not an int type. The iterator must know if more keys exist in the node, and a direct reference to the key integer itself does not include such information.

