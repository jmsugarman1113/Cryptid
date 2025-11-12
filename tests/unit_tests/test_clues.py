from cryptid.clue import (
    Clue,
    NullClue,
    ALPHA_CLUES,
    BETA_CLUES,
    GAMMA_CLUES,
    DELTA_CLUES,
    # EPSILON_CLUES,
    OnOneOfTwoTerrainClue,
)
from cryptid.board import Board
from cryptid.setup_card import SETUP_CARDS
from cryptid.hex import DoubledHeightCoordinateHex
from cryptid.tile import Terrain
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


class TestOnOneOfTwoTerrainClue:
    def test_on_one_of_two_terrain(self, board):
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

    def test_on_one_of_two_terrain_negated(self, board):
        clue = OnOneOfTwoTerrainClue(valid_terrains=[Terrain.WATER, Terrain.DESERT], negated=True)

        # locations and expected resolution
        trials: list[tuple[DoubledHeightCoordinateHex, bool]] = [
            (DoubledHeightCoordinateHex(1, 1), False),
            (DoubledHeightCoordinateHex(3, 7), False),
            (DoubledHeightCoordinateHex(0, 10), True),
            (DoubledHeightCoordinateHex(4, 16), True),
            (DoubledHeightCoordinateHex(6, 12), False),
            (DoubledHeightCoordinateHex(10, 8), True),
            (DoubledHeightCoordinateHex(7, 5), False),
        ]
        for location, outcome in trials:
            tile = board.tiles[location]
            assert clue.check_space(tile, board) == outcome
