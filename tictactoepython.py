#what is that?

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_win(board, player):
    win_cond = [player] * 3
    # rows, columns and diagonals
    return any([
        any([row == win_cond for row in board]),
        any([list(col) == win_cond for col in zip(*board)]),
        [board[i][i] for i in range(3)] == win_cond,
        [board[i][2 - i] for i in range(3)] == win_cond
    ])

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = [[" "]*3 for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)
        print(f"Player {current_player}, enter your move (row and col 0-2):")
        try:
            row, col = map(int, input().split())
            if board[row][col] != " ":
                print("Cell already taken!")
                continue
        except (ValueError, IndexError):
            print("Invalid input.")
            continue

        board[row][col] = current_player

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        elif board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()
