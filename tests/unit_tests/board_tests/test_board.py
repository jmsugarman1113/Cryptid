import random

from cryptid.board import Board
from cryptid.board_sections import BOARD_SECTION_OFFSETS, BOARD_SECTIONS
from cryptid.hex import DoubledHeightCoordinateHex
from cryptid.tile import AnimalTerritory, Terrain


class TestBoard:
    def test_board_from_board_sections(self):
        order = [1, 2, 3, 4, 5, 6]
        random.seed(0)
        random.shuffle(order)
        board = Board.from_board_sections(order)
        assert len(board.tiles) == 108

        for offset, board_section_idx in zip(BOARD_SECTION_OFFSETS, order):
            assert (
                board.tiles[offset]
                == BOARD_SECTIONS[board_section_idx - 1].tiles[DoubledHeightCoordinateHex.origin()] + offset
            )

    def test_board_from_board_sections_2(self):
        order = [1, 2, 3, 4, 5, 6]
        board = Board.from_board_sections(order)
        assert len(board.tiles) == 108

        for offset, board_section_idx in zip(BOARD_SECTION_OFFSETS, order):
            assert (
                board.tiles[offset]
                == BOARD_SECTIONS[board_section_idx - 1].tiles[DoubledHeightCoordinateHex.origin()] + offset
            )

        hex_location = DoubledHeightCoordinateHex(10, 10)
        assert board.tiles[hex_location].terrain == Terrain.WATER
        assert board.tiles[hex_location].animal_territory == AnimalTerritory.BEAR

    def test_board_from_board_sections_3(self):
        order = [1, 1, 1, 1, 1, 1]
        orientation = [False, False, True, True, False, False]
        board = Board.from_board_sections(order, orientation)
        assert len(board.tiles) == 108

        # (0, 0) top left corner and bottom right corner
        hex_origin = DoubledHeightCoordinateHex.origin()
        for offset, inverted in zip(BOARD_SECTION_OFFSETS, orientation):
            hex_location = hex_origin + offset
            terrain = Terrain.WATER if not inverted else Terrain.FOREST
            animal_territory = None if not inverted else AnimalTerritory.BEAR
            tile = board.tiles[hex_location]
            assert tile.terrain == terrain
            assert tile.animal_territory == animal_territory

        hex_origin = DoubledHeightCoordinateHex.from_row_col(3, 1)
        for offset, inverted in zip(BOARD_SECTION_OFFSETS, orientation):
            hex_location = hex_origin + offset
            terrain = Terrain.SWAMP if not inverted else Terrain.FOREST
            animal_territory = None
            tile = board.tiles[hex_location]
            assert tile.terrain == terrain
            assert tile.animal_territory == animal_territory

        hex_origin = DoubledHeightCoordinateHex.from_row_col(4, 4)
        for offset, inverted in zip(BOARD_SECTION_OFFSETS, orientation):
            hex_location = hex_origin + offset
            terrain = Terrain.DESERT if not inverted else Terrain.WATER
            animal_territory = AnimalTerritory.BEAR if not inverted else None
            tile = board.tiles[hex_location]
            assert tile.terrain == terrain
            assert tile.animal_territory == animal_territory

    def test_tiles_in_range(self):
        order = [1, 1, 1, 1, 1, 1]
        orientation = [False, False, True, True, False, False]
        board = Board.from_board_sections(order, orientation)

        assert len(board.get_tiles_in_range(loc=DoubledHeightCoordinateHex(0, 0), range=2)) == 7

        assert len(board.get_tiles_in_range(loc=board.tiles[DoubledHeightCoordinateHex.origin()], range=2)) == 7

        assert len(board.get_tiles_in_range(loc=DoubledHeightCoordinateHex(5, 9), range=1)) == 7

        assert len(board.get_tiles_in_range(loc=DoubledHeightCoordinateHex(5, 9), range=2)) == 19

        assert len(board.get_tiles_in_range(loc=DoubledHeightCoordinateHex(5, 9), range=3)) == 37

        assert len(board.get_tiles_in_range(loc=DoubledHeightCoordinateHex(9, 17), range=3)) == 18

    # TODO: test from cards
