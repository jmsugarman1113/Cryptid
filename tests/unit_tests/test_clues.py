from cryptid.clue import (
    Clue,
    NullClue,
    ALPHA_CLUES,
    BETA_CLUES,
    GAMMA_CLUES,
    DELTA_CLUES,
    # EPSILON_CLUES,
    OnOneOfTwoTerrainClue,
    WithinOneSpaceOfTerrainClue,
    WithinOneSpaceOfEitherAnimalTerritoryClue,
    WithinTwoSpacesOfShapeClue,
    WithinTwoSpacesOfAnimalTerritoryClue,
    WithinThreeSpacesOfColorClue,
)
from cryptid.board import Board
from cryptid.setup_card import SETUP_CARDS
from cryptid.hex import DoubledHeightCoordinateHex
from cryptid.tile import Terrain, Shape, Color, AnimalTerritory
import pytest


@pytest.fixture
def board() -> Board:
    return Board.from_setup_card(SETUP_CARDS[0])


class TestClues:
    def test_clue_books(self):
        for clue_book in [
            ALPHA_CLUES,
            BETA_CLUES,
            GAMMA_CLUES,
            DELTA_CLUES,
            # EPSILON_CLUES,
        ]:
            assert len(clue_book) == 97
            assert isinstance(clue_book[0], NullClue)
            assert all(isinstance(clue, Clue) and not isinstance(clue, NullClue) for clue in clue_book[1:])


class TestNullClue:
    def test_errors(self):
        clue = NullClue()

        with pytest.raises(TypeError, match="Incorrectly invoking a Null Clue"):
            _ = clue.describe()

        with pytest.raises(TypeError, match="Incorrectly invoking a Null Clue"):
            _ = clue.neg

    def test_check_space(self, board):
        clue = NullClue()
        tile = board.tiles[DoubledHeightCoordinateHex.origin()]

        with pytest.raises(TypeError, match="Incorrectly invoking a Null Clue"):
            _ = clue.check_space(tile, board)


class TestOnOneOfTwoTerrainClue:
    def test_instantiation(self):
        _ = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.DESERT])

        with pytest.raises(ValueError):
            _ = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER])

        with pytest.raises(ValueError):
            _ = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.DESERT, Terrain.FOREST])

        with pytest.raises(ValueError):
            _ = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.WATER])

    def test_hash(self):
        clue1 = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.DESERT])
        clue2 = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER])
        assert hash(clue1) == hash(clue2)
        assert id(clue1) != id(clue2)

        clue3 = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.FOREST])
        assert hash(clue1) != hash(clue3)

        dummy_dict = {clue1: "A", clue2: "B", clue3: "C"}
        assert len(dummy_dict) == 2
        assert dummy_dict[clue1] == "B"

    def test_equality(self):
        clue1 = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.DESERT])
        clue2 = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER])
        assert clue1 == clue2
        assert id(clue1) != id(clue2)

        clue3 = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.FOREST])
        assert clue1 != clue3

        with pytest.raises(TypeError):
            _ = clue1 == WithinOneSpaceOfTerrainClue(Terrain.WATER)

    def test_str(self):
        clue = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.DESERT])
        assert str(clue) == "The habitat is on water or desert"

        clue = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.DESERT, Terrain.WATER], negated=True)
        assert str(clue) == "The habitat is not on desert or water"

    def test_check_space(self, board):
        clue = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.DESERT])

        # locations and expected resolution
        trials: list[tuple[DoubledHeightCoordinateHex, bool]] = [
            (DoubledHeightCoordinateHex(1, 1), True),
            (DoubledHeightCoordinateHex(3, 7), True),
            (DoubledHeightCoordinateHex(0, 10), False),
            (DoubledHeightCoordinateHex(4, 16), False),
            (DoubledHeightCoordinateHex(6, 12), True),
            (DoubledHeightCoordinateHex(10, 8), False),
            (DoubledHeightCoordinateHex(7, 5), True),
        ]

        for location, outcome in trials:
            tile = board.tiles[location]
            assert clue.check_space(tile, board) == outcome

    def test_check_space_negated(self, board):
        clue = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.DESERT], negated=True)

        # locations and expected resolution
        trials: list[tuple[DoubledHeightCoordinateHex, bool]] = [
            (DoubledHeightCoordinateHex(1, 1), True),
            (DoubledHeightCoordinateHex(3, 7), True),
            (DoubledHeightCoordinateHex(0, 10), False),
            (DoubledHeightCoordinateHex(4, 16), False),
            (DoubledHeightCoordinateHex(6, 12), True),
            (DoubledHeightCoordinateHex(10, 8), False),
            (DoubledHeightCoordinateHex(7, 5), True),
        ]
        for location, outcome in trials:
            tile = board.tiles[location]
            assert clue.check_space(tile, board) != outcome


