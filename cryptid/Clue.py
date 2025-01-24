from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Annotated, Any, Final

from cryptid.Hex import FixedLength
from cryptid.Tile import AnimalTerritory, Color, Shape, Terrain, Tile

if TYPE_CHECKING:
    from cryptid.Board import Board


@dataclass(frozen=True)
class Clue(ABC):
    """
    Clue describing where the cryptid can or cannot be located
    """

    @property
    @abstractmethod
    def neg(self) -> bool:
        pass

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
        return output if not self.neg else not output

    @abstractmethod
    def describe(self) -> str:
        """
        describes the clue in plain english
        converts back to the language of the clue in the clue book
        :return: str
        """
        pass

    def __str__(self) -> str:
        not_str = "not " if self.neg else ""
        return f"The habitat is {not_str}{self.describe()}"


@dataclass(frozen=True)
class OnOneOfTwoTerrainClue(Clue):
    """
    cryptid is in one of two habitats
    """

    valid_terrains: Annotated[list[Terrain], FixedLength(2)]
    negated: bool = False

    def __post_init__(self):
        if (num_terrains := len(self.valid_terrains)) != 2:
            raise ValueError(f"must pass 2 valid terrains, got {num_terrains} instead")
        if self.valid_terrains[0] == self.valid_terrains[1]:
            raise ValueError(f"must pass 2 different valid terrains, got 2 of {self.valid_terrains[0].value} instead")

    def __hash__(self) -> int:
        terrains_sorted = sorted(self.valid_terrains)
        return hash((terrains_sorted[0], terrains_sorted[1], self.negated))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError(f"can only compare same types of clues, trying to compare {type(self)} to {type(other)}")
        return (self.negated == other.negated) and (sorted(self.valid_terrains) == sorted(other.valid_terrains))

    @property
    def neg(self) -> bool:
        return self.negated

    def resolve(self, tile: Tile, board: Board) -> bool:
        return tile.terrain in self.valid_terrains

    def describe(self) -> str:
        return f"on {self.valid_terrains[0].value.lower()} or {self.valid_terrains[1].value.lower()}"


@dataclass(frozen=True)
class WithinOneSpaceOfTerrainClue(Clue):
    """
    cryptid is either on or adjacent to a specific terrain
    """

    terrain: Terrain
    negated: bool = False

    @property
    def neg(self) -> bool:
        return self.negated

    def resolve(self, tile: Tile, board: Board) -> bool:
        for possible_hex in tile.hex.hexes_within_range(1):
            if (possible_tile := board.tiles.get(possible_hex, None)) is not None:
                if possible_tile.terrain == self.terrain:
                    return True
        return False
        # return any(
        #   (possible_tile := board.tiles.get(possible_hex, None)) is not None
        #   and possible_tile.terrain == self.terrain
        #   for possible_hex in curr_tile.hex.hexes_within_range(1)
        # )

    def describe(self) -> str:
        return f"within one space of {self.terrain.value.lower()}"


@dataclass(frozen=True)
class WithinOneSpaceOfEitherAnimalTerritoryClue(Clue):
    """
    cryptid is either on or adjacent to any animal territory
    """

    negated: bool = False

    @property
    def neg(self) -> bool:
        return self.negated

    def resolve(self, tile: Tile, board: Board) -> bool:
        for possible_hex in tile.hex.hexes_within_range(1):
            if (possible_tile := board.tiles.get(possible_hex, None)) is not None:
                if possible_tile.animal_territory is not None:
                    return True
        return False
        # return any(
        #   (possible_tile := board.tiles.get(possible_hex, None)) is not None
        #   and possible_tile.animal_territory is not None
        #   for possible_hex in curr_tile.hex.hexes_within_range(1)
        # )

    def describe(self) -> str:
        return "within one space of either animal territory"


