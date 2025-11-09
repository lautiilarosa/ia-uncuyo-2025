import pandas as pd


df = pd.read_csv("../../data/arbolado-mendoza-dataset-train.csv")


df = df.dropna(subset=['circ_tronco_cm'])


# c) Crear la variable categórica circ_tronco_cm_cat

# Primero Calculamos los cuartiles
q1 = df['circ_tronco_cm'].quantile(0.25)
q2 = df['circ_tronco_cm'].quantile(0.50)
q3 = df['circ_tronco_cm'].quantile(0.75)

# Mostrar los valores para referencia
print("Puntos de corte:")
print(f"  Bajo - Medio: {q1:.2f} cm")
print(f"  Medio - Alto: {q2:.2f} cm")
print(f"  Alto - Muy alto: {q3:.2f} cm")

# Creamos la nueva variable categórica
def categorizar_tronco(x):
    if x <= q1:
        return "bajo"
    elif x <= q2:
        return "medio"
    elif x <= q3:
        return "alto"
    else:
        return "muy alto"

df['circ_tronco_cm_cat'] = df['circ_tronco_cm'].apply(categorizar_tronco)

# Finalmente guardamos el archivo
output_path = "../../data/arbolado-mendoza-dataset-circ_tronco_cm-train.csv"
df.to_csv(output_path, index=False)
