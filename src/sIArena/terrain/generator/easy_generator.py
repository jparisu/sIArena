
from sIArena.terrain.Terrain import Coordinate, Terrain
from sIArena.terrain.generator.Generator import TerrainGenerator
from sIArena.terrain.generator.PernilGenerator import PernilGenerator
from sIArena.terrain.generator.FocusedGenerator import FocusedGenerator


def generate_random_terrain(
            generator_ctor: TerrainGenerator,
            n: int,
            m: int,
            min_height: int = 0,
            max_height: int = 99,
            min_step: int = 1,
            abruptness: float = 0.2,
            seed: int = None,
            origin: Coordinate = None,
            destination: Coordinate = None
        ) -> Terrain:
    return generator_ctor().generate_random_terrain(
        n=n,
        m=m,
        min_height=min_height,
        max_height=max_height,
        min_step=min_step,
        abruptness=abruptness,
        seed=seed,
        origin=origin,
        destination=destination
    )
