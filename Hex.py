from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Annotated
from dataclasses import dataclass, fields


@dataclass
class FixedLength:
    length: int


@dataclass(frozen=True)
class Hex(ABC):
    q: int
    r: int

    @abstractmethod
    def distance(self, other: Hex) -> int:
        pass

    @property
    @abstractmethod
    def neighbor_directions(self) -> Annotated[list[Hex], FixedLength(6)]:
        pass

    @property
    def neighbors(self) -> Annotated[list[Hex], FixedLength(6)]:
        return [self + dir for dir in self.neighbor_directions]

    def hexes_within_range(self, n: int) -> list[Hex]:
        output = list()
        center = self.to_axial_coordinate_hex()
        for q in range(-n, n + 1):
            for r in range(max(-n, -n - q), min(n, n - q) + 1):
                ah: AxialCoordinateHex = center + AxialCoordinateHex(q, r)
                output.append(self.from_axial_coordinate_hex(ah))
        return output

    def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(self.q, self.r)

    @classmethod
    def from_axial_coordinate_hex(cls, axial_hex: AxialCoordinateHex) -> Hex:
        return cls(axial_hex.q, axial_hex.r)

    def __copy__(self) -> Hex:
        return self.__class__(**{field.name: getattr(self, field.name) for field in fields(self)})

    def __add__(self, other: Any) -> Hex | NotImplemented:
        if isinstance(other, self.__class__):
            return self.__class__(
                **{
                    field.name: getattr(self, field.name) + getattr(other, field.name)
                    for field in fields(self)
                }
            )
        return NotImplemented(f"Can only add the same type of Hexes together.  Trying to add {type(self)} to {type(other)}")

    def __sub__(self, other: Any) -> Hex | NotImplemented:
        if isinstance(other, self.__class__):
            return self.__class__(
                **{
                    field.name: getattr(self, field.name) - getattr(other, field.name)
                    for field in fields(self)
                }
            )
        return NotImplemented(f"Can only add the same type of Hexes together.  Trying to subtract {type(other)} from {type(self)}")

    def __mul__(self, other: Any) -> Hex | NotImplemented:
        if isinstance(other, int):
            return self.__class__(
                **{
                    field.name: other*getattr(self, field.name)
                    for field in fields(self)
                }
            )
        return NotImplemented(f"Can only scale Hex's by integers, got {type(other)} instead")

    def __radd__(self, other: Any) -> Hex | NotImplemented:
        return self.__add__(other)

    def __rsub__(self, other: Any) -> Hex | NotImplemented:
        return self.__sub__(other)

    def __rmul__(self, other: Any) -> Hex | NotImplemented:
        return self.__mul__(other)

    def __neg__(self) -> Hex:
        return -1*self

    def to_2d_coordinates(self) -> tuple[int, int]:
        return self.q, self.r

    @classmethod
    def from_2d_coordinates(cls, x: int, y: int) -> Hex:
        return cls(q=x, r=y)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError(f"equality is only defined between the same type of Hexes.  Trying to compare {self.__class__} and {other.__class__} ")
        return self.distance(other) == 0

    def __ne__(self, other: Any) -> bool:
        return not (self == other)


@dataclass(frozen=True)
class DoubleCoordinateHex(Hex, ABC):
    def ___post_init__(self):
        assert (self.q + self.r) % 2 == 0, f"A doubled coordinate hex must have its coordinates be of the same parity"

    def to_cube_coordinate_hex(self) -> CubeCoordinateHex:
        return self.to_axial_coordinate_hex().to_cube_coordinate_hex()

    @classmethod
    @abstractmethod
    def from_cube_coordinate_hex(cls, cube_hex: CubeCoordinateHex) -> DoubleCoordinateHex:
        pass



