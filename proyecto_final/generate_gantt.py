import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta
import numpy as np

# Configuración de la figura
fig, ax = plt.subplots(figsize=(14, 8))

# Definir las actividades con sus duraciones
actividades = [
    ("Lectura\nAIMA", 1, '#B19CD9'),
    ("Lectura Q-Learning\ny DQN", 1, '#77DD77'),
    ("Configuración del\nentorno", 2, '#FFB347'),
    ("Exploración y\ndocumentación", 2, '#FF6961'),
    ("Implementación\nsolución aleatoria", 1, '#6BB6FF'),
    ("Diseño espacio\nestados y recompensa", 2, '#F49AC2'),
    ("Implementación\nQ-Learning", 4, '#FF8C94'),
    ("Implementación\nDQN ", 3, '#AEC6CF'),
    ("Entrenamiento y ajuste\nhiperparámetros", 3, '#CB99C9'),
    ("Evaluación y\ncomparación", 2, '#77DD77'),
    ("Recopilación métricas\ny gráficos", 2, '#6BB6FF'),
    ("Elaboración\ninforme final", 5, '#FFD700'),
    ("Elaboración\npresentación", 2, '#FFB6C1')
]

# Calcular posiciones de inicio
inicio_acumulado = 0
posiciones = []
for _, duracion, _ in actividades:
    posiciones.append(inicio_acumulado)
    inicio_acumulado += duracion

# Crear el diagrama
y_pos = np.arange(len(actividades))

# Dibujar las barras
for i, (nombre, duracion, color) in enumerate(actividades):
    ax.barh(y_pos[i], duracion, left=posiciones[i], height=0.6, 
            color=color, edgecolor='white', linewidth=2, alpha=0.85)
    
    # Añadir texto en el centro de cada barra si hay espacio
    if duracion >= 2:
        ax.text(posiciones[i] + duracion/2, y_pos[i], f'{duracion}d', 
                ha='center', va='center', fontsize=9, fontweight='bold', color='white')

# Configurar etiquetas del eje Y
ax.set_yticks(y_pos)
ax.set_yticklabels([nombre for nombre, _, _ in actividades], fontsize=10)

# Configurar el eje X (días)
max_dias = 30
ax.set_xlim(0, max_dias + 1)
ax.set_xticks(range(1, max_dias + 1, 2))
ax.set_xticklabels(range(1, max_dias + 1, 2), fontsize=9)
ax.set_xlabel('Días del Proyecto', fontsize=12, fontweight='bold')

# Título
ax.set_title('Diagrama de Gantt\nProyecto: The Legend of Zelda: A Link to the Past con RL', 
             fontsize=14, fontweight='bold', pad=20)

# Grilla
ax.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.5)
ax.set_axisbelow(True)

# Invertir el eje Y para que la primera actividad esté arriba
ax.invert_yaxis()

# Ajustar el layout
plt.tight_layout()

# Guardar la imagen
"""
plt.savefig('c:\\Users\\massa\\OneDrive\\Desktop\\Facultad\\ia-uncuyo-2025\\diagrama_gantt.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
guardar en pc juani

"""
plt.savefig('/home/lauti/Documentos/Facultad/proyecto_final/diagrama_gantt.png', 
            dpi=300, bbox_inches='tight', facecolor='white')




print("Diagrama de Gantt generado exitosamente: diagrama_gantt.png")

# Mostrar el diagrama
plt.show()
