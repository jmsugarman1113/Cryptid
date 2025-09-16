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
        board = Board.from_board_sections(order, [False] * 6)
        assert len(board.tiles) == 108

        for offset, board_section_idx in zip(BOARD_SECTION_OFFSETS, order):
            assert (
                board.tiles[offset]
                == BOARD_SECTIONS[board_section_idx - 1].tiles[DoubledHeightCoordinateHex.origin()] + offset
            )

    def test_board_from_board_sections2(self):
        order = [1, 2, 3, 4, 5, 6]
        board = Board.from_board_sections(order, [False] * 6)
        assert len(board.tiles) == 108

        for offset, board_section_idx in zip(BOARD_SECTION_OFFSETS, order):
            assert (
                board.tiles[offset]
                == BOARD_SECTIONS[board_section_idx - 1].tiles[DoubledHeightCoordinateHex.origin()] + offset
            )

        hex_location = DoubledHeightCoordinateHex(10, 10)
        assert board.tiles[hex_location].terrain == Terrain.WATER
        assert board.tiles[hex_location].animal_territory == AnimalTerritory.BEAR

    # TODO: test board section inversion
