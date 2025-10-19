def test_render_board(capsys) -> None:
    from types import SimpleNamespace
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    X = SimpleNamespace(value="X")
    O = SimpleNamespace(value="O")
    board = [X, O, None, None, X, None, None, O, None]
    game_state = SimpleNamespace(board=board)
    view = GameView()
    view.render(game_state)
    captured = capsys.readouterr()
    expected_output = "\n X | O | 3\n---+---+---\n 4 | X | 6\n---+---+---\n 7 | O | 9\n\n"
    assert captured.out == expected_output

def test_display_winner(capsys) -> None:
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    view = GameView()
    view.display_winner("X")
    captured = capsys.readouterr()
    assert captured.out == "Player X wins!\n"

def test_display_draw(capsys) -> None:
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    view = GameView()
    view.display_draw()
    captured = capsys.readouterr()
    assert captured.out == "It's a draw!\n"

def test_display_exit(capsys) -> None:
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    view = GameView()
    view.display_exit()
    captured = capsys.readouterr()
    assert captured.out == "Exiting game. Goodbye!\n"

def test_display_invalid_move(capsys) -> None:
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    view = GameView()
    view.display_invalid_move()
    captured = capsys.readouterr()
    assert captured.out == "Invalid move. Try again.\n"

def test_get_move_input(monkeypatch) -> None:
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    view = GameView()
    monkeypatch.setattr("builtins.input", lambda _: "5")
    move = view.get_move_input("doesn't matter")
    assert move == "5"
