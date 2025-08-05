from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum, auto, unique
from types import NotImplementedType
from typing import Any, Optional

from cryptid.hex import Hex


class UpperStrEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[str]) -> str:
        return name.upper()


@unique
class Terrain(UpperStrEnum):
    WATER = auto()
    MOUNTAIN = auto()
    FOREST = auto()
    SWAMP = auto()
    DESERT = auto()


@unique
class AnimalTerritory(UpperStrEnum):
    BEAR = auto()
    COUGAR = auto()


@unique
class Color(UpperStrEnum):
    WHITE = auto()
    GREEN = auto()
    BLUE = auto()
    BLACK = auto()


@unique
class Shape(UpperStrEnum):
    STANDING_STONE = auto()
    ABANDONED_SHACK = auto()


@unique
class PlayerName(UpperStrEnum):
    PLAYER1 = auto()
    PLAYER2 = auto()
    PLAYER3 = auto()
    PLAYER4 = auto()
    PLAYER5 = auto()


@dataclass(frozen=True)
class Structure:
    shape: Shape
    color: Color

    def __str__(self) -> str:
        return f"Structure(shape={self.shape.value}, color={self.color.value})"


@dataclass
class Tile:
    hex: Hex
    terrain: Terrain
    animal_territory: Optional[AnimalTerritory] = None
    structure: Optional[Structure] = None

    def __add__(self, other: Any) -> Tile | NotImplementedType:
        if isinstance(other, Tile):
            return replace(self, hex=self.hex + other.hex)
        if isinstance(other, Hex):
            return replace(self, hex=self.hex + other)
        return NotImplemented

    def __radd__(self, other: Any) -> Tile | NotImplementedType:
        return self.__add__(other)

    def __sub__(self, other: Any) -> Tile | NotImplementedType:
        if isinstance(other, Tile):
            return replace(self, hex=self.hex - other.hex)
        if isinstance(other, Hex):
            return replace(self, hex=self.hex - other)
        return NotImplemented

    def __rsub__(self, other: Any) -> Tile | NotImplementedType:
        return -self + other

    def __mul__(self, other: Any) -> Tile | NotImplementedType:
        if not isinstance(other, int):
            return NotImplemented
        return replace(self, hex=other * self.hex)

    def __rmul__(self, other: Any) -> Tile | NotImplementedType:
        return self.__mul__(other)

    def __neg__(self) -> Tile | NotImplementedType:
        return replace(self, hex=-self.hex)

    # def __str__(self) -> str:
    #     attr_strs = [
    #         f"hex={str(self.hex)}",
    #         f"terrain=Terrain.{self.terrain.value}",
    #     ]
    #     if self.animal_territory is not None:
    #         attr_strs.append(f"animal_territory={self.animal_territory.value}")
    #     if self.structure is not None:
    #         attr_strs.append(f"structure={str(self.structure)}")
    #     attr_str = ", ".join(attr_strs)
    #     return f"Tile({attr_str})"
