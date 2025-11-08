import time
import heapq
from utils import neighbors_from_desc, reconstruct_path, edge_cost_from_action

def uniform_cost_search(desc, start_idx, goal_idx, scenario=1):
    t0 = time.time()
    frontier = []
    heapq.heappush(frontier, (0, start_idx))
    came_from = {}
    cost_so_far = {start_idx: 0}
    explored = 0
    while frontier:
        cur_cost, cur = heapq.heappop(frontier)
        explored += 1
        if cur == goal_idx:
            states, actions = reconstruct_path(came_from, start_idx, goal_idx)
            return {'success': True, 'states': states, 'actions': actions, 'cost': cur_cost,
                    'explored': explored, 'time': time.time() - t0}
        for action, nxt in neighbors_from_desc(desc, cur):
            new_cost = cur_cost + edge_cost_from_action(action, scenario)
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                came_from[nxt] = (cur, action)
                heapq.heappush(frontier, (new_cost, nxt))
    return {'success': False, 'states': None, 'actions': None, 'cost': None,
            'explored': explored, 'time': time.time() - t0}
