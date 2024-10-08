import random
import math
from typing import List
import numpy as np

from sIArena.terrain.Terrain import Coordinate, Terrain
from sIArena.terrain.generator.Generator import TerrainGenerator

from sIArena.utils.decorators import override


class MazeGenerator(TerrainGenerator):

    def generate_random_terrain(
                self,
                n: int,
                m: int,
                min_height: int = 0,
                max_height: int = 99,
                min_step: int = 1,
                abruptness: float = 0.2,
                seed: int = None,
                origin: Coordinate = None,
                destination: Coordinate = None,
                terrain_ctor: Terrain = Terrain,
                cost_function: callable = None
            ) -> Terrain:
        """ This inherited method set the min, max and step height of the terrain"""
        if min_step == 1:
            min_height = 0
            max_height = n*m
            min_step = n*m

        return super().generate_random_terrain(
            n=n, m=m, min_height=min_height, max_height=max_height, min_step=min_step, abruptness=abruptness, seed=seed, origin=origin, destination=destination, terrain_ctor=terrain_ctor, cost_function=cost_function)


    @override
    def generate_random_matrix_(
                self,
                n: int,
                m: int,
                abruptness: float = 0.5,
                seed: int = None
            ) -> np.matrix:
        """
        TODO
        """

        if seed is not None:
            random.seed(seed)

        maze_n = (1 + n) // 2
        maze_m = (1 + m) // 2

        maze = Maze(maze_n, maze_m)

        matrix = np.zeros((n, m))

        for i in range(maze_n):
            for j in range(maze_m):
                up_left = (2*i, 2*j)        # always 0
                down_right = (2*i+1, 2*j+1) # always 1
                up_right = (2*i, 2*j+1)     # 1 when no right wall
                down_left = (2*i+1, 2*j)    # 1 when no down wall

                if 2*j+1 < m and not maze.tile((i, j)).right:
                    matrix[up_right] = 1
                if 2*i+1 < n and not maze.tile((i, j)).down:
                    matrix[down_left] = 1
                if 2*i+1 < n and 2*j+1 < m:
                    matrix[down_right] = 1

        # Assure last cell is 0
        matrix[-1][-1] = 0

        # If both n and m are even, add a connection between the last two cells
        if n % 2 == 0 and m % 2 == 0:
            matrix[-2][-1] = 0

        return matrix


class Tile:

    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.visited = False

    def add_up(self):
        self.up = True

    def add_down(self):
        self.down = True

    def add_left(self):
        self.left = True

    def add_right(self):
        self.right = True

    def visit(self):
        self.visited = True


def weigthed_distrubution(n, r=10):

    if n == 1:
        return 0

    choices = [i for i in range(n)]
    weights = [1 for i in range(n)]

    x = 0
    for i in range(n):
        weights[i] *= n-1
        weights[i] += x
        x += r - 1

    return random.choices(choices, weights=weights, k=1)[0]


class Maze:

    def __init__(self, n, m, start_point=None):
        self.n = n
        self.m = m
        self.matrix = [[Tile() for _ in range(m)] for _ in range(n)]

        if start_point is None:
            current = (n//2, m//2)
        else:
            current = start_point

        self.matrix[current[0]][current[1]].visit()
        to_visit = self.surrounding_coordinates(current)


        while to_visit:

            # Get a random number from 0 to n being the last ones more probable
            n = len(to_visit)
            r = weigthed_distrubution(n)
            next_tile = to_visit.pop(r)

            if self.tile(next_tile).visited:
                continue

            self.matrix[next_tile[0]][next_tile[1]].visit()

            # Get all surrounding tiles
            surrounding = self.surrounding_coordinates(next_tile)

            # Separate visited from non visited
            visited = []
            non_visited = []
            for s in surrounding:
                if self.tile(s).visited:
                    visited.append(s)
                else:
                    non_visited.append(s)

            # Join with a random visited one
            if visited:
                r = random.randint(0, len(visited) - 1)
                visited_tile = visited[r]
                self.join_tiles(next_tile, visited_tile)
                self.tile(visited_tile).visit()
            else:
                raise Exception("No visited tiles around")

            # Add non visited to to_visit
            for s in non_visited:
                to_visit.append(s)


    def tile(self, coor):
        return self.matrix[coor[0]][coor[1]]

    def surrounding_coordinates(self, coor):
        n, m = coor
        coords = []
        if n > 0:
            coords.append((n - 1, m))
        if n < self.n - 1:
            coords.append((n + 1, m))
        if m > 0:
            coords.append((n, m - 1))
        if m < self.m - 1:
            coords.append((n, m + 1))
        return coords

    def join_tiles(self, tile1, tile2):
        # Check if tile2 is up, down, left or right of tile1
        n1, m1 = tile1
        n2, m2 = tile2

        if n1 == n2:
            if m1 < m2:
                self.matrix[n1][m1].add_right()
                self.matrix[n2][m2].add_left()
            else:
                self.matrix[n1][m1].add_left()
                self.matrix[n2][m2].add_right()

        elif m1 == m2:
            if n1 < n2:
                self.matrix[n1][m1].add_down()
                self.matrix[n2][m2].add_up()
            else:
                self.matrix[n1][m1].add_up()
                self.matrix[n2][m2].add_down()

        else:
            raise Exception("Tiles are not adjacent")

    def __str__(self):
        s = ""
        for i in range(self.n):
            for j in range(self.m):
                if self.matrix[i][j].up:
                    s += "+    +"
                else:
                    s += "+----+"
            s += "\n"
            for _ in range(2):
                for j in range(self.m):
                    if self.matrix[i][j].left:
                        s += " "
                    else:
                        s += "|"
                    s += "    "
                    if self.matrix[i][j].right:
                        s += " "
                    else:
                        s += "|"
                s += "\n"
            for j in range(self.m):
                if self.matrix[i][j].down:
                    s += "+    +"
                else:
                    s += "+----+"
            s += "\n"

        return s
