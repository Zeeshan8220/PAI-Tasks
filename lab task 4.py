def solve_n_queens(n):
    def backtrack(row, cols, left_diags, right_diags, board):
        if row == n:  
            solutions.append(["".join(row) for row in board])  # Store a valid board
            return
        
        for col in range(n):
            if col in cols or (row + col) in left_diags or (row - col) in right_diags:
                continue  # Skip if under attack

            # Place queen
            board[row][col] = "Q"
            cols.add(col)
            left_diags.add(row + col)
            right_diags.add(row - col)

            # Recur to next row
            backtrack(row + 1, cols, left_diags, right_diags, board)

            # Remove queen (backtrack)
            board[row][col] = "."
            cols.remove(col)
            left_diags.remove(row + col)
            right_diags.remove(row - col)

    solutions = []
    empty_board = [["." for _ in range(n)] for _ in range(n)]
    backtrack(0, set(), set(), set(), empty_board)
    
    return solutions

# Example: Solve for N = 4
n = 4
results = solve_n_queens(n)
for board in results:
    for row in board:
        print(row)
    print()
