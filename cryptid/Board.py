from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from cryptid.BoardSections import BOARD_SECTION_OFFSETS, BOARD_SECTIONS
from cryptid.Hex import FixedLength, Hex
from cryptid.SetupCard import SetupCard
from cryptid.Tile import Structure, Tile


@dataclass
class Board:
    tiles: Annotated[dict[Hex, Tile], FixedLength(108)]

    @classmethod
    def from_board_sections(cls, order: Annotated[list[int], FixedLength(6)]) -> Board:
        tiles: dict[Hex, Tile] = dict()
        for offset, board_section in enumerate(order):
            tiles |= BOARD_SECTIONS[board_section - 1].offset(BOARD_SECTION_OFFSETS[offset]).tiles
        return cls(tiles=tiles)

    def place_structure(self, structure: Structure, location: Hex) -> None:
        self.tiles[location].structure = structure

    @classmethod
    def from_setup_card(cls, card: SetupCard) -> Board:
        board = cls.from_board_sections(card.board_sections)
        for location, structure in card.structures:
            board.place_structure(structure, location)
        return board
