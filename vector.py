"""

Implemented for cuboid visual in main project.


"""


class Vector:
    def __init__(self, x, y):
        self.dir = (x, y)

    def __add__(self, other):
        return Vector(self.dir[0] + other.dir[0], self.dir[1] + other.dir[1])

    def toTuple(self):
        return self.dir
