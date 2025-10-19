from unittest.mock import patch


def test_render_prints_grid() -> None:
	from case_studies.game_2048.src.game_view import GameView

	gv = GameView()
	# small 2x2 grid to keep output predictable
	grid = [[0, 2], [4, 0]]

	outputs = []

	def fake_print(*args, **kwargs):
		# capture printed lines as single string
		outputs.append(' '.join(str(a) for a in args))

	with patch('builtins.print', side_effect=fake_print):
		gv.render(grid)

	# Expect at least one separator line and content lines
	assert any('+----' in o for o in outputs)
	# Values 2 and 4 should appear in the printed output
	assert any('2' in o for o in outputs)
	assert any('4' in o for o in outputs)


def test_render_victory_and_game_over_and_exit_and_invalid_move() -> None:
	from case_studies.game_2048.src.game_view import GameView

	gv = GameView()

	with patch('builtins.print') as mock_print:
		gv.render_victory()
		gv.render_game_over()
		gv.render_exit()
		gv.render_invalid_move()

	# check that print was called for each message
	msgs = [c.args[0] for c in mock_print.call_args_list if c.args]
	assert any('Congratulations' in m for m in msgs)
	assert any('Game Over' in m for m in msgs)
	assert any('Exiting game' in m for m in msgs)
	assert any('Invalid move' in m for m in msgs)


def test_get_move_input_calls_input_and_returns_value() -> None:
	from case_studies.game_2048.src.game_view import GameView

	gv = GameView()
	with patch('builtins.input', return_value='h') as mock_input:
		res = gv.get_move_input()
	mock_input.assert_called_once()
	assert res == 'h'
