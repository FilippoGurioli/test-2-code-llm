from types import SimpleNamespace
from unittest.mock import patch, MagicMock


def make_fake_state_2048():
    # minimal fake state with a 4x4 board of zeros and not-victory/not-game-over
    class FakeCell:
        def __init__(self, v=0):
            self.value = v

        def is_empty(self):
            return self.value == 0

    board = [[FakeCell() for _ in range(4)] for _ in range(4)]
    dir = None

    def is_victory():
        return False

    def is_game_over():
        return False

    def get_next_state(_):
        return make_fake_state_2048()

    return SimpleNamespace(board=board, is_victory=is_victory, is_game_over=is_game_over, get_next_state=get_next_state)

def test_controller_quits_if_input_is_quit() -> None:
    from case_studies.game_2048.src.game_controller import GameController
    from case_studies.game_2048.src.game_view import GameView
    gs = make_fake_state_2048()
    view = GameView()
    view.get_move_input = lambda: 'q'
    outputs = []
    def fake_print(*args, **_):
        outputs.append(' '.join(str(a) for a in args))
    with patch('builtins.print', side_effect=fake_print):
        gc = GameController(view, initial_state=gs)
        cont = gc._loop_cycle()
    assert any('Exiting game' in o for o in outputs)
    assert cont is False

def test_controller_parses_valid_move_input() -> None:
    from case_studies.game_2048.src.game_controller import GameController
    from case_studies.game_2048.src.game_view import GameView
    from case_studies.game_2048.src.game_state import Direction
    gs = MagicMock(
        board=[[MagicMock() for _ in range(4)] for _ in range(4)],
        is_victory=MagicMock(return_value=False),
        is_game_over=MagicMock(return_value=False),
        get_next_state=MagicMock()
    )
    view = GameView()
    view.get_move_input = lambda: 'h'
    gc = GameController(view, initial_state=gs)
    cont = gc._loop_cycle()
    gs.get_next_state.assert_called_with(Direction.LEFT)
    assert cont is True

def test_controller_query_victory() -> None:
    from case_studies.game_2048.src.game_controller import GameController
    from case_studies.game_2048.src.game_view import GameView
    gs = MagicMock(
        board=[[MagicMock() for _ in range(4)] for _ in range(4)],
        is_victory=MagicMock(return_value=True),
        is_game_over=MagicMock(return_value=False),
        get_next_state=MagicMock()
    )
    view = GameView()
    view.get_move_input = lambda: 'h'
    view.render_victory = MagicMock()
    gc = GameController(view, initial_state=gs)
    cont = gc._loop_cycle()
    view.render_victory.assert_called()
    assert cont is False

def test_controller_query_game_over() -> None:
    from case_studies.game_2048.src.game_controller import GameController
    from case_studies.game_2048.src.game_view import GameView
    gs = MagicMock(
        board=[[MagicMock() for _ in range(4)] for _ in range(4)],
        is_victory=MagicMock(return_value=False),
        is_game_over=MagicMock(return_value=True),
        get_next_state=MagicMock()
    )
    view = GameView()
    view.get_move_input = lambda: 'h'
    view.render_game_over = MagicMock()
    gc = GameController(view, initial_state=gs)
    cont = gc._loop_cycle()
    view.render_game_over.assert_called()
    assert cont is False

def test_controller_query_invalid_move() -> None:
    from case_studies.game_2048.src.game_controller import GameController
    from case_studies.game_2048.src.game_view import GameView
    gs = MagicMock(
        board=[[MagicMock() for _ in range(4)] for _ in range(4)],
        is_victory=MagicMock(return_value=False),
        is_game_over=MagicMock(return_value=False),
        get_next_state=MagicMock()
    )
    view = GameView()
    view.get_move_input = lambda: 'x'  # invalid input
    outputs = []
    def fake_print(*args, **_):
        outputs.append(' '.join(str(a) for a in args))
    with patch('builtins.print', side_effect=fake_print):
        gc = GameController(view, initial_state=gs)
        cont = gc._loop_cycle()
    assert any('Invalid move' in o for o in outputs)
    assert cont is True
