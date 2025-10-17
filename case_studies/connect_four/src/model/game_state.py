from enum import Enum
from dataclasses import dataclass

class Player(Enum):
    RED = 1
    YELLOW = 2

ROW_WIDTH = 6
COL_WIDTH = 7

@dataclass
class GameState:

    def __init__(self, board: list[list[Player | None]] | None = None, starter: Player = Player.RED) -> None:
        if board is None:
            board = [[None for _ in range(COL_WIDTH)] for _ in range(ROW_WIDTH)]
        self._rows = len(board)
        self._cols = len(board[0]) if board else 0
        self._board = board
        self._current_player = starter
        self._winner = self._check_winner()

    @property
    def board(self) -> list[list[Player | None]]:
        return self._board

    @property
    def current_player(self) -> Player:
        return self._current_player

    @property
    def winner(self) -> Player | None:
        return self._winner

    def is_full(self) -> bool:
        return all(self._board[row][col] is not None for row in range(self._rows) for col in range(self._cols))

    def _check_winner(self) -> Player | None:
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        # explore each cell as a potential starting point
        for row in range(self._rows):
            for col in range(self._cols):
                player = self._board[row][col]
                if player is None:
                    continue
                # explore each direction
                for dr, dc in directions:
                    count = 1
                    r, c = row + dr, col + dc
                    # explore the current direction
                    while 0 <= r < self._rows and 0 <= c < self._cols and self._board[r][c] == player:
                        count += 1
                        if count == 4:
                            return player
                        r += dr
                        c += dc
        return None
