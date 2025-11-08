import random
import time
from utils import neighbors_from_desc, reconstruct_path, edge_cost_from_action

def random_search(desc, start_idx, goal_idx, life_limit=1000, scenario=1, seed=None):
    rnd = random.Random(seed)
    t0 = time.time()
    current = start_idx
    came_from = {}
    explored = set([current])
    steps = 0
    while steps < life_limit:
        if current == goal_idx:
            states, actions = reconstruct_path(came_from, start_idx, goal_idx)
            cost = sum(edge_cost_from_action(a, scenario) for a in actions)
            return {'success': True, 'states': states, 'actions': actions, 'cost': cost,
                    'explored': len(explored), 'time': time.time() - t0}
        neighs = neighbors_from_desc(desc, current)
        if not neighs:
            break
        action, nxt = rnd.choice(neighs)
        if nxt not in came_from:
            came_from[nxt] = (current, action)
        explored.add(nxt)
        current = nxt
        steps += 1
    return {'success': False, 'states': None, 'actions': None, 'cost': None,
            'explored': len(explored), 'time': time.time() - t0}
