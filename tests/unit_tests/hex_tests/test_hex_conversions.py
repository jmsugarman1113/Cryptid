from dataclasses import fields

from cryptid.hex import (
    AxialCoordinateHex,
    CubeCoordinateHex,
    DoubledHeightCoordinateHex,
    DoubledWidthCoordinateHex,
    EvenColumnOffsetCoordinateHex,
    EvenRowOffsetCoordinateHex,
    OddColumnOffsetCoordinateHex,
    OddRowOffsetCoordinateHex,
)


class TestHexConversions:
    @staticmethod
    def conversion_helper(
        axial: AxialCoordinateHex,
        cube: CubeCoordinateHex,
        double_height: DoubledHeightCoordinateHex,
        double_width: DoubledWidthCoordinateHex,
        odd_row: OddRowOffsetCoordinateHex,
        even_row: EvenRowOffsetCoordinateHex,
        odd_column: OddColumnOffsetCoordinateHex,
        even_column: EvenColumnOffsetCoordinateHex,
    ) -> None:
        assert axial.to_axial_coordinate_hex() == axial
        assert AxialCoordinateHex.from_axial_coordinate_hex(axial) == axial

        assert axial.to_cube_coordinate_hex() == cube
        assert AxialCoordinateHex.from_cube_coordinate_hex(cube) == axial
        assert cube.to_axial_coordinate_hex() == axial
        assert CubeCoordinateHex.from_axial_coordinate_hex(axial) == cube

        assert axial.to_double_height_coordinate_hex() == double_height
        assert AxialCoordinateHex.from_double_height_coordinate_hex(double_height) == axial
        assert double_height.to_axial_coordinate_hex() == axial
        assert DoubledHeightCoordinateHex.from_axial_coordinate_hex(axial) == double_height

        assert axial.to_double_width_coordinate_hex() == double_width
        assert AxialCoordinateHex.from_double_width_coordinate_hex(double_width) == axial
        assert double_width.to_axial_coordinate_hex() == axial
        assert DoubledWidthCoordinateHex.from_axial_coordinate_hex(axial) == double_width

        assert axial.to_odd_row_offset_coordinate_hex() == odd_row
        assert AxialCoordinateHex.from_odd_row_offset_coordinate_hex(odd_row) == axial
        assert odd_row.to_axial_coordinate_hex() == axial
        assert OddRowOffsetCoordinateHex.from_axial_coordinate_hex(axial) == odd_row

        assert axial.to_even_row_offset_coordinate_hex() == even_row
        assert AxialCoordinateHex.from_even_row_offset_coordinate(even_row) == axial
        assert even_row.to_axial_coordinate_hex() == axial
        assert EvenRowOffsetCoordinateHex.from_axial_coordinate_hex(axial) == even_row

        assert axial.to_odd_column_offset_coordinate_hex() == odd_column
        assert AxialCoordinateHex.from_odd_column_offset_coordinate_hex(odd_column) == axial
        assert odd_column.to_axial_coordinate_hex() == axial
        assert OddColumnOffsetCoordinateHex.from_axial_coordinate_hex(axial) == odd_column

        assert axial.to_even_column_offset_coordinate_hex() == even_column
        assert AxialCoordinateHex.from_even_column_offset_coordinate_hex(even_column) == axial
        assert even_column.to_axial_coordinate_hex() == axial
        assert EvenColumnOffsetCoordinateHex.from_axial_coordinate_hex(axial) == even_column

    def test_origins_all_equal(self):
        axial_origin = AxialCoordinateHex.origin()
        other_hex_types = [
            CubeCoordinateHex,
            DoubledHeightCoordinateHex,
            DoubledWidthCoordinateHex,
            OddRowOffsetCoordinateHex,
            EvenRowOffsetCoordinateHex,
            OddColumnOffsetCoordinateHex,
            EvenColumnOffsetCoordinateHex,
        ]
        for hex_type in other_hex_types:
            other_origin = hex_type.from_axial_coordinate_hex(axial_origin)
            assert other_origin == hex_type.origin()
            assert all(getattr(other_origin, f.name) == 0 for f in fields(other_origin))

            from_other_origin = hex_type.origin().to_axial_coordinate_hex()
            assert from_other_origin == axial_origin
            assert from_other_origin.q == 0 and from_other_origin.r == 0

        self.conversion_helper(axial_origin, *[hex_type.origin() for hex_type in other_hex_types])

    def test_conversions_1(self):
        axial = AxialCoordinateHex(1, 2)
        cube = CubeCoordinateHex(1, 2, -3)
        double_height = DoubledHeightCoordinateHex(1, 5)
        double_width = DoubledWidthCoordinateHex(4, 2)
        odd_row = OddRowOffsetCoordinateHex(2, 2)
        even_row = EvenRowOffsetCoordinateHex(2, 2)
        odd_column = OddColumnOffsetCoordinateHex(1, 2)
        even_column = EvenColumnOffsetCoordinateHex(1, 3)

        self.conversion_helper(
            axial=axial,
            cube=cube,
            double_height=double_height,
            double_width=double_width,
            odd_row=odd_row,
            even_row=even_row,
            odd_column=odd_column,
            even_column=even_column,
        )

    def test_conversions_2(self):
        self.conversion_helper(
            axial=AxialCoordinateHex(5, -1),
            cube=CubeCoordinateHex(5, -1, -4),
            double_height=DoubledHeightCoordinateHex(5, 3),
            double_width=DoubledWidthCoordinateHex(9, -1),
            odd_column=OddColumnOffsetCoordinateHex(5, 1),
            odd_row=OddRowOffsetCoordinateHex(4, -1),
            even_column=EvenColumnOffsetCoordinateHex(5, 2),
            even_row=EvenRowOffsetCoordinateHex(5, -1),
        )

    def test_equality_origin(self):
        assert AxialCoordinateHex.origin() == AxialCoordinateHex.origin()
        assert AxialCoordinateHex.origin() == CubeCoordinateHex.origin()
        assert AxialCoordinateHex.origin() == DoubledHeightCoordinateHex.origin()
        assert AxialCoordinateHex.origin() == DoubledWidthCoordinateHex.origin()
        assert AxialCoordinateHex.origin() == OddColumnOffsetCoordinateHex.origin()
        assert AxialCoordinateHex.origin() == OddRowOffsetCoordinateHex.origin()
        assert AxialCoordinateHex.origin() == EvenColumnOffsetCoordinateHex.origin()
        assert AxialCoordinateHex.origin() == EvenRowOffsetCoordinateHex.origin()

    def test_equality_1(self):
        assert AxialCoordinateHex(1, 2) == AxialCoordinateHex(1, 2)
        assert AxialCoordinateHex(1, 2) == CubeCoordinateHex(1, 2, -3)
        assert AxialCoordinateHex(1, 2) == DoubledHeightCoordinateHex(1, 5)
        assert AxialCoordinateHex(1, 2) == DoubledWidthCoordinateHex(4, 2)
        assert AxialCoordinateHex(1, 2) == OddRowOffsetCoordinateHex(2, 2)
        assert AxialCoordinateHex(1, 2) == EvenRowOffsetCoordinateHex(2, 2)
        assert AxialCoordinateHex(1, 2) == OddColumnOffsetCoordinateHex(1, 2)
        assert AxialCoordinateHex(1, 2) == EvenColumnOffsetCoordinateHex(1, 3)

        assert AxialCoordinateHex(0, 0) != AxialCoordinateHex(1, 2)
        assert AxialCoordinateHex(0, 0) != CubeCoordinateHex(1, 2, -3)
        assert AxialCoordinateHex(0, 0) != DoubledHeightCoordinateHex(1, 5)
        assert AxialCoordinateHex(0, 0) != DoubledWidthCoordinateHex(4, 2)
        assert AxialCoordinateHex(0, 0) != OddRowOffsetCoordinateHex(2, 2)
        assert AxialCoordinateHex(0, 0) != EvenRowOffsetCoordinateHex(2, 2)
        assert AxialCoordinateHex(0, 0) != OddColumnOffsetCoordinateHex(1, 2)
        assert AxialCoordinateHex(0, 0) != EvenColumnOffsetCoordinateHex(1, 3)