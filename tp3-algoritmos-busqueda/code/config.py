# config.py
import numpy as np

# Configuración global para todos los entornos
CONFIG = {
    "tamaño_mapa": 100,
    "prob_hielo": 0.92,
    "prob_agujero": 0.08,
    "max_pasos": 1000,
    "num_ejecuciones": 30,
    "semillas": list(range(42, 72)),  # 30 semillas diferentes
    "algoritmos": ["random" , "bfs", "dfs", "dfs_limitado" , "costo_uniforme" , "a_star"]
}