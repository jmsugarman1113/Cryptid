from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from types import NotImplementedType
from typing import Annotated, Any, Optional, Self


@dataclass(frozen=True)
class FixedLength:
    length: int


@dataclass(frozen=True)
class Hex(ABC):
    q: int
    r: int

    @abstractmethod
    def distance(self, other: Self) -> int:
        pass

    @property
    @abstractmethod
    def neighbor_directions(self) -> Annotated[list[Self], FixedLength(6)]:
        pass

    @property
    def neighbors(self) -> Annotated[list[Self], FixedLength(6)]:
        return [self + direction for direction in self.neighbor_directions]

    def hexes_within_range(self, n: int) -> list[Self]:
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
    def from_axial_coordinate_hex(cls, axial_hex: AxialCoordinateHex) -> Self:
        return cls(axial_hex.q, axial_hex.r)

    def to_cube_coordinate_hex(self) -> CubeCoordinateHex:
        return self.to_axial_coordinate_hex().to_cube_coordinate_hex()

    @classmethod
    def from_cube_coordinate_hex(cls, cube_hex: CubeCoordinateHex) -> Self:
        return cls.from_axial_coordinate_hex(cube_hex.to_axial_coordinate_hex())

    @classmethod
    def origin(cls) -> Self:
        return cls(**{field.name: 0 for field in fields(cls)})

    def reflect_over_hex(self, other: Optional[Self] = None) -> Self:
        if other is None:
            other = self.origin()
        elif not isinstance(other, self.__class__):
            raise NotImplementedError(f"reflection is only defined between the same type of Hex.  Trying to reflect {self.__class__} and {other.__class__}")  # fmt: skip
        # return 2*other - self
        return self.from_axial_coordinate_hex(2 * other.to_axial_coordinate_hex() - self.to_axial_coordinate_hex())

    def to_2d_coordinates(self) -> tuple[int, int]:
        return self.q, self.r

    @classmethod
    def from_2d_coordinates(cls, q: int, r: int) -> Self:
        return cls(q=q, r=r)

    def __copy__(self) -> Self:
        return self.__class__(**{field.name: getattr(self, field.name) for field in fields(self)})

    def __deepcopy__(self, memodict: dict = dict()) -> Self:
        return self.__class__(
            **{field.name: copy.deepcopy(getattr(self, field.name), memodict) for field in fields(self)}
        )

    def __eq__(self, other: Any) -> bool | NotImplementedType:
        if not isinstance(other, self.__class__):
            return NotImplemented  # (f"equality is only defined between the same type of Hexes.  Trying to compare {self.__class__} and {other.__class__} ")  # fmt: skip
        return self.distance(other) == 0

    def __ne__(self, other: Any) -> bool:
        return not (self.__eq__(other))

    def __add__(self, other: Any) -> Self | NotImplementedType:
        if isinstance(other, Hex):
            return self.from_axial_coordinate_hex(self.to_axial_coordinate_hex() + other.to_axial_coordinate_hex())
        return NotImplemented

    def __sub__(self, other: Any) -> Self | NotImplementedType:
        if isinstance(other, Hex):
            return self.from_axial_coordinate_hex(self.to_axial_coordinate_hex() - other.to_axial_coordinate_hex())
        return NotImplemented

    def __mul__(self, other: Any) -> Self | NotImplementedType:
        if isinstance(other, int):
            return self.from_axial_coordinate_hex(other * self.to_axial_coordinate_hex())
        return NotImplemented

    def __rmul__(self, other: Any) -> Self | NotImplementedType:
        return self.__mul__(other)

    def __neg__(self) -> Self | NotImplementedType:
        return -1 * self

    def __str__(self) -> str:
        field_str = ", ".join([f"{field.name}={getattr(self, field.name)}" for field in fields(self)])
        return f"{self.__class__.__name__}({field_str})"

    # NOTE: specifically don't implement radd and rsub so its clear what type of Hex will come out of arithmetic operations


