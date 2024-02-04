.. _getting_started_tutorial:

########
Tutorial
########

.. contents::
    :local:
    :backlinks: none
    :depth: 2

**sIArena** is a *Python* project that provides a simple and easy-to-use interface to test path finding algorithms.
It is able to generate pseudo-random maps called :ref:`elements_terrain` to simulate a 2D environment.

A :ref:`elements_terrain` is a 2D grid of cells formed by an integer matrix, a point of origin and a point of destination.
Each cell of the matrix represents the height of that cell, what it is used to calculate the cost of moving from one cell to another.
A :ref:`elements_path` is a list of :ref:`Coordinates <elements_coordinate>` that represents a path from the origin to the destination of a specific terrain.
These path could be measured to determine the total cost of moving from the origin to the destination.
As lower the cost, better the path.

This project implements the environment required to test different path finding algorithms and compare their performance in path cost and time.
It provides :ref:`generation tools <generation>` to create pseudo-random terrains,
:ref:`visualization tools <visualization>` to display terrains and paths in a graphical interface,
and :ref:`measure tools <measure>` to measure algorithm performance.


.. _getting_started_installation:

Installation
============

**sIArena** is a *Python* project,
check the :ref:`following section <installation>` to install the project and its dependencies.

The advised way to install **sIArena** is using a *Python Jupyter Notebook* in *Google Colab*,
or using a package manager like *pip* or *Anaconda* in a local environment.


.. _getting_started_generation:

Generate a terrain
==================

In order create a path finding algorithm, first we need to create a terrain to test it.
The library provides a set of :ref:`tools <generation>` to generate pseudo-random terrains.

The following snippet generates the terrain displayed below.

.. code-block:: python

    from sIArena.terrain.Terrain import Coordinate, Terrain, Path
    from sIArena.terrain.generator.PernilGenerator import PernilGenerator

    terrain = PernilGenerator().generate_random_terrain(
        n=25,
        m=25,
        min_height=0,
        max_height=100,
        min_step=25,
        abruptness=0.1,
        seed=60,
        origin=None,
        destination=None)

    # To print the terrain in ascii format
    print(terrain)

.. code-block:: text

    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |+ 50 |  50 |  50 |  50 |  50 |  25 |  25 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  50 |  50 |  50 |  50 |  50 |  25 |   0 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  75 |  75 | 100 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  50 |  50 |  50 |  50 |  50 |  25 |  25 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  50 |  50 |  50 |  50 |  50 |  25 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  50 |  50 |  50 |  50 |  50 |  25 |  25 |  25 |  50 |  50 |  50 |  25 |  25 |  50 |  50 |  50 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  50 |  50 |  50 |  50 |  50 |  25 |  25 |  25 |  50 |  50 |  50 |  25 |  25 |  25 |  50 |  50 |  50 |  75 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  50 |  50 |  50 |  50 |  25 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  75 |  75 |  50 |  50 |  50 |  50 |  75 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  50 |  25 |  25 |  25 |  25 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  50 |  75 |  75 |  75 |  75 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  25 |  25 |  25 |  25 |  25 |  25 |  25 |  25 |  50 |  50 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  75 |  75 |  75 |  75 |  75 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  25 |  25 |  25 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  75 |  75 |  75 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  25 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  25 |  25 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |  25 |  25 |  50 |  50 |  75 |  75 |  75 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  50 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |  50 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |  25 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  50 |  50 |  75 |  75 |  75 |  75 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |  50 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  25 |  25 |  25 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  75 |  75 |  75 |  75 |  75 |  75 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  25 |  25 |  25 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    | 100 |  75 |  75 |  75 |  75 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  50 |  25 |  25 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    | 100 | 100 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |  25 |  25 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  50 |  75 |  50 |  50 |  50 |  25 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    | 100 | 100 |  75 |  75 |  50 |  50 |  50 |  25 |  25 |  25 |  25 |  25 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    | 100 |  75 |  75 |  50 |  50 |  50 |  25 |  25 |  25 |  25 |  25 |  25 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    | 100 |  75 |  75 |  50 |  50 |  25 |  25 |  25 |  25 |  25 |  25 |  25 |  25 |  25 |  50 |  50 |  50 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  75 |  75 |  50 |  50 |  25 |  25 |  25 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  75 |  75 |  50 |  25 |  25 |  25 |  25 |  25 |  25 |  25 |  50 |  50 |  50 |  50 |  50 |  75 |  75 |  75 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  75 |  50 |  50 |  25 |  25 |   0 |   0 |   0 |  25 |  25 |  50 |  50 |  50 |  50 |  75 |  75 |  75 | 100 |  75 |  75 |  50 |  50 |  50 |  50 |  50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  50 |  50 |  50 |  25 |  25 |   0 |   0 |   0 |   0 |  25 |  50 |  50 |  50 |  50 |  75 |  75 | 100 | 100 |  75 |  75 |  50 |  50 |  50 |  50 |x 50 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+


