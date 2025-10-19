from unittest.mock import MagicMock


def test_model_and_controller_move_changes_state() -> None:
    from case_studies.game_2048.src.game_state import GameState, Cell
    from case_studies.game_2048.src.game_controller import GameController
    row = [Cell(2), Cell(2), Cell.empty(), Cell.empty()]
    board = [row[:] for _ in range(4)]
    gs = GameState(board=board, seed=0)
    view = MagicMock()
    view.get_move_input.return_value = 'h'
    gc = GameController(view, initial_state=gs)
    cont = gc._loop_cycle()
    assert gc.state.board[0][0].value == 4
    assert cont is True

def test_controller_can_receive_the_initial_state() -> None:
    from case_studies.game_2048.src.game_state import GameState
    from case_studies.game_2048.src.game_controller import GameController
    view = MagicMock()
    gs = GameState.new_game(seed=0)
    gc = GameController(view, initial_state=gs)
    assert gc.state == gs

def test_controller_detects_victory_from_model() -> None:
    from case_studies.game_2048.src.game_state import GameState, Cell
    from case_studies.game_2048.src.game_controller import GameController
    board = [[Cell.empty() for _ in range(4)] for _ in range(4)]
    board[0][0] = Cell(2048)
    gs = GameState(board=board, seed=0)
    view = MagicMock()
    gc = GameController(view, initial_state=gs)
    cont = gc._loop_cycle()
    view.render_victory.assert_called()
    assert cont is False

def test_controller_detects_game_over_from_model() -> None:
    from case_studies.game_2048.src.game_state import GameState, Cell
    from case_studies.game_2048.src.game_controller import GameController
    vals = [[2,4,8,16],[32,64,128,256],[512,1024,2,4],[8,16,32,64]]
    board = [[Cell(v) for v in row] for row in vals]
    gs = GameState(board=board, seed=0)
    view = MagicMock()
    gc = GameController(view, initial_state=gs)
    cont = gc._loop_cycle()
    view.render_game_over.assert_called()
    assert cont is False
