import random
from Tree234 import Tree234

def main():
    # Create a new Tree234 instance
    tree = Tree234()

    # Generate and insert random integers
    expected = []
    added = set()
    while len(expected) < 20:
        random_integer = random.randint(100, 999)
        if random_integer not in added:
            added.add(random_integer)
            expected.append(random_integer)
            tree.insert(random_integer)
    expected.sort()

    # Build the actual vector of integers by iterating through the tree. Keep
    # track of the number of iterations and if more iterations occur than
    # expected, then stop.
    actual = []
    iteration_count = 0
    for actual_int in tree:
        actual.append(actual_int)
        iteration_count += 1
        
        # If this iteration exceeded the expected number of iterations then
        # print a failure message
        if iteration_count > len(expected):
            print(f"FAIL: More than the expected {len(expected)} ", end="")
            print("iterations occurred.")
            return
    # Print the pass or fail messsage
    print("PASS" if (expected == actual) else "FAIL", end="")
    print(": Iteration through tree's keys:")
    print("  Actual:   " + str(actual))
    print("  Expected: " + str(expected))

main()