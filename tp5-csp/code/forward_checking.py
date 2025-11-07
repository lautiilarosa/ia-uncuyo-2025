import random
import copy
from csp import NQueensCSP

def forward_checking_search(csp):
    assignment = [None] * csp.n
    domains = copy.deepcopy(csp.domains)
    nodes_explored = [0]
    if forward_check(assignment, 0, domains, csp, nodes_explored):
        return assignment, nodes_explored[0]
    return None, nodes_explored[0]

def forward_check(assignment, col, domains, csp, nodes_explored):
    if col == csp.n:
        return True

   
    values = list(domains[col])
    random.shuffle(values)

    for row in values:
        nodes_explored[0] += 1
        if csp.is_consistent(assignment, col, row):
            assignment[col] = row
            new_domains = copy.deepcopy(domains)
            consistent = True
            for future_col in range(col + 1, csp.n):
                new_domains[future_col] = [
                    r for r in new_domains[future_col]
                    if csp.is_consistent(assignment, future_col, r)
                ]
                if not new_domains[future_col]:
                    consistent = False
                    break
            if consistent and forward_check(assignment, col + 1, new_domains, csp, nodes_explored):
                return True
            assignment[col] = None
    return False
