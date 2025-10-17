"""Minimal CLI Connect Four game used as a case study."""

def main() -> None:
    from .model.game_state import GameState
    from .view.game_view import GameView
    from .controller.game_controller import GameController

    view: GameView = GameView()
    controller: GameController = GameController(view)

    while controller.state is not None:
        controller.loop_cycle()


if __name__ == "__main__":
    main()
