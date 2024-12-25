from enum import StrEnum, auto
from dataclasses import dataclass
from typing import Optional
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
    STONE = auto().upper()
    SHACK = auto().upper()


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




