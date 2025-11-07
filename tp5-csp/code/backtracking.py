import random
from csp import NQueensCSP

def backtracking_search(csp):
    assignment = [None] * csp.n
    nodes_explored = [0]
    if backtrack(assignment, 0, csp, nodes_explored):
        return assignment, nodes_explored[0]
    return None, nodes_explored[0]

def backtrack(assignment, col, csp, nodes_explored):
    if col == csp.n:
        return True

    
    values = list(csp.domains[col])
    random.shuffle(values)

    for row in values:
        nodes_explored[0] += 1
        if csp.is_consistent(assignment, col, row):
            assignment[col] = row
            if backtrack(assignment, col + 1, csp, nodes_explored):
                return True
            assignment[col] = None
    return False