@dataclass(frozen=True)
class WithinTwoSpacesOfShapeClue(Clue):
    """
    cryptid is within 2 spaces of a specific type (shape) of structure
    """

    shape: Shape
    negated: bool = False

    @property
    def neg(self) -> bool:
        return self.negated

    def resolve(self, tile: Tile, board: Board) -> bool:
        for possible_hex in tile.hex.hexes_within_range(2):
            if (possible_tile := board.tiles.get(possible_hex, None)) is not None:
                if getattr(possible_tile.structure, "shape", None) == self.shape:
                    return True
        return False
        # return any(
        #   (possible_tile := board.tiles.get(possible_hex, None)) is not None
        #   and getattr(possible_tile.structure, 'shape', None) == self.shape
        #   for possible_hex in curr_tile.hex.hexes_within_range(2)
        # )

    def describe(self) -> str:
        shape_str = self.shape.value.lower().replace("_", " ")
        return f"within two spaces of a {shape_str}"


@dataclass(frozen=True)
class WithinTwoSpacesOfAnimalTerritoryClue(Clue):
    """
    cryptid is within 2 spaces a specific animal territory
    """

    animal_territory: AnimalTerritory
    negated: bool = False

    @property
    def neg(self) -> bool:
        return self.negated

    def resolve(self, tile: Tile, board: Board) -> bool:
        for possible_hex in tile.hex.hexes_within_range(2):
            if (possible_tile := board.tiles.get(possible_hex, None)) is not None:
                if possible_tile.animal_territory == self.animal_territory:
                    return True
        return False
        # return any(
        #   (possible_tile := board.tiles.get(possible_hex, None)) is not None
        #   and possible_tile.animal_territory == self.animal_territory
        #   for possible_hex in curr_tile.hex.hexes_within_range(2)
        # )

    def describe(self) -> str:
        return f"within two spaces of {self.animal_territory.value.lower()} territory"


@dataclass(frozen=True)
class WithinThreeSpacesOfColorClue(Clue):
    """
    cryptid is within 3 spaces of a color of structure
    """

    color: Color
    negated: bool = False

    @property
    def neg(self) -> bool:
        return self.negated

    def resolve(self, tile: Tile, board: Board) -> bool:
        for possible_hex in tile.hex.hexes_within_range(3):
            if (possible_tile := board.tiles.get(possible_hex, None)) is not None:
                if getattr(possible_tile.structure, "color", None) == self.color:
                    return True
        return False
        # return any(
        #   (possible_tile := board.tiles.get(possible_hex, None)) is not None
        #   and getattr(possible_tile.structure, 'color', None) == self.shape
        #   for possible_hex in curr_tile.hex.hexes_within_range(3)
        # )

    def describe(self) -> str:
        return f"within three spaces of a {self.color.value.lower()} structure"


# fmt: off
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

    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER]),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER]),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.SWAMP),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.MOUNTAIN]),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.FOREST),
    WithinThreeSpacesOfColorClue(color=Color.BLACK),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.SWAMP], negated=True),
    WithinThreeSpacesOfColorClue(color=Color.GREEN),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.SWAMP]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.SWAMP, Terrain.MOUNTAIN], negated=True),
    WithinThreeSpacesOfColorClue(color=Color.BLUE),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.MOUNTAIN, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.DESERT], negated=True),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.SWAMP, Terrain.MOUNTAIN], negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.ABANDONED_SHACK, negated=True),
    WithinThreeSpacesOfColorClue(color=Color.WHITE, negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.DESERT, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.SWAMP]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.MOUNTAIN], negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.SWAMP], negated=True),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.COUGAR),

    WithinOneSpaceOfEitherAnimalTerritoryClue(negated=True),
    WithinOneSpaceOfEitherAnimalTerritoryClue(),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.SWAMP], negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.MOUNTAIN),
    WithinThreeSpacesOfColorClue(color=Color.WHITE, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.SWAMP]),
    WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.MOUNTAIN]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.DESERT]),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.SWAMP, negated=True),
    WithinThreeSpacesOfColorClue(color=Color.BLACK, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.SWAMP, Terrain.WATER], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.SWAMP]),
    WithinThreeSpacesOfColorClue(color=Color.GREEN, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.MOUNTAIN], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.MOUNTAIN], negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.DESERT),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.MOUNTAIN]),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.DESERT, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.SWAMP]),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.DESERT),
    WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.MOUNTAIN], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.SWAMP, Terrain.MOUNTAIN]),

    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.WATER], negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.FOREST, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.DESERT], negated=True),
    WithinThreeSpacesOfColorClue(color=Color.WHITE, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.DESERT]),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.FOREST, negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.MOUNTAIN, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.MOUNTAIN]),
    WithinThreeSpacesOfColorClue(color=Color.BLUE, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.SWAMP], negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.ABANDONED_SHACK),
    WithinOneSpaceOfEitherAnimalTerritoryClue(),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER, negated=True),
    WithinThreeSpacesOfColorClue(color=Color.BLUE, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.WATER]),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.SWAMP, negated=True),
    WithinThreeSpacesOfColorClue(color=Color.BLACK, negated=True),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.MOUNTAIN]),
    WithinThreeSpacesOfColorClue(color=Color.BLACK),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.COUGAR, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.SWAMP]),
    WithinThreeSpacesOfColorClue(color=Color.GREEN, negated=True),
]

