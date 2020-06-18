# BFS, DFS, IDS, Greedy, A* and Hill-climbing
# B for BFS, D for DFS, I for IDS, G for Greedy, A for A*, H for Hill-climbing.

# Node Class (using code from Piazza provided by Givanna)
class Node:

    def __init__(self, digits, last_digit_changed=None, parent=None, children=None, depth=0, heuristic=None):
        self.digits = digits
        self.last_digit_changed = last_digit_changed
        self.parent = parent
        self.children = children
        self.depth = depth
        self.heuristic = heuristic

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def set_children(self, children):
        self.children = children

    def get_children(self):
        return self.children

    def set_heuristic(self, goal_node, search_strat):
        if search_strat == 'A':
            self.heuristic = self.depth + manhattan(self, goal_node)
        elif search_strat == 'G' or search_strat == 'H':
            self.heuristic = manhattan(self, goal_node)
        else:
            self.heuristic = None

    def generate_children(self, goal_node, search_strat):
        children = []
        for i in range(len(self.digits)):
            if i != self.last_digit_changed and self.digits[i] != '0':
                digits = list(self.digits)
                digits[i] = str(int(digits[i]) - 1)
                child_digits = ''.join(map(str, digits))
                child = Node(digits = child_digits, last_digit_changed=i, parent=self, depth=self.depth + 1)
                child.set_heuristic(goal_node, search_strat)
                #if child not in expanded:
                children.append(child)
            if i != self.last_digit_changed and self.digits[i] != '9':
                digits = list(self.digits)
                digits[i] = str(int(digits[i]) + 1)
                child_digits = ''.join(map(str, digits))
                child = Node(digits = child_digits, last_digit_changed=i, parent=self, depth=self.depth + 1)
                child.set_heuristic(goal_node, search_strat)
                #if child not in expanded:
                children.append(child)
        self.set_children(children)

# Search Strategies

def bfs(start_digits, goal_digits, search_strat, forbidden = []):
    # Convert start and goal into nodes
    start_node = Node(digits = start_digits)
    goal_node = Node(digits = goal_digits)

    fringe = [start_node]
    expanded = []

    while len(fringe) > 0:
        current_node = fringe[0]
        # Check if current node is goal
        if node_is_goal(current_node, start_node, goal_node, expanded) == True:
            return
        # If node is not on forbidden list
        if node_forbidden(current_node, forbidden) == False:
            # Get its children
            current_node.generate_children(goal_node, search_strat)
            children = current_node.get_children()
            # Check if node has same digits and children as any node in expanded list
            if same_node(current_node, expanded) == False:
                expanded.append(current_node)
                fringe.pop(0)
                for child in children:
                    fringe.append(child)
            else:
                fringe.pop(0)
        # If node is on forbidden list, pop from fringe and move to next node
        else:
            fringe.pop(0)
        # Check depth limit
        if check_expanded_limit(expanded):
            return

    print('No solution found.')
    print_list(expanded)

def dfs(start_digits, goal_digits, search_strat, forbidden = []):
    # Convert start and goal into nodes
    start_node = Node(digits = start_digits)
    goal_node = Node(digits = goal_digits)

    fringe = [start_node]
    expanded = []

    while len(fringe) > 0:
        current_node = fringe[0]
        # Check if current node is goal
        if node_is_goal(current_node, start_node, goal_node, expanded) == True:
            return
        # If node is not on forbidden list
        if node_forbidden(current_node, forbidden) == False:
            # Get its children
            current_node.generate_children(goal_node, search_strat)
            current_node_children = current_node.get_children()
            # Check if node has same digits and children as any node in expanded list
            if same_node_dfs(current_node, expanded) == False:
                expanded.append(current_node)
                fringe.pop(0)
                # Add children to fringe
                current_node_children.reverse()
                for child in current_node_children:
                    fringe.insert(0, child)
            else:
                fringe.pop(0)
        # If node is on forbidden list, pop from fringe and move to next node
        else:
            fringe.pop(0)
        # Check depth limit
        if check_expanded_limit(expanded):
            return

    print('No solution found.')
    print_list(expanded)

