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


@dataclass
class Structure:
    shape: Shape
    color: Color


class Tile:
    hex: Hex
    terrain: Terrain
    animal_territory: Optional[AnimalTerritory]
    structure: Optional[Structure]

