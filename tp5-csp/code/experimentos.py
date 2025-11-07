import csv
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from csp import NQueensCSP
from backtracking import backtracking_search
from forward_checking import forward_checking_search

def ejecutar_experimentos():
    tamanos = [4, 8, 10]
    algoritmos = {
        "Backtracking": backtracking_search,
        "Forward Checking": forward_checking_search
    }

    resultados = []
    num_semillas = 30

    for n in tamanos:
        for nombre_alg, funcion in algoritmos.items():
            for semilla in range(num_semillas):
                random.seed(semilla)
                csp = NQueensCSP(n)

                inicio = time.time()
                solucion, nodos = funcion(csp)
                fin = time.time()

                tiempo = fin - inicio
                exito = 1 if solucion is not None else 0

                resultados.append({
                    "Algoritmo": nombre_alg,
                    "Tamaño": n,
                    "Semilla": semilla,
                    "Éxito": exito,
                    "Tiempo": tiempo,
                    "Nodos": nodos
                })

   
    with open("resultados.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)

    print("CSV generado: resultados.csv")
    return resultados

def generar_boxplots():
    df = pd.read_csv("resultados.csv")

   
    tamanos = sorted(df["Tamaño"].unique())

    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({
        "figure.figsize": (8, 6),
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11
    })

  
    for n in tamanos:
        subset = df[df["Tamaño"] == n]

    
        fig, ax = plt.subplots()
        subset.boxplot(column="Tiempo", by="Algoritmo", ax=ax, grid=False, patch_artist=True)
        ax.set_title(f"Distribución de tiempos de ejecución ({n} reinas)")
        ax.set_xlabel("Algoritmo")
        ax.set_ylabel("Tiempo (segundos)")
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:.4f}"))
        plt.suptitle("")  
        plt.tight_layout()
        plt.savefig(f"boxplot_tiempos_{n}reinas.png", dpi=300)
        plt.close()

       
        fig, ax = plt.subplots()
        subset.boxplot(column="Nodos", by="Algoritmo", ax=ax, grid=False, patch_artist=True)
        ax.set_title(f"Distribución de nodos explorados ({n} reinas)")
        ax.set_xlabel("Algoritmo")
        ax.set_ylabel("Nodos explorados")
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))  
        plt.suptitle("")
        plt.tight_layout()
        plt.savefig(f"boxplot_nodos_{n}reinas.png", dpi=300)
        plt.close()

    print("Boxplots generados: uno por tamaño de tablero (4, 8, 10).")

if __name__ == "__main__":
    ejecutar_experimentos()
    generar_boxplots()
