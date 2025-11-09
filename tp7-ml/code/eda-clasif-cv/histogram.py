import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("../../data/arbolado-mendoza-dataset-train.csv")
df = df.dropna(subset=['circ_tronco_cm'])


# a) Histograma general de circ_tronco_cm


bins_list = [30, 40, 50]

for bins in bins_list:
    plt.figure(figsize=(8,5))
    plt.hist(df['circ_tronco_cm'], bins=bins, color='steelblue', edgecolor='black')
    plt.title(f"Histograma de 'circ_tronco_cm' con {bins} bins")
    plt.xlabel("Circunferencia del tronco (cm)")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig(f"../../images/hist_circ_tronco_{bins}bins.png")
    plt.close()

# b) Histograma separado por inclinacion_peligrosa

clases = sorted(df['inclinacion_peligrosa'].unique())

for bins in bins_list:
    plt.figure(figsize=(8,5))
    for clase in clases:
        subset = df[df['inclinacion_peligrosa'] == clase]
        plt.hist(subset['circ_tronco_cm'], bins=bins, alpha=0.6, label=f"Inclinación = {clase}")
        
    plt.title(f"'circ_tronco_cm' por clase de inclinación peligrosa ({bins} bins)")
    plt.xlabel("Circunferencia del tronco (cm)")
    plt.ylabel("Frecuencia")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"../../images/hist_circ_tronco_inclinacion_{bins}bins.png")
    plt.close()