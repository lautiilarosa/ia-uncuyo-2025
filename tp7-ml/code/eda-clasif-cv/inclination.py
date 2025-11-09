import pandas as pd
import matplotlib.pyplot as plt

# Cargamos el conjunto de entrenamiento
df = pd.read_csv("../../data/arbolado-mendoza-dataset-train.csv")

# a) ¿Cual es la distribución de las clase inclinacion_peligrosa?

conteo = df['inclinacion_peligrosa'].value_counts()

# Gráfico de barras
fig, ax = plt.subplots(figsize=(6,4))
bars = ax.bar(conteo.index.astype(str), conteo.values, color=['skyblue', 'salmon'])
ax.set_title("Distribución de la variable 'inclinacion_peligrosa'")
ax.set_xlabel("¿Inclinación peligrosa?")
ax.set_ylabel("Cantidad de árboles")

# Mostrar cantidad exacta arriba de cada barra
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 10, f"{int(height)}", 
            ha='center', va='bottom', fontsize=10)
    
plt.tight_layout()
plt.show()
plt.savefig("../../images/grafico_inclinacion.png")  
plt.close()
    


# b) ¿Se puede considerar alguna sección más peligrosa que la otra?

peligro_por_seccion = df.groupby('seccion')['inclinacion_peligrosa'].mean().sort_values(ascending=False)

# Gráfico de barras 
fig, ax = plt.subplots(figsize=(10,5))
peligro_por_seccion.plot(kind='bar', color='orange', ax=ax)
ax.set_title("Proporción de árboles con inclinación peligrosa por sección")
ax.set_xlabel("Sección")
ax.set_ylabel("Proporción de árboles peligrosos")

# Ajustar el límite superior del eje Y para que no quede aplastado
max_val = peligro_por_seccion.max()
ax.set_ylim(0, max_val * 1.2)

for i, val in enumerate(peligro_por_seccion):
    ax.text(i, val + max_val * 0.02, f"{val:.2f}", ha='center', va='bottom', fontsize=9)

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("../../images/inclinacion_por_seccion.png")
plt.close()



# c) ¿Se puede considera alguna especie más peligrosa que la otra?


peligro_por_especie = df.groupby('especie')['inclinacion_peligrosa'].mean().sort_values(ascending=False).head(10)

# Seleccionar las especies más comunes
fig, ax = plt.subplots(figsize=(10,5))
peligro_por_especie.plot(kind='bar', color='seagreen', ax=ax)
ax.set_title("Top 10 especies con mayor proporción de inclinación peligrosa")
ax.set_xlabel("Especie")
ax.set_ylabel("Proporción de árboles peligrosos")
max_val = peligro_por_especie.max()
ax.set_ylim(0, max_val * 1.2)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("../../images/inclinacion_por_especie.png")
plt.close()
