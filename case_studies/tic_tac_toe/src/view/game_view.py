from ..model.game_state import GameState, Symbol

class GameView:
    def render(self, game_state: GameState) -> None:
        b = [c.value if c is not None else str(i + 1) for i, c in enumerate(game_state.board)]
        print()
        print(f" {b[0]} | {b[1]} | {b[2]}")
        print("---+---+---")
        print(f" {b[3]} | {b[4]} | {b[5]}")
        print("---+---+---")
        print(f" {b[6]} | {b[7]} | {b[8]}")
        print()

    def display_winner(self, winner: str) -> None:
        print(f"Player {winner} wins!")

    def display_draw(self) -> None:
        print("It's a draw!")

    def get_move_input(self, player: str) -> str:
        return input(f"Player {player}, enter move (1-9) or q to quit: ")

    def display_exit(self) -> None:
        print("Exiting game. Goodbye!")

    def display_invalid_move(self) -> None:
        print("Invalid move. Try again.")
