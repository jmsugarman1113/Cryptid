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

    def to_cube_coordinate_hex(self) -> CubeCoordinateHex:
        return self.to_axial_coordinate_hex().to_cube_coordinate_hex()

    @classmethod
    def from_cube_coordinate_hex(cls, cube_hex: CubeCoordinateHex) -> Hex:
        return cls.from_axial_coordinate_hex(cube_hex.to_axial_coordinate_hex())

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

    # def __radd__(self, other: Any) -> Hex | NotImplemented:
    #     return self.__add__(other)
    #
    # def __rsub__(self, other: Any) -> Hex | NotImplemented:
    #     return self.__sub__(other)

    def __rmul__(self, other: Any) -> Hex | NotImplemented:
        return self.__mul__(other)

    def __neg__(self) -> Hex:
        return -1*self

    def to_2d_coordinates(self) -> tuple[int, int]:
        return self.q, self.r

    @classmethod
    def from_2d_coordinates(cls, q: int, r: int) -> Hex:
        return cls(q=q, r=r)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError(f"equality is only defined between the same type of Hexes.  Trying to compare {self.__class__} and {other.__class__} ")
        return self.distance(other) == 0

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def reflect_over(self, other: Hex) -> Hex:
        if not isinstance(other, self.__class__):
            raise NotImplementedError(f"relfection is only defined between the same type of Hex.  Trying to reflect {self.__class__} and {other.__class__}")
        return 2*other - self


@dataclass(frozen=True)
class OffsetCoordinateHex(Hex, ABC):
    @property
    def row(self) -> int:
        return self.r

    @property
    def col(self) -> int:
        return self.q

    @classmethod
    def from_row_col(cls, row: int, col: int) -> OffsetCoordinateHex:
        return cls(q=col, r=row)


@dataclass(frozen=True)
class DoubleCoordinateHex(OffsetCoordinateHex, ABC):
    # q is col
    # r is row
    def ___post_init__(self):
        assert (self.q + self.r) % 2 == 0, f"A doubled coordinate hex must have its coordinates be of the same parity"


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
        drow = abs(self.row - other.row)
        dcol = abs(self.col - other.col)
        return dcol + max(0, (drow-dcol)//2)

    def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(self.q, (self.r - self.q) // 2)

    @classmethod
    def from_axial_coordinate_hex(cls, axial_hex: AxialCoordinateHex) -> DoubledHeightCoordinateHex:
        return axial_hex.to_double_height_coordinate_hex()

    # @classmethod
    # def from_cube_coordinate_hex(cls, cube_hex: CubeCoordinateHex) -> DoubledHeightCoordinateHex:
    #     return cube_hex.to_double_height_coordinate_hex()

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
        dcol = abs(self.col - other.col)
        drow = abs(self.row - other.row)
        return drow + max(0, (dcol - drow) // 2)

    def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
        return AxialCoordinateHex((self.r - self.q) // 2, self.q)

    @classmethod
    def from_axial_coordinate_hex(cls, axial_hex: AxialCoordinateHex) -> DoubledWidthCoordinateHex:
        return axial_hex.to_double_width_coordinate_hex()

    # @classmethod
    # def from_cube_coordinate_hex(cls, cube_hex: CubeCoordinateHex) -> DoubledWidthCoordinateHex:
    #     return cube_hex.to_double_width_coordinate_hex()

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
        return DoubledWidthCoordinateHex.from_row_col(col=2*self.q + self.r, row=self.r)

    @classmethod
    def from_double_width_coordinate_hex(cls, double_width_hex: DoubledWidthCoordinateHex) -> AxialCoordinateHex:
        return double_width_hex.to_axial_coordinate_hex()

    def to_double_height_coordinate_hex(self) -> DoubledHeightCoordinateHex:
        return DoubledHeightCoordinateHex.from_row_col(col=self.q, row=2*self.r + self.q)

    @classmethod
    def from_double_height_coordinate_hex(cls, double_height_hex: DoubledHeightCoordinateHex) -> AxialCoordinateHex:
        return double_height_hex.to_axial_coordinate_hex()

    def reflect_over_Q_axis(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(self.q, -self.q-self.r)

    def reflect_over_R_axis(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(-self.q-self.r, self.r)

    def reflect_over_S_axis(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(self.r, self.q)

    # def reflect_over_Q(self, q: int) -> AxialCoordinateHex:
    #     reference_point = AxialCoordinateHex(0, q)
    #     shifted = self - reference_point
    #     reflected = shifted.reflect_over_R_axis()
    #     return reflected + reference_point
    #
    # def reflect_over_R(self, r: int) -> AxialCoordinateHex:
    #     reference_point = AxialCoordinateHex(r, 0)
    #     shifted = self - reference_point
    #     reflected = shifted.reflect_over_Q_axis()
    #     return reflected + reference_point
    #
    # def reflect_over_S(self, s: int) -> AxialCoordinateHex:
    #     reference_point = AxialCoordinateHex(s, 0)
    #     shifted = self - reference_point
    #     reflected = shifted.reflect_over_Q_axis()
    #     return reflected + reference_point


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
    def from_2d_coordinates(cls, q: int, r: int) -> CubeCoordinateHex:
        return cls(q=q, r=r, s=-q-r)

    def reflect_over_Q_axis(self) -> CubeCoordinateHex:
        return CubeCoordinateHex(self.q, self.s, self.r)

    def reflect_over_R_axis(self) -> CubeCoordinateHex:
        return CubeCoordinateHex(self.s, self.r, self.q)

    def reflect_over_S_axis(self) -> CubeCoordinateHex:
        return CubeCoordinateHex(self.r, self.q, self.s)


@dataclass(frozen=True)
class EvenRowOffsetCoordinateHex(OffsetCoordinateHex):
    def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(q=self.col - (self.row + (self.row & 1)) // 2, r=self.row)


@dataclass(frozen=True)
class OddRowOffsetCoordinateHex(OffsetCoordinateHex):
    def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(q=self.col - (self.row - (self.row & 1)) // 2, r=self.row)


@dataclass(frozen=True)
class EvenColumnOffsetCoordinateHex(OffsetCoordinateHex):
    def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(q=self.col, r=self.row - (self.col + (self.col & 1)) // 2)


@dataclass(frozen=True)
class OddColumnffsetCoordinateHex(OffsetCoordinateHex):
    def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(q=self.col, r=self.row - (self.col - (self.col & 1)) // 2)





