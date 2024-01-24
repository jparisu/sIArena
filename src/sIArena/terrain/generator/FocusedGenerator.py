import random
import math
from typing import List
import numpy as np

from sIArena.terrain.Terrain import Coordinate, Terrain
from sIArena.terrain.generator.Generator import TerrainGenerator

from sIArena.utils.decorators import override


class FocusedGenerator(TerrainGenerator):

    @override
    def generate_random_matrix_(
                self,
                n: int,
                m: int,
                abruptness: float = 0.5,
                seed: int = None,
            ) -> np.matrix:
        """
        TODO
        """

        if seed is not None:
            random.seed(seed)

        matrix = np.ones((n, m))

        # Generate first row
        for j in range(1, m):
            matrix[0][j] = FocusedGenerator.focused_value_generator(
                [matrix[0][j - 1]], abruptness)

        # Generate first column
        for i in range(1, n):
            matrix[i][0] = FocusedGenerator.focused_value_generator(
                [matrix[i - 1][0]], abruptness)

        # Generate the rest of the matrix
        for i in range(1, n):
            for j in range(1, m):
                matrix[i][j] = FocusedGenerator.focused_value_generator(
                    [matrix[i - 1][j], matrix[i][j - 1]], abruptness)

        print(matrix)

        return matrix


    def focused_value_generator(
                sources: List[float],
                abrutness: float,
                possibilities: int = 5,
            ) -> float:
        """
        TODO
        """
        # First lets calculate the mean of the sources
        cmean = sum(sources) / len(sources)
        cmax = max(sources)
        cmin = min(sources)

        vmin = cmin - (abrutness * cmean)
        vmax = cmax + (abrutness * cmean)
        vstep = (vmax - vmin) / (possibilities - 1)

        # Now lets calculate the possible values
        values = [vmin + i * vstep for i in range(possibilities)]

        return random.choice(values)
