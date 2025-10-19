from types import SimpleNamespace
from unittest.mock import MagicMock


class FakeCell:
	def __init__(self, v: int):
		self.value = v


def make_fake_state(board_vals=None, victory=False, game_over=False):
	if board_vals is None:
		board_vals = [[0 for _ in range(4)] for _ in range(4)]
	board = [[FakeCell(v) for v in row] for row in board_vals]
	def is_victory():
		return victory
	def is_game_over():
		return game_over
	def get_next_state(_):
		# return a new distinct state object for testing moves
		return SimpleNamespace(board=board, is_victory=is_victory, is_game_over=is_game_over, get_next_state=lambda d: None)
	return SimpleNamespace(board=board, is_victory=is_victory, is_game_over=is_game_over, get_next_state=get_next_state)


def test_loop_cycle_exit_on_q() -> None:
	from case_studies.game_2048.src.game_controller import GameController

	fake_state = make_fake_state()
	view = MagicMock()
	view.get_move_input.return_value = 'q'
	gc = GameController(view, initial_state=fake_state)
	cont = gc._loop_cycle()
	view.render_exit.assert_called_once()
	assert cont is False


def test_loop_cycle_invalid_input_calls_render_invalid_move() -> None:
	from case_studies.game_2048.src.game_controller import GameController

	fake_state = make_fake_state()
	view = MagicMock()
	view.get_move_input.return_value = 'x'
	gc = GameController(view, initial_state=fake_state)
	cont = gc._loop_cycle()
	view.render_invalid_move.assert_called_once()
	assert cont is True


def test_loop_cycle_valid_move_updates_state_when_changed() -> None:
	from case_studies.game_2048.src.game_controller import GameController
	from case_studies.game_2048.src.game_state import Direction

	base_vals = [[0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
	fake_state = make_fake_state(board_vals=base_vals)
	new_vals = [[2, 0, 0, 0] for _ in range(4)]
	new_state = make_fake_state(board_vals=new_vals)
	def gns(_):
		return new_state
	fake_state.get_next_state = gns
	view = MagicMock()
	view.get_move_input.return_value = 'h'
	gc = GameController(view, initial_state=fake_state)
	cont = gc._loop_cycle()
	assert gc.state is new_state
	assert cont is True


def test_loop_cycle_detects_victory_and_stops() -> None:
	from case_studies.game_2048.src.game_controller import GameController

	fake_state = make_fake_state(victory=True)
	view = MagicMock()
	gc = GameController(view, initial_state=fake_state)
	cont = gc._loop_cycle()
	view.render_victory.assert_called_once()
	assert cont is False


def test_loop_cycle_detects_game_over_and_stops() -> None:
	from case_studies.game_2048.src.game_controller import GameController

	fake_state = make_fake_state(game_over=True)
	view = MagicMock()
	gc = GameController(view, initial_state=fake_state)
	cont = gc._loop_cycle()
	view.render_game_over.assert_called_once()
	assert cont is False


def test_view_render_called_with_converted_grid() -> None:
	from case_studies.game_2048.src.game_controller import GameController

	vals = [[0, 2, 4, 0], [0, 0, 0, 0], [8, 0, 0, 0], [0, 0, 0, 16]]
	fake_state = make_fake_state(board_vals=vals)
	view = MagicMock()
	# input 'q' so loop will stop after render
	view.get_move_input.return_value = 'q'
	gc = GameController(view, initial_state=fake_state)
	gc._loop_cycle()
	assert view.render.called
	args = view.render.call_args[0]
	assert len(args) == 1
	grid_passed = args[0]
	assert isinstance(grid_passed, list)
	assert grid_passed[0][1] == 2
	assert grid_passed[2][0] == 8
