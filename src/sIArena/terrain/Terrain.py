from typing import List, Tuple, Set
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


class NoPathTerrain:
    """
    This class represents a 2D terrain in a NxM int matrix where each value is the height.

    The problem to solve would be to find the lowest path to go from 0x0 (top left) to N-1xM-1 (bottom right).
    Each step in the path can only be to the right, down, left or up (no diagonals).
    The cost for each step in the path is calculated regarding the cost function
    """

    def __init__(
                self,
                matrix: List[List[int]],
                cost_function: callable = default_cost_function,
            ):
        """
        Construct a terrain from a matrix of integers

        :param matrix: matrix of integers
        :param origin: origin of the path (if None top left corner)
        :param destinations: list of destinations in order(if None bottom right corner)
        """
        self.matrix = matrix
        self.n = len(matrix)
        self.m = len(matrix[0])
        self.cost_function = cost_function

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


    def is_complete_path(self, path: Path) -> Tuple[bool, str]:
        """True if valid path"""
        return self.is_valid_path(path)


    def is_valid_path(self, path: Path) -> bool:
        return self.why_valid_path()[0]

    def why_valid_path(self, path: Path) -> Tuple[bool, str]:
        """Returns True if the given path is valid"""
        if path is None or len(path) == 0:
            return False

        for i in range(len(path) - 1):
            if path[i + 1] not in self.get_neighbors(path[i]):
                return False, f"Invalid path: {path[i]} -> {path[i + 1]}"
        return True, "Valid path"


    def get_destinations(self) -> List[Coordinate]:
        return None

class Terrain (NoPathTerrain):
    """
    This class is a Terrain with an origin and a destination
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
        super().__init__(matrix, cost_function)
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
            raise AttributeError(f"Destination row is out of bounds: {self.destination[0]}")
        if self.destination[1] < 0 and self.destination[1] >= self.m:
            raise AttributeError(f"Destination column is out of bounds: {self.destination[1]}")


    def is_complete_path(self, path: Path) -> bool:
        return self.is_complete_path()[0]

    def why_complete_path(self, path: Path) -> Tuple[bool, str]:
        """Returns True if the given path goes from the origin to the destination"""
        # Check that the path is valid
        valid = self.is_valid_path(path)
        if not valid[0]:
            return valid

        # Check that the path goes from the origin to the destination
        if path[0] != self.origin:
            return False, f"Path does not start in the origin {self.origin}"
        if path[-1] != self.destination:
            return False, f"Path does not end in the destination {self.destination}"
        return True, "Complete path"


    def __str__(self):
        """Returns a string representation of the terrain"""
        # Calculate the maximum length of a cell
        max_length = len(str(self.matrix.max()))
        # Create the string representation
        s = "+" + ("-" * (max_length + 3) + "+") * self.m + "\n"
        for i in range(self.n):
            for j in range(self.m):
                s += "|"
                if (i,j) == self.origin:
                    s += "O "
                elif (i,j) == self.destination:
                    s += "X "
                else:
                    s += "  "
                s += str(self[(i,j)]).rjust(max_length) + " "
            s += "|\n"
            s += "+" + ("-" * (max_length + 3) + "+") * self.m + "\n"
        return s


    def get_destinations(self) -> List[Coordinate]:
        return [self.destination]


class DestinationSetTerrain (NoPathTerrain):
    """
    This class represents a Terrain with an origin and a set of destinations that the paths must go through without order.
    """

    def __init__(
                self,
                matrix: List[List[int]],
                origin: Coordinate = None,
                destination: Set[Coordinate] = None,
                cost_function: callable = default_cost_function,
            ):
        """
        Construct a terrain from a matrix of integers

        :param matrix: matrix of integers
        :param origin: origin of the path (if None top left corner)
        :param destinations: list of destinations in order(if None bottom right corner)
        """
        super().__init__(matrix, cost_function)
        self.origin = origin
        self.destinations = destination

        if self.origin is None:
            self.origin = (0, 0)
        else:
            self.origin = (origin[0], origin[1])

        if self.destinations is None:
            self.destinations = {(self.n - 1, self.m - 1)}
        else:
            self.destinations = set(destination)

        # Check that the origin is valid
        if self.origin[0] < 0 and self.origin[0] >= self.n:
            raise AttributeError(f"Origin row is out of bounds: {self.origin[0]}")
        if self.origin[1] < 0 and self.origin[1] >= self.m:
            raise AttributeError(f"Origin column is out of bounds: {self.origin[1]}")

        # Check that the destinations are valid
        for destination in self.destinations:
            if destination[0] < 0 and destination[0] >= self.n:
                raise AttributeError(f"Destination row is out of bounds: {destination[0]}")
            if destination[1] < 0 and destination[1] >= self.m:
                raise AttributeError(f"Destination column is out of bounds: {destination[1]}")
            # Check there are not the origin
            if destination == self.origin:
                raise AttributeError(f"Destination is the origin: {destination}")


    def is_complete_path(self, path: Path) -> bool:
        return self.why_complete_path()[0]

    def why_complete_path(self, path: Path) -> Tuple[bool, str]:
        """Returns True if the given path goes from the origin to all the destinations"""
        # Check that the path is valid
        valid = self.is_valid_path(path)
        if not valid[0]:
            return valid

        # Check that the path goes from the origin to all the destinations
        if path[0] != self.origin:
            return False, f"Path does not start in the origin {self.origin}"

        for destination in self.destinations:
            if destination not in path:
                return False, f"Path does not go through the destination {destination}"

        return True, "Complete path"


    def __str__(self):
        """Returns a string representation of the terrain"""
        # Calculate the maximum length of a cell
        max_length = len(str(self.matrix.max()))
        # Create the string representation
        s = "+" + ("-" * (max_length + 3) + "+") * self.m + "\n"
        for i in range(self.n):
            for j in range(self.m):
                s += "|"
                if (i,j) == self.origin:
                    s += "O "
                elif (i,j) in self.destinations:
                    s += "X "
                else:
                    s += "  "
                s += str(self[(i,j)]).rjust(max_length) + " "
            s += "|\n"
            s += "+" + ("-" * (max_length + 3) + "+") * self.m + "\n"
        return s


    def get_destinations(self) -> List[Coordinate]:
        return self.destinations
