.. _tutorial:

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
:ref:`visualization tools <plotting>` to display terrains and paths in a graphical interface,
and :ref:`measure tools <measure>` to measure algorithm performance.


.. _tutorial_installation:

Installation
============

**sIArena** is a *Python* project,
check the :ref:`following section <installation>` to install the project and its dependencies.

The advised way to install **sIArena** is using a *Python Jupyter Notebook* in *Google Colab*,
or using a package manager like *pip* or *Anaconda* in a local environment.


.. _tutorial_generation:

Generate a terrain
==================

In order create a path finding algorithm, first we need to create a terrain to test it.
The library provides a set of :ref:`tools <generation>` to generate pseudo-random terrains.

The following snippet generates the terrain displayed below.

.. literalinclude:: /resources/scripts/tutorial.py
    :language: python
    :lines: 4-19

We can see printed the terrain matrix.
The origin cell is represented by a ``+``, and the destination cell by a ``x``.

.. _tutorial_plotting:

Plot the terrain
================

The terrains could be graphically displayed using the :ref:`plotting tools <plotting>`.
These tools allow to display the terrain as a height map in 2D or 3D.

The following snippet plots the terrain generated in the previous section:

.. literalinclude:: /resources/scripts/tutorial.py
    :language: python
    :lines: 24-28


.. image:: /resources/images/2dplot_big.png

.. image:: /resources/images/3dplot_big.png


.. _tutorial_path_finding:

Path finding algorithm
======================

The main goal of the library is to allow to create and test different path finding algorithms.
These algorithms are expected to find the lowest cost possible path from the origin to the destination of a terrain.
To generate such kind of algorithms, just create a function which only parameter is a terrain, and that returns a path.

A path is a list of sequently :ref:`Coordinates <elements_coordinate>` from the origin to the destination of a specific terrain.
In order for a path to be valid, each coordinate must be adjacent to the next one,
this means, to be at a distance of 1 in the x or y axis, but not in both at the same time.

The following snippet shows different methods from terrain that could be useful to build the path finding algorithm:

.. literalinclude:: /resources/scripts/tutorial.py
    :language: python
    :lines: 33-44


In order for a path to be complete, the first coordinate must be the origin and the last one the destination.
The following snippet shows different a path finding algorithm that goes down to the end of the map, and then right.
Be aware that not all the terrains start and end in the corners, but their origin and destination may vary.

.. literalinclude:: /resources/scripts/tutorial.py
    :language: python
    :lines: 49-65


And in the following some methods to check the path and its cost:

.. literalinclude:: /resources/scripts/tutorial.py
    :language: python
    :lines: 70-79


Plot the path
=============

The library also support to show a path in the terrain, as shown in the following snippet:

.. literalinclude:: /resources/scripts/tutorial.py
    :language: python
    :lines: 84-88


.. image:: /resources/images/2dplot_big_solved_down.png

.. image:: /resources/images/3dplot_big_solved_down.png


.. _tutorial_measurement:

Measurement
===========

The library also provides a way to :ref:`measure <measure>` the performance of the path finding algorithms.
This is done by measuring the mean time and the minimum cost of the path found by the algorithm over a terrain.

The following snippet shows how to measure the performance of the algorithm implemented before:

.. literalinclude:: /resources/scripts/tutorial.py
    :language: python
    :lines: 93-101

The previous algorithm finds in fractions of milliseconds a path with cost ``559``.

Conclusion
==========

Creating a terrain, and the testing a path finding algorithm is a simple and easy task using **sIArena**.
Knowing the time needed to find a path, and the cost of it,
different algorithms could be compared to determine which one is the best for a specific terrain.

For instance, in the map generated before,
the lowest cost path should look like the following, with cost ``121``:

.. image:: /resources/images/3dplot_big_solved.png
