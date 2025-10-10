from typing import List, Optional
from ..model.game_state import GameState, Symbol
from ..view.game_view import GameView

class GameController:

    def __init__(self, view: GameView, state: Optional[GameState] = None) -> None:
        self.view = view
        self.state = state if state else GameState.new_game()

    def parse_move(self, text: str) -> Optional[int]:
        try:
            v = int(text.strip())
        except ValueError:
            return None
        if 1 <= v <= 9:
            return v - 1
        return None

    def compute_next_state(self, game_state: GameState) -> Optional[GameState]:
        self.view.render(game_state)
        winner = game_state.check_winner()
        if winner is not None:
            self.view.display_winner(winner.value)
            return game_state
        if game_state.is_full():
            self.view.display_draw()
            return None
        move = self.view.get_move_input(game_state.current_symbol.value).strip().lower()
        if move in ("q", "quit", "exit"):
            self.view.display_exit()
            return None
        pos = self.parse_move(move)
        if pos is None:
            self.view.display_invalid_move()
            return game_state
        new_state = self.apply_move(game_state, pos)
        if new_state is not None:
            return new_state
        else:
            self.view.display_invalid_move()
            return game_state

    def apply_move(self, state: GameState, pos: int) -> Optional[GameState]:
        if pos < 0 or pos >= 9:
            return None
        if state.board[pos] is not None:
            return None

        new_board: List[Optional[Symbol]] = state.board.copy()
        new_board[pos] = state.current_symbol
        new_symbol: Symbol = Symbol.O if state.current_symbol == Symbol.X else Symbol.X
        return GameState(new_board, new_symbol)
