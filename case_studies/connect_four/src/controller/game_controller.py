from ..model.game_state import GameState, Player
from ..view.game_view import GameView, Cell

class GameController:
    def __init__(self, view: GameView, init_state: GameState | None = None) -> None:
        self._view = view
        if init_state is None:
            init_state = GameState()
        self._state = init_state

    @property
    def state(self) -> GameState:
        return self._state

    def loop_cycle(self) -> None:
        self._view.display_board(self._convert_board(self._state.board))
        if self._state.winner is not None:
            self._view.display_winner(self._state.winner.value)
            self._state = None
            return
        if self._state.is_full():
            self._view.display_draw()
            self._state = None
            return
        move = self._view.get_move_input(self._state.current_player.value, len(self._state.board[0])).strip().lower()
        if move == "q":
            self._view.display_exit()
            self._state = None
            return
        try:
            col = int(move) - 1
            if col < 0 or col >= len(self._state.board[0]):
                self._view.display_invalid_move()
                return
            for row in reversed(range(len(self._state.board))):
                if self._state.board[row][col] is None:
                    self._state = GameState(
                        board=self._compute_next_board(row, col),
                        starter=Player.RED if self._state.current_player == Player.YELLOW else Player.YELLOW
                    )
                    return
            self._view.display_invalid_move()
            return
        except ValueError:
            self._view.display_invalid_move()
            return

    def _convert_board(self, board: list[list[Player | None]]) -> list[list[Cell]]:
        str_board: list[list[str]] = []
        for row in board:
            str_row: list[str] = []
            for cell in row:
                if cell is None:
                    str_row.append(Cell.EMPTY)
                elif cell == Player.RED:
                    str_row.append(Cell.RED)
                else:
                    str_row.append(Cell.YELLOW)
            str_board.append(str_row)
        return str_board

    def _compute_next_board(self, drop_row: int, drop_col: int) -> list[list[Player | None]]:
        board = [self._state.board[r][:] for r in range(len(self._state.board))]
        board[drop_row][drop_col] = self._state.current_player
        return board
