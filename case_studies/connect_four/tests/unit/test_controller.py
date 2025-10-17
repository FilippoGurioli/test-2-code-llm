from types import SimpleNamespace
from unittest.mock import MagicMock

def make_fake_state(board, winner=None, current_player=None, is_full=False):
    def _is_full():
        return is_full
    return SimpleNamespace(board=board, winner=winner, current_player=current_player, is_full=_is_full)

def test_loop_cycle_with_winner_calls_display_winner_and_clears_state(monkeypatch) -> None:
    from case_studies.connect_four.src.controller.game_controller import GameController
    from case_studies.connect_four.src.model.game_state import Player
    board = [[None for _ in range(7)] for _ in range(6)]
    fake_state = make_fake_state(board=board, winner=Player.RED, current_player=Player.RED, is_full=False)
    view = MagicMock()
    gc = GameController(view=view, init_state=fake_state)
    gc.loop_cycle()
    assert view.display_board.called
    view.display_winner.assert_called_once_with(Player.RED.value)
    assert gc.state is None

def test_loop_cycle_with_full_board_calls_display_draw_and_clears_state(monkeypatch) -> None:
    from case_studies.connect_four.src.controller.game_controller import GameController
    board = [[None for _ in range(7)] for _ in range(6)]
    fake_state = make_fake_state(board=board, winner=None, current_player=None, is_full=True)
    view = MagicMock()
    gc = GameController(view=view, init_state=fake_state)
    gc.loop_cycle()
    view.display_draw.assert_called_once()
    assert gc.state is None

def test_loop_cycle_quit_calls_display_exit_and_clears_state(monkeypatch) -> None:
    from case_studies.connect_four.src.controller.game_controller import GameController
    from case_studies.connect_four.src.model.game_state import Player
    board = [[None for _ in range(7)] for _ in range(6)]
    fake_state = make_fake_state(board=board, winner=None, current_player=Player.YELLOW, is_full=False)
    view = MagicMock()
    view.get_move_input.return_value = ' q '
    gc = GameController(view=view, init_state=fake_state)
    gc.loop_cycle()
    view.display_exit.assert_called_once()
    assert gc.state is None

def test_loop_cycle_invalid_input_calls_display_invalid_move_and_keeps_state(monkeypatch) -> None:
    from case_studies.connect_four.src.controller.game_controller import GameController
    from case_studies.connect_four.src.model.game_state import Player
    board = [[None for _ in range(7)] for _ in range(6)]
    fake_state = make_fake_state(board=board, winner=None, current_player=Player.RED, is_full=False)
    view = MagicMock()
    view.get_move_input.return_value = 'not-a-number'
    gc = GameController(view=view, init_state=fake_state)
    gc.loop_cycle()
    view.display_invalid_move.assert_called_once()
    assert gc.state is fake_state

def test_loop_cycle_valid_move_creates_new_state_via_GameState_and_sets_state(monkeypatch) -> None:
    from case_studies.connect_four.src.controller import game_controller as controller_module
    from case_studies.connect_four.src.controller.game_controller import GameController
    from case_studies.connect_four.src.model.game_state import Player
    rows, cols = 6, 7
    board = [[None for _ in range(cols)] for _ in range(rows)]
    board[rows - 1][0] = Player.RED
    fake_state = make_fake_state(board=board, winner=None, current_player=Player.RED, is_full=False)
    view = MagicMock()
    view.get_move_input.return_value = '2'
    fake_new_state = object()
    fake_GameState = MagicMock(return_value=fake_new_state)
    monkeypatch.setattr(controller_module, 'GameState', fake_GameState)
    gc = GameController(view=view, init_state=fake_state)
    gc.loop_cycle()
    fake_GameState.assert_called_once()
    call_kwargs = fake_GameState.call_args.kwargs
    assert 'board' in call_kwargs and 'starter' in call_kwargs
    new_board = call_kwargs['board']
    assert new_board[rows - 1][1] == Player.RED
    assert call_kwargs['starter'] == Player.YELLOW
    assert gc.state is fake_new_state
