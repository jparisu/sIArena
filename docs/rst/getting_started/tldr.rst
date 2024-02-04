.. _tldr:

#####
TL;DR
#####

Too hard to read? Here is a quick summary of the project.

.. contents::
    :local:
    :backlinks: none
    :depth: 2

================
Project Overview
================

This project helps you to generate 2D terrains, that are matrix of integers, with a point of origin and a point of destination.
The main goal is to develop an algorithm that is able to find the best path from the origin to the destination.

Check :ref:`elements` for more details.


============
Installation
============

Just use the following command in your notebook:

.. code-block:: py

    !pip install git+https://github.com/jparisu/sIArena.git

Check the :ref:`installation guide <installation>` for more details.


=========================
How to generate a terrain
=========================

Use the following code changing some parameters:

.. code-block:: py

    from sIArena.terrain.generator.Generator import TerrainGenerator
    from sIArena.terrain.generator.FocusedGenerator import FocusedGenerator
    from sIArena.terrain.generator.PernilGenerator import PernilGenerator

    terrain = PernilGenerator().generate_random_terrain(
        n=20,
        m=20,
        min_height=0,
        max_height=10,
        min_step=1,
        abruptness=0.1,
        seed=0,
        origin=(0,0),
        destination=(19,19))

Check :ref:`generation` for more details.


=====================================
How to write a path finding algorithm
=====================================

Easy, create an algorithm that is able to retrieve a list of sequently :ref:`elements_coordinate`
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

Check :ref:`measure` for more details.
