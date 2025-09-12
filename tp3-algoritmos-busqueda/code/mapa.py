import gymnasium as gym
import numpy as np

def generar_mapa(tamaño : int = 100,prob_hole : int = 0.08) -> list[str]:
        """
        Generamos el mapa de 100x100 con probabilidad de agujero de un 8% y el 92% de hielo
        """ 

        map = np.full((tamaño,tamaño),"F",dtype="<U1")
        for i in range(tamaño):
            for j in range(tamaño):
                if np.random.random() < prob_hole:
                    map[i,j] = "H"
    

        map[0,0] = "S"
        map[tamaño-1,tamaño-1] = "G"

        return [''.join(fila) for fila in map]