def dls(start_digits, goal_digits, depth_limit, search_strat, forbidden = []):
    # Convert start and goal into nodes
    start_node = Node(digits = start_digits, depth = 0)
    goal_node = Node(digits = goal_digits)

    fringe = [start_node]
    expanded = []
    found_goal = False

    while len(fringe) > 0:
        current_node = fringe[0]
        # Only consider nodes that are at or below depth limit
        if current_node.depth <= depth_limit:
            # Check if current node is goal
            if node_is_goal_dls(current_node, start_node, goal_node, expanded) == True:
                found_goal = True
                return (found_goal, expanded, current_node)
            # If node is not on forbidden list
            if node_forbidden(current_node, forbidden) == False:
                # Get its children
                current_node.generate_children(goal_node, search_strat)
                current_node_children = current_node.get_children()
                # Check if node has same digits and children as any node in expanded list
                if same_node_dfs(current_node, expanded) == False:
                    expanded.append(current_node)
                    fringe.pop(0)
                    # Add children to fringe
                    current_node_children.reverse()
                    for child in current_node_children:
                        fringe.insert(0, child)
                # If node is on forbidden list, pop from fringe and move to next node
                else:
                    fringe.pop(0)
            # If node has depth > depth limit, pop from fringe
            else:
                fringe.pop(0)
            # Check expanded list limit
            if check_expanded_limit(expanded):
                return
        else:
            fringe.pop(0)
    return (found_goal, expanded, None)

def ids(start_digits, goal_digits, search_strat, forbidden = []):
    start_node = Node(digits = start_digits)
    expanded = []
    found_goal = False
    goal = None
    depth_limit = 0
    while found_goal == False:
        dls_results = dls(start_digits, goal_digits, depth_limit, search_strat, forbidden)
        found_goal = dls_results[0]
        expanded_partial = dls_results[1]
        if check_expanded_limit_ids(expanded):
            trim_length = 1000 - len(expanded)
            del expanded[trim_length:]
            print_list(expanded)
            return
        expanded += expanded_partial
        goal = dls_results[2]
        depth_limit += 1

    if found_goal == True:
        path = find_solution_path(goal, start_node)
        path.reverse()
        print_list(path)
        print_list(expanded)
        return

def greedy(start_digits, goal_digits, search_strat, forbidden = []):
    # Convert start and goal into nodes
    start_node = Node(digits = start_digits)
    goal_node = Node(digits = goal_digits)
    start_node.set_heuristic(goal_node, search_strat)

    fringe = [start_node]
    expanded = []

    # Select node from fringe to expand
    while len(fringe) > 0:
        index = smallest_manhattan(fringe)[0]
        current_node = fringe[index]
        # Check if current node is goal
        if node_is_goal(current_node, start_node, goal_node, expanded) == True:
            return
        # If node is not on forbidden list
        if node_forbidden(current_node, forbidden) == False:
            # Get its children
            current_node.generate_children(goal_node, search_strat)
            children = current_node.get_children()
            # Check if node has same digits and children as any node in expanded list
            if same_node(current_node, expanded) == False:
                expanded.append(current_node)
                fringe.pop(index)
                for child in children:
                    fringe.append(child)
            else:
                fringe.pop(index)
        # If node is on forbidden list, pop from fringe and move to next node
        else:
            fringe.pop(index)
        # Check depth limit
        if check_expanded_limit(expanded):
            return

    print('No solution found.')
    print_list(expanded)

def hill_climbing(start_digits, goal_digits, search_strat, forbidden = []):
    # Convert start and goal into nodes
    start_node = Node(digits = start_digits)
    goal_node = Node(digits = goal_digits)
    start_node.set_heuristic(goal_node, search_strat)

    fringe = [start_node]
    expanded = []
    current_node = start_node

    while len(fringe) > 0:
        if current_node == None:
            print("No solution found.")
            print_list(expanded)
            return
        # Check if current node is goal
        if node_is_goal(current_node, start_node, goal_node, expanded) == True:
            return
        else:
            current_node.generate_children(goal_node, search_strat)
            fringe = current_node.get_children()
            best_child_index, best_child_distance = smallest_manhattan(fringe)
            # If node is not on forbidden list
            if node_forbidden(current_node, forbidden) == False:
                current_node = compare_parent_children(current_node, fringe, goal_node, expanded, forbidden, best_child_index, best_child_distance)
            else:
                fringe.pop(best_child_index)
                best_child_index, best_child_distance = smallest_manhattan(fringe)
                current_node = compare_parent_children(current_node, fringe, goal_node, expanded, forbidden, best_child_index, best_child_distance)
        # Check depth limit
        if check_expanded_limit(expanded):
            return

    print('No solution found.')
    print_list(expanded)

