import math
from typing import Callable, Final, Iterable

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

from cryptid.setup_card import SETUP_CARDS
from cryptid.board import Board
from cryptid.hex import AxialCoordinateHex
from cryptid.tile import AnimalTerritory, Terrain, Tile, Shape

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

SHAPE_MAPPING: dict = {
    Shape.ABANDONED_SHACK: (3, 0),
    Shape.STANDING_STONE: (8, math.pi / 8),
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
        ax.text(x, y - radius * 0.75, tile.animal_territory.value.lower(), ha="center", va="center", size=text_size)

    # Also add a text label
    if annotate_position:
        ax.text(x, y + 0.2, (axial.q, axial.r), ha="center", va="center", size=text_size)
        ax.text(x, y - 0.2, (tile.hex.q, tile.hex.r), ha="center", va="center", size=text_size)

    if tile.structure:
        shape_info = SHAPE_MAPPING[tile.structure.shape]
        shape_abbr = "".join([s[0] for s in tile.structure.shape.value.split("_")])
        structure_center = (x - 0.6 * radius, y)
        structure_patch = RegularPolygon(
            structure_center,
            numVertices=shape_info[0],
            radius=radius / 5,
            orientation=shape_info[1],
            facecolor=tile.structure.color.value.lower(),
            alpha=0.8,
            edgecolor=tile.structure.color.value.lower(),
        )
        ax.add_patch(structure_patch)
        ax.text(
            structure_center[0],
            structure_center[1],
            shape_abbr,
            ha="center",
            va="center",
            size=text_size,
            color="red",
            weight="bold",
        )


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
    # board = Board.from_board_sections(order=[1, 6, 2, 5, 3, 4], orientation=[True, True, False, False, True, False])
    card = SETUP_CARDS[0]
    board = Board.from_setup_card(card)
    # plot_pointy(board.tiles.values())
    plot_flat(board.tiles.values(), annotate_position=True)
