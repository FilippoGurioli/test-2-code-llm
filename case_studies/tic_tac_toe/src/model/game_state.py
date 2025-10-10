from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class Symbol(str, Enum):
    X = ("X")
    O = ("O")

@dataclass
class GameState:

    def __init__(self, board: List[Optional[Symbol]], starter: Symbol) -> None:
        self._board: List[Optional[Symbol]] = board
        self._current: Symbol = starter

    @staticmethod
    def new_game() -> "GameState":
        return GameState(board=[None] * 9, starter=Symbol.X)

    @property
    def board(self) -> List[Optional[Symbol]]:
        return self._board

    @property
    def current_symbol(self) -> Symbol:
        return self._current

    def is_full(self) -> bool:
        return all(cell is not None for cell in self._board)

    def check_winner(self) -> Optional[Symbol]:
        lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]
        for a, b, c in lines:
            if self._board[a] is not None and self._board[a] == self._board[b] == self._board[c]:
                return self._board[a]
        return None
