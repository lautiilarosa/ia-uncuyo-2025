import time
from utils import neighbors_from_desc, reconstruct_path, edge_cost_from_action

def depth_limited_search(desc, start_idx, goal_idx, limit=50, scenario=1):
    t0 = time.time()
    explored = set()
    came_from = {}

    def dls(node, depth, visited):
        explored.add(node)
        if node == goal_idx:
            return True
        if depth == 0:
            return False
        for action, nxt in neighbors_from_desc(desc, node):
            if nxt not in visited:
                visited.add(nxt)
                came_from[nxt] = (node, action)
                found = dls(nxt, depth - 1, visited)
                if found:
                    return True
                # backtrack
                visited.remove(nxt)
                came_from.pop(nxt, None)
        return False

    found = dls(start_idx, limit, set([start_idx]))
    t = time.time() - t0
    if found:
        states, actions = reconstruct_path(came_from, start_idx, goal_idx)
        cost = sum(edge_cost_from_action(a, scenario) for a in actions)
        return {'success': True, 'states': states, 'actions': actions, 'cost': cost,
                'explored': len(explored), 'time': t}
    else:
        return {'success': False, 'states': None, 'actions': None, 'cost': None,
                'explored': len(explored), 'time': t}
