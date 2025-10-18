from .game_state import GameState, Direction
from .game_view import GameView

class GameController:

    def __init__(self, initial_state: GameState | None = None):
        if initial_state is None:
            initial_state = GameState.new_game()
        self._state: GameState = initial_state
        self._view = GameView()

    @property
    def state(self) -> GameState:
        return self._state

    def run(self) -> None:
        """Run the main game loop."""
        while True:
            if not self._loop_cycle():
                break

    def _loop_cycle(self) -> bool:
        """Run a single cycle of the game loop."""
        self._view.render(self._convert_state_to_grid())
        if self._state.is_victory():
            self._view.render_victory()
            return False

        if self._state.is_game_over():
            self._view.render_game_over()
            return False
        move = self._view.get_move_input()
        if move == 'q':
            self._view.render_exit()
            return False

        direction = self._convert_input_to_direction(move)
        if direction:
            new_state = self._state.get_next_state(direction)
            if new_state != self._state:
                self._state = new_state
            else:
                self._view.render_invalid_move()
        else:
            self._view.render_invalid_move()
        return True

    def _convert_state_to_grid(self) -> list[list[int]]:
        """Convert the current game state to a grid of integers for rendering."""
        return [[cell.value for cell in row] for row in self._state.board]

    def _convert_input_to_direction(self, move: str) -> Direction | None:
        """Convert user input to a Direction enum."""
        direction_map = {'h': Direction.LEFT, 'j': Direction.DOWN, 'k': Direction.UP, 'l': Direction.RIGHT}
        return direction_map.get(move, None)
