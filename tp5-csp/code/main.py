# main.py
from csp import NQueensCSP
from backtracking import backtracking_search
from forward_checking import forward_checking_search

def print_board_array(solution):
    print("Solución como array:", solution)
    n = len(solution)
    board = [['.' for _ in range(n)] for _ in range(n)]
    for col, row in enumerate(solution):
        board[row][col] = 'Q'
    for row in board:
        print(' '.join(row))
    print()

if __name__ == "__main__":
    n = 12
    csp = NQueensCSP(n)

    print("=== Backtracking ===")
    solution_bt = backtracking_search(csp)
    if solution_bt:
        print_board_array(solution_bt)
    else:
        print("No se encontró solución.")

    print("=== Forward Checking ===")
    solution_fc = forward_checking_search(csp)
    if solution_fc:
        print_board_array(solution_fc)
    else:
        print("No se encontró solución.")
