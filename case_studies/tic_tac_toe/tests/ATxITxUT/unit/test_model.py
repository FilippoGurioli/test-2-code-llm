def test_new_game_starts_empty() -> None:
    from case_studies.tic_tac_toe.src.model.game_state import GameState, Symbol
    game_state = GameState.new_game()
    assert all(cell is None for cell in game_state.board)
    assert game_state.current_symbol == Symbol.X
    assert not game_state.is_full()
    assert game_state.check_winner() is None

def test_constructor() -> None:
    from case_studies.tic_tac_toe.src.model.game_state import GameState, Symbol
    board = [Symbol.X, Symbol.O, None, None, Symbol.X, None, None, Symbol.O, None]
    game_state = GameState(board=board, starter=Symbol.O)
    assert game_state.board == board
    assert game_state.current_symbol == Symbol.O
    assert not game_state.is_full()
    assert game_state.check_winner() is None

def test_is_full() -> None:
    from case_studies.tic_tac_toe.src.model.game_state import GameState, Symbol
    full_board = [Symbol.X, Symbol.O, Symbol.X, Symbol.O, Symbol.X, Symbol.O, Symbol.X, Symbol.O, Symbol.X]
    game_state_full = GameState(board=full_board, starter=Symbol.X)
    assert game_state_full.is_full()
    not_full_board = [Symbol.X, Symbol.O, None, None, Symbol.X, None, None, Symbol.O, None]
    game_state_not_full = GameState(board=not_full_board, starter=Symbol.O)
    assert not game_state_not_full.is_full()

def test_check_winner() -> None:
    from case_studies.tic_tac_toe.src.model.game_state import GameState, Symbol
    winning_boards = [
        ([Symbol.X, Symbol.X, Symbol.X, None, None, None, None, None, None], Symbol.X),
        ([None, None, None, Symbol.O, Symbol.O, Symbol.O, None, None, None], Symbol.O),
        ([None, None, None, None, None, None, Symbol.X, Symbol.X, Symbol.X], Symbol.X),
        ([Symbol.O, None, None, Symbol.O, None, None, Symbol.O, None, None], Symbol.O),
        ([None, Symbol.X, None, None, Symbol.X, None, None, Symbol.X, None], Symbol.X),
        ([None, None, Symbol.O, None, None, Symbol.O, None, None, Symbol.O], Symbol.O),
        ([Symbol.X, None, None, None, Symbol.X, None, None, None, Symbol.X], Symbol.X),
        ([None, None, Symbol.O, None, Symbol.O, None, Symbol.O, None, None], Symbol.O),
    ]
    for board, expected_winner in winning_boards:
        game_state = GameState(board=board, starter=Symbol.X)
        assert game_state.check_winner() == expected_winner
    no_winner_board = [Symbol.X, Symbol.O, Symbol.X, Symbol.O, Symbol.X, Symbol.O, Symbol.O, Symbol.X, Symbol.O]
    game_state_no_winner = GameState(board=no_winner_board, starter=Symbol.X)
    assert game_state_no_winner.check_winner() is None
