"""Module defining the game state of 2048."""

import random
from enum import Enum

class Direction(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

class Cell:
    """Class representing a cell in the 2048 game."""

    def __init__(self, value: int, is_merged: bool = False) -> None:
        if value < 0 or (value & (value - 1)) != 0:
            raise ValueError(f"Cell value must be a power of 2 or 0, got {value}")
        self._value = value
        self._is_merged = is_merged

    @staticmethod
    def empty() -> 'Cell':
        return Cell(0)

    @staticmethod
    def spawn(seed: int | None = None) -> 'Cell':
        """Spawn a new cell with value 2 or 4 at the given position."""
        if seed is not None:
            random.seed(seed)
        # 10% chance of spawning a 4, otherwise spawn a 2
        value = 4 if random.random() < 0.1 else 2
        return Cell(value)

    @property
    def value(self) -> int:
        return self._value

    @property
    def is_merged(self) -> bool:
        return self._is_merged

    def is_empty(self) -> bool:
        return self._value == 0

    def is_mergeable_with(self, other: 'Cell') -> bool:
        return self._value == other.value and not self._is_merged and not other.is_merged

    def merge_with(self, other: 'Cell') -> 'Cell':
        if not self.is_mergeable_with(other):
            raise ValueError(f"Cells {self} and {other} cannot be merged")
        return Cell(self._value * 2, is_merged=True)

    def __str__(self) -> str:
        return str(f"C:{self._value} (merged: {self._is_merged})")


DEFAULT_BOARD_SIZE = 4

class GameState:

    def __init__(self, board: list[list[Cell]] | None = None, seed: int | None = None) -> None:
        if board is None:
            board = GameState.new_game(seed)._board
        self._board = board
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
        self._random = random.Random(seed)

    @staticmethod
    def new_game(seed: int | None = None) -> 'GameState':
        """Return a new game state with only 2 cells."""
        board = [[Cell.empty() for _ in range(DEFAULT_BOARD_SIZE)] for _ in range(DEFAULT_BOARD_SIZE)]
        gs = GameState(board, seed)
        gs._spawn_cell()
        gs._spawn_cell()
        return gs

    def _spawn_cell(self) -> None:
        """Spawn a new cell in a random empty position on the board."""
        if self.is_full():
            raise ValueError("Cannot spawn new cell on a full board") from None
        empty_positions = [(r, c) for r in range(DEFAULT_BOARD_SIZE) for c in range(DEFAULT_BOARD_SIZE) if self._board[r][c].is_empty()]
        r, c = self._random.choice(empty_positions)
        self._board[r][c] = Cell.spawn(self._random.randint(0, 2**32 - 1))

    def is_full(self) -> bool:
        """Check if the board is full."""
        return all(not cell.is_empty() for row in self._board for cell in row)

    def is_game_over(self) -> bool:
        """Check if the game is over (no moves possible)."""
        if not self.is_full():
            return False
        for r in range(DEFAULT_BOARD_SIZE):
            for c in range(DEFAULT_BOARD_SIZE):
                cell = self._board[r][c]
                # Check right
                if c + 1 < DEFAULT_BOARD_SIZE and cell.is_mergeable_with(self._board[r][c + 1]):
                    return False
                # Check down
                if r + 1 < DEFAULT_BOARD_SIZE and cell.is_mergeable_with(self._board[r + 1][c]):
                    return False
        return True

    def is_victory(self) -> bool:
        """Check if the player has won (a cell with value 2048 exists)."""
        return any(cell.value == 2048 for row in self._board for cell in row)

    @property
    def board(self) -> list[list[Cell]]:
        """Get the current board."""
        return self._board

    def get_next_state(self, direction: Direction) -> 'GameState':
        """Return the next game state after moving in the given direction."""
        # Deep copy of board
        board = [[Cell(cell.value, cell.is_merged) for cell in row] for row in self._board]
        # Transform according to direction
        board = self._transform_board(board, direction)
        # Move rows
        moved = False
        new_board: list[list[Cell]] = []
        for row in board:
            new_row, row_moved = self._move_row_left(row)
            new_board.append(new_row)
            moved = moved or row_moved
        # Reverse transform
        new_board = self._inverse_transform_board(new_board, direction)
        for row in new_board:
            for cell in row:
                cell._is_merged = False
        new_state = GameState(new_board, seed=self._random.randint(0, 2**32 - 1))
        # If anything moved, spawn a new cell
        if moved:
            new_state._spawn_cell()
        return new_state

    def _transform_board(self, board: list[list[Cell]], direction: Direction) -> list[list[Cell]]:
        if direction == Direction.UP:
            return self._transpose(board)
        elif direction == Direction.DOWN:
            return self._reverse_rows(self._transpose(board))
        elif direction == Direction.RIGHT:
            return self._reverse_rows(board)
        return board

    def _inverse_transform_board(self, board: list[list[Cell]], direction: Direction) -> list[list[Cell]]:
        if direction == Direction.UP:
            return self._transpose(board)
        elif direction == Direction.DOWN:
            return self._transpose(self._reverse_rows(board))
        elif direction == Direction.RIGHT:
            return self._reverse_rows(board)
        return board

    def _transpose(self, board: list[list[Cell]]) -> list[list[Cell]]:
        return [list(row) for row in zip(*board)]

    def _reverse_rows(self, board: list[list[Cell]]) -> list[list[Cell]]:
        return [list(reversed(row)) for row in board]

    def _move_row_left(self, row: list[Cell]) -> tuple[list[Cell], bool]:
        """Slide and merge a single row to the left. Returns (new_row, moved)."""
        # Filter non-empty
        non_empty = [c for c in row if not c.is_empty()]
        merged: list[Cell] = []
        moved = False
        skip = False
        for i in range(len(non_empty)):
            if skip:
                skip = False
                continue
            if i + 1 < len(non_empty) and non_empty[i].is_mergeable_with(non_empty[i + 1]):
                merged.append(non_empty[i].merge_with(non_empty[i + 1]))
                skip = True
                moved = True
            else:
                merged.append(non_empty[i])
        # Fill with empties
        merged += [Cell.empty() for _ in range(len(row) - len(merged))]
        # Detect if anything moved
        if [c.value for c in merged] != [c.value for c in row]:
            moved = True
        return merged, moved
