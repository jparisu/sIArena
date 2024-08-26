import matplotlib.pyplot as plt
from typing import List

from sIArena.terrain.Terrain import Coordinate, Terrain, Path


def plot_terrain_2D(
            terrain: Terrain,
            path: Path = None,
            paths: List[Path] = [],
            paths_legends: List[str] = None,
            add_cost_to_legend: bool = False,
            colors: List[str] = ['r', 'y', 'm', 'k', 'c', 'g', 'b'],
            cmap: str = 'terrain',
            title: str = 'Terrain',
        ):
    """Plots the terrain and the given paths"""

    if path is not None:
        paths = [path]

    plt.clf()
    plt.imshow(terrain.matrix, cmap=cmap)

    # Mark with red the origin and destination
    plt.plot(terrain.origin[1], terrain.origin[0], 'r+')
    for dest in terrain.destinations:
        plt.plot(dest[1], dest[0], 'rx')

    # Set path legends if unset
    paths_legends_ = paths_legends
    if paths_legends_ is None:
        paths_legends_ = [""]
    while len(paths_legends_) < len(paths):
        paths_legends_.append("")

    # Plot the paths
    for i, p in enumerate(paths):
        if add_cost_to_legend:
            paths_legends_[i] = f'{paths_legends_[i]} ({terrain.get_path_cost(p)})'
        plt.plot(
            [pos[1] for pos in p],
            [pos[0] for pos in p],
            colors[i % len(colors)],
            label=paths_legends_[i],)

    plt.xlabel('col')
    plt.ylabel('row')
    plt.title(title)

    if paths_legends or add_cost_to_legend:
        plt.legend()

    plt.colorbar()
    plt.show(block=False)
    plt.pause(0.001)
