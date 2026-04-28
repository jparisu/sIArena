
.. _elements_terrain:

#######
Terrain
#######

.. code-block:: python

    from sIArena.terrain.Terrain import Terrain


The main element is the :term:`Terrain`.
This element represent a *map* or *grid* where the search algorithm will be performed.

It is a matrix of size ``NxM`` where each cell or tile contains an ``integer`` value.
Each value represents the *height* of the terrain at that point.
The difference of value between adjacent cells is used to determine the cost of moving from one cell to another.

The terrain has within it cells 2 special cells: the *origin* and the *destination*.
These cells are used to determine the start and end of the path to be found.
It also counts with a *cost_function* that is used to determine the cost of moving from one cell to another depending on their values.

Attributes
**********

- ``n``: number of rows
- ``m``: number of columns
- ``matrix``: ``numpy`` matrix of size ``NxM``
- ``origin``: ``tuple(int,int)`` with the coordinates of the origin cell
- ``destination``: ``tuple(int,int)`` with the coordinates of the destination cell
- ``cost_function``: function that receives 2 integers ``x,y`` and returns the cost of moving from one cell with value ``x`` to another with value ``y``

Built-in Methods
****************

- ``str``: returns a string representation of the matrix of the terrain.
  The origin and destination cells are marked with the characters ``+`` and ``x`` respectively.

- ``getitem [Coordinate]``: returns the value of the cell at the given coordinates.
  *i.e.* ``terrain[(0,0)]``.

- ``ctor``: constructor that receives a matrix.

  - ``matrix``: ``numpy`` matrix of size ``NxM``

  - ``origin``: ``Coordinate`` with the coordinates of the origin cell.
    If ``None`` is provided, the origin will be set to ``(0,0)``

  - ``destination``: ``Coordinate`` with the coordinates of the destination cell.
    If ``None`` is provided, the destination will be set to ``(n-1,m-1)``

  - ``cost_function``: function that receives 2 integers ``x,y`` and returns the cost of moving from one cell with value ``x`` to another with value ``y``.
    In case is not provided, the :ref:`elements_terrain_default_cost_function` will be used.


Methods
*******

- ``size``: returns a tuple with ``(n,m)``.
- ``get_neighbors``: returns a list of the coordinates of the cells that are adjacent to the given cell.
  - ``pos``: ``Coordinate``
- ``get_cost``: returns the cost of moving from one cell to another.
  - ``pos1``: ``Coordinate``
  - ``pos2``: ``Coordinate``
- ``get_path_cost``: returns the cost of a whole Path.
  - ``path``: ``Path``
- ``is_complete_path``: returns ``True`` if the given Path is valid and complete.
  - ``path``: ``Path``
- ``why_complete_path``: returns the same value as ``is_complete_path`` and also retrieves a string with information why the path is not complete (if this is the case).
  - ``path``: ``Path``

*Some of this methods use the element* :ref:`elements_path` *that is seeing afterwards.*


.. _elements_terrain_cost_function:

Cost Function
*************

The cost function is a function that receives 2 integers ``x,y``
referring to the *height* of 2 adjacent cells,
and returns the cost of moving from one cell with value ``x`` to another with value ``y``.

.. _elements_terrain_default_cost_function:

Default cost function
=====================

The default cost function is as follows:

- If the origin cell and the target cell are at same height (``x==y``), the cost is ``1``.
- If the origin cell is higher than the target cell (``x>y``), it means it moves down,
  and the cost is their difference: ``x-y``.
- If the origin cell is lower than the target cell (``x<y``), it means it moves up,
  and the cost is double their difference: ``2*(y-x)``.

The following snippet shows the implementation of the default cost function:

.. code-block:: python

    def default_cost_function(x,y):
        if x == y: return 1
        elif x > y: return x-y
        else: return 2*(y-x)


Visualization
*************

There are several ways to easily visualize the terrain:


String
======

Function ``str`` returns a string representation of the matrix of the terrain:
The origin and destination cells are marked with the characters ``+`` and ``x`` respectively.

.. code-block:: python

    print(terrain)

.. code-block:: text

  +---+---+---+---+---+
  |+3 | 9 | 3 | 9 | 3 |
  +---+---+---+---+---+
  | 9 | 2 | 0 | 3 | 0 |
  +---+---+---+---+---+
  | 3 | 9 | 3 | 3 | 3 |
  +---+---+---+---+---+
  | 0 | 6 | 3 | 0 | 6 |
  +---+---+---+---+---+
  | 3 | 9 | 3 | 3 |x3 |
  +---+---+---+---+---+


2D plot
=======

.. image:: /resources/images/2dplot_5_5.png

In order to learn how to visualize a 2D plot of the terrain, please refer to the :ref:`plotting_2d` section.


3D plot
=======

.. image:: /resources/images/3dplot_5_5.png

In order to learn how to visualize a 3D plot of the terrain, please refer to the :ref:`plotting_3d` section.


Multiple Destinations Terrain
*****************************

