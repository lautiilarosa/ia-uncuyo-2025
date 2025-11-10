import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score, RandomizedSearchCV
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
from category_encoders import TargetEncoder, WOEEncoder
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
import warnings
warnings.filterwarnings('ignore')

TRAIN_CSV = "../../arbolado-mza-dataset.csv"
TEST_CSV  = "../../arbolado-mza-dataset-test.csv"
ID_COL    = "id"
TARGET    = "inclinacion_peligrosa"
RANDOM_STATE = 42


# 1) Cargar datos
train = pd.read_csv(TRAIN_CSV)
test = pd.read_csv(TEST_CSV)


test_original_order = test[ID_COL].copy()
print(f"Primeros 10 IDs en test: {test_original_order.head(10).tolist()}")


print("=" * 50)
print("ANÁLISIS EXPLORATORIO")
print("=" * 50)
print("Train shape:", train.shape)
print("Test shape:", test.shape)
print("\nDistribución del target:")
print(train[TARGET].value_counts())
print(train[TARGET].value_counts(normalize=True))

# 3) Feature engineering avanzado
def advanced_feature_engineering(df):
    df = df.copy()
    
    # Ejemplo: crear features de interacción si existen estas columnas
    if all(col in df.columns for col in ['diametro_tronco', 'altura_arbol']):
        df['diametro_altura_ratio'] = df['diametro_tronco'] / (df['altura_arbol'] + 1e-5)
    
    # Crear categorías más robustas para circ_tronco_cm
    if "circ_tronco_cm" in df.columns:
        bins = [0, 20, 50, 100, 200, float('inf')]
        labels = ['muy_delgado', 'delgado', 'medio', 'grueso', 'muy_grueso']
        df['circ_tronco_cat'] = pd.cut(df['circ_tronco_cm'], bins=bins, labels=labels)
    
    # Features polinomiales para variables numéricas importantes
    if "edad_arbol" in df.columns:
        df['edad_arbol_squared'] = df['edad_arbol'] ** 2

    # Agregar features estadísticos por categorías si hay muchas variables categóricas
    categorical_cols = df.select_dtypes(include=['object']).columns
    for cat_col in categorical_cols:
        if df[cat_col].nunique() < 20:  # Solo para categorías con pocos valores únicos
            # Calcular frecuencia de cada categoría
            freq_encoding = df[cat_col].value_counts().to_dict()
            df[f'{cat_col}_freq'] = df[cat_col].map(freq_encoding)
    
    return df

print("\nAplicando feature engineering...")
train = advanced_feature_engineering(train)
test = advanced_feature_engineering(test)

# 4) Selección inteligente de features
def select_features(df, target_col, id_col, null_threshold=0.5, cardinality_threshold=100):
    features_to_drop = []
    
    for col in df.columns:
        if col in [target_col, id_col]:
            continue
            
      
        null_ratio = df[col].isnull().mean()
        if null_ratio > null_threshold:
            features_to_drop.append(col)
            continue
            
      
        if df[col].dtype == 'object':
            if df[col].nunique() > cardinality_threshold:
                features_to_drop.append(col)
    
    return [col for col in df.columns if col not in features_to_drop and col not in [target_col, id_col]]

selected_features = select_features(train, TARGET, ID_COL)
print(f"\nFeatures seleccionados: {len(selected_features)}")


num_features = []
cat_features = []

for c in selected_features:
    if train[c].dtype.kind in "ifc":  
        num_features.append(c)
    else:
        cat_features.append(c)

print(f"Num features: {len(num_features)}")
print(f"Cat features: {len(cat_features)}")


num_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

cat_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
    ("target_enc", TargetEncoder())
])

preprocessor = ColumnTransformer(transformers=[
    ("num", num_transformer, num_features),
    ("cat", cat_transformer, cat_features)
])


models = {
    'xgb': xgb.XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=RANDOM_STATE
    ),
    'rf': RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=3,
        random_state=RANDOM_STATE,
        class_weight='balanced'
    )
}


def evaluate_model(model, X, y, model_name):
    print(f"\n{'-'*20} Evaluando {model_name} {'-'*20}")
    
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    aucs = []
    
    fold = 1
    for train_idx, val_idx in skf.split(X, y):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]
        
        pipeline = ImbPipeline(steps=[
            ("preproc", preprocessor),
            ("smote", SMOTE(random_state=RANDOM_STATE, sampling_strategy=0.5)),
            ("clf", model)
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred_proba = pipeline.predict_proba(X_val)[:, 1]
        auc = roc_auc_score(y_val, y_pred_proba)
        
        print(f"Fold {fold} AUC: {auc:.4f}")
        aucs.append(auc)
        fold += 1
    
    print(f"{model_name} - AUC mean: {np.mean(aucs):.4f} ± {np.std(aucs):.4f}")
    return np.mean(aucs), np.std(aucs), pipeline


print("Iniciando evaluación de modelos...")
X = train[selected_features]
y = train[TARGET].values

best_score = 0
best_model_name = None
best_pipeline = None

for model_name, model in models.items():
    mean_auc, std_auc, pipeline = evaluate_model(model, X, y, model_name)
    
    if mean_auc > best_score:
        best_score = mean_auc
        best_model_name = model_name
        best_pipeline = pipeline

print(f"\n{'='*50}")
print(f"MEJOR MODELO: {best_model_name} con AUC: {best_score:.4f}")
print(f"{'='*50}")


print(f"\nEntrenando modelo final {best_model_name} con todos los datos...")
final_pipeline = ImbPipeline(steps=[
    ("preproc", preprocessor),
    ("smote", SMOTE(random_state=RANDOM_STATE, sampling_strategy=0.5)),
    ("clf", models[best_model_name])
])

final_pipeline.fit(X, y)


print("Generando predicciones...")
test_proba = final_pipeline.predict_proba(test[selected_features])[:, 1]


submission = pd.DataFrame({
    ID_COL: test_original_order,  
    TARGET: test_proba
})


submission[TARGET] = np.clip(submission[TARGET], 0.001, 0.999)

#
print(f"\nVerificación del orden:")
print(f"Primeros 10 IDs en submission: {submission[ID_COL].head(10).tolist()}")
print(f"Primeras 10 predicciones: {submission[TARGET].head(10).tolist()}")

# Guardar submission
submission.to_csv("submission_corregida.csv", index=False)
print("\nsubmission_corregida.csv guardado correctamente.")

# Mostrar estadísticas de las predicciones
print(f"\nEstadísticas de las predicciones:")
print(f"Rango: [{submission[TARGET].min():.4f}, {submission[TARGET].max():.4f}]")
print(f"Media: {submission[TARGET].mean():.4f}")
print(f"Percentiles:")
print(f"  25%: {submission[TARGET].quantile(0.25):.4f}")
print(f"  50%: {submission[TARGET].quantile(0.50):.4f}")
print(f"  75%: {submission[TARGET].quantile(0.75):.4f}")

print(f"\nAnálisis del modelo final ({best_model_name}):")


y_train_pred_proba = final_pipeline.predict_proba(X)[:, 1]
train_auc = roc_auc_score(y, y_train_pred_proba)
print(f"AUC en datos de entrenamiento: {train_auc:.4f}")


train_predictions = final_pipeline.predict(X)
print(f"\nDistribución de clases predichas en train:")
print(pd.Series(train_predictions).value_counts())