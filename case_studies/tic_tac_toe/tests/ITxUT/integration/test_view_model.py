def test_view_renders_board_and_winner(capsys) -> None:
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    from case_studies.tic_tac_toe.src.model.game_state import GameState, Symbol
    board = [Symbol.X, Symbol.X, Symbol.X, None, None, None, None, None, None]
    state = GameState(board=board, starter=Symbol.X)
    view = GameView()
    view.render(state)
    view.display_winner(state.check_winner().value)
    captured = capsys.readouterr()
    assert " X | X | X" in captured.out
    assert "Player X wins!" in captured.out


def test_view_renders_draw(capsys) -> None:
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    from case_studies.tic_tac_toe.src.model.game_state import GameState, Symbol
    board = [
        Symbol.X,
        Symbol.O,
        Symbol.X,
        Symbol.X,
        Symbol.O,
        Symbol.O,
        Symbol.O,
        Symbol.X,
        Symbol.X,
    ]
    state = GameState(board=board, starter=Symbol.X)
    view = GameView()
    view.render(state)
    assert state.is_full()
    assert state.check_winner() is None
    view.display_draw()
    captured = capsys.readouterr()
    assert "It's a draw!" in captured.out
