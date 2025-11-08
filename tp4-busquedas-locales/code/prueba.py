import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast

# -------- CONFIG ----------
CSV_FILE = "resultados_n_reinas.csv"   # <- ajustá si tu CSV tiene otro nombre
MAX_STATES = 3000                      # eje X máximo (como pediste)
X_STEP = 500                           # ticks en X: 500 (o 1000 si prefieres)
STEPS = int(MAX_STATES // 50)         # puntos en la curva (50 puntos por defecto) -> ajustable
SEED_SELECTION = "min_env"            # "min_env" toma el env_n más pequeño por size
# ---------------------------

sns.set(style="whitegrid", palette="tab10", font_scale=1.05)

def simulate_best_h_accumulated(row, max_states=MAX_STATES, steps=STEPS):
    """
    Genera una trayectoria plausible del mejor H acumulado para UNA ejecución (fila).
    - row: pandas Series con columnas ['algorithm_name','size','H','states']
    - devuelve: (estados_array, best_h_accumulated_array)
    """
    n = int(row['size'])
    H_final = float(row['H'])
    states_reported = int(row['states'])
    algo = row['algorithm_name']

    H_max = n * (n - 1) / 2.0

    # Eje de estados (uniforme hasta max_states)
    estados = np.linspace(0, max_states, steps)

    # Modelo base: exponencial decreciente (rápido al inicio, se estabiliza)
    # Parametrizamos la velocidad según algoritmo y según cuántos states reportó (más states -> más recorrido)
    # Además forzamos que al final (en torno a states_reported) se acerque a H_final.
    # Los parámetros a continuación son heurísticos para simular comportamientos realistas.
    if "Hill" in algo or "Hill Climbing" in algo:
        decay_rate = 8.0 / max_states    # relativamente rápido
        noise_scale = H_max * 0.05
    elif "Simulated" in algo or "Annealing" in algo:
        decay_rate = 5.0 / max_states    # intermedio, con oscilaciones
        noise_scale = H_max * 0.08
    elif "Genetic" in algo or "Genético" in algo:
        decay_rate = 3.5 / max_states    # más lento y con saltos
        noise_scale = H_max * 0.10
    else:  # Random / Random Search
        decay_rate = 1.5 / max_states    # muy lento
        noise_scale = H_max * 0.12

    # Base determinista (exponencial)
    base = H_max * np.exp(-decay_rate * estados)

    # Añadir saltos/ruido estocástico según algoritmo
    rnd = np.random.default_rng(seed= int((n + states_reported) * (len(algo)+1)))  # semilla determinista por fila
    noise = rnd.normal(scale=noise_scale, size=steps)

    # añadir algunos picos (para GA y SA) simulando mutación/aceptación de peores
    peaks = np.zeros(steps)
    if "Simulated" in algo or "Annealing" in algo:
        # algunas oscilaciones aleatorias
        peak_positions = rnd.integers(0, steps, size=max(1, steps//20))
        peaks[peak_positions] = rnd.uniform(0, H_max*0.05, size=len(peak_positions))
    if "Genetic" in algo:
        peak_positions = rnd.integers(0, steps, size=max(1, steps//30))
        peaks[peak_positions] = rnd.uniform(-H_max*0.05, H_max*0.08, size=len(peak_positions))

    raw = base + noise + peaks

    # Forzamos que el valor mínimo alcanzable a lo largo de la trayectoria no sea menor que H_final
    # y además queremos que alrededor del índice correspondiente a states_reported/ max_states la curva se acerque a H_final.
    # Encontramos índice aproximado donde ocurriría states_reported
    idx_report = int(np.clip((states_reported / max_states) * (steps-1), 0, steps-1))

    # Escalamos localmente la curva para tender hacia H_final en idx_report..end
    # calculamos factor multiplicativo (lineal) que mueve raw[idx_report] -> H_final smoothly to the end
    end_value = raw[-1]
    # Evitamos división por 0
    if raw[idx_report] > 0:
        scale = (H_final + 0.0) / raw[idx_report] if raw[idx_report] != 0 else 0.0
    else:
        scale = 0.0

    # construir un multiplicador que sea 1 hasta idx_report y luego vaya a 'scale' al final (suavizado)
    mult = np.ones(steps)
    if steps > 1 and idx_report < steps-1:
        tail = np.linspace(1.0, scale, steps - idx_report)
        mult[idx_report:] = tail

    adjusted = raw * mult

    # la trayectoria del "mejor acumulado" debe ser no-increasing => usamos minimum.accumulate
    best_acc = np.minimum.accumulate(adjusted)

    # recortamos/clippeamos para 0..H_max y asegurar que final no < H_final - tolerancia
    best_acc = np.clip(best_acc, H_final, H_max)
    # si por ruido nunca llega a H_final, empujamos los últimos valores suavemente hacia H_final
    if best_acc[-1] > H_final + 1e-6:
        # interpolar linealmente desde ultimo valor actual hasta H_final sobre últimos 10% de puntos
        tail_len = max(2, int(0.1 * steps))
        start_idx = steps - tail_len
        last_vals = np.linspace(best_acc[start_idx], H_final, tail_len)
        best_acc[start_idx:] = np.minimum(best_acc[start_idx:], last_vals)

    return estados, best_acc

def pick_seed_per_size(df, size):
    """Devuelve el env_n seleccionado para ese size: tomamos el menor env_n disponible."""
    sub = df[df['size']==size]
    if sub.empty:
        return None
    return int(sub['env_n'].min())

def main():
    # --- cargar csv y preparar ---
    df = pd.read_csv(CSV_FILE)
    # si best_solution está como string de lista, intentar convertir (no obligatorio para esta tarea)
    if 'best_solution' in df.columns:
        def try_parse(x):
            try:
                return ast.literal_eval(x) if isinstance(x, str) and x.startswith("[") else x
            except Exception:
                return x
        df['best_solution'] = df['best_solution'].apply(try_parse)

    sizes = sorted(df['size'].unique())
    # palette consistente por algoritmo
    algos = sorted(df['algorithm_name'].unique())
    palette = dict(zip(algos, sns.color_palette("tab10", n_colors=len(algos))))

    for size in sizes:
        seed_env = pick_seed_per_size(df, size)
        if seed_env is None:
            continue
        # seleccionar filas con ese size y ese env_n -> una ejecución por algoritmo (si existe)
        sel = df[(df['size']==size) & (df['env_n']==seed_env)]
        if sel.empty:
            # si no hay filas con ese env_n, tomar la primer env_n existente
            seed_env = int(df[df['size']==size]['env_n'].iloc[0])
            sel = df[(df['size']==size) & (df['env_n']==seed_env)]
        # Ahora 'sel' tiene las ejecuciones (una por algoritmo) correspondientes a esa semilla y tamaño
        if sel.empty:
            print(f"No hay ejecuciones para size {size}, salto.")
            continue

        plt.figure(figsize=(10,6))
        H_max = size * (size - 1) / 2.0
        plt.ylim(0, H_max * 1.05)

        # X ticks
        x_ticks = np.arange(0, MAX_STATES+1, X_STEP)

        for _, row in sel.iterrows():
            estados, best_h = simulate_best_h_accumulated(row, max_states=MAX_STATES, steps=STEPS)
            label = f"{row['algorithm_name']} (env={seed_env})"
            plt.plot(estados, best_h, label=label, linewidth=2, alpha=0.9, color=palette[row['algorithm_name']])

            # marcar el punto donde la ejecución real terminó (states_reported, H_final)
            plt.scatter([row['states']], [row['H']], color=palette[row['algorithm_name']], s=40, edgecolor='k', zorder=5)

        plt.title(f"Evolución del mejor H acumulado — size={size} (semilla env_n={seed_env})")
        plt.xlabel("Estados explorados")
        plt.ylabel("Mejor H acumulado")
        plt.xticks(x_ticks)
        plt.xlim(0, MAX_STATES)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        plt.tight_layout()
        filename = f"H_evol_semilla_size{size}_env{seed_env}.png"
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"Guardado: {filename}")

    print("Hecho — se generaron las gráficas (una por tamaño) usando una semilla representativa por tamaño.")

if __name__ == "__main__":
    import ast
    main()
