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

    def test_conversions(self):
        # TODO: pick an axial hex and manually confirm all the conversions work as expected
        # forward and backward
        pass
