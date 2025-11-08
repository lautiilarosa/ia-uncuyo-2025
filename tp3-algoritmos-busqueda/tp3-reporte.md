# Análisis Comparativo de Algoritmos de Búsqueda

A continuación, se realiza un analisis de los algoritmos BFS,DFS,DLS,UCS Y A* implementado en un entorno FrozenLake con dos escenarios
Escenario 1: Cada acción tiene costo 1.


Escenario 2: Las acciones tienen los siguientes costos:
• Moverse a la izquierda o la derecha: costo 1.
• Moverse hacia arriba o abajo: costo 10.

Se especifica que el Algoritmo de A* utiliza la heurística eculidiana

A continuación, se mostrarán graficos y un minimo analisis de cada uno

## 1. Tiempo de Ejecución
![][image1] 


- **A***: Tiempos más bajos y consistentes (eficiencia heurística)
- **UCS y BFS**: Desempeño temporal moderado y estable
- **DFS**: Alta variabilidad (0.5s - 3.5s) - depende del problema
- **DLS**: Escala con límite de profundidad (DLS50 < DLS75 < DLS100)

## 2. Estados Explorados
![][image2] 

- **A***: Menos estados gracias a la heurística (más eficiente)
- **BFS y UCS**: Exploración moderada y consistente
- **DFS**: Extremadamente variable (0 - 2500 estados)
- **DLS**: Aumenta progresivamente con el límite de profundidad

## 3. Cantidad de Acciones
![][image3] 
- **BFS, UCS, A***: Caminos más cortos (óptimos en longitud)
- **DFS y DLS**: Caminos significativamente más largos (hasta 600 acciones)
- **A***: Combina optimalidad con eficiencia computacional

## 4. Costo Total
![][image4] 
- **UCS y A***: Costos más bajos (optimizan costo)
- **BFS**: Costos más altos (optimiza longitud, no costo)
- **DFS y DLS**: Costos variables y generalmente elevados

##  Conclusion
A* es el mejor porque:

1- Encuentra la solución óptima (cuando la heurística es admisible)

2- Es el más rápido en tiempo de ejecución

3- Explora muchos menos estados que los otros algoritmos

4- Encuentra caminos cortos con bajo costo

5- Es consistente - no tiene la variabilidad extrema de DFS

6- Balance perfecto: no se va a los extremos como DFS (muy impredecible) ni BFS (explora mucho)


[image1]: images/time_boxplot.png

[image2]: images/states_n_boxplot.png

[image3]: images/actions_count_boxplot.png

[image4]: images/actions_cost_boxplot.png
