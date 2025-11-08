# main.py
import os
from env_generator import create_environment, print_environment
from metrics_and_plots import save_results_csv, make_boxplots

# agentes
from agents.random_agent import random_search
from agents.bfs_agent import bfs
from agents.dfs_agent import dfs
from agents.dls_agent import depth_limited_search
from agents.ucs_agent import uniform_cost_search
from agents.astar_agent import a_star

# parámetros
NUM_ENVS = 30
SIZE = 100
P_FROZEN = 0.92
SEED_BASE = 1000
LIFE_LIMIT = 1000

ALGORITHMS = [
    ('random', None),
    ('bfs', None),
    ('dfs', None),
    ('dls50', 50),
    ('dls75', 75),
    ('dls100', 100),
    ('ucs', None),
    ('astar', None)
]

RESULTS_DIR = 'results'
os.makedirs(RESULTS_DIR, exist_ok=True)

def run_experiments(num_envs=NUM_ENVS, scenario=1, seed_base=SEED_BASE):
    rows = []
    for i in range(num_envs):
        seed = seed_base + i
        env, desc = create_environment(size=SIZE, p=P_FROZEN, seed=seed)
        nrows = len(desc)
        ncols = len(desc[0])
        start_idx = 0  
        goal_idx = nrows * ncols - 1  

     
        if i == 0:
            print("Ejemplo de entorno (desc):")
            print_environment(desc)

        for alg_name, param in ALGORITHMS:
            if alg_name == 'random':
                res = random_search(desc, start_idx, goal_idx, life_limit=LIFE_LIMIT, scenario=scenario, seed=seed)
            elif alg_name == 'bfs':
                res = bfs(desc, start_idx, goal_idx, scenario=scenario)
            elif alg_name == 'dfs':
                res = dfs(desc, start_idx, goal_idx, scenario=scenario)
            elif alg_name.startswith('dls'):
                limit = param
                res = depth_limited_search(desc, start_idx, goal_idx, limit=limit, scenario=scenario)
            elif alg_name == 'ucs':
                res = uniform_cost_search(desc, start_idx, goal_idx, scenario=scenario)
            elif alg_name == 'astar':
                res = a_star(desc, start_idx, goal_idx, scenario=scenario)
            else:
                raise ValueError("Alg desconocido")
            
            if res['success'] and res['actions'] is not None and len(res['actions']) > LIFE_LIMIT:
                res['success'] = False
                res['states'] = None
                res['actions'] = None
                res['cost'] = None
            rows.append({
                'env_idx': i,
                'seed': seed,
                'algorithm': alg_name,
                'scenario': scenario,
                'success': res['success'],
                'explored': res['explored'],
                'actions': len(res['actions']) if res['actions'] else None,
                'cost': res['cost'],
                'time': res['time']
            })
    return rows

if __name__ == '__main__':
    all_rows = []

    # Escenario 1
    print("Corriendo escenario 1 (coste 1 por acción)...")
    rows1 = run_experiments(num_envs=NUM_ENVS, scenario=1, seed_base=SEED_BASE)
    all_rows.extend(rows1)

    # Escenario 2
    print("Corriendo escenario 2 (LR=1, UD=10)...")
    rows2 = run_experiments(num_envs=NUM_ENVS, scenario=2, seed_base=SEED_BASE + 1000)
    all_rows.extend(rows2)

    # Guardamos todo en un solo CSV
    df = save_results_csv(all_rows, os.path.join(RESULTS_DIR, 'results.csv'))

    # Generamos boxplots 
    make_boxplots(df, out_dir=os.path.join(RESULTS_DIR, 'figs_all'))

