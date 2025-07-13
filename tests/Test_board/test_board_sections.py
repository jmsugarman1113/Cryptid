from cryptid.board_sections import BOARD_SECTIONS
from cryptid.hex import DoubledHeightCoordinateHex
from cryptid.tile import AnimalTerritory, Terrain
from tests.test_utils import get_random_DoubleHeightCoordinateHex


class TestBoardSections:
    def test_board_section_lengths(self):
        for board_section in BOARD_SECTIONS:
            assert len(board_section.tiles) == 18

    def test_board_section_hexes_and_tiles_line_up(self):
        for board_section in BOARD_SECTIONS:
            assert all(tile.hex == hex for hex, tile in board_section.tiles.items())

    def test_offset(self):
        offset_hex = get_random_DoubleHeightCoordinateHex(10, 123456)
        for board_section in BOARD_SECTIONS:
            new_board_section = board_section.offset(offset_hex)
            assert board_section is not new_board_section
            assert len(new_board_section.tiles) == 18
            assert all(tile.hex == hex for hex, tile in new_board_section.tiles.items())

        offset_hex = DoubledHeightCoordinateHex(3, 5)
        original_board_section = BOARD_SECTIONS[0]
        new_board_section = original_board_section.offset(offset_hex)

        assert offset_hex in new_board_section.tiles
        tile = new_board_section.tiles[offset_hex]
        assert tile.terrain == Terrain.WATER
        assert tile.animal_territory is None

        assert DoubledHeightCoordinateHex(6, 10) in new_board_section.tiles
        tile = new_board_section.tiles[DoubledHeightCoordinateHex(6, 10)]
        assert tile.terrain == Terrain.DESERT
        assert tile.animal_territory == AnimalTerritory.BEAR
