import gymnasium as gym
from gymnasium import wrappers
import pygame as pg

env = gym.make("FrozenLake-v1", render_mode='human', is_slippery=False)
print("Número de estados: ",env.observation_space.n)
print("Número de acciones:",env.action_space.n)

print("")

state = env.reset()
print("Posici ́on inicial del agente:", state[0])
done = truncated = False
i=0
while not (done or truncated):
    action = env.action_space.sample()
    i+=1
    # Acci ́on aleatoria
    next_state, reward, done, truncated, _ = env.step(action)
    print(f"Acci ́on: {action}, Nuevo estado: {next_state}, Recompensa: {reward}")
    if not reward == 1.0:
        print(f"¿Gano? (encontro el objetivo): False")
        print(f"¿Perdio? (se cayo): {done}")
        print(f"¿Freno? (alcanzo el maximo de pasos posible): {truncated}\n")
    else:
        print(f"¿Gano? (encontro el objetivo): {done}")
    state = next_state






