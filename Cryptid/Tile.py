from __future__ import annotations
from enum import StrEnum, auto
from dataclasses import dataclass, replace
from typing import Optional, Any
from Cryptid.Hex import Hex


class UpperStrEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[str]) -> str:
        return name.upper()


class Terrain(UpperStrEnum):
    WATER = auto()
    MOUNTAIN = auto()
    FOREST = auto()
    SWAMP = auto()
    DESERT = auto()


class AnimalTerritory(UpperStrEnum):
    BEAR = auto()
    COUGAR = auto()


class Color(UpperStrEnum):
    WHITE = auto()
    GREEN = auto()
    BLUE = auto()
    BLACK = auto()


class Shape(UpperStrEnum):
    STANDING_STONE = auto()
    ABANDONED_SHACK = auto()


class PlayerName(UpperStrEnum):
    PLAYER1 = auto()
    PLAYER2 = auto()
    PLAYER3 = auto()
    PLAYER4 = auto()
    PLAYER5 = auto()


@dataclass
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

    def __add__(self, other: Any) -> Tile | NotImplemented:
        if isinstance(other, self.__class__):
            return replace(self, hex=self.hex + other.hex)
        if isinstance(other, self.hex.__class__):
            return replace(self, hex=self.hex + other)
        return NotImplemented

    def __radd__(self, other: Any) -> Tile | NotImplemented:
        return self.__add__(other)

    def __sub__(self, other: Any) -> Tile | NotImplemented:
        if isinstance(other, self.__class__):
            return replace(self, hex=self.hex - other.hex)
        if isinstance(other, self.hex.__class__):
            return replace(self, hex=self.hex - other)
        return NotImplemented

    def __rsub__(self, other: Any) -> Tile | NotImplemented:
        return self.__sub__(other)

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
