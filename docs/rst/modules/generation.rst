.. _generation:

################
Generate Terrain
################

.. contents::
    :local:
    :backlinks: none
    :depth: 2

There are several classes that help to generate a random terrain so the user does not have to create the matrix manually.

The class ``Generator`` has a function ``generate_random_terrain`` that create an object of type ``Terrain`` (or ``DestinationSetTerrain`` if set).
These are the arguments for such function (some arguments are not used for different Generators):

- ``n: int`` number of rows
- ``m: int`` number of columns
- ``min_height: int = 0`` minimum height of the terrain
- ``max_height: int = 99`` maximum height of the terrain
- ``min_step: int = 1`` minimum step between two heights
- ``abruptness: float = 0.2`` 0: smooth, 1: abrupt
- ``seed: int = None`` seed for the random number generator
- ``origin: Coordinate = None`` origin of the terrain
- ``destination: Coordinate = None`` destination of the terrain
- ``terrain_ctor: Terrain = Terrain`` whether to use ``Terrain``or ``DestinationSetTerrain``
- ``cost_function: callable = None`` cost function for the terrain (if None use default)

There exist different generators that create the random matrix from different criteria:

.. code-block:: python

    from sIArena.terrain.generator.FocusedGenerator import FocusedGenerator
    from sIArena.terrain.generator.PerlinGenerator import PerlinGenerator
    from sIArena.terrain.generator.MazeGenerator import MazeGenerator

In order to generate a terrain, the user must create a generator object and call the function ``generate_random_terrain``:

.. code-block:: python

    generator = FocusedGenerator()
    terrain = generator.generate_random_terrain(n=10, m=10)


Focused Generator
=================

This generator generates the map from top-left corner to bottom-right corner.
It generates each cell depending on the contiguous cells and a distribution probability.

It tends to create very craggy and with diagonal mountains.

.. code-block:: python

    terrain = FocusedGenerator().generate_random_terrain(n=100, m=100, seed=0)

.. image:: /resources/images/focused100x100_0.png


Perlin Generator
================

This generator uses perlin noise to generate the terrain.

It tends to create smooth terrains with some hills and valleys.

.. code-block:: python

    terrain = PerlinGenerator().generate_random_terrain(n=100, m=100, seed=0)

.. image:: /resources/images/perlin100x100_0.png



Maze Generator
==============

This generator creates a maze.
This is, it creates a terrain with 1 width valley and 1 width very high wall.
The valley connects the whole map, so the terrain can be walked through without climbing any wall.

The origin and destination must be set afterwards.
It is assured to connect every valley point, and the top-left corner and bottom-right corner are always in a valley.

.. code-block:: python

    terrain = MazeGenerator().generate_random_terrain(n=100, m=100, seed=0)

.. image:: /resources/images/maze100x100_0.png
