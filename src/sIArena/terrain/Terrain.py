from typing import List, Tuple
import numpy as np
import math

# Object representing a coordinate in the terrain (row, column)
Coordinate = Tuple[int,int]
# Object representing a path in the terrain (list of coordinates)
Path = List[Coordinate]


def default_cost_function(origin_height: int, target_height: int) -> int:
    """Default cost function"""
    if origin_height == target_height:
        # step in same level has cost 1
        return 1
    elif origin_height > target_height:
        # step down has same cost as the difference in height
        return origin_height - target_height
    else:
        # step up has double cost as the difference in height
        return (target_height - origin_height) * 2



class Terrain:
    """
    This class represents a 2D terrain in a NxM int matrix where each value is the height.

    The problem to solve would be to find the lowest path to go from 0x0 (top left) to N-1xM-1 (bottom right).
    Each step in the path can only be to the right, down, left or up (no diagonals).
    The cost for each step in the path is calculated as follows:

    From cell with cost X to cell with cost Y:
    - If X == Y: cost = 1           [keep in the same level]
    - If X > Y: cost = X - Y        [climb down]
    - If X < Y: cost = 2 * (Y - X)  [climb up]
    """

    def __init__(
                self,
                matrix: List[List[int]],
                origin: Coordinate = None,
                destination: Coordinate = None,
                cost_function: callable = default_cost_function,
            ):
        """
        Construct a terrain from a matrix of integers

        :param matrix: matrix of integers
        :param origin: origin of the path (if None top left corner)
        :param destination: destination of the path (if None bottom right corner)
        """
        self.matrix = matrix
        self.n = len(matrix)
        self.m = len(matrix[0])
        self.cost_function = cost_function

        self.origin = origin
        self.destination = destination

        if self.origin is None:
            self.origin = (0, 0)
        else:
            self.origin = (origin[0], origin[1])

        if self.destination is None:
            self.destination = (self.n - 1, self.m - 1)
        else:
            self.destination = (destination[0], destination[1])

        # Check that the origin is valid
        if self.origin[0] < 0 and self.origin[0] >= self.n:
            raise AttributeError(f"Origin row is out of bounds: {self.origin[0]}")
        if self.origin[1] < 0 and self.origin[1] >= self.m:
            raise AttributeError(f"Origin column is out of bounds: {self.origin[1]}")

        # Check that the destination is valid
        if self.destination[0] < 0 and self.destination[0] >= self.n:
            raise AttributeError("Destination row is out of bounds")
        if self.destination[1] < 0 and self.destination[1] >= self.m:
            raise AttributeError("Destination column is out of bounds")

        # Check that the matrix is valid
        for row in matrix:
            if len(row) == self.m:
                AttributeError("Matrix is not rectangular")

        # Check that the matrix is numpy or else convert it
        if not isinstance(self.matrix, np.ndarray):
            self.matrix = np.matrix(self.matrix, dtype=int)


    def __str__(self):
        """Returns a string representation of the terrain"""
        # Calculate the maximum length of a cell
        max_length = len(str(self.matrix.max()))
        # Create the string representation
        s = "+" + ("-" * (max_length + 2) + "+") * self.m + "\n"
        for i in range(self.n):
            for j in range(self.m):
                if (i,j) == self.origin:
                    s += "|+"
                elif (i,j) == self.destination:
                    s += "|x"
                else:
                    s += "| "
                s += str(self[(i,j)]).rjust(max_length) + " "
            s += "|\n"
            s += "+" + ("-" * (max_length + 2) + "+") * self.m + "\n"
        return s


    def __len__(self) -> int:
        """Returns the number of cells in the terrain"""
        return self.n * self.m


    def size(self) -> Tuple[int, int]:
        """Returns the size of the terrain (rows, columns)"""
        return (self.n, self.m)


    def __getitem__(self, key: Coordinate) -> int:
        """Returns the value of the cell at the given position"""
        return self.matrix[key[0],key[1]]


    def __repr__(self) -> str:
        """Returns a string representation of the terrain"""
        return str(self)


    def get_neighbors(self, pos: Coordinate) -> List[Coordinate]:
        """Returns the list of neighbors of the given position"""
        neighbors = []
        if pos[0] > 0:
            neighbors.append((pos[0] - 1, pos[1]))
        if pos[0] < self.n - 1:
            neighbors.append((pos[0] + 1, pos[1]))
        if pos[1] > 0:
            neighbors.append((pos[0], pos[1] - 1))
        if pos[1] < self.m - 1:
            neighbors.append((pos[0], pos[1] + 1))
        return neighbors


    def get_cost(self, pos1: Coordinate, pos2: Coordinate) -> int:
        """Returns the cost of going from pos1 to pos2"""
        return self.cost_function(self[pos1], self[pos2])


    def get_path_cost(self, path: Path) -> int:
        """Returns the cost of the given path"""
        cost = 0
        for i in range(len(path) - 1):
            c = self.get_cost(path[i], path[i + 1])
            cost += self.get_cost(path[i], path[i + 1])
        return cost


    def is_complete_path(self, path: Path) -> bool:
        """Returns True if the given path goes from the top left corner to the bottom right corner"""
        return self.is_valid_path(path) and path[0] == self.origin and path[-1] == self.destination


    def is_valid_path(self, path: Path) -> bool:
        """Returns True if the given path is valid"""
        if path is None or len(path) == 0:
            return False

        for i in range(len(path) - 1):
            if path[i + 1] not in self.get_neighbors(path[i]):
                return False
        return True
