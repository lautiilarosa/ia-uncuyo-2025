import pandas as pd

"""
En este archivo se divide el dataset en 2 archivos , armamos el conjunto de entrenamiento y otro el de validación

"""


df = pd.read_csv("arbolado-mza-dataset.csv")

df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
split_index = int(len(df_shuffled) * 0.8)


train_df = df_shuffled[:split_index]
validation_df = df_shuffled[split_index:]

# Guardar los nuevos archivos
train_df.to_csv("arbolado-mendoza-dataset-train.csv", index=False)
validation_df.to_csv("arbolado-mendoza-dataset-validation.csv", index=False)

print("Archivos generados correctamente:")
