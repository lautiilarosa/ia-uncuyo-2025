
from collections import deque


ACTION_DELTAS = {
    0: (0, -1),   # LEFT
    1: (1, 0),    # DOWN
    2: (0, 1),    # RIGHT
    3: (-1, 0)    # UP
}

def idx_to_rc(idx, ncols):
    r = idx // ncols
    c = idx % ncols
    return (r, c)

def rc_to_idx(r, c, ncols):
    return r * ncols + c

def is_traversable_from_desc(desc, r, c):
    return desc[r][c] != 'H'

def neighbors_from_desc(desc, state_idx):
    """
    Devuelve lista de (action, next_idx) para transiciones deterministas (is_slippery=False).
    Ignora movimientos fuera de bounds o hacia 'H'.
    """
    nrows = len(desc)
    ncols = len(desc[0])
    r, c = idx_to_rc(state_idx, ncols)
    neighs = []
    for action, (dr, dc) in ACTION_DELTAS.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < nrows and 0 <= nc < ncols:
            if is_traversable_from_desc(desc, nr, nc):
                neighs.append((action, rc_to_idx(nr, nc, ncols)))
    return neighs

def edge_cost_from_action(action, scenario=1):
    """
    Escenario 1: todo costo 1.
    Escenario 2: left/right = 1, up/down = 10.
    Recibe action como int (0..3).
    """
    if scenario == 1:
        return 1
    else:
        
        if action in (0, 2):  
            return 1
        else:  
            return 10

def reconstruct_path(came_from, start_idx, goal_idx):
    """
    came_from: dict next_idx -> (prev_idx, action)
    devuelve lista de (state_idx) y lista de acciones
    """
    path_states = []
    path_actions = []
    cur = goal_idx
    if cur not in came_from and cur != start_idx:
        return [], []
    while cur != start_idx:
        prev, action = came_from[cur]
        path_states.append(cur)
        path_actions.append(action)
        cur = prev
    path_states.append(start_idx)
    path_states.reverse()
    path_actions.reverse()
    return path_states, path_actions

def manhattan_heuristic(a_idx, b_idx, ncols):
    ar, ac = idx_to_rc(a_idx, ncols)
    br, bc = idx_to_rc(b_idx, ncols)
    return abs(ar - br) + abs(ac - bc)
