library(dplyr)

# a ) Generar Prediction_Prob
add_random_prediction_prob <- function(df, seed = NULL) {
  if (!is.null(seed)) set.seed(seed)
  df$prediction_prob <- runif(nrow(df), 0, 1)
  return(df)
}

# b) Clasificador Aleatorio
random_classifier <- function(df) {
  df$prediction_class <- ifelse(df$prediction_prob > 0.5, 1, 0)
  return(df)
}

# c) Cargar el CSV y evaluar el clasificador
library(dplyr)


validation_path <- "../../data/arbolado-mendoza-dataset-validation.csv"


validation_df <- read.csv(validation_path)


validation_df <- add_random_prediction_prob(validation_df, seed = 42)
validation_df <- random_classifier(validation_df)

head(validation_df[, c("prediction_prob", "prediction_class")])

# d) Calcular Métricas i,ii,iii,iv y Matriz de Confusión
# True Positive: predijo 1 y realmente era 1
TP <- validation_df %>% filter(inclinacion_peligrosa == 1, prediction_class == 1) %>% nrow()

# True Negative: predijo 0 y realmente era 0
TN <- validation_df %>% filter(inclinacion_peligrosa == 0, prediction_class == 0) %>% nrow()

# False Positive: predijo 1 pero era 0
FP <- validation_df %>% filter(inclinacion_peligrosa == 0, prediction_class == 1) %>% nrow()

# False Negative: predijo 0 pero era 1
FN <- validation_df %>% filter(inclinacion_peligrosa == 1, prediction_class == 0) %>% nrow()

# Matriz de confusion
confusion_matrix <- matrix(
  c(TN, FP, FN, TP),
  nrow = 2,
  byrow = TRUE,
  dimnames = list(
    "Actual" = c("NO", "YES"),
    "Predicted" = c("NO", "YES")
  )
)

confusion_matrix

# Métricas
accuracy <- (TP + TN) / (TP + TN + FP + FN)
precision <- ifelse((TP + FP) == 0, 0, TP / (TP + FP))
recall <- ifelse((TP + FN) == 0, 0, TP / (TP + FN))
specificity <- ifelse((TN + FP) == 0, 0, TN / (TN + FP))
cat("Accuracy:", accuracy, "\n")
cat("Precision:", precision, "\n")
cat("Recall:", recall, "\n")
cat("Specificity:", specificity, "\n")

