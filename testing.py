from Hex import AxialCoordinateHex, CubeCoordinateHex, DoubledHeightCoordinateHex, DoubledWidthCoordinateHex

if __name__ == "__main__":

    A = AxialCoordinateHex(0, 0)

    print(A.neighbors)

    print(A.neighbors[0]*-1)