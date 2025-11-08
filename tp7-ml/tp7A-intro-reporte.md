# Trabajo Práctico 7 
Parte A

### Ejercicio 1

En cada uno de los siguientes ejercicios, indique si en general se espera que un método de aprendizaje de máquinas flexible se comporte mejor o peor que uno inflexible. Justifique su respuesta.

**a) El tamaño de la muestra \( n \) es extremadamente grande, y el número de predictores \( p \) es pequeño.**  
**→ Mejor un método flexible.**  
Con muchas observaciones, la varianza del estimador disminuye, lo que permite utilizar métodos más complejos sin riesgo excesivo de sobreajuste. Al ser \( p \) pequeño, hay suficiente información por predictor para capturar relaciones no lineales o interacciones sin aumentar mucho la varianza.



**b) El número de predictores \( p \) es extremadamente grande, y el número de observaciones \( n \) es pequeño.**  
**→ Mejor un método inflexible.**  
En este caso cuando hay muchos predictores y poco el volumen de datos, vamos a enocontrar que los métodos flexibles tienden a sobreajustar (es decir alta varianza). Los métodos inflexibles, con supuestos más fuertes o regularización, reducen el riesgo de sobreajuste y tienden a generalizar mejor.


**c) La relación entre los predictores y la variable dependiente es altamente no lineal.**  
**→ Mejor un método flexible.**  
Los métodos inflexibles no pueden capturar relaciones no lineales en cambio los métodos flexibles, siempre que tengan controlada la varianza, pueden adaptarse mejor a la complejidad del verdadero patrón de datos.


**d) La varianza de los términos de error (\( \sigma^2 = Var(\varepsilon) \)) es extremadamente alta.**  
**→ Mejor un método inflexible.**  
Los métodos inflexibles son más estables frente al ruido, sacrificando un poco de sesgo pero mejorando la generalización a diferencia de los métodos flexibles.

---

### Ejercicio 2

Explique si cada escenario representa un problema de clasificación o de regresión, e indique si el interés principal es inferir o predecir. Especifique n (cantidad de observaciones) y p (cantidad de predictores) en cada caso.

**a) Análisis de salarios de directores ejecutivos.**  
- **Tipo de problema:** **Regresión.**  
- **Objetivo principal:** **Inferencia.**  
- **Cantidad de observaciones:** \( n = 500 \).  
- **Cantidad de predictores:** \( p = 3 \)  

**b) Evaluación del éxito de un nuevo producto.**  
- **Tipo de problema:** **Clasificación.**  
- **Objetivo principal:** **Predicción.**  
- **Cantidad de observaciones:** \( n = 20 \)   
- **Cantidad de predictores:** \( p = 13 \)  

**c) Predicción del tipo de cambio USD/Euro.**  
- **Tipo de problema:** **Regresión.**  
- **Objetivo principal:** **Predicción.**  
- **Cantidad de observaciones:** \( n = 52 \)  
- **Cantidad de predictores:** \( p = 3 \)  

---

### Ejercicio 3 

#### **Ventajas de un enfoque flexible**
- **Menor sesgo:** los métodos flexibles pueden capturar relaciones complejas o no lineales entre las variables predictoras y la respuesta.  
- **Mayor capacidad de ajuste:** permiten adaptarse a estructuras de datos con patrones difíciles de modelar usando técnicas rígidas (por ejemplo, interacciones o curvaturas).  
- **Mejor rendimiento cuando hay muchos datos y poca restricción:** si \( n \) es grande y la relación subyacente es compleja, los modelos flexibles pueden generalizar muy bien.

#### **Desventajas de un enfoque flexible**
- **Alta varianza:** los métodos muy flexibles tienden a sobreajustar los datos de entrenamiento, aprendiendo también el ruido.  
- **Mayor complejidad computacional:** suelen requerir más tiempo de cómputo y ajuste de hiperparámetros.  
- **Menor interpretabilidad:** es más difícil extraer conclusiones claras sobre la relación entre los predictores y la variable respuesta.

