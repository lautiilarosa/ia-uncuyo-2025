import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

def cargar_datos(csv_file="resultados_n_reinas.csv"):
    df = pd.read_csv(csv_file)
    # Convertir 'best_solution' de string a lista
    df["best_solution"] = df["best_solution"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith("[") else x
    )
    return df

def estadisticas(df):
    resumen = df.groupby(["algorithm_name", "size"]).agg(
        porcentaje_optimos=("H", lambda x: (x==0).sum()/len(x)*100),
        H_mean=("H", "mean"),
        H_std=("H", "std"),
        time_mean=("time", "mean"),
        time_std=("time", "std"),
        states_mean=("states", "mean"),
        states_std=("states", "std")
    ).reset_index()
    print(resumen)

def generar_boxplot(df, size, y_col, titulo, log_scale=False):
    plt.figure(figsize=(8,5))
    subset = df[df["size"] == size]
    sns.boxplot(data=subset, x="algorithm_name", y=y_col)
    plt.title(f"{titulo} - {size} reinas")
    plt.xlabel("Algoritmo")
    plt.ylabel(y_col)
    if log_scale:
        plt.yscale("log")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(f"boxplot_{y_col}_{size}.png", dpi=300)
    plt.close()

def graficar_todos_boxplots(df):
    tamaños = sorted(df["size"].unique())
    for t in tamaños:
        generar_boxplot(df, t, "H", "Distribución de H()")
        generar_boxplot(df, t, "states", "Estados explorados", log_scale=True)
        generar_boxplot(df, t, "time", "Tiempo de ejecución", log_scale=True)
    print("\n✅ Gráficos guardados por tamaño y métrica.")

def graficar_evolucion_H(H_history, algoritmo, size):
    """
    Grafica la evolución de H() a lo largo de las iteraciones
    para una única ejecución.
    """
    plt.figure(figsize=(8,5))
    plt.plot(range(len(H_history)), H_history, marker="o", linewidth=1.8)
    plt.xlabel("Iteración")
    plt.ylabel("H()")
    plt.title(f"Evolución de H() - {algoritmo} ({size} reinas)")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"H_evolucion_{algoritmo}_{size}.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    df = cargar_datos()
    estadisticas(df)
    graficar_todos_boxplots(df)