class TestWithinOneSpaceOfTerrainClue:
    def test_str(self):
        clue = WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER)
        assert str(clue) == "The habitat is within one space of water"

        clue = WithinOneSpaceOfTerrainClue(terrain=Terrain.FOREST, negated=True)
        assert str(clue) == "The habitat is not within one space of forest"

    def test_check_space(self, board):
        clue = WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER)

        # locations and expected resolution
        trials: list[tuple[DoubledHeightCoordinateHex, bool]] = [
            (DoubledHeightCoordinateHex(1, 1), False),
            (DoubledHeightCoordinateHex(3, 7), True),
            (DoubledHeightCoordinateHex(0, 10), False),
            (DoubledHeightCoordinateHex(4, 16), False),
            (DoubledHeightCoordinateHex(6, 12), True),
            (DoubledHeightCoordinateHex(10, 8), False),
            (DoubledHeightCoordinateHex(7, 5), True),
        ]

        for location, outcome in trials:
            tile = board.tiles[location]
            assert clue.check_space(tile, board) == outcome

    def test_check_space_negated(self, board):
        clue = WithinOneSpaceOfTerrainClue(terrain=Terrain.WATER, negated=True)

        # locations and expected resolution
        trials: list[tuple[DoubledHeightCoordinateHex, bool]] = [
            (DoubledHeightCoordinateHex(1, 1), False),
            (DoubledHeightCoordinateHex(3, 7), True),
            (DoubledHeightCoordinateHex(0, 10), False),
            (DoubledHeightCoordinateHex(4, 16), False),
            (DoubledHeightCoordinateHex(6, 12), True),
            (DoubledHeightCoordinateHex(10, 8), False),
            (DoubledHeightCoordinateHex(7, 5), True),
        ]

        for location, outcome in trials:
            tile = board.tiles[location]
            assert clue.check_space(tile, board) != outcome


class TestWithinOneSpaceOfEitherAnimalTerritoryClue:
    def test_str(self):
        clue = WithinOneSpaceOfEitherAnimalTerritoryClue()
        assert str(clue) == "The habitat is within one space of either animal territory"

        clue = WithinOneSpaceOfEitherAnimalTerritoryClue(negated=True)
        assert str(clue) == "The habitat is not within one space of either animal territory"

    def test_check_space(self, board):
        clue = WithinOneSpaceOfEitherAnimalTerritoryClue()

        # locations and expected resolution
        trials: list[tuple[DoubledHeightCoordinateHex, bool]] = [
            (DoubledHeightCoordinateHex(1, 1), True),
            (DoubledHeightCoordinateHex(3, 7), False),
            (DoubledHeightCoordinateHex(0, 10), True),
            (DoubledHeightCoordinateHex(4, 16), False),
            (DoubledHeightCoordinateHex(6, 12), True),
            (DoubledHeightCoordinateHex(10, 6), True),
            (DoubledHeightCoordinateHex(7, 5), False),
        ]

        for location, outcome in trials:
            tile = board.tiles[location]
            assert clue.check_space(tile, board) == outcome

    def test_check_space_negated(self, board):
        clue = WithinOneSpaceOfEitherAnimalTerritoryClue(negated=True)

        # locations and expected resolution
        trials: list[tuple[DoubledHeightCoordinateHex, bool]] = [
            (DoubledHeightCoordinateHex(1, 1), True),
            (DoubledHeightCoordinateHex(3, 7), False),
            (DoubledHeightCoordinateHex(0, 10), True),
            (DoubledHeightCoordinateHex(4, 16), False),
            (DoubledHeightCoordinateHex(6, 12), True),
            (DoubledHeightCoordinateHex(10, 6), True),
            (DoubledHeightCoordinateHex(7, 5), False),
        ]

        for location, outcome in trials:
            tile = board.tiles[location]
            assert clue.check_space(tile, board) != outcome


class TestWithinTwoSpacesOfShapeClue:
    def test_str(self):
        clue = WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE)
        assert str(clue) == "The habitat is within two spaces of a standing stone"

        clue = WithinTwoSpacesOfShapeClue(shape=Shape.ABANDONED_SHACK, negated=True)
        assert str(clue) == "The habitat is not within two spaces of an abandoned shack"

    def test_check_space(self, board):
        clue = WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE)

        # locations and expected resolution
        trials: list[tuple[DoubledHeightCoordinateHex, bool]] = [
            (DoubledHeightCoordinateHex(1, 1), True),
            (DoubledHeightCoordinateHex(3, 7), True),
            (DoubledHeightCoordinateHex(0, 10), False),
            (DoubledHeightCoordinateHex(4, 16), False),
            (DoubledHeightCoordinateHex(6, 12), False),
            (DoubledHeightCoordinateHex(10, 6), False),
            (DoubledHeightCoordinateHex(7, 5), True),
        ]

        for location, outcome in trials:
            tile = board.tiles[location]
            assert clue.check_space(tile, board) == outcome

    def test_check_space_negated(self, board):
        clue = WithinTwoSpacesOfShapeClue(shape=Shape.STANDING_STONE, negated=True)

        # locations and expected resolution
        trials: list[tuple[DoubledHeightCoordinateHex, bool]] = [
            (DoubledHeightCoordinateHex(1, 1), True),
            (DoubledHeightCoordinateHex(3, 7), True),
            (DoubledHeightCoordinateHex(0, 10), False),
            (DoubledHeightCoordinateHex(4, 16), False),
            (DoubledHeightCoordinateHex(6, 12), False),
            (DoubledHeightCoordinateHex(10, 6), False),
            (DoubledHeightCoordinateHex(7, 5), True),
        ]

        for location, outcome in trials:
            tile = board.tiles[location]
            assert clue.check_space(tile, board) != outcome