@dataclass(frozen=True)
class VectorHex(Hex, ABC):
    def __add__(self, other: Any) -> Self | NotImplementedType:
        if isinstance(other, self.__class__):
            return self.__class__(
                **{field.name: getattr(self, field.name) + getattr(other, field.name) for field in fields(self)}
            )
        elif isinstance(other, Hex):
            return super().__add__(other)
        return NotImplemented  # (f"Can only add Hexes together.  Trying to add {type(self)} to {type(other)}")

    def __sub__(self, other: Any) -> Self | NotImplementedType:
        if isinstance(other, self.__class__):
            return self.__class__(
                **{field.name: getattr(self, field.name) - getattr(other, field.name) for field in fields(self)}
            )
        elif isinstance(other, Hex):
            return super().__sub__(other)
        return NotImplemented  # (f"Can only subtract Hexes from each other.  Trying to subtract {type(other)} from {type(self)}")  # fmt: skip

    def __mul__(self, other: Any) -> Self | NotImplementedType:
        if isinstance(other, int):
            return self.__class__(**{field.name: other * getattr(self, field.name) for field in fields(self)})
        return NotImplemented  # (f"Can only scale Hex's by integers, got {type(other)} instead")

    # def __radd__(self, other: Any) -> Hex | NotImplementedType:
    #     return self.__add__(other)
    #
    # def __rsub__(self, other: Any) -> Hex | NotImplementedType:
    #     return self.__sub__(other)

    def __rmul__(self, other: Any) -> Self | NotImplementedType:
        return self.__mul__(other)

    def __neg__(self) -> Self | NotImplementedType:
        return -1 * self


@dataclass(frozen=True)
class OffsetCoordinateHex(Hex, ABC):
    @property
    def row(self) -> int:
        return self.r

    @property
    def col(self) -> int:
        return self.q

    @classmethod
    def from_row_col(cls, row: int, col: int) -> Self:
        return cls(col, row)

    def distance(self, other: Self) -> int:
        if not isinstance(other, self.__class__):
            raise NotImplementedError(f"distance is only defined between the same type of Hexes.  Trying to compare {self.__class__} to {other.__class__}")  # fmt: skip
        return self.to_axial_coordinate_hex().distance(other.to_axial_coordinate_hex())


@dataclass(frozen=True)
class DoubleCoordinateHex(OffsetCoordinateHex, VectorHex, ABC):
    # q is col
    # r is row
    def __post_init__(self) -> None:
        # print("in Double Coord hex post init")
        assert (self.q + self.r) % 2 == 0, "A doubled coordinate hex must have its coordinates be of the same parity"  # fmt: skip


