
.. _elements_path:

====
Path
====

.. code-block:: python

    from sIArena.terrain.Terrain import Path

A :term:`Path` is a sequence of :ref:`elements_coordinate` that represents a route from one point to another in a :ref:`elements_terrain`.

In order to be **valid**, each step of the path (each pair of consecutive coordinates)
must be a movement of one step in one of the four cardinal directions (up, down, left, right).
Mathematically:

.. code-block:: python

    def are_consecutive(coor1: Coordinate, coor2: Coordinate) -> bool:
        return
            ( abs(coor1.x - coor2.x) == 1 and abs(coor1.y - coor2.y) == 0 ) or
            ( abs(coor1.x - coor2.x) == 0 and abs(coor1.y - coor2.y) == 1 )

In order to be **complete**, the path must be valid and:

- The first coordinate must be the ``origin`` point of the terrain.
- The last coordinate must be the ``destination`` point of the terrain.


In Python, the Path is represented as a list of coordinates:

.. code-block:: python

    Path = List[Coordinate]


A complete path is **better** as lower is the cost of it.
To calculate the cost of a path, it is used the :ref:`elements_terrain_cost_function`.
