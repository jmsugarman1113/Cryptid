from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from cryptid.board_sections import BOARD_SECTION_OFFSETS, BOARD_SECTIONS
from cryptid.hex import FixedLength, Hex
from cryptid.setup_card import SetupCard
from cryptid.tile import Structure, Tile


@dataclass
class Board:
    tiles: Annotated[dict[Hex, Tile], FixedLength(108)]

    @classmethod
    def from_board_sections(
        cls,
        order: Annotated[list[int], FixedLength(6)],
        orientation: Annotated[list[bool], FixedLength(6)],
    ) -> Board:
        tiles: dict[Hex, Tile] = dict()
        for offset, (board_section, inverted) in enumerate(zip(order, orientation)):
            tiles |= BOARD_SECTIONS[board_section - 1].invert(inverted).offset(BOARD_SECTION_OFFSETS[offset]).tiles
        return cls(tiles=tiles)

    def place_structure(self, structure: Structure, location: Hex) -> None:
        self.tiles[location].structure = structure

    @classmethod
    def from_setup_card(cls, card: SetupCard) -> Board:
        board = cls.from_board_sections(card.board_sections, card.board_sections_inverted)
        for location, structure in card.structures:
            board.place_structure(structure, location)
        return board