@dataclass(frozen=True)
class DoubledHeightCoordinateHex(DoubleCoordinateHex):
    @property
    def neighbor_directions(self) -> Annotated[list[DoubledHeightCoordinateHex], FixedLength(6)]:
        return [
            DoubledHeightCoordinateHex(q=1, r=1),
            DoubledHeightCoordinateHex(q=1, r=-1),
            DoubledHeightCoordinateHex(q=0, r=-2),
            DoubledHeightCoordinateHex(q=-1, r=-1),
            DoubledHeightCoordinateHex(q=-1, r=1),
            DoubledHeightCoordinateHex(q=0, r=2),
        ]

    def distance(self, other: DoubledHeightCoordinateHex) -> int:
        dcol = abs(self.r - other.r)
        drow = abs(self.q - other.q)
        return dcol + max(0, (drow-dcol)//2)

    def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(self.r, (self.q - self.r) // 2)

    @classmethod
    def from_axial_coordinate_hex(cls, axial_hex: AxialCoordinateHex) -> DoubledHeightCoordinateHex:
        return axial_hex.to_double_height_coordinate_hex()

    @classmethod
    def from_cube_coordinate_hex(cls, cube_hex: CubeCoordinateHex) -> DoubledHeightCoordinateHex:
        return cube_hex.to_double_height_coordinate_hex()

    # TODO: override to_2d to support array with less wasted space?


@dataclass(frozen=True)
class DoubledWidthCoordinateHex(DoubleCoordinateHex):
    @property
    def neighbor_directions(self) -> list[DoubledWidthCoordinateHex]:
        return [
            DoubledWidthCoordinateHex(q=2, r=0),
            DoubledWidthCoordinateHex(q=1, r=-1),
            DoubledWidthCoordinateHex(q=-1, r=-1),
            DoubledWidthCoordinateHex(q=-2, r=0),
            DoubledWidthCoordinateHex(q=-1, r=1),
            DoubledWidthCoordinateHex(q=1, r=1),
        ]

    def distance(self, other: DoubledWidthCoordinateHex) -> int:
        dcol = abs(self.r - other.r)
        drow = abs(self.q - other.q)
        return drow + max(0, (dcol - drow) // 2)

    def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
        return AxialCoordinateHex((self.r - self.q) // 2, self.q)

    @classmethod
    def from_axial_coordinate_hex(cls, axial_hex: AxialCoordinateHex) -> DoubledWidthCoordinateHex:
        return axial_hex.to_double_width_coordinate_hex()

    @classmethod
    def from_cube_coordinate_hex(cls, cube_hex: CubeCoordinateHex) -> DoubledWidthCoordinateHex:
        return cube_hex.to_double_width_coordinate_hex()

    # TODO: override to_2d to support array with less wasted space??


@dataclass(frozen=True)
class AxialCoordinateHex(Hex):

    @property
    def neighbor_directions(self) -> Annotated[list[AxialCoordinateHex], FixedLength(6)]:
        return [
            AxialCoordinateHex(q=1, r=0),
            AxialCoordinateHex(q=1, r=-1),
            AxialCoordinateHex(q=0, r=-1),
            AxialCoordinateHex(q=-1, r=0),
            AxialCoordinateHex(q=-1, r=1),
            AxialCoordinateHex(q=0, r=1),
        ]

    def distance(self, other: AxialCoordinateHex) -> int:
        d = self - other
        s = -d.q - d.r
        return max(abs(d.q), abs(d.r), abs(s))

    def to_cube_coordinate_hex(self) -> CubeCoordinateHex:
        return CubeCoordinateHex(self.q, self.r, -self.q - self.r)

    @classmethod
    def from_cube_coordinate_hex(cls, cube_hex: CubeCoordinateHex) -> AxialCoordinateHex:
        return cube_hex.to_axial_coordinate_hex()

    def to_double_width_coordinate_hex(self) -> DoubledWidthCoordinateHex:
        return DoubledWidthCoordinateHex(2*self.q + self.r, self.r)

    @classmethod
    def from_double_width_coordinate_hex(cls, double_width_hex: DoubledWidthCoordinateHex) -> AxialCoordinateHex:
        return double_width_hex.to_axial_coordinate_hex()

    def to_double_height_coordinate_hex(self) -> DoubledHeightCoordinateHex:
        return DoubledHeightCoordinateHex(self.q, 2*self.r + self.q)

    @classmethod
    def from_double_height_coordinate_hex(cls, double_height_hex: DoubledHeightCoordinateHex) -> AxialCoordinateHex:
        return double_height_hex.to_axial_coordinate_hex()


@dataclass(frozen=True)
class CubeCoordinateHex(AxialCoordinateHex):
    s: int

    def __post_init__(self):
        assert (intercept := (self.q + self.r + self.s)) == 0, f"A Cube Hex must lie in a plane through the origin (q + r + s = 0), got {intercept} instead"

    @property
    def neighbor_directions(self) -> Annotated[list[CubeCoordinateHex], FixedLength(6)]:
        return [
            CubeCoordinateHex(q=1, r=0, s=-1),
            CubeCoordinateHex(q=1, r=-1, s=0),
            CubeCoordinateHex(q=0, r=-1, s=1),
            CubeCoordinateHex(q=-1, r=0, s=1),
            CubeCoordinateHex(q=-1, r=1, s=0),
            CubeCoordinateHex(q=0, r=1, s=-1),
        ]

    def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(self.q, self.r)

    @classmethod
    def from_axial_coordinate_hex(cls, axial_hex: AxialCoordinateHex) -> CubeCoordinateHex:
        return axial_hex.to_cube_coordinate_hex()

    @classmethod
    def from_2d_coordinates(cls, x: int, y: int) -> CubeCoordinateHex:
        return cls(x, y, -x-y)





