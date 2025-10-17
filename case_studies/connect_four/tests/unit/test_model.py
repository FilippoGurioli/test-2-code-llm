def test_init_calls_check_winner_and_print(monkeypatch) -> None:
    from case_studies.connect_four.src.model.game_state import GameState, Player
    called = {}
    def fake_check_winner(_) -> None:
        called['invoked'] = True
        return Player.RED
    monkeypatch.setattr(GameState, "_check_winner", fake_check_winner)
    gs = GameState()
    assert called.get('invoked', False) is True
    assert gs.winner == Player.RED

def test_is_full_true_and_false() -> None:
    from case_studies.connect_four.src.model.game_state import GameState, Player
    full_board = [[Player.RED for _ in range(7)] for _ in range(6)]
    gs_full = GameState(board=full_board)
    assert gs_full.is_full() is True
    not_full_board = [[Player.RED for _ in range(7)] for _ in range(6)]
    not_full_board[0][0] = None
    gs_not_full = GameState(board=not_full_board)
    assert gs_not_full.is_full() is False

def test_winner_detection_horizontal() -> None:
    from case_studies.connect_four.src.model.game_state import GameState, Player
    board = [[None for _ in range(7)] for _ in range(6)]
    row = 2
    for c in range(1, 5):
        board[row][c] = Player.YELLOW
    gs = GameState(board=board)
    assert gs.winner == Player.YELLOW

def test_winner_detection_vertical() -> None:
    from case_studies.connect_four.src.model.game_state import GameState, Player
    board = [[None for _ in range(7)] for _ in range(6)]
    col = 3
    for r in range(1, 5):
        board[r][col] = Player.RED
    gs = GameState(board=board)
    assert gs.winner == Player.RED

def test_winner_detection_diagonal() -> None:
    from case_studies.connect_four.src.model.game_state import GameState, Player
    board = [[None for _ in range(7)] for _ in range(6)]
    coords = [(0, 0), (1, 1), (2, 2), (3, 3)]
    for r, c in coords:
        board[r][c] = Player.YELLOW
    gs = GameState(board=board)
    assert gs.winner == Player.YELLOW
