
.. _example:

=======
Example
=======

The following snippet shows the different features of the elements:

.. code-block:: python

    from sIArena.terrain.Terrain import Coordinate, Path, Terrain

    # TERRAIN
    ##########

    # Create a matrix with heights of the terrain
    matrix = [[6, 5, 4, 1],
              [5, 4, 2, 0],
              [4, 1, 0, 0]]

    # Create a terrain with the matrix with different destination that default
    terrain = Terrain(matrix, destination=(2, 2))

    # Get size
    terrain.n  # Output: 3
    terrain.m  # Output: 4

    # Get origin and destination
    terrain.origin  # Output: (0, 0)
    terrain.destination  # Output: (2, 2)

    # Get the height of the terrain in a coordinate
    terrain[(0, 0)]  # Output: 6
    terrain[(2, 1)]  # Output: 1

    str(terrain)  # Output:
    # +---+---+---+---+
    # |*6 | 5 | 4 | 1 |
    # +---+---+---+---+
    # | 5 | 4 | 2 | 0 |
    # +---+---+---+---+
    # | 4 | 1 |x0 | 0 |
    # +---+---+---+---+

    # BUILDING PATH
    ################

    # Get the cost of a step from a coordinate to another
    terrain.get_cost((0, 0), (0, 1))  # Output: 1
    terrain.get_cost((0, 1), (0, 0))  # Output: 2

    # Get the neighbors of a coordinate
    terrain.get_neighbors((0, 0))  # Output: [(0, 1), (1, 0)]
    terrain.get_neighbors((1, 1))  # Output: [(0, 1), (1, 0), (1, 2), (2, 1)]


    # PATH
    #######

    # Create a path with the terrain that goes from origin to destination
    path = [(0,0), (0,1), (0,2), (0,3), (1,3), (1,2), (2,2)]

    # Check the path is complete
    terrain.is_valid_path(path, terrain)  # Output: True

    # Check the path cost
    terrain.get_path_cost(path, terrain)  # Output: 12
