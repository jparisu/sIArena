import random
import math
import numpy as np
from typing import List

from sIArena.terrain.Terrain import Coordinate, Terrain
from sIArena.utils.math_utils import scalade
from sIArena.utils.decorators import pure_virtual

class TerrainGenerator:

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
        # Max and min abruptness
        abruptness = min(1, max(0, abruptness))

        # Matrix
        m = self.generate_random_matrix_(
            n=n,
            m=m,
            abruptness=abruptness,
            seed=seed)

        # Virtual max
        vmax = max_height // min_step

        # Normalize matrix
        m = scalade(m, min_height, vmax)

        # Convert the matrix to integers using numpy
        final_m = np.zeros(m.shape, dtype=int)
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                final_m[i,j] = round(m[i,j])

        final_m *= min_step

        if cost_function is not None:
            return terrain_ctor(final_m, origin=origin, destination=destination, cost_function=cost_function)
        else:
            return terrain_ctor(final_m, origin=origin, destination=destination)


    @pure_virtual
    def generate_random_matrix_(
                self,
                n: int,
                m: int,
                abruptness: float = 0.5,
                seed: int = None,
            ) -> np.matrix:
        pass
