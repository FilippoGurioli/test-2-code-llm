import pytest


def test_cell_invalid_value_raises() -> None:
	from case_studies.game_2048.src.game_state import Cell

	with pytest.raises(ValueError):
		Cell(3)  # not a power of two


def test_cell_merge_and_properties() -> None:
	from case_studies.game_2048.src.game_state import Cell

	a = Cell(2)
	b = Cell(2)
	assert a.is_mergeable_with(b)
	merged = a.merge_with(b)
	assert merged.value == 4
	assert merged.is_merged is True
	# originals unchanged
	assert a.value == 2 and b.value == 2

def test_cell_merge_invalid_raises() -> None:
    from case_studies.game_2048.src.game_state import Cell

    a = Cell(2)
    b = Cell(4)
    with pytest.raises(ValueError):
        a.merge_with(b)  # different values cannot merge

def test_cell_factory_empty() -> None:
    from case_studies.game_2048.src.game_state import Cell

    empty_cell = Cell.empty()
    assert empty_cell.value == 0
    assert empty_cell.is_empty() is True

def test_cell_factory_spawn() -> None:
    from case_studies.game_2048.src.game_state import Cell

    cell = Cell.spawn(seed=42)
    assert cell.value in (2, 4)


def test_move_row_left_merges_into_four_and_spawns() -> None:
	from case_studies.game_2048.src.game_state import GameState, Cell, Direction

	# prepare a board where first row will merge when moved left
	row = [Cell(2), Cell(2), Cell.empty(), Cell.empty()]
	board = [row[:] for _ in range(4)]
	gs = GameState(board=board, seed=0)

	new_state = gs.get_next_state(Direction.LEFT)

	# first cell merged to 4
	assert new_state.board[0][0].value == 4
	# merged flag must be reset after get_next_state
	assert all(not cell.is_merged for r in new_state.board for cell in r)


def test_get_next_state_no_move_returns_equivalent_board() -> None:
	from case_studies.game_2048.src.game_state import GameState, Cell, Direction

	board = [[Cell.empty() for _ in range(4)] for _ in range(4)]
	gs = GameState(board=board, seed=0)
	new_state = gs.get_next_state(Direction.LEFT)

	# since there was no movement, values should remain all zeros
	assert all(cell.value == 0 for row in new_state.board for cell in row)


def test_is_full_and_is_game_over() -> None:
	from case_studies.game_2048.src.game_state import GameState, Cell

	# full board with no mergeable neighbors
	vals = [[2,4,8,16],[32,64,128,256],[512,1024,2,4],[8,16,32,64]]
	board = [[Cell(v) for v in row] for row in vals]
	gs = GameState(board=board, seed=0)

	assert gs.is_full() is True
	assert gs.is_game_over() is True


def test_is_victory_detects_2048() -> None:
	from case_studies.game_2048.src.game_state import GameState, Cell

	board = [[Cell.empty() for _ in range(4)] for _ in range(4)]
	board[2][1] = Cell(2048)
	gs = GameState(board=board, seed=0)

	assert gs.is_victory() is True

def test_new_game_factory() -> None:
    from case_studies.game_2048.src.game_state import GameState
    gs = GameState.new_game()
    assert gs is not None
    # assert that there are two non-empty cells on the board
    non_empty_cells = sum(1 for row in gs.board for cell in row if not cell.is_empty())
    assert non_empty_cells == 2
