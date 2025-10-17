from enum import Enum

RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

class Cell(Enum):
    EMPTY = f"{RESET}○{RESET}"
    RED = f"{RED}●{RESET}"
    YELLOW = f"{YELLOW}●{RESET}"

class GameView:
    def display_board(self, board: list[list[Cell]]) -> None:
        print()
        for row in board:
            print(" | ".join(cell.value for cell in row))
            print("-" * 26)
        print()

    def display_winner(self, winner: str) -> None:
        print(f"Player {winner} wins!")

    def display_draw(self) -> None:
        print("It's a draw!")

    def get_move_input(self, player: str, columns: int) -> str:
        return input(f"Player {player}, enter column (1-{columns}) or q to quit: ")

    def display_exit(self) -> None:
        print("Exiting game. Goodbye!")

    def display_invalid_move(self) -> None:
        print("Invalid move. Try again.")