def a_star(start_digits, goal_digits, search_strat, forbidden = []):
    # Convert start and goal into nodes
    start_node = Node(digits = start_digits)
    goal_node = Node(digits = goal_digits)
    start_node.set_heuristic(goal_node, search_strat)

    fringe = [start_node]
    expanded = []

    # Select node from fringe to expand
    while len(fringe) > 0:
        index = smallest_manhattan(fringe)[0]
        current_node = fringe[index]
        # Check if current node is goal
        if node_is_goal(current_node, start_node, goal_node, expanded) == True:
            return
        # If node is not on forbidden list
        if node_forbidden(current_node, forbidden) == False:
            # Get its children
            current_node.generate_children(goal_node, search_strat)
            children = current_node.get_children()
            # Check if node has same digits and children as any node in expanded list
            if same_node(current_node, expanded) == False:
                expanded.append(current_node)
                fringe.pop(index)
                for child in children:
                    fringe.append(child)
            else:
                fringe.pop(index)
        # If node is on forbidden list, pop from fringe and move to next node
        else:
            fringe.pop(index)
        # Check depth limit
        if check_expanded_limit(expanded):
            return

    print('No solution found.')
    print_list(expanded)

# Helper Functions

def compare_parent_children(current_node, children, goal_node, expanded, forbidden, best_child_index, best_child_distance):
    # Check if node has same digits and children as any node in expanded list
    if same_node(current_node, expanded) == False and node_forbidden(current_node, forbidden) == False:
        if current_node.heuristic < best_child_distance:
            expanded.append(current_node)
            return None
        else:
            expanded.append(current_node)
            current_node = children[best_child_index]
            return current_node

def smallest_manhattan(fringe):
    index = None
    smallest_distance = 100 # largest possible distance by Manhattan metric is 27 (for 000 and 999)
    for i in range(len(fringe)):
        distance = fringe[i].heuristic
        if distance <= smallest_distance:
            smallest_distance = distance
            index = i
    return index, smallest_distance

def manhattan(current_node, goal_node):
    current = list(current_node.digits)
    goal = list(goal_node.digits)
    distance = abs(int(current[0]) - int(goal[0])) + abs(int(current[1]) - int(goal[1])) + abs(int(current[2]) - int(goal[2]))
    return distance

def node_is_goal(node, start_node, goal_node, expanded):
    if node.digits == goal_node.digits:
        expanded.append(node)
        path = find_solution_path(node, start_node)
        path.reverse()
        print_list(path)
        print_list(expanded)
        return True

def node_is_goal_dls(node, start_node, goal_node, expanded):
    if node.digits == goal_node.digits:
        expanded.append(node)
        return True

def node_forbidden(node, forbidden):
    is_forbidden = False
    for x in forbidden:
        if node.digits == x:
            is_forbidden = True
    return is_forbidden

def same_node(node, expanded):
    is_same_node = False
    for exp_node in expanded:
        node_children_digits = get_digits(node.get_children())
        exp_node_children_digits = get_digits(exp_node.get_children())
        if node.digits == exp_node.digits and node_children_digits == exp_node_children_digits:
            is_same_node = True
    return is_same_node

def same_node_dfs(node, expanded):
    is_same_node = False
    for exp_node in expanded:
        node_children_digits = get_digits(node.get_children())
        exp_node_children_digits = get_digits(exp_node.get_children())
        exp_node_children_digits.reverse()
        if node.digits == exp_node.digits and node_children_digits == exp_node_children_digits:
            is_same_node = True
    return is_same_node

def get_digits(node_list):
    digits_list = []
    for node in node_list:
        digits = node.digits
        digits_list.append(digits)
    return digits_list

def check_expanded_limit(expanded):
    if len(expanded) >= 1000:
        print("No solution found.")
        print_list(expanded)
        return True

def check_expanded_limit_ids(expanded):
    if len(expanded) >= 1000:
        print("No solution found.")
        return True

def find_solution_path(node, start_node):
    path = [node.digits]
    while node.get_parent() != None:
        parent = node.get_parent()
        path.append(parent.digits)
        node = parent
    return path

def print_list(my_list):
    string = ''
    for elem in my_list:
        if type(elem) == Node:
            string += elem.digits + ','
        elif type(elem) == str:
            string += elem + ','
    print(string[:-1])

# Main Method

import sys

def main(search, file_name):

    file = open(file_name, "r")
    lines = file.readlines()
    start_digits = lines[0].rstrip()
    goal_digits = lines[1].rstrip()
    if len(lines) == 3:
        forbidden = lines[2].rstrip().split(',')
    else:
        forbidden = []

    # Use search arg to decide which search strategy to use
    if search == 'B':
        bfs(start_digits, goal_digits, search, forbidden)
    elif search == 'D':
        dfs(start_digits, goal_digits, search, forbidden)
    elif search == 'I':
        ids(start_digits, goal_digits, search, forbidden)
    elif search == 'G':
        greedy(start_digits, goal_digits, search, forbidden)
    elif search == 'A':
        a_star(start_digits, goal_digits, search, forbidden)
    elif search == 'H':
        hill_climbing(start_digits, goal_digits, search, forbidden)

if __name__ == "__main__":
   main(search=sys.argv[1], file_name=sys.argv[2])
