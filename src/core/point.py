from dataclasses import dataclass
from core.rectangle import Rectangle


@dataclass(eq=True)
class Point(Rectangle):
    """
    Represents a point in 2D space, inheriting from Rectangle, but only using its (x, y)
    coordinates.
    """

    def post_init__(self):
        """
        Initializes the point with width and height set to 0.
        """
        self.width = 0
        self.height = 0

    def __iter__(self):
        yield self.x
        yield self.y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return self.__str__()

    def check_valid_distance(self, other: "Point", distance: tuple[int, int]) -> bool:
        """
        Checks if the distance to another point is valid in both axes.

        Args:
            other (Point): The other point to compare.
            distance (tuple(int, int)): Minimum required distance (dx, dy).

        Returns:
            bool: True if the distance is valid, False otherwise.
        """
        return (
            abs(self.x - other.x) >= distance[0]
            and abs(self.y - other.y) >= distance[1]
        )
