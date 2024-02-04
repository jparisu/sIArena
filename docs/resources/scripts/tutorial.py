
#####################################################################

from sIArena.terrain.Terrain import Coordinate, Terrain, Path
from sIArena.terrain.generator.PernilGenerator import PernilGenerator

terrain = PernilGenerator().generate_random_terrain(
    n=25,
    m=25,
    min_height=0,
    max_height=100,
    min_step=25,
    abruptness=0.1,
    seed=60,
    origin=None,
    destination=None)

# To print the terrain in ascii format
print(terrain)


#####################################################################

from sIArena.terrain.plot.plot_2D import plot_terrain_2D
from sIArena.terrain.plot.plot_3D import plot_terrain_3D

plot_terrain_2D(terrain)
plot_terrain_3D(terrain, angles=[(80, 10), (30, 190), (30, 10)])


#####################################################################

from sIArena.terrain.plot.plot_2D import plot_terrain_2D
from sIArena.terrain.plot.plot_3D import plot_terrain_3D

path = [terrain.origin, terrain.destination]

plot_terrain_2D(terrain, paths=[path])
plot_terrain_3D(terrain, paths=[path], angles=[(80, 10), (30, 190), (30, 10)])


#####################################################################

import random # import and seed random module
random.seed(0)

from sIArena.terrain.Terrain import Coordinate, Terrain, Path

def find_path(terrain: Terrain) -> Path:
    # Get the terrain size
    n, m = terrain.size()

    # Get origin and destination coordinates
    origin = terrain.origin
    destination = terrain.destination

    # Create a path that starts in origin
    path = [origin]

    # Check the possible neighbors of the origin (thus, the possible next step of the path)
    neigs = terrain.get_neighbors(path[-1])

    # Check the cost from the origin to each neighbor
    costs = [terrain.get_cost(path[-1], neig) for neig in neigs]

    # Using these functions, we can create a random path that starts in the origin and ends in the destination
    while path[-1] != destination:
        next_step = random.choice(terrain.get_neighbors(path[-1]))
        path.append(next_step)

    # Return the path
    return path


# Get the path solution
path = find_path(terrain)

# Check if a path is complete (it must be with our implementation)
terrain.is_complete_path(path)

# Calculate the cost of a path
terrain.get_path_cost(path)


#####################################################################

from sIArena.measurements.measurements import measure_function

min_cost, second, path = measure_function(
    find_path,
    terrain,
    iterations=5,
    debug=True)

print(f"Minimum cost: {min_cost} found in {second} seconds:\n{path}")
