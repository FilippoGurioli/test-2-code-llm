from .game_controller import GameController
from .game_view import GameView

def main() -> None:
    GameController(GameView()).run()

if __name__ == "__main__":
    main()
