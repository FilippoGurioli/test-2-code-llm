from unittest.mock import MagicMock


def test_integration_controller_applies_move_and_updates_state() -> None:
    from case_studies.connect_four.src.controller.game_controller import GameController
    from case_studies.connect_four.src.model.game_state import GameState, Player
    gs = GameState()
    view = MagicMock()
    view.get_move_input.return_value = '1'
    gc = GameController(view=view, init_state=gs)
    gc.loop_cycle()
    assert gc.state is not None
    new_board = gc.state.board
    assert new_board[len(new_board) - 1][0] == Player.RED


def test_integration_controller_detects_winner_from_model() -> None:
    from case_studies.connect_four.src.controller.game_controller import GameController
    from case_studies.connect_four.src.model.game_state import GameState, Player, COL_WIDTH, ROW_WIDTH
    board = [[None for _ in range(COL_WIDTH)] for _ in range(ROW_WIDTH)]
    row = 5
    for c in range(0, 4):
        board[row][c] = Player.YELLOW
    gs = GameState(board=board, starter=Player.YELLOW)
    view = MagicMock()
    gc = GameController(view=view, init_state=gs)
    gc.loop_cycle()
    view.display_winner.assert_called()


def test_integration_controller_draw_when_board_full() -> None:
    from case_studies.connect_four.src.controller.game_controller import GameController
    from case_studies.connect_four.src.model.game_state import GameState, Player, COL_WIDTH, ROW_WIDTH
    from case_studies.connect_four.src.view.game_view import GameView
    def generate_full_draw_board() -> list[list[Player]]:
        counter = 0
        start = Player.RED
        board: list[list[Player]] = []
        for _ in range(ROW_WIDTH):
            if counter % 3 == 0:
                counter = 0
                start = Player.RED if start == Player.YELLOW else Player.YELLOW
            counter += 1
            row: list[Player] = []
            current = start
            for _ in range(COL_WIDTH):
                row.append(current)
                current = Player.RED if current == Player.YELLOW else Player.YELLOW
            board.append(row)
        return board
    full_board = generate_full_draw_board()
    gs = GameState(board=full_board)
    view = MagicMock()
    gc = GameController(view=view, init_state=gs)
    gc.loop_cycle()
    view.display_draw.assert_called_once()
