class GameView:
    def render(self, grid: list[list[int]]) -> None:
        for row in grid:
            print("+----" * len(row) + "+")
            print("".join(f"|{str(val).center(4) if val != 0 else '    '}" for val in row) + "|")
        print("+----" * len(grid[0]) + "+")

    def render_victory(self) -> None:
        print("Congratulations! You've reached 2048!")

    def render_game_over(self) -> None:
        print("Game Over! No more moves possible.")

    def get_move_input(self) -> str:
        return input("Enter move (h/j/k/l for left/down/up/right, q to quit): ")

    def render_exit(self) -> None:
        print("Exiting game. Goodbye!")

    def render_invalid_move(self) -> None:
        print("Invalid move. Please try again.")
