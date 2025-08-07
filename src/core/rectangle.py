from dataclasses import dataclass, field

@dataclass
class Rectangle:
    """
    Represents a rectangle with position, dimensions, and optional contained rectangles.

    Attributes:
        width (int): The width of the rectangle.
        height (int): The height of the rectangle.
        x (int): The x-coordinate of the rectangle's bottom-left corner.
        y (int): The y-coordinate of the rectangle's bottom-left corner.
        contains (list[Rectangle]): List of rectangles contained within this rectangle.
    """

    width: int = 0
    height: int = 0
    x: int = 0
    y: int = 0
    contains: list["Rectangle"] = field(default_factory=list)

    def __str__(self):
        return f"[[{self.width}x{self.height}] @ ({self.x},{self.y})]"

    def __repr__(self):
        return self.__str__()

    def overlap(self, other: "Rectangle") -> bool:
        """
        Checks if this rectangle overlaps with another rectangle.

        Args:
            other (Rectangle): The other rectangle to check overlap with.

        Returns:
            bool: True if rectangles overlap, False otherwise.
        """
        return not (
            self.x >= other.x + other.width
            or self.x + self.width <= other.x
            or self.y >= other.y + other.height
            or self.y + self.height <= other.y
        )

    def rotate(self, axis=(0, 0), clockwise=False) -> None:
        """
        Rotates the rectangle 90 degrees around a given axis.

        Args:
            axis (tuple[int, int], optional): The (x, y) axis to rotate around.
            clockwise (bool, optional): Determines the orientation of rotation.
        """
        self.width, self.height = self.height, self.width

        if clockwise:
            new_x = axis[0] + (self.y - axis[1])
            new_y = axis[1] - (self.x - axis[0]) - self.height
        else:
            new_x = axis[0] - (self.y - axis[1]) - self.width
            new_y = axis[1] + (self.x - axis[0])
        self.x, self.y = new_x, new_y

        for o in self.contains:
            if o != self:
                o.rotate(axis, clockwise)

    def mirror(self, axis=(0, 0), x_mirror=True) -> None:
        """
        Mirrors the rectangle across a given axis, either horizontally or vertically.

        Args:
            axis (tuple[int, int], optional): The (x, y) axis to mirror across.
            x_mirror (bool, optional): Determines the direction of mirroring.
        """
        if x_mirror:
            self.x = axis[0] * 2 - self.x - self.width
        else:
            self.y = axis[1] * 2 - self.y - self.height

        for o in self.contains:
            if o != self:
                o.mirror(axis, x_mirror)

    def flip(self, axis=(0, 0), clockwise=False) -> None:
        """
        Rotates and then mirrors the rectangle across a given axis.

        Args:
            axis (tuple[int, int], optional): The (x, y) axis to operate on.
            clockwise (bool, optional): Determines the orientation of rotation.
        """
        old_y = self.y
        self.rotate(axis, clockwise)
        self.mirror(
            axis=axis,
            x_mirror=(old_y >= axis[1] and self.y >= axis[1]),
        )

    def shift(self, amount: int, x_shift=True) -> None:
        """
        Shifts the rectangle by a specified amount in the x or y direction.

        Args:
            amount (int): The amount to shift.
            x_shift (bool, optional): Determines the direction of shifting.
        """
        if x_shift:
            self.x += amount
        else:
            self.y += amount

        for o in self.contains:
            if o != self:
                o.shift(amount, x_shift)

    def merge(self, other: "Rectangle", x_merge=True) -> "Rectangle":
        """
        Merges this rectangle with another by placing them adjacent along x or y axis.

        Args:
            other (Rectangle): The other rectangle to merge with.
            x_merge (bool, optional): Determines the direction of merging.

        Returns:
            Rectangle: A new object containing both rectangles.
        """
        other.shift(
            amount=self.width if x_merge else self.height,
            x_shift=x_merge,
        )

        return Rectangle(
            width=self.width + (other.width if x_merge else 0),
            height=self.height + (0 if x_merge else other.height),
            x=self.x,
            y=self.y,
            contains=self.contains + other.contains,
        )

    def can_be_split(
        self,
        board_width: int,
        board_height: int,
        min_ratio: float,
        points: int,
    ) -> bool:
        """
        Determines if the rectangle can be split into smaller rectangles of valid size.

        Args:
            board_width (int): The width of the board.
            board_height (int): The height of the board.
            min_ratio (float): Minimum ratio for the split rectangles.
            points (int): Number of points to split.

        Returns:
            bool: True if the rectangle can be split, False otherwise.
        """
        min_distances = [
            int(board_width * min_ratio),
            int(board_height * min_ratio),
        ]

        if points > 0:
            return self.width >= min_distances[0] * (
                points + 1
            ) and self.height >= min_distances[1] * (points + 1)

        else:
            return (
                self.width >= min_distances[0] * 2 and self.height >= min_distances[1]
            ) or (
                self.width >= min_distances[0] and self.height >= min_distances[1] * 2
            )

    def get_split_axes(
        self,
        board_width: int,
        board_height: int,
        min_ratio: float,
    ) -> dict[str, bool]:
        """
        Determines along which axes the rectangle can be split based on minimum size.

        Args:
            board_width (int): The width of the board.
            board_height (int): The height of the board.
            min_ratio (float): Minimum ratio for the split rectangles.

        Returns:
            axes (dict[str, bool]): Dictionary indicating if split is possible along each axis.
        """
        min_distances = [
            int(board_width * min_ratio),
            int(board_height * min_ratio),
        ]

        return {
            "x": self.width >= min_distances[0] * 2,
            "y": self.height >= min_distances[1] * 2,
        }
