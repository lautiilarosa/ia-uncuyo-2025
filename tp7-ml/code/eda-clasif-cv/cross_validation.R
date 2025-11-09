library(rpart)
library(dplyr)

# a) Crear los folds
create_folds <- function(df, k = 10, seed = NULL) {
  if (!is.null(seed)) set.seed(seed)
  
  n <- nrow(df)
  shuffled_indices <- sample(1:n)  # mezcla aleatoria
  folds <- split(shuffled_indices, cut(seq_along(shuffled_indices), k, labels = FALSE))
  
  names(folds) <- paste0("Fold", 1:k)
  return(folds)
}

## funcion para calcular metricas
confusion_metrics <- function(actual, predicted) {
  TP <- sum(actual == 1 & predicted == 1, na.rm = TRUE)
  TN <- sum(actual == 0 & predicted == 0, na.rm = TRUE)
  FP <- sum(actual == 0 & predicted == 1, na.rm = TRUE)
  FN <- sum(actual == 1 & predicted == 0, na.rm = TRUE)
  
  Accuracy <- (TP + TN) / (TP + TN + FP + FN)
  Precision <- ifelse((TP + FP) == 0, NA, TP / (TP + FP))
  Sensitivity <- ifelse((TP + FN) == 0, NA, TP / (TP + FN))
  Specificity <- ifelse((TN + FP) == 0, NA, TN / (TN + FP))
  
  return(c(Accuracy = Accuracy, Precision = Precision, Sensitivity = Sensitivity, Specificity = Specificity))
}

# b) Implementar Cross-Validation
cross_validation <- function(df, k = 10, seed = 42) {
  folds <- create_folds(df, k, seed)
  metrics_list <- list()
  
  factor_cols <- c("seccion", "especie")  # columnas categóricas
  
  for (i in 1:k) {
    test_idx <- folds[[i]]
    train_idx <- setdiff(1:nrow(df), test_idx)
    
    train_fold <- df[train_idx, ]
    test_fold <- df[test_idx, ]
    
    # Convertir variable objetivo a factor
    train_fold$inclinacion_peligrosa <- as.factor(train_fold$inclinacion_peligrosa)
    test_fold$inclinacion_peligrosa <- as.factor(test_fold$inclinacion_peligrosa)
    
    # Alinear niveles de factores entre train y test
    for (col in factor_cols) {
      levels_train <- levels(as.factor(train_fold[[col]]))
      train_fold[[col]] <- factor(train_fold[[col]], levels = levels_train)
      test_fold[[col]] <- factor(test_fold[[col]], levels = levels_train)
    }
    
    # Fórmula del modelo
    train_formula <- formula(inclinacion_peligrosa ~ altura + circ_tronco_cm + lat + long + seccion + especie)
    
    # Entrenamiento del árbol
    tree_model <- rpart(train_formula, data = train_fold)
    
    # Predicciones
    predictions <- predict(tree_model, test_fold, type = "class")
    predictions <- as.numeric(as.character(predictions))
    
    # Calcular métricas
    metrics <- confusion_metrics(actual = as.numeric(as.character(test_fold$inclinacion_peligrosa)),
                                 predicted = predictions)
    
    metrics_list[[i]] <- metrics
    cat(sprintf("Fold %d completado\n", i))
  }



 metrics_df <- as.data.frame(do.call(rbind, metrics_list))
  
  # Resumen (media y desvío estándar)
  summary <- data.frame(
    Mean_Accuracy = mean(metrics_df$Accuracy, na.rm = TRUE),
    SD_Accuracy = sd(metrics_df$Accuracy, na.rm = TRUE),
    Mean_Precision = mean(metrics_df$Precision, na.rm = TRUE),
    SD_Precision = sd(metrics_df$Precision, na.rm = TRUE),
    Mean_Sensitivity = mean(metrics_df$Sensitivity, na.rm = TRUE),
    SD_Sensitivity = sd(metrics_df$Sensitivity, na.rm = TRUE),
    Mean_Specificity = mean(metrics_df$Specificity, na.rm = TRUE),
    SD_Specificity = sd(metrics_df$Specificity, na.rm = TRUE)
  )
  
  cat("\nMétricas por fold:\n")
  print(metrics_df)
  cat("\nResumen (media y desvío estándar):\n")
  print(summary)
  
  return(list(metrics_by_fold = metrics_df, summary = summary))
}

# Ejecución 

train_df <- read.csv("../../data/arbolado-mendoza-dataset-train.csv")

set.seed(123)
cv_results <- cross_validation(train_df, k = 10)