GREEN_CLUES: Final[Annotated[list[Clue], FixedLength(96)]] = [
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.SWAMP]),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.COUGAR),
    WithinThreeSpacesOfColorClue(color=Color.BLUE),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.SWAMP], negated=True),
    WithinThreeSpacesOfColorClue(color=Color.GREEN),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.DESERT),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.SWAMP], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.SWAMP]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.SWAMP], negated=True),
    WithinThreeSpacesOfColorClue(color=Color.BLACK, negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.ABANDONED_SHACK),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.DESERT, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.WATER]),
    WithinThreeSpacesOfColorClue(color=Color.WHITE, negated=True),
    WithinOneSpaceOfEitherAnimalTerritoryClue(negated=True),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.SWAMP, Terrain.MOUNTAIN], negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.MOUNTAIN),
    WithinThreeSpacesOfColorClue(color=Color.BLACK, negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.SWAMP, negated=True),
    WithinThreeSpacesOfColorClue(color=Color.BLACK),
    WithinThreeSpacesOfColorClue(color=Color.GREEN, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.DESERT], negated=True),

    WithinOneSpaceOfTerrainClue(terrain=Terrain.SWAMP),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.MOUNTAIN], negated=True),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.MOUNTAIN]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.SWAMP, Terrain.MOUNTAIN]),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.COUGAR, negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.SWAMP]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER]),
    WithinThreeSpacesOfColorClue(color=Color.BLUE),
    WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.MOUNTAIN]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.SWAMP], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.SWAMP], negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.ABANDONED_SHACK, negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.MOUNTAIN, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.MOUNTAIN], negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.FOREST),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR),
    WithinOneSpaceOfEitherAnimalTerritoryClue(negated=True),
    WithinThreeSpacesOfColorClue(color=Color.GREEN),
    WithinOneSpaceOfEitherAnimalTerritoryClue(),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.MOUNTAIN]),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR, negated=True),

    WithinOneSpaceOfTerrainClue(terrain=Terrain.MOUNTAIN),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER], negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.FOREST, negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.ABANDONED_SHACK, negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.ABANDONED_SHACK),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.SWAMP),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.DESERT, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.SWAMP], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.MOUNTAIN], negated=True),
    WithinThreeSpacesOfColorClue(color=Color.BLACK),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.FOREST, negated=True),
    WithinThreeSpacesOfColorClue(color=Color.BLUE, negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.WATER]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER], negated=True),
    WithinThreeSpacesOfColorClue(color=Color.WHITE),
    WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.COUGAR),
    WithinOneSpaceOfEitherAnimalTerritoryClue(),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER, negated=True),
    WithinThreeSpacesOfColorClue(color=Color.BLUE, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.DESERT], negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.FOREST),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.MOUNTAIN], negated=True),

    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.SWAMP]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.MOUNTAIN]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.SWAMP, Terrain.MOUNTAIN], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.DESERT]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER]),
    WithinThreeSpacesOfColorClue(color=Color.WHITE, negated=True),
    WithinThreeSpacesOfColorClue(color=Color.WHITE),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.DESERT),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.MOUNTAIN, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.DESERT]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.MOUNTAIN]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.MOUNTAIN], negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.SWAMP]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.WATER], negated=True),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.COUGAR, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.MOUNTAIN]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.SWAMP]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.MOUNTAIN], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.SWAMP, Terrain.MOUNTAIN]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.WATER], negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE, negated=True),
    WithinThreeSpacesOfColorClue(color=Color.GREEN, negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.SWAMP, negated=True),
]

