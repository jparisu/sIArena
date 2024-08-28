from noise import pnoise2
import random
import math
import numpy as np

from sIArena.terrain.Terrain import Coordinate, Terrain
from sIArena.terrain.generator.Generator import TerrainGenerator

from sIArena.utils.decorators import override

class PerlinGenerator(TerrainGenerator):

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
        abruptness *= 25
        abruptness = max(0.0001, abruptness)

        if seed is not None:
            random.seed(seed)
        base = random.randint(0, 999999)

        scale = math.sqrt(n * m) / abruptness

        map = np.zeros((n,m))
        for i in range(n):
            for j in range(m):
                map[i][j] = PerlinGenerator.perlin_value_generator(
                    i, j, base, scale)
        return map


    def perlin_value_generator(
                i: int,
                j: int,
                base: int,
                scale: int,
                persistence: float = 0.5,
                octaves: int = 2,
                lacunarity: float = 2.0
            ) -> int:
        """
        Generates a random value for a cell of a terrain using Perlin noise

        :param i: row of the cell
        :param j: column of the cell
        :param base: base value of the cell
        :param persistence: level of persistence of the terrain (0 = smooth, 1 = abrupt)
        :param scale: index of change of the terrain (0 = smooth, 1 = abrupt)
        :param octave: number of octaves of the noise
        :param lacunarity: lacunarity of the noise
        """

        return pnoise2(
            (base + i) / scale,
            (base + j) / scale,
            persistence=persistence,
            octaves=octaves,
            lacunarity=lacunarity)
