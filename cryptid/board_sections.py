from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Final

from cryptid.hex import AxialCoordinateHex, DoubledHeightCoordinateHex, FixedLength, Hex
from cryptid.tile import AnimalTerritory, Terrain, Tile


@dataclass
class BoardSection:
    tiles: Annotated[dict[Hex, Tile], FixedLength(18)]

    def offset(self, offset_hex: Hex) -> BoardSection:
        new_tiles: dict[Hex, Tile] = dict()
        for k, tile in self.tiles.items():
            new_tile: Tile = tile + offset_hex
            new_tiles[new_tile.hex] = new_tile
        return BoardSection(tiles=new_tiles)

    def invert(self, inverted: bool) -> BoardSection:
        if not inverted:
            return self

        new_tile_list: list[Tile] = [AxialCoordinateHex(5, 0) - tile for tile in self.tiles.values()]  # type: ignore
        return BoardSection.from_tile_list(new_tile_list)

    @classmethod
    def from_tile_list(cls, tile_list: Annotated[list[Tile], FixedLength(18)]) -> BoardSection:
        return cls(tiles={tile.hex: tile for tile in tile_list})


# fmt: off
SECTION_1: Final[BoardSection] = BoardSection.from_tile_list([
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=0), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=2), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=4), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=1), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=3), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=5), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=0), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=2), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=4), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=1), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=3), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=5), terrain=Terrain.DESERT, animal_territory=AnimalTerritory.BEAR),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=0), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=2), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=4), terrain=Terrain.DESERT, animal_territory=AnimalTerritory.BEAR),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=1), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=3), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=5), terrain=Terrain.FOREST, animal_territory=AnimalTerritory.BEAR),
])

SECTION_2: Final[BoardSection] = BoardSection.from_tile_list([
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=0), terrain=Terrain.SWAMP, animal_territory=AnimalTerritory.COUGAR),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=2), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=4), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=1), terrain=Terrain.FOREST, animal_territory=AnimalTerritory.COUGAR),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=3), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=5), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=0), terrain=Terrain.FOREST, animal_territory=AnimalTerritory.COUGAR),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=2), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=4), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=1), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=3), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=5), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=0), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=2), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=4), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=1), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=3), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=5), terrain=Terrain.DESERT),
])

SECTION_3: Final[BoardSection] = BoardSection.from_tile_list([
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=0), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=2), terrain=Terrain.SWAMP, animal_territory=AnimalTerritory.COUGAR),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=4), terrain=Terrain.MOUNTAIN, animal_territory=AnimalTerritory.COUGAR),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=1), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=3), terrain=Terrain.SWAMP, animal_territory=AnimalTerritory.COUGAR),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=5), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=0), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=2), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=4), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=1), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=3), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=5), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=0), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=2), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=4), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=1), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=3), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=5), terrain=Terrain.WATER),
])

SECTION_4: Final[BoardSection] = BoardSection.from_tile_list([
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=0), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=2), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=4), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=1), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=3), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=5), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=0), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=2), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=4), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=1), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=3), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=5), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=0), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=2), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=4), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=1), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=3), terrain=Terrain.WATER, animal_territory=AnimalTerritory.COUGAR),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=5), terrain=Terrain.FOREST, animal_territory=AnimalTerritory.COUGAR),
])

SECTION_5: Final[BoardSection] = BoardSection.from_tile_list([
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=0), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=2), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=4), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=1), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=3), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=5), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=0), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=2), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=4), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=1), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=3), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=5), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=0), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=2), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=4), terrain=Terrain.WATER, animal_territory=AnimalTerritory.BEAR),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=1), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=3), terrain=Terrain.MOUNTAIN, animal_territory=AnimalTerritory.BEAR),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=5), terrain=Terrain.WATER, animal_territory=AnimalTerritory.BEAR),
])

SECTION_6: Final[BoardSection] = BoardSection.from_tile_list([
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=0), terrain=Terrain.DESERT, animal_territory=AnimalTerritory.BEAR),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=2), terrain=Terrain.MOUNTAIN, animal_territory=AnimalTerritory.BEAR),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=0, row=4), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=1), terrain=Terrain.DESERT),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=3), terrain=Terrain.MOUNTAIN),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=1, row=5), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=0), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=2), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=2, row=4), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=1), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=3), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=3, row=5), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=0), terrain=Terrain.SWAMP),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=2), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=4, row=4), terrain=Terrain.WATER),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=1), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=3), terrain=Terrain.FOREST),
    Tile(hex=DoubledHeightCoordinateHex.from_row_col(col=5, row=5), terrain=Terrain.FOREST),
])
# fmt: on


BOARD_SECTIONS: Final[Annotated[list[BoardSection], FixedLength(6)]] = [
    SECTION_1,
    SECTION_2,
    SECTION_3,
    SECTION_4,
    SECTION_5,
    SECTION_6,
]

BOARD_SECTION_OFFSETS: Final[Annotated[list[DoubledHeightCoordinateHex], FixedLength(6)]] = [
    DoubledHeightCoordinateHex.from_row_col(col=0, row=0),
    DoubledHeightCoordinateHex.from_row_col(col=0, row=6),
    DoubledHeightCoordinateHex.from_row_col(col=0, row=12),
    DoubledHeightCoordinateHex.from_row_col(col=6, row=0),
    DoubledHeightCoordinateHex.from_row_col(col=6, row=6),
    DoubledHeightCoordinateHex.from_row_col(col=6, row=12),
]
