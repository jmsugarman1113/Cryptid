from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Optional

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
        orientation: Optional[Annotated[list[bool], FixedLength(6)]] = None,
    ) -> Board:
        tiles: dict[Hex, Tile] = dict()
        orientation = orientation if orientation is not None else [False] * 6
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

    def get_tiles_in_range(self, loc: Tile | Hex, range: int) -> list[Tile]:
        tiles = []
        if isinstance(loc, Tile):
            loc = loc.hex
        for possible_hex in loc.hexes_within_range(range):
            if (possible_tile := self.tiles.get(possible_hex, None)) is not None:
                tiles.append(possible_tile)
        return tiles