class TestWithinTwoSpacesOfAnimalTerritoryClue:
    def test_str(self):
        clue = WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR)
        assert str(clue) == "The habitat is within two spaces of bear territory"

        clue = WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.COUGAR, negated=True)
        assert str(clue) == "The habitat is not within two spaces of cougar territory"

    def test_check_space(self, board):
        clue = WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR)

        # locations and expected resolution
        trials: list[tuple[DoubledHeightCoordinateHex, bool]] = [
            (DoubledHeightCoordinateHex(1, 1), True),
            (DoubledHeightCoordinateHex(3, 7), True),
            (DoubledHeightCoordinateHex(0, 10), False),
            (DoubledHeightCoordinateHex(4, 16), False),
            (DoubledHeightCoordinateHex(6, 12), True),
            (DoubledHeightCoordinateHex(10, 6), True),
            (DoubledHeightCoordinateHex(7, 5), False),
        ]

        for location, outcome in trials:
            tile = board.tiles[location]
            assert clue.check_space(tile, board) == outcome

    def test_check_space_negated(self, board):
        clue = WithinTwoSpacesOfAnimalTerritoryClue(animal_territory=AnimalTerritory.BEAR, negated=True)

        # locations and expected resolution
        trials: list[tuple[DoubledHeightCoordinateHex, bool]] = [
            (DoubledHeightCoordinateHex(1, 1), True),
            (DoubledHeightCoordinateHex(3, 7), True),
            (DoubledHeightCoordinateHex(0, 10), False),
            (DoubledHeightCoordinateHex(4, 16), False),
            (DoubledHeightCoordinateHex(6, 12), True),
            (DoubledHeightCoordinateHex(10, 6), True),
            (DoubledHeightCoordinateHex(7, 5), False),
        ]

        for location, outcome in trials:
            tile = board.tiles[location]
            assert clue.check_space(tile, board) != outcome


class TestWithinThreeSpacesOfColorClue:
    def test_str(self):
        clue = WithinThreeSpacesOfColorClue(color=Color.BLUE)
        assert str(clue) == "The habitat is within three spaces of a blue structure"

        clue = WithinThreeSpacesOfColorClue(color=Color.WHITE, negated=True)
        assert str(clue) == "The habitat is not within three spaces of a white structure"

    def test_check_space(self, board):
        clue = WithinThreeSpacesOfColorClue(color=Color.GREEN)

        # locations and expected resolution
        trials: list[tuple[DoubledHeightCoordinateHex, bool]] = [
            (DoubledHeightCoordinateHex(1, 1), False),
            (DoubledHeightCoordinateHex(3, 7), False),
            (DoubledHeightCoordinateHex(0, 10), False),
            (DoubledHeightCoordinateHex(4, 16), False),
            (DoubledHeightCoordinateHex(6, 12), True),
            (DoubledHeightCoordinateHex(10, 6), True),
            (DoubledHeightCoordinateHex(7, 5), False),
        ]

        for location, outcome in trials:
            tile = board.tiles[location]
            assert clue.check_space(tile, board) == outcome

    def test_check_space_negated(self, board):
        clue = WithinThreeSpacesOfColorClue(color=Color.GREEN, negated=True)

        # locations and expected resolution
        trials: list[tuple[DoubledHeightCoordinateHex, bool]] = [
            (DoubledHeightCoordinateHex(1, 1), False),
            (DoubledHeightCoordinateHex(3, 7), False),
            (DoubledHeightCoordinateHex(0, 10), False),
            (DoubledHeightCoordinateHex(4, 16), False),
            (DoubledHeightCoordinateHex(6, 12), True),
            (DoubledHeightCoordinateHex(10, 6), True),
            (DoubledHeightCoordinateHex(7, 5), False),
        ]

        for location, outcome in trials:
            tile = board.tiles[location]
            assert clue.check_space(tile, board) != outcome
