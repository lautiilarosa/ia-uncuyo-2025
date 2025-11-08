import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map

def create_environment(size=100, p=0.92, seed=None):
    """
    Genera un entorno FrozenLake determinista (is_slippery=False)
    de tamaño `size x size` con probabilidad `p` de ser 'F' (frozen).
    Devuelve (env, desc) donde desc es la lista de strings del mapa.
    """
    random_map = generate_random_map(size=size, p=p, seed=seed)
    env = gym.make("FrozenLake-v1", desc=random_map, is_slippery=False)
    return env, random_map

def print_environment(desc):
    for row in desc:
        print(row)
