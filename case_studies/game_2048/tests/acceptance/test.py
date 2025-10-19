from unittest.mock import patch


def test_merge_and_move_updates_board() -> None:
    from case_studies.game_2048.src.game_state import GameState, Cell, Direction, DEFAULT_BOARD_SIZE
    row = [Cell(2), Cell(2), Cell.empty(), Cell.empty()]
    board = [row[:] for _ in range(DEFAULT_BOARD_SIZE)]
    gs = GameState(board=board, seed=42)
    new_state = gs.get_next_state(Direction.LEFT)
    assert new_state.board[0][0].value == 4

def test_victory_detection_printed_by_controller() -> None:
    from case_studies.game_2048.src.game_controller import GameController
    from case_studies.game_2048.src.game_state import GameState, Cell, DEFAULT_BOARD_SIZE
    from case_studies.game_2048.src.game_view import GameView
    board = [[Cell.empty() for _ in range(DEFAULT_BOARD_SIZE)] for _ in range(DEFAULT_BOARD_SIZE)]
    board[0][0] = Cell(2048)
    gs = GameState(board=board, seed=0)
    outputs = []
    view = GameView()
    def fake_print(*args, **_):
        outputs.append(' '.join(str(a) for a in args))
    with patch('builtins.print', side_effect=fake_print):
        gc = GameController(view, initial_state=gs)
        cont = gc._loop_cycle()
    assert any('Congratulations' in o for o in outputs)
    assert cont is False

def test_game_over_detection_printed_by_controller() -> None:
    from case_studies.game_2048.src.game_controller import GameController
    from case_studies.game_2048.src.game_state import GameState, Cell
    from case_studies.game_2048.src.game_view import GameView
    # board with no mergeable neighbours
    vals = [[2,4,8,16],[32,64,128,256],[512,1024,2,4],[8,16,32,64]]
    board = [[Cell(v) for v in row] for row in vals]
    gs = GameState(board=board, seed=0)
    outputs = []
    view = GameView()
    def fake_print(*args, **_):
        outputs.append(' '.join(str(a) for a in args))
    with patch('builtins.print', side_effect=fake_print):
        gc = GameController(view, initial_state=gs)
        cont = gc._loop_cycle()
    assert any('Game Over' in o for o in outputs)
    assert cont is False

def test_invalid_input_triggers_invalid_move_message() -> None:
    from case_studies.game_2048.src.game_controller import GameController
    from case_studies.game_2048.src.game_state import GameState
    from case_studies.game_2048.src.game_view import GameView
    gs = GameState.new_game(seed=0)
    outputs = []
    view = GameView()
    def fake_print(*args, **_):
        outputs.append(' '.join(str(a) for a in args))
    with patch('builtins.input', return_value='x'), patch('builtins.print', side_effect=fake_print):
        gc = GameController(view, initial_state=gs)
        cont = gc._loop_cycle()
    assert any('Invalid move' in o for o in outputs)
    assert cont is True

def test_quit_renders_exit_and_stops() -> None:
    from case_studies.game_2048.src.game_controller import GameController
    from case_studies.game_2048.src.game_state import GameState
    from case_studies.game_2048.src.game_view import GameView
    gs = GameState.new_game(seed=0)
    outputs = []
    view = GameView()
    def fake_print(*args, **_):
        outputs.append(' '.join(str(a) for a in args))
    with patch('builtins.input', return_value='q'), patch('builtins.print', side_effect=fake_print):
        gc = GameController(view, initial_state=gs)
        cont = gc._loop_cycle()
    assert any('Exiting game' in o for o in outputs)
    assert cont is False
