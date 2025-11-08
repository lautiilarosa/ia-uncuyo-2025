import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

def analizar_resultados():
    # --- Cargar CSV ---
    df = pd.read_csv("resultados_n_reinas.csv")

    # --- Convertir la columna 'best_solution' de string a lista ---
    # (solo si no está vacía o mal formateada)
    df["best_solution"] = df["best_solution"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith("[") else x
    )

    # --- i) Porcentaje de soluciones óptimas (H == 0) ---
    porcentaje_optimos = (
        df.groupby(["algorithm_name", "size"])["H"]
        .apply(lambda x: (x == 0).sum() / len(x) * 100)
        .reset_index(name="porcentaje_optimos")
    )

    # --- ii) H promedio y desviación estándar ---
    H_stats = df.groupby(["algorithm_name", "size"])["H"].agg(["mean", "std"]).reset_index()

    # --- iii) Tiempo promedio y desviación estándar ---
    time_stats = df.groupby(["algorithm_name", "size"])["time"].agg(["mean", "std"]).reset_index()

    # --- iv) Estados promedio y desviación estándar ---
    states_stats = df.groupby(["algorithm_name", "size"])["states"].agg(["mean", "std"]).reset_index()

    # --- Mostrar resumen por consola ---
    print("\n📈 Porcentaje de soluciones óptimas:")
    print(porcentaje_optimos)
    print("\n📊 H promedio y desviación estándar:")
    print(H_stats)
    print("\n⏱ Tiempo promedio y desviación estándar:")
    print(time_stats)
    print("\n🔁 Estados promedio y desviación estándar:")
    print(states_stats)

    # --- Graficar Boxplots por tamaño de tablero ---
    sns.set(style="whitegrid", palette="muted", font_scale=1.1)
    tamaños = sorted(df["size"].unique())

    # --- Boxplot de H() ---
    for t in tamaños:
        plt.figure(figsize=(8, 5))
        subset = df[df["size"] == t]
        sns.boxplot(data=subset, x="algorithm_name", y="H")
        plt.title(f"Distribución de H() - {t} reinas")
        plt.xlabel("Algoritmo")
        plt.ylabel("Valor de H()")
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.savefig(f"boxplot_H_{t}.png", dpi=300)
        plt.close()

    # --- Boxplot de tiempos ---
    for t in tamaños:
        plt.figure(figsize=(8, 5))
        subset = df[df["size"] == t]
        sns.boxplot(data=subset, x="algorithm_name", y="time")
        plt.title(f"Tiempo de ejecución - {t} reinas")
        plt.xlabel("Algoritmo")
        plt.ylabel("Tiempo (s)")
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.savefig(f"boxplot_time_{t}.png", dpi=300)
        plt.close()

    # --- Boxplot de estados explorados ---
    for t in tamaños:
        plt.figure(figsize=(8, 5))
        subset = df[df["size"] == t]
        sns.boxplot(data=subset, x="algorithm_name", y="states")
        plt.title(f"Estados explorados - {t} reinas")
        plt.xlabel("Algoritmo")
        plt.ylabel("Cantidad de estados")
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.savefig(f"boxplot_states_{t}.png", dpi=300)
        plt.close()

    print("\n✅ Gráficos guardados por tamaño de tablero:")
    print("   → boxplot_H_[size].png")
    print("   → boxplot_time_[size].png")
    print("   → boxplot_states_[size].png")


def graficar_evolucion_H(H_history, algoritmo, size):
    """
    Grafica la evolución de H() a lo largo de las iteraciones
    para una única ejecución (inciso 6 del trabajo).
    """
    plt.figure(figsize=(8, 5))
    plt.plot(range(len(H_history)), H_history, marker="o", linewidth=1.8)
    plt.xlabel("Iteración")
    plt.ylabel("H()")
    plt.title(f"Evolución de H() - {algoritmo} ({size} reinas)")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"H_evolucion_{algoritmo}_{size}.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    analizar_resultados()