@dataclass(frozen=True)
class DoubledHeightCoordinateHex(DoubleCoordinateHex):
    def __post_init__(self) -> None:
        super().__post_init__()

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
        return dcol + max(0, (drow - dcol) // 2)

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
    def __post_init__(self) -> None:
        super().__post_init__()

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
        return AxialCoordinateHex((self.col - self.row) // 2, self.row)

    @classmethod
    def from_axial_coordinate_hex(cls, axial_hex: AxialCoordinateHex) -> DoubledWidthCoordinateHex:
        return axial_hex.to_double_width_coordinate_hex()

    # @classmethod
    # def from_cube_coordinate_hex(cls, cube_hex: CubeCoordinateHex) -> DoubledWidthCoordinateHex:
    #     return cube_hex.to_double_width_coordinate_hex()

    # TODO: override to_2d to support array with less wasted space??


@dataclass(frozen=True)
class AxialCoordinateHex(VectorHex):
    @property
    def _s(self) -> int:
        return -self.q - self.r

    @property
    def neighbor_directions(self) -> Annotated[list[Self], FixedLength(6)]:
        return [
            self.from_axial_coordinate_hex(AxialCoordinateHex(q=1, r=0)),
            self.from_axial_coordinate_hex(AxialCoordinateHex(q=1, r=-1)),
            self.from_axial_coordinate_hex(AxialCoordinateHex(q=0, r=-1)),
            self.from_axial_coordinate_hex(AxialCoordinateHex(q=-1, r=0)),
            self.from_axial_coordinate_hex(AxialCoordinateHex(q=-1, r=1)),
            self.from_axial_coordinate_hex(AxialCoordinateHex(q=0, r=1)),
        ]

    def distance(self, other: AxialCoordinateHex) -> int:
        d = self - other
        return max(abs(d.q), abs(d.r), abs(d._s))

    def to_cube_coordinate_hex(self) -> CubeCoordinateHex:
        return CubeCoordinateHex(self.q, self.r, self._s)

    @classmethod
    def from_cube_coordinate_hex(cls, cube_hex: CubeCoordinateHex) -> AxialCoordinateHex:
        return cube_hex.to_axial_coordinate_hex()

    def to_double_width_coordinate_hex(self) -> DoubledWidthCoordinateHex:
        return DoubledWidthCoordinateHex.from_row_col(col=2 * self.q + self.r, row=self.r)

    @classmethod
    def from_double_width_coordinate_hex(cls, double_width_hex: DoubledWidthCoordinateHex) -> AxialCoordinateHex:
        return double_width_hex.to_axial_coordinate_hex()

    def to_double_height_coordinate_hex(self) -> DoubledHeightCoordinateHex:
        return DoubledHeightCoordinateHex.from_row_col(col=self.q, row=2 * self.r + self.q)

    @classmethod
    def from_double_height_coordinate_hex(cls, double_height_hex: DoubledHeightCoordinateHex) -> AxialCoordinateHex:
        return double_height_hex.to_axial_coordinate_hex()

    def to_even_row_offset_coordinate_hex(self) -> EvenRowOffsetCoordinateHex:
        return EvenRowOffsetCoordinateHex.from_row_col(row=self.r, col=self.q + (self.r + (self.r & 1)) // 2)

    @classmethod
    def from_even_row_offset_coordinate(cls, even_row_offset_hex: EvenRowOffsetCoordinateHex) -> AxialCoordinateHex:
        return even_row_offset_hex.to_axial_coordinate_hex()

    def to_odd_row_offset_coordinate_hex(self) -> OddRowOffsetCoordinateHex:
        return OddRowOffsetCoordinateHex.from_row_col(row=self.r, col=self.q + (self.r - (self.r & 1)) // 2)

    @classmethod
    def from_odd_row_offset_coordinate_hex(cls, odd_row_offset_hex: OddRowOffsetCoordinateHex) -> AxialCoordinateHex:
        return odd_row_offset_hex.to_axial_coordinate_hex()

    def to_even_column_offset_coordinate_hex(self) -> EvenColumnOffsetCoordinateHex:
        return EvenColumnOffsetCoordinateHex.from_row_col(row=self.r + (self.q + (self.q & 1)) // 2, col=self.q)

    @classmethod
    def from_even_column_offset_coordinate_hex(
        cls, even_column_offset_hex: EvenColumnOffsetCoordinateHex
    ) -> AxialCoordinateHex:
        return even_column_offset_hex.to_axial_coordinate_hex()

    def to_odd_column_offset_coordinate_hex(self) -> OddColumnOffsetCoordinateHex:
        return OddColumnOffsetCoordinateHex.from_row_col(row=self.r + (self.q - (self.q & 1)) // 2, col=self.q)

    @classmethod
    def from_odd_column_offset_coordinate_hex(
        cls, odd_column_offset_hex: OddColumnOffsetCoordinateHex
    ) -> AxialCoordinateHex:
        return odd_column_offset_hex.to_axial_coordinate_hex()

    def reflect_over_Q_axis(self) -> AxialCoordinateHex:
        return self.from_axial_coordinate_hex(AxialCoordinateHex(self.q, self._s))

    def reflect_over_R_axis(self) -> AxialCoordinateHex:
        return self.from_axial_coordinate_hex(AxialCoordinateHex(self._s, self.r))

    def reflect_over_S_axis(self) -> AxialCoordinateHex:
        return self.from_axial_coordinate_hex(AxialCoordinateHex(self.r, self.q))

    def reflect_over_Q(self, q: int = 0) -> AxialCoordinateHex:
        reference_point = AxialCoordinateHex(q, 0)
        shifted = self.to_axial_coordinate_hex() - reference_point
        reflected = shifted.reflect_over_Q_axis().reflect_over_hex()
        return self.from_axial_coordinate_hex(reflected + reference_point)

    def reflect_over_R(self, r: int = 0) -> AxialCoordinateHex:
        reference_point = AxialCoordinateHex(0, r)
        shifted = self.to_axial_coordinate_hex() - reference_point
        reflected = shifted.reflect_over_R_axis().reflect_over_hex()
        return self.from_axial_coordinate_hex(reflected + reference_point)

    def reflect_over_S(self, s: int = 0) -> AxialCoordinateHex:
        reference_point = AxialCoordinateHex(s, 0)
        shifted = self.to_axial_coordinate_hex() - reference_point
        reflected = shifted.reflect_over_S_axis().reflect_over_hex()
        return self.from_axial_coordinate_hex(reflected + reference_point)


@dataclass(frozen=True)
class CubeCoordinateHex(AxialCoordinateHex):
    s: int

    def __post_init__(self) -> None:
        assert (intercept := (self.q + self.r + self.s)) == 0, f"A Cube Hex must lie in a plane through the origin (q + r + s = 0), got {intercept} instead"  # fmt: skip

    # @property
    # def neighbor_directions(self) -> Annotated[list[CubeCoordinateHex], FixedLength(6)]:
    #     return [
    #         CubeCoordinateHex(q=1, r=0, s=-1),
    #         CubeCoordinateHex(q=1, r=-1, s=0),
    #         CubeCoordinateHex(q=0, r=-1, s=1),
    #         CubeCoordinateHex(q=-1, r=0, s=1),
    #         CubeCoordinateHex(q=-1, r=1, s=0),
    #         CubeCoordinateHex(q=0, r=1, s=-1),
    #     ]

    # def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
    #     return AxialCoordinateHex(self.q, self.r)

    @classmethod
    def from_axial_coordinate_hex(cls, axial_hex: AxialCoordinateHex) -> CubeCoordinateHex:
        return axial_hex.to_cube_coordinate_hex()

    @classmethod
    def from_2d_coordinates(cls, q: int, r: int) -> CubeCoordinateHex:
        return cls(q=q, r=r, s=-q - r)


@dataclass(frozen=True)
class EvenRowOffsetCoordinateHex(OffsetCoordinateHex):
    def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(q=self.col - (self.row + (self.row & 1)) // 2, r=self.row)

    @classmethod
    def from_axial_coordinate_hex(cls, axial_hex: AxialCoordinateHex) -> EvenRowOffsetCoordinateHex:
        return axial_hex.to_even_row_offset_coordinate_hex()

    @property
    def neighbor_directions(self) -> Annotated[list[EvenRowOffsetCoordinateHex], FixedLength(6)]:
        if self.row & 1:
            return [
                EvenRowOffsetCoordinateHex(1, 0),
                EvenRowOffsetCoordinateHex(0, -1),
                EvenRowOffsetCoordinateHex(-1, -1),
                EvenRowOffsetCoordinateHex(-1, 0),
                EvenRowOffsetCoordinateHex(-1, 1),
                EvenRowOffsetCoordinateHex(0, 1),
            ]
        return [
            EvenRowOffsetCoordinateHex(1, 0),
            EvenRowOffsetCoordinateHex(1, -1),
            EvenRowOffsetCoordinateHex(0, -1),
            EvenRowOffsetCoordinateHex(-1, 0),
            EvenRowOffsetCoordinateHex(0, 1),
            EvenRowOffsetCoordinateHex(1, 1),
        ]


@dataclass(frozen=True)
class OddRowOffsetCoordinateHex(OffsetCoordinateHex):
    def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(q=self.col - (self.row - (self.row & 1)) // 2, r=self.row)

    @classmethod
    def from_axial_coordinate_hex(cls, axial_hex: AxialCoordinateHex) -> OddRowOffsetCoordinateHex:
        return axial_hex.to_odd_row_offset_coordinate_hex()

    @property
    def neighbor_directions(self) -> Annotated[list[OddRowOffsetCoordinateHex], FixedLength(6)]:
        if self.row & 1:
            return [
                OddRowOffsetCoordinateHex(1, 0),
                OddRowOffsetCoordinateHex(1, -1),
                OddRowOffsetCoordinateHex(0, -1),
                OddRowOffsetCoordinateHex(-1, 0),
                OddRowOffsetCoordinateHex(0, 1),
                OddRowOffsetCoordinateHex(1, 1),
            ]
        return [
            OddRowOffsetCoordinateHex(1, 0),
            OddRowOffsetCoordinateHex(0, -1),
            OddRowOffsetCoordinateHex(-1, -1),
            OddRowOffsetCoordinateHex(-1, 0),
            OddRowOffsetCoordinateHex(-1, 1),
            OddRowOffsetCoordinateHex(0, 1),
        ]


@dataclass(frozen=True)
class EvenColumnOffsetCoordinateHex(OffsetCoordinateHex):
    def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(q=self.col, r=self.row - (self.col + (self.col & 1)) // 2)

    @classmethod
    def from_axial_coordinate_hex(cls, axial_hex: AxialCoordinateHex) -> EvenColumnOffsetCoordinateHex:
        return axial_hex.to_even_column_offset_coordinate_hex()

    @property
    def neighbor_directions(self) -> Annotated[list[EvenColumnOffsetCoordinateHex], FixedLength(6)]:
        if self.col & 1:
            return [
                EvenColumnOffsetCoordinateHex(1, 0),
                EvenColumnOffsetCoordinateHex(1, -1),
                EvenColumnOffsetCoordinateHex(0, -1),
                EvenColumnOffsetCoordinateHex(-1, -1),
                EvenColumnOffsetCoordinateHex(-1, 0),
                EvenColumnOffsetCoordinateHex(0, 1),
            ]
        return [
            EvenColumnOffsetCoordinateHex(1, 1),
            EvenColumnOffsetCoordinateHex(1, 0),
            EvenColumnOffsetCoordinateHex(0, -1),
            EvenColumnOffsetCoordinateHex(-1, 0),
            EvenColumnOffsetCoordinateHex(-1, 1),
            EvenColumnOffsetCoordinateHex(0, 1),
        ]


@dataclass(frozen=True)
class OddColumnOffsetCoordinateHex(OffsetCoordinateHex):
    def to_axial_coordinate_hex(self) -> AxialCoordinateHex:
        return AxialCoordinateHex(q=self.col, r=self.row - (self.col - (self.col & 1)) // 2)

    @classmethod
    def from_axial_coordinate_hex(cls, axial_hex: AxialCoordinateHex) -> OddColumnOffsetCoordinateHex:
        return axial_hex.to_odd_column_offset_coordinate_hex()

    @property
    def neighbor_directions(self) -> Annotated[list[OddColumnOffsetCoordinateHex], FixedLength(6)]:
        if self.col & 1:
            return [
                OddColumnOffsetCoordinateHex(1, 1),
                OddColumnOffsetCoordinateHex(1, 0),
                OddColumnOffsetCoordinateHex(0, -1),
                OddColumnOffsetCoordinateHex(-1, 0),
                OddColumnOffsetCoordinateHex(-1, 1),
                OddColumnOffsetCoordinateHex(0, 1),
            ]
        return [
            OddColumnOffsetCoordinateHex(1, 0),
            OddColumnOffsetCoordinateHex(1, -1),
            OddColumnOffsetCoordinateHex(0, -1),
            OddColumnOffsetCoordinateHex(-1, -1),
            OddColumnOffsetCoordinateHex(-1, 0),
            OddColumnOffsetCoordinateHex(0, 1),
        ]
