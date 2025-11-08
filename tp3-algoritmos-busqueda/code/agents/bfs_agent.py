
import time
from collections import deque
from utils import neighbors_from_desc, reconstruct_path, edge_cost_from_action

def bfs(desc, start_idx, goal_idx, scenario=1):
    t0 = time.time()
    q = deque([start_idx])
    came_from = {}
    visited = set([start_idx])
    explored = 0
    while q:
        cur = q.popleft()
        explored += 1
        if cur == goal_idx:
            states, actions = reconstruct_path(came_from, start_idx, goal_idx)
            cost = sum(edge_cost_from_action(a, scenario) for a in actions)
            return {'success': True, 'states': states, 'actions': actions, 'cost': cost,
                    'explored': explored, 'time': time.time() - t0}
        for action, nxt in neighbors_from_desc(desc, cur):
            if nxt not in visited:
                visited.add(nxt)
                came_from[nxt] = (cur, action)
                q.append(nxt)
    return {'success': False, 'states': None, 'actions': None, 'cost': None,
            'explored': explored, 'time': time.time() - t0}
