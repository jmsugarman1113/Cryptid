from __future__ import annotations
from enum import StrEnum, auto
from dataclasses import dataclass, replace
from typing import Optional, Any
from Hex import Hex


class Terrain(StrEnum):
    WATER = auto().upper()
    MOUNTAIN = auto().upper()
    FOREST = auto().upper()
    SWAMP = auto().upper()
    DESERT = auto().upper()


class AnimalTerritory(StrEnum):
    BEAR = auto().upper()
    COUGAR = auto().upper()


class Color(StrEnum):
    WHITE = auto().upper()
    GREEN = auto().upper()
    BLUE = auto().upper()
    BLACK = auto().upper()


class Shape(StrEnum):
    STANDING_STONE = auto().upper()
    ABANDONED_SHACK = auto().upper()


class PlayerName(StrEnum):
    PLAYER1 = auto().upper()
    PLAYER2 = auto().upper()
    PLAYER3 = auto().upper()
    PLAYER4 = auto().upper()
    PLAYER5 = auto().upper()


@dataclass
class Structure:
    shape: Shape
    color: Color


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



