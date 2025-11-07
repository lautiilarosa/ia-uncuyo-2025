
class NQueensCSP:
    def __init__(self, n):
        self.n = n
        # Las variables son las columnas (0 a n-1)
        self.variables = list(range(n))
        # Dominio: posibles filas para cada columna
        self.domains = {var: list(range(n)) for var in self.variables}

    def is_consistent(self, assignment, var, value):
        """
        Chequea si al poner value en la columna var no se rompe ninguna restricción.
        """
        for col, row in enumerate(assignment):
            if row is None:
                continue
            # Misma fila
            if row == value:
                return False
            # Misma diagonal
            if abs(col - var) == abs(row - value):
                return False
        return True
