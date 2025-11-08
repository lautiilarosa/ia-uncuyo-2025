import os
import pandas as pd
import matplotlib.pyplot as plt

def save_results_csv(rows, path):
    """
    rows: lista de dicts con keys:
    env_idx, seed, algorithm, scenario, success, explored, actions, cost, time
    """
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    return df

def make_boxplots(df, out_dir='results/figs', metrics=None):
    os.makedirs(out_dir, exist_ok=True)
    if metrics is None:
        metrics = ['explored', 'actions', 'cost', 'time']

    for metric in metrics:
        plt.figure(figsize=(12,6))
        grouped = df.groupby(['algorithm', 'scenario'])
        data = []
        labels = []
        for (alg, sc), group in grouped:
            if metric in ('actions', 'cost'):
                vals = group[group['success'] == True][metric].dropna()
            else:
                vals = group[metric].dropna()
            if len(vals) == 0:
                continue
            data.append(vals.values)
            labels.append(f"{alg}\n(S{sc})")

        if not data:
            print(f"No hay datos para {metric}")
            continue

        plt.boxplot(data, labels=labels, showfliers=False)
        plt.title(f'Boxplot: {metric} por algoritmo y escenario')
        plt.ylabel(metric)
        plt.xticks(rotation=45)
        plt.tight_layout()
        filename = f"{out_dir}/boxplot_{metric}.png"
        plt.savefig(filename)
        plt.close()
        print("Guardado:", filename)
