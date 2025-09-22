import math
from typing import Callable, Final, Iterable

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

from cryptid.board import Board
from cryptid.hex import AxialCoordinateHex
from cryptid.tile import AnimalTerritory, Terrain, Tile

SQRT3: Final[float] = math.sqrt(3)
SQRT3_OVER2: Final[float] = math.sqrt(3) / 2

HEX_COLOR_MAPPING: Final[dict[Terrain, str]] = {
    Terrain.WATER: "blue",
    Terrain.SWAMP: "brown",
    Terrain.DESERT: "yellow",
    Terrain.FOREST: "green",
    Terrain.MOUNTAIN: "gray",
}

ANIMAL_COLOR_MAPPING: Final[dict[AnimalTerritory, str]] = {
    AnimalTerritory.COUGAR: "red",
    AnimalTerritory.BEAR: "black",
}


def hex_to_pointy_coords(axial: AxialCoordinateHex, radius: float = 1) -> tuple[float, float]:
    x = radius * (SQRT3 * axial.q + SQRT3_OVER2 * axial.r)
    y = -1.5 * radius * axial.r
    return x, y


def hex_to_flat_coords(axial: AxialCoordinateHex, radius: float = 1) -> tuple[float, float]:
    x = 1.5 * radius * axial.q
    y = -radius * (SQRT3 * axial.r + SQRT3_OVER2 * axial.q)
    return x, y


def plot_hex(
    tile: Tile,
    radius: float,
    text_size: int,
    ax: plt.axes,
    orientation: float,
    coords_func: Callable[[AxialCoordinateHex, float], tuple[float, float]],
    annotate_position: bool = False,
) -> None:
    color = HEX_COLOR_MAPPING[tile.terrain]
    axial = tile.hex.to_axial_coordinate_hex()
    x, y = coords_func(axial, radius)
    hexagon = RegularPolygon(
        (x, y), numVertices=6, radius=radius, orientation=orientation, facecolor=color, alpha=0.2, edgecolor="k"
    )
    ax.add_patch(hexagon)

    if tile.animal_territory:
        animal_color = ANIMAL_COLOR_MAPPING[tile.animal_territory]
        animal_hexagon = RegularPolygon(
            (x, y),
            numVertices=6,
            radius=2 / 3 * radius,
            orientation=orientation,
            edgecolor=animal_color,
            alpha=0.8,
            fill=False,
            linestyle="--",
        )
        ax.add_patch(animal_hexagon)
    # Also add a text label
    if annotate_position:
        ax.text(x, y + 0.2, (axial.q, axial.r), ha="center", va="center", size=text_size)
        ax.text(x, y - 0.2, (tile.hex.q, tile.hex.r), ha="center", va="center", size=text_size)


def plot_pointy(tiles: Iterable[Tile], radius: float = 1, text_size: int = 5, annotate_position: bool = False) -> None:
    fig, ax = plt.subplots(1)

    for tile in tiles:
        plot_hex(
            tile=tile,
            radius=radius,
            text_size=text_size,
            orientation=0,
            coords_func=hex_to_pointy_coords,
            ax=ax,
            annotate_position=annotate_position,
        )

    plt.show()


def plot_flat(tiles: Iterable[Tile], radius: float = 1, text_size: int = 5, annotate_position: bool = False) -> None:
    fig, ax = plt.subplots(1)

    for tile in tiles:
        plot_hex(
            tile=tile,
            radius=radius,
            text_size=text_size,
            orientation=math.pi / 6,
            coords_func=hex_to_flat_coords,
            ax=ax,
            annotate_position=annotate_position,
        )
    plt.show()


if __name__ == "__main__":
    # board = BOARD_SECTIONS[2].invert(True)
    board = Board.from_board_sections(order=[1, 6, 2, 5, 3, 4], orientation=[True, True, False, False, True, False])
    # plot_pointy(board.tiles.values())
    plot_flat(board.tiles.values(), annotate_position=True)
