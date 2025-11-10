# Informe Breve - Pipeline Árboles Mendoza

## 1. Preprocesamiento
- Se eliminaron columnas con >50% nulos y categóricas con alta cardinalidad (>100).
- Se crearon nuevas features:
  - `diametro_altura_ratio`, `circ_tronco_cat`, `edad_arbol_squared`.
  - Frecuencia de categorías para variables categóricas con <20 valores únicos.
- Variables numéricas: imputación por mediana + escalado StandardScaler.
- Variables categóricas: imputación constante + Target Encoding.
- Balanceo de clases: SMOTE (50% de la clase minoritaria).

## 2. Modelos
- **XGBoost**: n_estimators=300, max_depth=6, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8.
- **Random Forest**: n_estimators=200, max_depth=10, min_samples_split=5, min_samples_leaf=3, class_weight='balanced'.
- Pipeline: preprocesamiento → SMOTE → clasificador.
- Validación: StratifiedKFold (5 folds), métrica: AUC.

## 3. Resultados Validación (5 folds)
- **XGBoost** AUCs: 0.7784, 0.7690, 0.7603, 0.7686, 0.7672  
  Media ± std: 0.7687 ± 0.0058
- **Random Forest** AUCs: 0.7683, 0.7574, 0.7593, 0.7665, 0.7587  
  Media ± std: 0.7620 ± 0.0045
- Mejor modelo: **XGBoost**.

## 4. Resultados Kaggle
- Public leaderboard AUC: **0.75979**

## 5. Análisis del modelo final
- AUC en datos de entrenamiento: 0.8355
- Distribución de clases predichas en train:
  - Clase 0: 27,676
  - Clase 1: 4,236

## 6. Descripción Algoritmo
- Clasificador basado en árboles (XGBoost) capaz de capturar relaciones no lineales e interacciones.
- Preprocesamiento consistente + balanceo de clases con SMOTE garantiza robustez y mejor generalización.
