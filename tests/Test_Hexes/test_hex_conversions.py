from dataclasses import fields

from cryptid.Hex import (
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
    def test_origins_all_equal(self):
        axial_origin = AxialCoordinateHex.origin()
        for hex_type in [
            CubeCoordinateHex,
            DoubledHeightCoordinateHex,
            DoubledWidthCoordinateHex,
            EvenRowOffsetCoordinateHex,
            OddRowOffsetCoordinateHex,
            EvenColumnOffsetCoordinateHex,
            OddColumnOffsetCoordinateHex,
        ]:
            other_origin = hex_type.from_axial_coordinate_hex(axial_origin)
            assert other_origin == hex_type.origin()
            assert all(getattr(other_origin, f.name) == 0 for f in fields(other_origin))

    def test_conversions_1(self):
        axial = AxialCoordinateHex(1, 2)
        cube = CubeCoordinateHex(1, 2, -3)
        double_height = DoubledHeightCoordinateHex(1, 5)
        double_width = DoubledWidthCoordinateHex(4, 2)
        odd_row = OddRowOffsetCoordinateHex(2, 2)
        even_row = EvenRowOffsetCoordinateHex(2, 2)
        odd_column = OddColumnOffsetCoordinateHex(1, 2)
        even_column = EvenColumnOffsetCoordinateHex(1, 3)

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
