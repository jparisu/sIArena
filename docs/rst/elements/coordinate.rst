
.. _elements_coordinate:

==========
Coordinate
==========

.. code-block:: python

    from sIArena.terrain.Terrain import Coordinate

A :term:`Coordinate` is a point in space 2D grid or matrix.
It is defined by a Tuple of 2 integers, the first being the number of the row of a matrix and the second being the column.

.. code-block:: python

    Coordinate = Tuple[int,int]

This is used to represent the position of an element in a :ref:`elements_terrain` or each step of a :ref:`elements_path`.
