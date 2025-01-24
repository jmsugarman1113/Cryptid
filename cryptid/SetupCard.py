from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from cryptid.Clue import Clue
from cryptid.Hex import FixedLength, Hex
from cryptid.Tile import Structure


@dataclass
class SetupCard:
    board_sections: Annotated[list[int], FixedLength(6)]
    structures: list[tuple[Hex, Structure]]
    clues: Annotated[dict[int, list[Clue]], FixedLength(3)]  # keys are guaranteed to be 3, 4, 5 for num players
