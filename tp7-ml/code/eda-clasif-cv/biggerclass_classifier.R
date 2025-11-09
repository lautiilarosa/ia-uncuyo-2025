# a) Clasificador por clase mayoritaria
biggerclass_classifier <- function(df, target_col) {

  majority_class <- df %>%
    group_by(!!sym(target_col)) %>%
    summarise(count = n()) %>%
    arrange(desc(count)) %>%
    slice(1) %>%
    pull(!!sym(target_col))
  
  # Crear columna de predicción constante
  df$prediction_class <- majority_class
  
  return(df)
}

# b) Repetir los ejercicios 4c y 4d
library(dplyr)


validation_path <- "../../data/arbolado-mendoza-dataset-validation.csv"
validation_df <- read.csv(validation_path)


validation_df <- biggerclass_classifier(validation_df, "inclinacion_peligrosa")


head(validation_df[, c("inclinacion_peligrosa", "prediction_class")])



TP <- validation_df %>% filter(inclinacion_peligrosa == 1, prediction_class == 1) %>% nrow()
TN <- validation_df %>% filter(inclinacion_peligrosa == 0, prediction_class == 0) %>% nrow()
FP <- validation_df %>% filter(inclinacion_peligrosa == 0, prediction_class == 1) %>% nrow()
FN <- validation_df %>% filter(inclinacion_peligrosa == 1, prediction_class == 0) %>% nrow()


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
cat("Recall (Sensitivity):", recall, "\n")
cat("Specificity:", specificity, "\n")
