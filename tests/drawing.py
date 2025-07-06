import math
from typing import Final

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

from cryptid.board_sections import BOARD_SECTIONS
from cryptid.hex import AxialCoordinateHex
from cryptid.tile import Terrain

SQRT3: Final[float] = math.sqrt(3)
SQRT3_OVER2: Final[float] = math.sqrt(3) / 2

HEX_COLOR_MAPPING: Final[dict[Terrain, str]] = {
    Terrain.WATER: "blue",
    Terrain.SWAMP: "brown",
    Terrain.DESERT: "yellow",
    Terrain.FOREST: "green",
    Terrain.MOUNTAIN: "gray",
}


def hex_to_pointy_coords(axial: AxialCoordinateHex, radius: float = 1) -> tuple[float, float]:
    x = radius * (SQRT3 * axial.q + SQRT3_OVER2 * axial.r)
    y = -radius * 1.5 * axial.r

    return x, y


if __name__ == "__main__":
    board = BOARD_SECTIONS[0]
    r = 1

    fig, ax = plt.subplots(1)
    # ax.set_aspect('equal')

    # Add some coloured hexagons
    for tile in board.tiles.values():
        color = HEX_COLOR_MAPPING[tile.terrain]
        axial = tile.hex.to_axial_coordinate_hex()
        x, y = hex_to_pointy_coords(axial, radius=r)
        hexagon = RegularPolygon(
            (x, y), numVertices=6, radius=r, orientation=0, facecolor=color, alpha=0.2, edgecolor="k"
        )
        ax.add_patch(hexagon)
        # Also add a text label
        ax.text(x, y + 0.2, (axial.q, axial.r), ha="center", va="center", size=8)
        ax.text(x, y - 0.2, (tile.hex.q, tile.hex.r), ha="center", va="center", size=8)

    plt.show()
