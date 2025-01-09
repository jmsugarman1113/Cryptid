from __future__ import annotations

from BoardSections import BoardSection, BOARD_SECTION_OFFSETS, BOARD_SECTIONS
from Tile import Tile, Shape, Color, Structure
from Hex import Hex, FixedLength
from dataclasses import dataclass
from typing import Optional, Any, Final, Annotated


@dataclass
class Board:
    tiles: Annotated[dict[Hex, Tile], FixedLength[108]]

    @classmethod
    def from_board_sections(cls, order: list[int]) -> Board:
        tiles = dict()
        for offset, idx in enumerate(order):
            tiles |= BOARD_SECTIONS[idx-1].offset(BOARD_SECTION_OFFSETS[offset])
        return cls(tiles=tiles)

    def place_structure(self, structure: Structure, location: Hex):
        self.tiles[location].structure = structure