BLUE_CLUES: Final[Annotated[list[Clue], FixedLength(96)]] = [
    WithinThreeSpacesOfColorClue(color=Color.BLUE),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.MOUNTAIN], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.SWAMP]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER], negated=True),
    WithinThreeSpacesOfColorClue(color=Color.BLUE),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.DESERT, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.SWAMP], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.WATER], negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE, negated=True),
    WithinThreeSpacesOfColorClue(color=Color.GREEN),
    WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.WATER]),
    WithinThreeSpacesOfColorClue(color=Color.BLACK, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.SWAMP], negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE, negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.MOUNTAIN, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.MOUNTAIN]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.SWAMP], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.SWAMP]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.DESERT]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.DESERT], negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.MOUNTAIN),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.SWAMP, negated=True),

    WithinThreeSpacesOfColorClue(color=Color.BLACK),
    WithinThreeSpacesOfColorClue(color=Color.BLUE, negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.FOREST),
    WithinThreeSpacesOfColorClue(color=Color.WHITE),
    WithinOneSpaceOfEitherAnimalTerritoryClue(),
    WithinThreeSpacesOfColorClue(color=Color.WHITE, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.SWAMP]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.SWAMP, Terrain.MOUNTAIN]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.SWAMP], negated=True),
    WithinThreeSpacesOfColorClue(color=Color.GREEN, negated=True),
    WithinThreeSpacesOfColorClue(color=Color.GREEN),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.FOREST),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER], negated=True),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.MOUNTAIN]),
    WithinThreeSpacesOfColorClue(color=Color.WHITE),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.MOUNTAIN]),
    WithinThreeSpacesOfColorClue(color=Color.BLUE, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.MOUNTAIN]),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.SWAMP, negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.FOREST, negated=True),
    WithinThreeSpacesOfColorClue(color=Color.BLACK),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.SWAMP]),

    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.COUGAR),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.COUGAR),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.SWAMP, Terrain.MOUNTAIN], negated=True),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR, negated=True),
    WithinOneSpaceOfEitherAnimalTerritoryClue(),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.MOUNTAIN], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.SWAMP], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.MOUNTAIN], negated=True),
    WithinOneSpaceOfEitherAnimalTerritoryClue(negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.WATER], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.MOUNTAIN], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.DESERT], negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER, negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.SWAMP, Terrain.MOUNTAIN], negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.ABANDONED_SHACK),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.SWAMP], negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.MOUNTAIN, negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.DESERT),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.COUGAR, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.SWAMP]),
    WithinTwoSpacesOfShapeClue(shape=Shape.ABANDONED_SHACK),
    WithinThreeSpacesOfColorClue(color=Color.GREEN, negated=True),

    WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.DESERT]),
    WithinOneSpaceOfEitherAnimalTerritoryClue(negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.FOREST, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.MOUNTAIN]),
    WithinTwoSpacesOfShapeClue(shape=Shape.ABANDONED_SHACK, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.MOUNTAIN], negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.MOUNTAIN]),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.DESERT),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER, negated=True),
    WithinTwoSpacesOfShapeClue(shape=Shape.ABANDONED_SHACK, negated=True),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.SWAMP),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER]),
    WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.COUGAR, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.WATER]),
    WithinThreeSpacesOfColorClue(color=Color.BLACK, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.FOREST, Terrain.SWAMP]),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.MOUNTAIN], negated=True),
    WithinThreeSpacesOfColorClue(color=Color.WHITE, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER]),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.MOUNTAIN),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.SWAMP),
    WithinOneSpaceOfTerrainClue(terrain=Terrain.DESERT, negated=True),
    OnOneOfTwoTerrainClue(valid_terrains=[Terrain.SWAMP, Terrain.MOUNTAIN]),
]

BROWN_CLUES: Final[Annotated[list[Clue], FixedLength(96)]] = [

]

PURPLE_CLUES: Final[Annotated[list[Clue], FixedLength(96)]] = [

]
# fmt: on


# name aliases based on player symbols, may delete later
ALPHA_CLUES = RED_CLUES
BETA_CLUES = GREEN_CLUES
GAMMA_CLUES = BLUE_CLUES
DELTA_CLUES = BROWN_CLUES
EPSILON_CLUES = PURPLE_CLUES
