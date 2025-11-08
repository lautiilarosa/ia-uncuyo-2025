import time
import heapq
from utils import neighbors_from_desc, reconstruct_path, edge_cost_from_action, manhattan_heuristic

def a_star(desc, start_idx, goal_idx, scenario=1):
    t0 = time.time()
    ncols = len(desc[0])
    def heuristic(a, b):
        
        return manhattan_heuristic(a, b, ncols) * 1

    frontier = []
    start_h = heuristic(start_idx, goal_idx)
    heapq.heappush(frontier, (start_h, 0, start_idx))
    came_from = {}
    cost_so_far = {start_idx: 0}
    explored = 0
    while frontier:
        _, cur_cost, cur = heapq.heappop(frontier)
        explored += 1
        if cur == goal_idx:
            states, actions = reconstruct_path(came_from, start_idx, goal_idx)
            return {'success': True, 'states': states, 'actions': actions, 'cost': cur_cost,
                    'explored': explored, 'time': time.time() - t0}
        for action, nxt in neighbors_from_desc(desc, cur):
            new_cost = cur_cost + edge_cost_from_action(action, scenario)
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                priority = new_cost + heuristic(nxt, goal_idx)
                came_from[nxt] = (cur, action)
                heapq.heappush(frontier, (priority, new_cost, nxt))
    return {'success': False, 'states': None, 'actions': None, 'cost': None,
            'explored': explored, 'time': time.time() - t0}
