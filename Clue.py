from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Annotated, Final, ClassVar
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

    @abstractmethod
    def describe(self) -> str:
        """
        describes the clue in plain english
        converts back to the language of the clue in the cluebook
        :return: str
        """
        pass

    def __str__(self) -> str:
        not_str = "not " if self.negated else ""
        return f"The habitat is {not_str} {self.describe()}"


@dataclass(frozen=True)
class OnOneOfTwoTerrainClue(Clue):
    """
    Cryptid is in one of two habitats
    """
    valid_terrains: Annotated[list[Terrain], FixedLength(2)]
    negated: bool = False

    def resolve(self, tile: Tile, board: Board) -> bool:
        return tile.terrain in self.valid_terrains

    def describe(self) -> str:
        return f"on {self.valid_terrains[0].value.lower()} or {self.valid_terrains[1].value.lower()}"


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

    def describe(self) -> str:
        return f"within one space of {self.terrain.value.lower()}"


@dataclass(frozen=True)
class WithinOneSpaceOfEitherAnimalTerritoryClue(Clue):
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

    def describe(self) -> str:
        return f"within one space of either animal territory"


@dataclass(frozen=True)
class WithinTwoSpacesOfShapeClue(Clue):
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

    def describe(self) -> str:
        shape_str = ' '.join(self.shape.value.lower().split('_'))
        return f"within two spaces of a {shape_str}"


@dataclass(frozen=True)
class WithinTwoSpacesOfAnimalTerritoryClue(Clue):
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

    def describe(self) -> str:
        return f"within two spaces of {self.animal_territory.value.lower()} territory"


@dataclass(frozen=True)
class WithinThreeSpacesOfColorClue(Clue):
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

    def describe(self) -> str:
        return f"within three spaces of a {self.color.value.lower()} structure"


RED_CLUES: Final[Annotated[list[Clue], FixedLength(96)]] = [
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.MOUNTAIN]),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.MOUNTAIN),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.MOUNTAIN], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.WATER], negated=True),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.SWAMP], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.SWAMP, Terrain.MOUNTAIN]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.WATER]),
    WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE, negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.FOREST),
    WithinThreeSpacesOfColorClue(color=Color.WHITE),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.MOUNTAIN], negated=True),
    WithinOneSpaceOfEitherAnimalTerritoryClue(negated=True),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.COUGAR),
    WithinThreeSpacesOfColorClue(color=Color.BLUE),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.SWAMP),
    WithinThreeSpacesOfColorClue(color=Color.GREEN),
    WithinTwoSpacesOfShapeClue(shape=Shape.ABANDONED_SHACK),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER], negated=True),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.COUGAR, negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.ABANDONED_SHACK, negated=True),
]

GREEN_CLUES: Final[Annotated[list[Clue], FixedLength(96)]] = [

]

BLUE_CLUES: Final[Annotated[list[Clue], FixedLength(96)]] = [

]

BROWN_CLUES: Final[Annotated[list[Clue], FixedLength(96)]] = [

]

PURPLE_CLUES: Final[Annotated[list[Clue], FixedLength(96)]] = [

]


# name aliases based on player symbols, may delete later
ALPHA_CLUES = RED_CLUES
BETA_CLUES = GREEN_CLUES
GAMMA_CLUES = BLUE_CLUES
DELTA_CLUES = BROWN_CLUES
EPSILON_CLUES = PURPLE_CLUES
