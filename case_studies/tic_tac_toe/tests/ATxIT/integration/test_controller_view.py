def test_controller_view_win(capsys, monkeypatch) -> None:
    """Play a short sequence of moves that leads to a win for X and assert output."""
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    from case_studies.tic_tac_toe.src.controller.game_controller import GameController

    moves = iter(["1", "4", "2", "5", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(moves))
    view = GameView()
    controller = GameController(view)
    state = controller.state
    while state is not None:
        state = controller.compute_next_state(state)
    captured = capsys.readouterr()
    assert "Player X wins!" in captured.out


def test_controller_view_draw(capsys, monkeypatch) -> None:
    """Play a full-game sequence that ends in a draw and assert output."""
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    from case_studies.tic_tac_toe.src.controller.game_controller import GameController
    moves = iter(["1", "3", "2", "4", "5", "8", "6", "9", "7"])
    monkeypatch.setattr("builtins.input", lambda _: next(moves))
    view = GameView()
    controller = GameController(view)
    state = controller.state
    while state is not None:
        state = controller.compute_next_state(state)
    captured = capsys.readouterr()
    assert "It's a draw!" in captured.out


def test_controller_view_quit(capsys, monkeypatch) -> None:
    """Start a game and quit early; assert exit message is printed."""
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    from case_studies.tic_tac_toe.src.controller.game_controller import GameController
    moves = iter(["1", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(moves))
    view = GameView()
    controller = GameController(view)
    state = controller.state
    while state is not None:
        state = controller.compute_next_state(state)
    captured = capsys.readouterr()
    assert "Exiting game. Goodbye!" in captured.out