There is other class for Terrain that is called ``MultipleDestinationTerrain``.
This class allows to have multiple destinations in the terrain.
This means that the path must pass through all of them in order to be considered complete.
The destinations are not sorted, so they can be visited in any order.

.. code-block:: python

    from sIArena.terrain.Terrain import MultipleDestinationTerrain


The use and methods of this class are similar to ``Terrain`` ones.
It changes:

- The argument ``destination`` in the constructor is now a set of ``Coordinate``.
- The method ``is_complete_path`` now checks if the path passes through all the destinations.
- To get the destinations, use the attribute ``destinations``, that is a set of ``Coordinate``.

Example on how to create a ``MultipleDestinationTerrain``:

.. code-block:: python

    from sIArena.terrain.Terrain import MultipleDestinationTerrain
    from sIArena.terrain.Coordinate import Coordinate

    matrix = np.array(...)
    destinations = {Coordinate(4,4), Coordinate(0,4)}
    # It uses the top-left cell as origin by default
    terrain = MultipleDestinationTerrain(matrix, destination=destinations)

    # To get the destinations of the terrain
    destinations = terrain.destinations


Multi Endpoint Terrain
**********************

There is another Terrain class called ``MultiEndpointTerrain``.
This class is used when the problem has several possible starting points and several possible ending points.
Paths valid are those that start in any of the allowed origins and end in any of the allowed destinations, as long as they are valid paths in the terrain.

.. code-block:: python

    from sIArena.terrain.Terrain import MultiEndpointTerrain

Difference with Terrain
=======================

The complete-path rule for ``MultiEndpointTerrain`` is:

- The path must be valid: every consecutive pair of coordinates must be neighbors in the terrain.
- The first coordinate of the path must belong to the set of allowed origins.
- The last coordinate of the path must belong to the set of allowed destinations.
- The path may pass through other origins or destinations in the middle, but this is not required.
- The path does not need to visit all destinations.

This ``MultiEndpointTerrain`` class is similar to ``Terrain`` with some minor differences:

- Method `get_origins()` returns the set of allowed origins, instead of a single origin.
- Method `get_destinations()` returns the set of allowed destinations, instead of a single destination.
- There is no attribute ``origin`` or ``destination``.

The constructor keeps the same parameter names as the standard ``Terrain`` constructor:

- ``origin``: a single ``Coordinate`` or a collection of ``Coordinate`` values.
- ``destination``: a single ``Coordinate`` or a collection of ``Coordinate`` values.

Examples
========

Example with several origins and several destinations:

.. code-block:: python

    from sIArena.terrain.Terrain import MultiEndpointTerrain

    matrix = [
        [0, 0, 0, 0],
        [0, 5, 5, 0],
        [0, 0, 0, 0],
    ]

    terrain = MultiEndpointTerrain(
        matrix,
        origin={(0, 0), (2, 0)},
        destination={(0, 3), (2, 3)},
    )

    path = [(2, 0), (2, 1), (2, 2), (2, 3)]

    terrain.is_complete_path(path)      # True
    terrain.get_origins()               # {(0, 0), (2, 0)}
    terrain.get_destinations()          # {(0, 3), (2, 3)}


The following path is also complete in the same terrain, because it starts in another valid origin and ends in another valid destination:

.. code-block:: python

    other_path = [(0, 0), (0, 1), (0, 2), (0, 3)]

    terrain.is_complete_path(other_path)  # True


However, this path is not complete, even if it is a valid sequence of neighboring cells, because it does not start in one of the allowed origins:

.. code-block:: python

    wrong_start = [(1, 0), (2, 0), (2, 1), (2, 2), (2, 3)]

    terrain.is_valid_path(wrong_start)     # True
    terrain.is_complete_path(wrong_start)  # False


And this path is not complete because it does not end in one of the allowed destinations:

.. code-block:: python

    wrong_end = [(2, 0), (2, 1), (2, 2)]

    terrain.is_valid_path(wrong_end)       # True
    terrain.is_complete_path(wrong_end)    # False



Sequential Destinations Terrain
*******************************

There is other class for Terrain that is called ``SequentialDestinationTerrain``.
This class have multiple destinations, but in this case the path must pass through them in the same order as they are provided.

.. code-block:: python

    from sIArena.terrain.Terrain import SequentialDestinationTerrain


The use and methods of this class are similar to ``Terrain`` ones.
It changes:

- The argument ``destination`` in the constructor is now a list of ``Coordinate``.
- The method ``is_complete_path`` now checks if the path passes through all the destinations in the same order as they are provided.
- To get the destinations, use the attribute ``destinations``, that is a list of ``Coordinate``.

Example on how to create a ``SequentialDestinationTerrain``:

.. code-block:: python

    from sIArena.terrain.Terrain import SequentialDestinationTerrain
    from sIArena.terrain.Coordinate import Coordinate

    matrix = np.array(...)
    destinations = [Coordinate(4,4), Coordinate(0,4)]
    # It uses the top-left cell as origin by default
    terrain = SequentialDestinationTerrain(matrix, destination=destinations)

    # To get the destinations of the terrain
    destinations = terrain.destinations