.. image:: /resources/images/2dplot_10_10.png

For further information about the terrain generation, check the :ref:`generation section <generation>`.


.. _getting_started_plotting:

Plot the terrain
================

The terrains could be graphically displayed using the :ref:`plotting tools <visualization>`.
These tools allow to display the terrain as a height map in 2D or 3D.

The following snippet plots the terrain generated in the previous section:

.. code-block:: python

    from sIArena.terrain.plot.plot_2D import plot_terrain_2D
    from sIArena.terrain.plot.plot_3D import plot_terrain_3D

    plot_terrain_2D(terrain)
    plot_terrain_3D(terrain, angles=[(80, 10), (30, 190), (30, 10)])

.. image:: /resources/images/2dplot_10_10.png

.. image:: /resources/images/3dplot_10_10.png


The library also support to show a path in the terrain, as shown in the following snippet:

.. code-block:: python

    from sIArena.terrain.plot.plot_2D import plot_terrain_2D
    from sIArena.terrain.plot.plot_3D import plot_terrain_3D

    # Create a path (it is not valid neither complete)
    path = [terrain.origin, terrain.destination]

    plot_terrain_2D(terrain, paths=[path])
    plot_terrain_3D(terrain, paths=[path], angles=[(80, 10), (30, 190), (30, 10)])


.. image:: /resources/images/2dplot_10_10_solved.png

.. image:: /resources/images/3dplot_10_10_solved.png

For further information about the terrain plotting, check the :ref:`plotting section <visualization>`.


.. _getting_started_path_finding:

Path finding algorithm
======================

The main goal of the library is to allow to create and test different path finding algorithms.
These algorithms are expected to find the lowest cost possible path from the origin to the destination of a terrain.
To generate such kind of algorithms, just create a function which only parameter is a terrain, and that returns a path.

Complete path
-------------

A path is a list of sequently :ref:`Coordinates <elements_coordinate>` from the origin to the destination of a specific terrain.
In order for a path to be valid, each coordinate must be adjacent to the next one,
this means, to be at a distance of 1 in the x or y axis, but not in both at the same time.

Be aware that not all the terrains start and end in the corners, but their origin and destination may vary.
In order for a path to be complete, the first coordinate must be the origin and the last one the destination.

The following snippet shows different terrain methods that helps to create a path:

.. code-block:: python

    import random # import and seed random module
    random.seed(0)

    from sIArena.terrain.Terrain import Coordinate, Terrain, Path

    def find_path(terrain: Terrain) -> Path:
        # Get the terrain size
        n, m = terrain.size()

        # Get origin and destination coordinates
        origin = terrain.origin
        destination = terrain.destination

        # Create a path that starts in origin
        path = [origin]

        # Check the possible neighbors of the origin (thus, the possible next step of the path)
        neigs = terrain.get_neighbors(path[-1])

        # Check the cost from the origin to each neighbor
        costs = [terrain.get_cost(path[-1], neig) for neig in neigs]

        # Using these functions, we can create a random path that starts in the origin and ends in the destination
        while path[-1] != destination:
            next_step = random.choice(terrain.get_neighbors(path[-1]))
            path.append(next_step)

        # Return the path
        return path


    # Get the path solution
    path = find_path(terrain)

    # Check if a path is complete (it must be with our implementation)
    terrain.is_complete_path(path)

    # Calculate the cost of a path
    terrain.get_path_cost(path)




Measurement
===========

The library also provides a way to :ref:`measure <measure>` the performance of the path finding algorithms.
This is done by measuring the mean time and the minimum cost of the path found by the algorithm over a terrain.

The following snippet shows how to measure the performance of the algorithm implemented before:

.. code-block:: python

    from sIArena.measurements.measurements import measure_function

    min_cost, second, path = measure_function(
        find_path,
        terrain,
        iterations=5,
        debug=True)

    print(f"Minimum cost: {min_cost} found in {second} seconds:\n{path}")
