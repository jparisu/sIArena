import matplotlib.pyplot as plt
from typing import List

from sIArena.terrain.Terrain import Coordinate, Terrain, Path


def plot_terrain_2D(
            terrain: Terrain,
            paths: List[Path] = [],
            colors: List[str] = ['r', 'y', 'm', 'k', 'c', 'g', 'b'],
            cmap: str = 'terrain'):
    """Plots the terrain and the given paths"""

    plt.clf()
    plt.imshow(terrain.matrix, cmap=cmap)

    # Mark with red the origin and destination
    plt.plot(terrain.origin[1], terrain.origin[0], 'r+')
    plt.plot(terrain.destination[1], terrain.destination[0], 'rx')

    # Plot the paths
    for i, p in enumerate(paths):
        plt.plot(
            [pos[1] for pos in p],
            [pos[0] for pos in p],
            colors[i % len(colors)])

    plt.xlabel('row')
    plt.ylabel('col')

    plt.colorbar()
    plt.show(block=False)
    plt.pause(0.001)
