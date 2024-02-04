
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

# Get the terrain size
n, m = terrain.size()

# Get origin and destination coordinates
origin = terrain.origin
destination = terrain.destination

# Check the possible neighbors of the origin (thus, the possible next step of the path)
neigs = terrain.get_neighbors(origin)

# Check the cost from the origin to each neighbor
costs = [terrain.get_cost(origin, neig) for neig in neigs]


#####################################################################

from sIArena.terrain.Terrain import Coordinate, Terrain, Path

def find_path(terrain: Terrain) -> Path:

    # Create a path that starts in origin
    path = [origin]

    # Go to the buttom of the map (assuming destination is in [N-1,M-1])
    for i in range(n-1):
        path.append((path[-1][0] + 1, path[-1][1]))

    # Go to the right of the map (assuming destination is in [N-1,M-1])
    for i in range(m-1):
        path.append((path[-1][0], path[-1][1] + 1))

    # Return the path
    return path


#####################################################################

# Get the path solution
path = find_path(terrain)

# Check if a path is complete (it must be with our implementation)
is_complete = terrain.is_complete_path(path)

# Calculate the cost of a path
cost = terrain.get_path_cost(path)

print(f"The path {path} with cost {cost} {'is' if is_complete else 'is not'} complete.")

#####################################################################

from sIArena.terrain.plot.plot_2D import plot_terrain_2D
from sIArena.terrain.plot.plot_3D import plot_terrain_3D

plot_terrain_2D(terrain, paths=[path])
plot_terrain_3D(terrain, paths=[path], angles=[(80, 10), (30, 190), (30, 10)])


#####################################################################

from sIArena.measurements.measurements import measure_function

min_cost, second, min_path = measure_function(
    find_path,
    terrain,
    iterations=5,
    debug=True)

print(f"Minimum cost: {min_cost} found in {second} seconds:\n{path}")
