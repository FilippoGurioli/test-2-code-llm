def test_constructor() -> None:
    from case_studies.tic_tac_toe.src.controller.game_controller import GameController
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    view = GameView()
    controller = GameController(view)
    assert controller.view == view
    from case_studies.tic_tac_toe.src.model.game_state import Symbol
    assert controller.state.board == [None] * 9
    assert controller.state.current_symbol == Symbol.X

def test_parse_move() -> None:
    from case_studies.tic_tac_toe.src.controller.game_controller import GameController
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    view = GameView()
    controller = GameController(view)
    assert controller.parse_move("1") == 0
    assert controller.parse_move(" 5 ") == 4
    assert controller.parse_move("9") == 8
    assert controller.parse_move("0") is None
    assert controller.parse_move("10") is None
    assert controller.parse_move("a") is None
    assert controller.parse_move("") is None

def test_apply_move() -> None:
    from case_studies.tic_tac_toe.src.controller.game_controller import GameController
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    from case_studies.tic_tac_toe.src.model.game_state import GameState, Symbol
    view = GameView()
    controller = GameController(view)
    state = GameState.new_game()
    new_state = controller.apply_move(state, 0)
    assert new_state is not None
    assert new_state.board[0] == Symbol.X
    assert new_state.current_symbol == Symbol.O
    new_state2 = controller.apply_move(new_state, 0)
    assert new_state2 is None
    new_state3 = controller.apply_move(new_state, 9)
    assert new_state3 is None

def test_compute_next_state(monkeypatch) -> None:
    from case_studies.tic_tac_toe.src.controller.game_controller import GameController
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    from case_studies.tic_tac_toe.src.model.game_state import GameState, Symbol
    view = GameView()
    controller = GameController(view)
    moves = ["1","2","3","5","6","4","8","7","9"]
    monkeypatch.setattr("builtins.input", lambda _: moves.pop(0))
    state = GameState.new_game()
    while state is not None:
        state = controller.compute_next_state(state)
    assert state is None  # Game should end after a series of valid moves
