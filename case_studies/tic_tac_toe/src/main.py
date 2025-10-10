"""Minimal CLI Tic-Tac-Toe game used as a case study."""

def main() -> None:
    from case_studies.tic_tac_toe.src.model.game_state import GameState
    from case_studies.tic_tac_toe.src.view.game_view import GameView
    from case_studies.tic_tac_toe.src.controller.game_controller import GameController

    view: GameView = GameView()
    controller: GameController = GameController(view)
    state: GameState = controller.state

    while state is not None:
        state = controller.compute_next_state(state)


if __name__ == "__main__":
    main()
