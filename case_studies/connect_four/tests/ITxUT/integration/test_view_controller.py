from unittest.mock import patch

def test_view_and_controller_full_cycle_move_and_quit() -> None:
    from case_studies.connect_four.src.view.game_view import GameView
    from case_studies.connect_four.src.controller.game_controller import GameController
    from case_studies.connect_four.src.model.game_state import GameState
    gv = GameView()
    gs = GameState()
    inputs = ['1', 'q']
    def fake_input(_=''):
        return inputs.pop(0)
    with patch('builtins.input', side_effect=fake_input) as mock_input, patch('builtins.print'):
        gc = GameController(view=gv, init_state=gs)
        gc.loop_cycle()
        if gc.state is not None:
            gc.loop_cycle()
    assert mock_input.call_count >= 1

def test_view_and_controller_displays_invalid_move_for_out_of_range() -> None:
    from case_studies.connect_four.src.view.game_view import GameView
    from case_studies.connect_four.src.controller.game_controller import GameController
    from case_studies.connect_four.src.model.game_state import GameState
    gv = GameView()
    gs = GameState()
    with patch('builtins.input', return_value='999'), patch('builtins.print') as mock_print:
        gc = GameController(view=gv, init_state=gs)
        gc.loop_cycle()
    found = any('Invalid move' in ''.join(call.args) for call in mock_print.call_args_list if call.args)
    assert found
