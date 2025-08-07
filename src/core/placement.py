from dataclasses import dataclass, field
from copy import deepcopy
from core.rectangle import Rectangle
from core.point import Point


@dataclass
class Placement:
    """
    Handles the placement of rectangles on a board using bottom-left (BL) and
    bottom-left-fill (BLF) algorithms.

    Attributes:
        boundary (Point): Dimensions of the board (width, height).
        placed (list[Rectangle]): List of objects placed on the board.
        fill (bool): Placement algorithm to use (False for BL, True for BLF).
    """

    boundary: Point
    placed: list[Rectangle] = field(default_factory=list)
    fill: bool = False

    def check_overlaps(self, object: Rectangle) -> bool:
        """
        Checks if the given rectangle overlaps with any already placed rectangles.

        Args:
            object (Rectangle): The rectangle to check for overlaps.

        Returns:
            bool: True if the rectangle overlaps with any placed rectangle,
            False otherwise.
        """
        for other in self.placed:
            if object.overlap(other):
                return True
        return False

    def bottom_left(self, object: Rectangle) -> None:
        """
        Places a rectangle object using the BL algorithm.
        The object is moved downwards (decreasing y) until it cannot move further
        without overlapping other objects or exceeding the lower boundary. Then, it is
        moved leftwards (decreasing x) in the same manner. The process repeats until the
        object cannot be moved further in either direction, at which point it is placed.

        Args:
            object (Rectangle): The object to be placed using the BL algorithm.
        """
        while True:
            object.y -= 1
            if self.check_overlaps(object) or object.y < 0:
                object.y += 1
                object.x -= 1
                if self.check_overlaps(object) or object.x < 0:
                    object.x += 1
                    break

        self.placed.append(deepcopy(object))

    def bottom_left_fill(self, object: Rectangle) -> None:
        """
        Places a rectangle object on the board using the BLF algorithm.
        First, the object is placed using the standard BL approach. Then, the method
        attempts to improve the placement by scanning for a better position below the
        initially placed object, moving in a reverse bottom-left direction, and checking
        for overlaps.

        Args:
            object (Rectangle): The rectangle object to be placed on the board.
        """
        self.bottom_left(object)

        best = Rectangle(width=object.width, height=object.height)
        while (best.x, best.y) != (object.x, object.y):
            if not self.check_overlaps(best):
                object = deepcopy(best)
                break
            # Move to the next position in the reverse bottom-left direction
            if best.x + best.width == self.boundary.x:
                best.x = 0
                best.y += 1
            else:
                best.x += 1

    def check_full_placement(
        self,
        objects: list[Rectangle],
    ) -> bool:
        """
        Simulates the placement of all objects on the board.

        Args:
            objects (list[Rectangle]): List of objects to place.

        Returns:
            bool: True if all objects are placed successfully, False if any object is
            out of bounds.
        """

        for object in objects:
            # Apply the placement algorithm
            if not self.fill:
                self.bottom_left(object)
            else:
                self.bottom_left_fill(object)

            # Ends the placement if the object is out of bounds
            if object.y + object.height > self.boundary.y:
                return False

        # Return a successful BL placement
        return True

    def place_object(
        self,
        object: Rectangle,
        set_height: int,
    ) -> int:
        """
        Simulates the placement of a single object on the board.

        Args:
            object (Rectangle): The rectangle to place.
            set_height (int): The height of the current set of placed objects.

        Returns:
            int: The updated set height after placement.
        """

        # Update the object's initial position
        object.x = self.boundary.x - object.width
        object.y = set_height

        # Apply the placement algorithm
        if not self.fill:
            self.bottom_left(object)
        else:
            self.bottom_left_fill(object)

        # Update the set height
        set_height = max(set_height, object.y + object.height)

        return set_height

    def get_bl_order(
        self,
        solution: list[Rectangle],
    ) -> list[Rectangle]:
        """
        Determines the BL placement order of the objects in a given solution for the
        bin-packing problem.

        Args:
            solution (list[Rectangle]): The current placement solution.

        Returns:
            list[Rectangle]: A reordered list of objects which results in the input
            solution if the BL algorithm is applied to it.
        """

        objects = deepcopy(solution)
        bl_order: list[Rectangle] = []

        # Find the bottom-left order of the objects in the solution
        for _ in range(len(objects)):
            current_object: Rectangle = objects[0]
            max_y = 0

            # Find the object with the max y coordinate at x = 0
            for object in objects:
                if object.x == 0 and object.y >= max_y:
                    max_y = object.y
                    current_object = object

            # Find objects that are directly to the right of the current object and
            # higher - meaning they need to be placed first; When there are no more
            # objects that fulfill this condition, add the updated current object
            # to the bottom-left order and remove it from the solution
            while True:
                new_object_found = False
                for object in objects:
                    if (
                        object.x == current_object.x + current_object.width
                        and object.y >= current_object.y
                    ):
                        max_y = object.y
                        current_object = object
                        new_object_found = True

                if new_object_found:
                    continue

                current_object.x = self.boundary.x - current_object.width
                current_object.y = self.boundary.y
                bl_order.append(current_object)
                objects.remove(current_object)
                break

        # Reverse the order to get the bottom-left placement order
        bl_order.reverse()
        print(f"BL order: {bl_order}\n")
        return bl_order
