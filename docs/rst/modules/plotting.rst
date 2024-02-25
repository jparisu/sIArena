
.. _plotting:

############
Plot Terrain
############

.. contents::
    :local:
    :backlinks: none
    :depth: 2

Certain functions allow to plot a :ref:`elements_terrain` to visualize the heights easily.


.. _plotting_2d:

2D Plot
=======

.. code-block:: python

    from sIArena.terrain.plot.plot_2D import plot_terrain_2D

Visualizing a Terrain in 2D is very useful to understand the heights of the terrain.
Use the function :func:`plot_terrain_2D` to plot the terrain in 2D.
It is possible also to plot one or multiple paths on the terrain.

Parameters
----------

- ``terrain: Terrain``: The terrain to plot
- ``path: Path = None``: The path to plot
- ``paths: List[Path] = []``: The paths to plot (if ``path`` is not used)
- ``paths_legends: List[str] = None``: The legend message for each path
- ``add_cost_to_legend: bool = False``: If True, the cost of the path will be added as legend
- ``colors: List[str] = ['r', 'y', 'm', 'k', 'c', 'g', 'b']``: The colors to use for each paths
- ``cmap: str = 'terrain'``: The ``colormap`` to use for the terrain
- ``title: str = 'Terrain'``: The title of the plot

Example
-------

.. code-block:: python

    from sIArena.terrain.Terrain import Coordinate, Terrain, Path
    from sIArena.terrain.plot.plot_2D import plot_terrain_2D

    matrix = [[6, 5, 4, 1],
            [5, 4, 2, 0],
            [4, 1, 0, 0]]
    terrain = Terrain(matrix, destination=(2, 2))
    path = [(0,0), (0,1), (0,2), (0,3), (1,3), (1,2), (2,2)]

    plot_terrain_2D(
        terrain=terrain,
        paths=[path],
        paths_legends=['Path 1'],
        add_cost_to_legend=True)

.. image:: /resources/images/2dplot_3_4_path.png


.. _plotting_3d:

3D Plot
=======


.. code-block:: python

    from sIArena.terrain.plot.plot_3D import plot_terrain_3D

Visualizing a Terrain in 2D is very useful to understand the heights of the terrain.
Use the function :func:`plot_terrain_2D` to plot the terrain in 2D.
It is possible also to plot one or multiple paths on the terrain.

Parameters
----------

- ``terrain: Terrain``: The terrain to plot
- ``path: Path = None``: The path to plot
- ``paths: List[Path] = []``: The paths to plot (if ``path`` is not used)
- ``angles: List[tuple] = [(45, 45), (45, 225)]``: The angles from where to plot the terrain
- ``colors: List[str] = ['r', 'y', 'm', 'k', 'c', 'g', 'b']``: The colors to use for each paths
- ``cmap: str = 'terrain'``: The ``colormap`` to use for the terrain
- ``title: str = 'Terrain'``: The title of the plot

Example
-------

.. code-block:: python

    from sIArena.terrain.Terrain import Coordinate, Terrain, Path
    from sIArena.terrain.plot.plot_3D import plot_terrain_3D

    matrix = [[6, 5, 4, 1],
            [5, 4, 2, 0],
            [4, 1, 0, 0]]
    terrain = Terrain(matrix, destination=(2, 2))
    path = [(0,0), (0,1), (0,2), (0,3), (1,3), (1,2), (2,2)]

    plot_terrain_3D(
        terrain=terrain,
        angles=[(80, 10), (30, 190), (30, 10)],
        paths=[path])

.. image:: /resources/images/3dplot_3_4_path.png



Examples
========

When used in bigger terrains, the result is much more interesting.

.. image:: /resources/images/2dplot_10_10_solved.png

.. image:: /resources/images/3dplot_10_10_solved.png


.. warning::

    While in 2D the cell is represented by a color square,
    in 3D the cell is represented by a point in the map, and the squares are the connections between cells.
    So the colors and paths could be difficult to interpret in both at the same time.
