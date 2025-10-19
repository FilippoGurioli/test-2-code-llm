class DummyView:
    """Minimal view used for integration tests.

    Implemented inline so tests only reference controller and model modules.
    Captures events in `events` for assertions.
    """
    def __init__(self, inputs=None):
        self._inputs = list(inputs or [])
        self.events = []
    def render(self, game_state) -> None:
        # integration tests don't need full rendering; record a marker
        self.events.append(("render", tuple(cell.value if cell is not None else None for cell in game_state.board)))

    def display_winner(self, winner: str) -> None:
        self.events.append(("winner", winner))

    def display_draw(self) -> None:
        self.events.append(("draw", True))

    def get_move_input(self, _=None) -> str:
        if not self._inputs:
            return "q"
        return self._inputs.pop(0)

    def display_exit(self) -> None:
        self.events.append(("exit", True))

    def display_invalid_move(self) -> None:
        self.events.append(("invalid", True))

def test_compute_next_state_winner() -> None:
    from case_studies.tic_tac_toe.src.controller.game_controller import GameController
    from case_studies.tic_tac_toe.src.model.game_state import GameState, Symbol
    board = [Symbol.X, Symbol.X, Symbol.X, None, None, None, None, None, None]
    state = GameState(board=board, starter=Symbol.X)
    view = DummyView()
    controller = GameController(view=view, state=state)
    next_state = controller.compute_next_state(state)
    assert next_state is None
    assert view.events == [
        ("render", ("X", "X", "X", None, None, None, None, None, None)),
        ("winner", "X"),
    ]

def test_compute_next_state_draw() -> None:
    from case_studies.tic_tac_toe.src.controller.game_controller import GameController
    from case_studies.tic_tac_toe.src.model.game_state import GameState, Symbol
    board = [
        Symbol.X,
        Symbol.O,
        Symbol.X,
        Symbol.X,
        Symbol.O,
        Symbol.O,
        Symbol.O,
        Symbol.X,
        Symbol.X,
    ]
    state = GameState(board=board, starter=Symbol.X)
    view = DummyView()
    controller = GameController(view=view, state=state)
    next_state = controller.compute_next_state(state)
    assert next_state is None
    assert view.events == [
        ("render", ("X", "O", "X", "X", "O", "O", "O", "X", "X")),
        ("draw", True),
    ]

def test_compute_next_state_quit() -> None:
    from case_studies.tic_tac_toe.src.controller.game_controller import GameController
    from case_studies.tic_tac_toe.src.model.game_state import GameState, Symbol
    board = [None] * 9
    state = GameState(board=board, starter=Symbol.X)
    view = DummyView(inputs=["q"])
    controller = GameController(view=view, state=state)
    next_state = controller.compute_next_state(state)
    assert next_state is None
    assert view.events == [
        ("render", (None, None, None, None, None, None, None, None, None)),
        ("exit", True),
    ]

def test_apply_move() -> None:
    from case_studies.tic_tac_toe.src.controller.game_controller import GameController
    from case_studies.tic_tac_toe.src.model.game_state import GameState, Symbol
    board = [None] * 9
    state = GameState(board=board, starter=Symbol.X)
    view = DummyView()
    controller = GameController(view=view, state=state)

    new_state = controller.apply_move(state, 0)
    assert new_state is not None
    assert new_state.board[0] == Symbol.X
    assert new_state.current_symbol == Symbol.O

    new_state = controller.apply_move(state, 9)
    assert new_state is None

    state_with_move = GameState(board=[Symbol.X] + [None] * 8, starter=Symbol.O)
    new_state = controller.apply_move(state_with_move, 0)
    assert new_state is None
