import builtins
from unittest.mock import patch


def test_display_board_prints_rows_and_separators() -> None:
    from case_studies.connect_four.src.view.game_view import GameView, Cell
    gv = GameView()
    board = [
        [Cell.EMPTY, Cell.RED, Cell.YELLOW],
        [Cell.RED, Cell.EMPTY, Cell.YELLOW],
    ]
    with patch.object(builtins, 'print') as mock_print:
        gv.display_board(board)
    assert mock_print.call_count >= 1 + len(board) * 2 + 1

def test_display_winner_prints_message() -> None:
    from case_studies.connect_four.src.view.game_view import GameView
    gv = GameView()
    with patch.object(builtins, 'print') as mock_print:
        gv.display_winner('RED')
    mock_print.assert_called_once_with('Player RED wins!')

def test_display_draw_prints_message() -> None:
    from case_studies.connect_four.src.view.game_view import GameView
    gv = GameView()
    with patch.object(builtins, 'print') as mock_print:
        gv.display_draw()
    mock_print.assert_called_once_with("It's a draw!")

def test_get_move_input_calls_input_with_prompt() -> None:
    from case_studies.connect_four.src.view.game_view import GameView
    gv = GameView()
    with patch.object(builtins, 'input', return_value='2') as mock_input:
        res = gv.get_move_input('YELLOW', 7)
    mock_input.assert_called_once()
    assert res == '2'


def test_display_exit_and_invalid_move_prints_messages() -> None:
    from case_studies.connect_four.src.view.game_view import GameView
    gv = GameView()
    with patch.object(builtins, 'print') as mock_print:
        gv.display_exit()
        gv.display_invalid_move()
    actual_msgs = [call.args for call in mock_print.call_args_list if call.args]
    assert ("Exiting game. Goodbye!",) in actual_msgs
    assert (("Invalid move. Try again.",) in actual_msgs)
