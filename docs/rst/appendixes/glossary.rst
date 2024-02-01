
.. _glossary:

########
Glossary
########

.. glossary::

    Terrain
        2D matrix of integers representing the height of a map at each cell.

    Coordinate
        A tuple of two integers ``(x,y)`` representing a cell in the terrain.

    Path
        A list of coordinates in the terrain.
        To be correct, it must start in the origin, end in the destination, and each step must be adjacent to the previous one.

    Cost
        An integer number related with a path.
        It represents a measure of the cost of the path in steps and climbs.

    Path Finding Algorithm
        A function that receives a terrain and returns a valid path.
