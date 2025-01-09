from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Annotated
from Hex import FixedLength
from Tile import Tile, Terrain, AnimalTerritory, Shape, Color
from Board import Board


@dataclass(frozen=True)
class Clue(ABC):
    negated: bool

    @abstractmethod
    def resolve(self, tile: Tile, board: Board) -> bool:
        """
        Resolve the rule as if it was the base game (not advanced)
        :param tile: the tile to check
        :param board: the board setup
        :return: if the cryptid can be there
        """
        pass

    def check_space(self, tile: Tile, board: Board) -> bool:
        """
        return if the cryptid can be on this tile according to this clue
        :param tile: the tile to check
        :param board: the board setup
        :return: if the cryptid can be there
        """
        output = self.resolve(tile, board)
        return output if not self.negated else not output


@dataclass(frozen=True)
class OnOneOfTwoTerrainClue(Clue):
    """
    Cryptid is in one of two habitats
    """
    valid_terrains: Annotated[list[Terrain], FixedLength[2]]
    negated: bool = False

    def resolve(self, tile: Tile, board: Board) -> bool:
        return tile.terrain in self.valid_terrains


@dataclass(frozen=True)
class WithinOneSpaceOfTerrainClue(Clue):
    """
    Cryptid is either on or adjacent to a specific terrain
    """
    terrain: Terrain
    negated: bool = False

    def resolve(self, tile: Tile, board: Board) -> bool:
        possible_hex_locations = tile.hex.hexes_within_range(1)
        for hex in possible_hex_locations:
            if (possible_tile := board.tiles.get(hex, None)) is not None:
                if possible_tile.terrain == self.terrain:
                    return True
        return False
        # return any((possible_tile := board.tiles.get(hex, None)) is not None and possible_tile.terrain == self.terrain for hex in curr_tile.hex.hexes_within_range(1))


@dataclass(frozen=True)
class WithinOneSpaceOfAnimalTerritory(Clue):
    """
    Cryptid is either on or adjacent to any animal territory
    """
    negated: bool = False

    def resolve(self, tile: Tile, board: Board) -> bool:
        possible_hex_locations = tile.hex.hexes_within_range(1)
        for hex in possible_hex_locations:
            if (possible_tile := board.tiles.get(hex, None)) is not None:
                if possible_tile.animal_territory is not None:
                    return True
        return False
        # return any((possible_tile := board.tiles.get(hex, None)) is not None and possible_tile.animal_territory is not None for hex in curr_tile.hex.hexes_within_range(1))


@dataclass(frozen=True)
class WithinTwoSpacesOfShape(Clue):
    """
    Cruptid is within 2 spaces of a specific type (shape) of structure
    """
    shape: Shape
    negated: bool = False

    def resolve(self, tile: Tile, board: Board) -> bool:
        possible_hex_locations = tile.hex.hexes_within_range(2)
        for hex in possible_hex_locations:
            if (possible_tile := board.tiles.get(hex, None)) is not None:
                if getattr(possible_tile.structure, 'shape', None) == self.shape:
                    return True
        return False
        # return any((possible_tile := board.tiles.get(hex, None)) is not None and getattr(possible_tile.structure, 'shape', None) == self.shape for hex in curr_tile.hex.hexes_within_range(2))


@dataclass(frozen=True)
class WithinTwoSpacesOfAnimalTerritory(Clue):
    """
    Cryptid is within 2 spaces a specific animal territory
    """
    animal_territory: AnimalTerritory
    negated: bool = False

    def resolve(self, tile: Tile, board: Board) -> bool:
        possible_hex_locations = tile.hex.hexes_within_range(2)
        for hex in possible_hex_locations:
            if (possible_tile := board.tiles.get(hex, None)) is not None:
                if possible_tile.animal_territory == self.animal_territory:
                    return True
        return False
        # return any((possible_tile := board.tiles.get(hex, None)) is not None and possible_tile.animal_territory == self.animal_territory for hex in curr_tile.hex.hexes_within_range(2))


@dataclass(frozen=True)
class WithinThreeSpacesOfColor(Clue):
    """
    Cryptid is within 3 spaces of a color of structure
    """
    color: Color
    negated: bool = False

    def resolve(self, tile: Tile, board: Board) -> bool:
        possible_hex_locations = tile.hex.hexes_within_range(3)
        for hex in possible_hex_locations:
            if (possible_tile := board.tiles.get(hex, None)) is not None:
                if getattr(possible_tile.structure, 'color', None) == self.color:
                    return True
        return False
        # return any((possible_tile := board.tiles.get(hex, None)) is not None and getattr(possible_tile.structure, 'color', None) == self.shape for hex in curr_tile.hex.hexes_within_range(3))
