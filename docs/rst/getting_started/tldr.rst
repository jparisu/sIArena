.. _getting_started_tldr:

#####
TL;DR
#####

================
Project Overview
================

This project helps you to generate 2D terrains, that are matrix of integers, with a point of origin and a point of destination.
Over these terrains you have several features:

- You can print it in the console
- You can plot it in a ``matplotlib`` 2D plot
- You can plot it in 3D with different angles
- **You can check the total length of a given path from origin to destination**
- You can even draw the paths in the plots previously mentioned


============
Installation
============

Just use the following command in your notebook:

.. code-block:: py

    !pip install git+https://github.com/jparisu/sIArena.git

Check the :ref:`installation guide <getting_started_installation>` for more details.


=========================
How to generate a terrain
=========================

In order to generate a pseudorandom :ref:`elements_terrain`,
the abstract class ``TerrainGenerator`` is provided.
The main function use the following parameters:

- ``n: int`` number of rows
- ``m: int`` number of columns
- ``min_height: int = 0`` minimum height of the terrain
- ``max_height: int = 99`` maximum height of the terrain
- ``min_step: int = 1`` minimum step between two heights
- ``abruptness: float = 0.2`` 0: smooth, 1: abrupt
- ``seed: int = None`` seed for the random number generator
- ``origin: Coordinate = None`` origin of the terrain
- ``destination: Coordinate = None`` destination of the terrain

There are 2 main generators: ``FocusedTerrainGenerator`` and ``PernilTerrainGenerator``.

Create your terrain as follows:

.. code-block:: py

    from sIArena.terrain.generator.Generator import TerrainGenerator
    from sIArena.terrain.generator.FocusedGenerator import FocusedGenerator
    from sIArena.terrain.generator.PernilGenerator import PernilGenerator

    N = 20
    M = 20
    MIN_HEIGHT = 0
    MAX_HEIGHT = 10
    MIN_STEP = 1
    ABR = 0.1
    ORIGIN = None
    DESTINATION = None
    SEED = 60
    GENERATOR = PernilGenerator()

    terrain = TerrainGenerator.generate_random_terrain(
        GENERATOR,
        n=N,
        m=M,
        min_height=MIN_HEIGHT,
        max_height=MAX_HEIGHT,
        min_step=MIN_STEP,
        abruptness=ABR,
        seed=SEED,
        origin=ORIGIN,
        destination=DESTINATION)


=====================================
How to write a path finding algorithm
=====================================

Easy, create an algorithm that is able to retrieve a list of sequently :ref:`elements_coordinates`
that goes from the origin to the destination of the terrain.


.. code-block:: py

    from sIArena.terrain.Terrain import Coordinate, Path, Terrain
    from sIArena.measurements.measurements import measure_function

    terrain = ...  # Terrain already created

    def my_algorithm(terrain: Terrain) -> Path:
        path = [terrain.origin]

        # To check the possible next cells:
        terrain.get_neighbors(path[-1])
        # Add new sequently coordinates till the destination
        path.add(...)
        # ...

        return path + [terrain.destination]

    # measure your algorithm cost and time
    min_cost, second, path = measure_function(my_algorithm, terrain)
