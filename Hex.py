from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Annotated
from dataclasses import dataclass


@dataclass
class FixedLength:
    length: int


class Hex(ABC):
    @property
    @abstractmethod
    def coordinates_in_2d(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def distance(self, other: Hex) -> int:
        pass

    @abstractmethod
    def __add__(self, other: Any) -> Hex:
        pass

    @abstractmethod
    def __sub__(self, other: Any) -> Hex:
        pass

    @property
    @abstractmethod
    def neighbor_directions(self) -> Annotated[list[Hex], FixedLength(6)]:
        pass

    @property
    def neighbors(self) -> Annotated[list[Hex], FixedLength(6)]:
        return [self + dir for dir in self.neighbor_directions]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Hex):
            raise NotImplementedError
        return self.distance(other) == 0

    def __ne__(self, other: Any) -> bool:
        return not (self == other)


class DoubleCoordinateHex(Hex, ABC):
    row: int
    col: int

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = row

        assert (row + col) % 2 == 0, f"A doubled coordinate hex must have its coordinates be of the same parity"

    @property
    def coordinates_in_2d(self) -> tuple[int, int]:
        return self.row, self.col

    def __add__(self, other: Any) -> DoubleCoordinateHex:
        if isinstance(other, DoubleCoordinateHex):
            return DoubleCoordinateHex(self.row + other.row, self.col + other.col)
        raise TypeError(f"other needs to be an instance of DoubleCoordinateHex")

    def __sub__(self, other: Any) -> DoubleCoordinateHex:
        if isinstance(other, DoubleCoordinateHex):
            return DoubleCoordinateHex(self.row - other.row, self.col - other.col)
        raise TypeError(f"other needs to be an instance of DoubleCoordinateHex")


class DoubledHeightCoordinateHex(DoubleCoordinateHex):
    @property
    def neighbor_directions(self) -> list[DoubledHeightCoordinateHex]:
        return [
            DoubledHeightCoordinateHex(1, 1),
            DoubledHeightCoordinateHex(1, -1),
            DoubledHeightCoordinateHex(0, -2),
            DoubledHeightCoordinateHex(-1, -1),
            DoubledHeightCoordinateHex(-1, 1),
            DoubledHeightCoordinateHex(0, 2),
        ]

    def distance(self, other: DoubleCoordinateHex) -> int:
        dcol = abs(self.col - other.col)
        drow = abs(self.row - other.row)
        return dcol + max(0, (drow-dcol)//2)


class DoubledWidthCoordinateHex(DoubleCoordinateHex):
    @property
    def neighbor_directions(self) -> list[DoubledWidthCoordinateHex]:
        return [
            DoubledWidthCoordinateHex(2, 0),
            DoubledWidthCoordinateHex(1, -1),
            DoubledWidthCoordinateHex(-1, -1),
            DoubledWidthCoordinateHex(-2, 0),
            DoubledWidthCoordinateHex(-1, 1),
            DoubledWidthCoordinateHex(1, 1),
        ]

    def distance(self, other: DoubledWidthCoordinateHex) -> int:
        dcol = abs(self.col - other.col)
        drow = abs(self.row - other.row)
        return drow + max(0, (dcol - drow) // 2)

