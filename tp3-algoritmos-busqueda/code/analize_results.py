import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Crear carpeta de salida
os.makedirs("plots", exist_ok=True)

# 1. Cargar los datos
df = pd.read_csv("results.csv")

# 2. Filtrar solo las soluciones encontradas
df_solved = df[df["solution_found"] == True]

# 3. Calcular estadísticas
stats = df_solved.groupby("algorithm_name")[["states_n", "actions_count", "actions_cost", "time"]].agg(["mean", "std"])
print("=== Estadísticas (media y desviación estándar) ===")
print(stats)

# 4. Crear boxplots comparativos
metrics = {
    "states_n": "Cantidad de estados explorados",
    "actions_count": "Cantidad de acciones tomadas",
    "actions_cost": "Costo total de las acciones",
    "time": "Tiempo empleado (s)"
}

for metric, label in metrics.items():
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df_solved, x="algorithm_name", y=metric, hue="algorithm_name", palette="pastel", legend=False)
    plt.title(f"Distribución de {label} por algoritmo")
    plt.xlabel("Algoritmo")
    plt.ylabel(label)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    # Guardar gráfico
    plt.savefig(f"plots/{metric}_boxplot.png")
    plt.close()

print("\n✅ Gráficos guardados en la carpeta 'plots/'")
