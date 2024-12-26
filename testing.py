from Hex import AxialCoordinateHex, CubeCoordinateHex, DoubledHeightCoordinateHex, DoubledWidthCoordinateHex

if __name__ == "__main__":

    A = AxialCoordinateHex(0, 0)

    print(A.neighbors)

    print(-1*A.neighbors[0])

    print(-A.neighbors[1])

    print(A.hexes_within_range(0))
    print(A.hexes_within_range(1))
    print((l := A.hexes_within_range(3)), f'\n{len(l)}')

    B = A.to_cube_coordinate_hex()
    print(B.neighbors)

    C = AxialCoordinateHex(-4, 4)
    D = AxialCoordinateHex(-2, 1)
    E = C.reflect_over(D)
    print(E)