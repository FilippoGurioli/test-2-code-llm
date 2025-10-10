"""Minimal CLI Tic-Tac-Toe game used as a case study."""

def main() -> None:
    from .model.game_state import GameState
    from .view.game_view import GameView
    from .controller.game_controller import GameController

    view: GameView = GameView()
    controller: GameController = GameController(view)
    state: GameState = controller.state

    while state is not None:
        state = controller.compute_next_state(state)


if __name__ == "__main__":
    main()
