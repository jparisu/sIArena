import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List
import numpy as np

from sIArena.terrain.Terrain import Coordinate, Terrain, Path


def plot_terrain_3D(
            terrain: Terrain,
            angles: List[tuple] = [(45, 45), (45, 225)],
            paths: List[Path] = [],
            colors: List[str] = ['r', 'y', 'm', 'k', 'c', 'g', 'b'],
            cmap: str = 'terrain'):
    """Plots the terrain and the given paths"""

    fig = plt.figure(figsize=(18, 6))

    np_matrix = np.array(terrain.matrix)

    # Create subplots with different viewing angles
    for i, angle in enumerate(angles):
        ax = fig.add_subplot(1, len(angles), i+1, projection='3d')
        ax.view_init(*angle)
        ax.set_title(f'Angle {angle}')

        # Create a meshgrid for plotting
        x = np.arange(np_matrix.shape[0])
        y = np.arange(np_matrix.shape[1])
        X, Y = np.meshgrid(x, y)
        Z = np_matrix[X, Y]

        # Plot the surface
        ax.plot_surface(X, Y, Z, cmap=cmap)

        # Plot the origin point
        ax.plot([terrain.origin[0]], [terrain.origin[1]], [terrain[terrain.origin]], 'r+', markersize=5, zorder=6)

        # Plot the destination point
        ax.plot([terrain.destination[0]], [terrain.destination[1]], [terrain[terrain.destination]], 'rx', markersize=5, zorder=6)

        # Plot the paths
        for i, p in enumerate(paths):
            ax.plot(
                [pos[0] for pos in p],
                [pos[1] for pos in p],
                [terrain[pos] for pos in p],
                color=colors[i % len(colors)],
                linewidth=2, zorder=5)

        # Set limits one unit above and below the terrain
        ax.set_xlim(-1, np_matrix.shape[0] + 1)
        ax.set_ylim(-1, np_matrix.shape[1] + 1)
        ax.set_zlim(np_matrix.min() - 1, np_matrix.max() + 1)

        ax.set_xlabel('row')
        ax.set_ylabel('col')

    plt.show()
