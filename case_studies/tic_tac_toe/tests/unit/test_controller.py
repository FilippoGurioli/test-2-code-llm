def test_constructor() -> None:
    from types import SimpleNamespace
    from case_studies.tic_tac_toe.src.controller.game_controller import GameController

    fake_view = SimpleNamespace()
    fake_state = SimpleNamespace(board=[None] * 9, current_symbol=SimpleNamespace(value="X"))
    controller = GameController(fake_view, state=fake_state)
    assert controller.view == fake_view
    assert controller.state.board == [None] * 9
    assert controller.state.current_symbol.value == "X"

def test_parse_move() -> None:
    from types import SimpleNamespace
    from case_studies.tic_tac_toe.src.controller.game_controller import GameController

    fake_view = SimpleNamespace()
    fake_state = SimpleNamespace(board=[None] * 9, current_symbol=SimpleNamespace(value="X"))
    controller = GameController(fake_view, state=fake_state)
    assert controller.parse_move("1") == 0
    assert controller.parse_move(" 5 ") == 4
    assert controller.parse_move("9") == 8
    assert controller.parse_move("0") is None
    assert controller.parse_move("10") is None
    assert controller.parse_move("a") is None
    assert controller.parse_move("") is None

def test_apply_move() -> None:
    import importlib
    from types import SimpleNamespace
    gc = importlib.import_module("case_studies.tic_tac_toe.src.controller.game_controller")
    class FakeSymbol:
        def __init__(self, name: str):
            self.name = name
        def __eq__(self, other: object) -> bool:
            return isinstance(other, FakeSymbol) and self.name == other.name
        @property
        def value(self) -> str:
            return self.name

    X = FakeSymbol("X")
    O = FakeSymbol("O")
    gc.Symbol = SimpleNamespace(X=X, O=O)

    class FakeGameState:
        def __init__(self, board, starter):
            self._board = board
            self._current = starter
        @property
        def board(self):
            return self._board
        @property
        def current_symbol(self):
            return self._current

    gc.GameState = FakeGameState

    fake_view = SimpleNamespace()
    fake_state = SimpleNamespace(board=[None] * 9, current_symbol=X)
    controller = gc.GameController(fake_view, state=fake_state)

    new_state = controller.apply_move(controller.state, 0)
    assert new_state is not None
    assert new_state.board[0] == X
    assert new_state.current_symbol == O

    new_state2 = controller.apply_move(new_state, 0)
    assert new_state2 is None
    new_state3 = controller.apply_move(new_state, 9)
    assert new_state3 is None

def test_compute_next_state() -> None:
    import importlib
    from types import SimpleNamespace
    gc = importlib.import_module("case_studies.tic_tac_toe.src.controller.game_controller")
    class FakeSymbol:
        def __init__(self, name: str):
            self.name = name
        def __eq__(self, other: object) -> bool:
            return isinstance(other, FakeSymbol) and self.name == other.name
        @property
        def value(self) -> str:
            return self.name

    X = FakeSymbol("X")
    O = FakeSymbol("O")
    gc.Symbol = SimpleNamespace(X=X, O=O)

    class FakeGameState:
        def __init__(self, board, starter):
            self._board = board
            self._current = starter
        @property
        def board(self):
            return self._board
        @property
        def current_symbol(self):
            return self._current
        def check_winner(self):
            lines = [
                (0, 1, 2),
                (3, 4, 5),
                (6, 7, 8),
                (0, 3, 6),
                (1, 4, 7),
                (2, 5, 8),
                (0, 4, 8),
                (2, 4, 6),
            ]
            for a, b, c in lines:
                if self._board[a] is not None and self._board[a] == self._board[b] == self._board[c]:
                    return self._board[a]
            return None
        def is_full(self):
            return all(cell is not None for cell in self._board)

    gc.GameState = FakeGameState

    moves = ["1", "2", "3", "5", "6", "4", "8", "7", "9"]

    class FakeView:
        def __init__(self, moves_list):
            self.moves = moves_list
            self.rendered = 0
        def render(self, state):
            self.rendered += 1
        def display_winner(self, winner):
            pass
        def display_draw(self):
            pass
        def get_move_input(self, player):
            return self.moves.pop(0)
        def display_exit(self):
            pass
        def display_invalid_move(self):
            pass

    fake_view = FakeView(moves)
    fake_state = FakeGameState(board=[None] * 9, starter=X)
    controller = gc.GameController(fake_view, state=fake_state)

    state = controller.state
    while state is not None:
        state = controller.compute_next_state(state)
    assert state is None  # Game should end after a series of valid moves