#### **Ventajas de un enfoque menos flexible**
- **Menor varianza:** tienden a generalizar mejor cuando los datos son escasos o ruidosos.  
- **Mayor interpretabilidad:** los modelos simples (como una regresión lineal o logística) permiten entender cómo cada variable influye en la respuesta.  
- **Mayor estabilidad:** pequeños cambios en los datos no alteran drásticamente los resultados.

#### **Desventajas de un enfoque menos flexible**
- **Mayor sesgo:** pueden no capturar relaciones no lineales o interacciones entre variables.  
- **Peor ajuste en relaciones complejas:** si el verdadero modelo es intrincado, el modelo simple puede subestimar la realidad.

#### **Cuándo preferir un enfoque más flexible**
- Cuando se dispone de un **gran número de observaciones** (\( n \) grande).  
- Cuando se sospecha que la relación entre las variables es **no lineal o compleja**.  
- Cuando el **ruido en los datos es bajo** (\( \sigma^2 \) pequeño).  
#### **Cuándo preferir un enfoque menos flexible**
- Cuando el conjunto de datos es **pequeño** o contiene **mucho ruido**.  
- Cuando se prioriza la **interpretabilidad** o se busca **inferir relaciones causales**.  
- Cuando se desea **evitar el sobreajuste**, especialmente si \( p \) es grande en relación a \( n \).

---

### Ejercicio 4

### Diferencias entre enfoques paramétricos y no paramétricos

Un enfoque **paramétrico** asume una forma funcional específica para la relación entre las variables predictoras y la respuesta (por ejemplo, una relación lineal). Luego estima un conjunto fijo de parámetros a partir de los datos.

En cambio, un enfoque **no paramétrico** no impone una forma funcional predeterminada, sino que busca que los datos determinen la estructura del modelo.

**Ventajas del enfoque paramétrico:**
- Es más **simple e interpretable**.  
- Requiere **menos datos** y tiene **menor varianza**.  

**Desventajas del enfoque paramétrico:**
- Tiene **mayor sesgo** si la forma asumida no representa bien la realidad.  
- Es **poco flexible** para relaciones no lineales o complejas.

**Ventajas del enfoque no paramétrico:**
- Es **más flexible** y puede capturar relaciones complejas.  
- Hace **menos supuestos** sobre la estructura de los datos.

**Desventajas del enfoque no paramétrico:**
- Tiene **mayor varianza** y necesita **más datos** para generalizar bien.  
- Suele ser **más difícil de interpretar**.

---

### Ejercicio 5

### K-NN sobre el dataset de 6 observaciones

Datos (cada fila = observación):  
| Obs. | X1 | X2 | X3 | Y     |
|------|----|----|----|-------|
| 1    | 0  | 3  | 0  | Rojo  |
| 2    | 2  | 0  | 0  | Rojo  |
| 3    | 0  | 1  | 3  | Rojo  |
| 4    | 0  | 1  | 2  | Verde |
| 5    | -1 | 0  | 1  | Verde |
| 6    | 1  | 1  | 1  | Rojo  |

**Punto de prueba:** \(X = (0,0,0)\).

**a) Distancias euclidianas al punto de prueba**

| Obs. | X1 | X2 | X3 | Clase | Distancia euclidiana |
|------|----|----|----|--------|----------------------|
| 1 | 0 | 3 | 0 | Rojo  | 3.0000 |
| 2 | 2 | 0 | 0 | Rojo  | 2.0000 |
| 3 | 0 | 1 | 3 | Rojo  | 3.1623 |
| 4 | 0 | 1 | 2 | Verde | 2.2361 |
| 5 | -1 | 0 | 1 | Verde | 1.4142 |
| 6 | 1 | 1 | 1 | Rojo  | 1.7321 |

**b) Predicción con \(K=1\)**  
El vecino más cercano es **Obs 5** , cuya clase es **Verde**.  
**Predicción:** **Verde**.

**c) Predicción con \(K=3\)**  
Los 3 vecinos más cercanos son: Obs5 (Verde), Obs6 (Rojo), Obs2 (Rojo). Votos: Rojo = 2, Verde = 1.  
**Predicción (mayoría):** **Rojo**.


**d) Si la frontera de decisión de Bayes es altamente no lineal, ¿K grande o chico?**  
Se prefieren valores de **K pequeños** ya que esta va a permitir que tenga una frontera local más flexible








