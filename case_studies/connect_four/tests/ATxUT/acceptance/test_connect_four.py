from unittest.mock import patch


def run_game_with_inputs(inputs):
    from case_studies.connect_four.src.view.game_view import GameView
    from case_studies.connect_four.src.controller.game_controller import GameController
    from case_studies.connect_four.src.model.game_state import GameState
    gv = GameView()
    gs = GameState()
    outputs = []
    def fake_print(*args, **_):
        outputs.append(' '.join(str(a) for a in args))
    def fake_input(_=''):
        return inputs.pop(0)
    with patch('builtins.print', side_effect=fake_print), patch('builtins.input', side_effect=fake_input):
        gc = GameController(view=gv, init_state=gs)
        while gc.state is not None:
            gc.loop_cycle()
    return outputs

def test_acceptance_horizontal_win() -> None:
    moves = [
        '1',  # R -> col 0
        '7',  # Y
        '2',  # R -> col 1
        '7',  # Y
        '3',  # R -> col 2
        '7',  # Y
        '4',  # R -> col 3 -> win
    ]
    outputs = run_game_with_inputs(moves)
    assert any('wins' in o for o in outputs)


def test_acceptance_vertical_win() -> None:
    moves = [
        '1',  # R
        '2',  # Y
        '1',  # R
        '2',  # Y
        '1',  # R
        '2',  # Y
        '1',  # R -> win vertically
    ]
    outputs = run_game_with_inputs(moves)
    assert any('wins' in o for o in outputs)


def test_acceptance_diagonal_win() -> None:
    moves = [
        '1', '2',
        '2', '3',
        '3', '4',
        '3', '4',
        '4', '5',
        '4',
    ]
    outputs = run_game_with_inputs(moves)
    assert any('wins' in o for o in outputs)

def test_acceptance_draw() -> None:
    moves = [
        '1', '2', '1', '2', '1', '2',
        '3', '4', '3', '4', '3', '4',
        '5', '6', '5', '6', '5', '6',
        '7', '1', '7', '1', '7', '1',
        '2', '3', '2', '3', '2', '3',
        '4', '5', '4', '5', '4', '5',
        '6', '7', '6', '7', '6', '7',
    ]
    outputs = run_game_with_inputs(moves)
    assert any("draw" in o.lower() for o in outputs)
