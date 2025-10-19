def test_draw(capsys, monkeypatch) -> None:
    from case_studies.tic_tac_toe.src.main import main
    moves = iter(["1", "3", "2", "4", "5", "8", "6", "9", "7"])
    monkeypatch.setattr("builtins.input", lambda _: next(moves))
    main()
    captured = capsys.readouterr()
    assert "It's a draw!" in captured.out

def test_win(capsys, monkeypatch) -> None:
    from case_studies.tic_tac_toe.src.main import main
    moves = iter(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    monkeypatch.setattr("builtins.input", lambda _: next(moves))
    main()
    captured = capsys.readouterr()
    assert "Player X wins!" in captured.out

def test_quit(capsys, monkeypatch) -> None:
    from case_studies.tic_tac_toe.src.main import main
    moves = iter(["1", "2", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(moves))
    main()
    captured = capsys.readouterr()
    assert "Exiting game. Goodbye!" in captured.out
