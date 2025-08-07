from dataclasses import dataclass
from core.rectangle import Rectangle
from core.placement import Placement
from algorithm_base import AlgorithmBase

@dataclass
class GuillotineDivide(AlgorithmBase):
    """
    Orders that result in a valid placement are externally found using the superclass'
    test_orders() method, and check_by_dividing() is used to check if it is
    guillotinable by attempting to recursively divide the set of objects into each
    individual one.

    Attributes:
        find_all_orders (bool): Whether to find all valid orders or stop at the first.
    """

    find_all_orders: bool = False

    def divide(self, objects: list[Rectangle], x=False) -> list[list[Rectangle]]:
        """
        Divides a list of rectangles into groups that can be separated by a single
        guillotine cut along the x or y axis.

        Args:
            objects (list[Rectangle]): The list of rectangles to divide.
            x (bool): Determines the axis along which to cut (x or y).

        Returns:
            divisions (list[list[Rectangle]]): A list of groups of rectangles after 
            division.
        """
        # Sort by relevant coordinate
        intervals: list[tuple[int, int]] = sorted(
            [(o.x, o.x + o.width) if x else (o.y, o.y + o.height) for o in objects],
            key=lambda interval: interval[0],
        )

        divisions: list[list[Rectangle]] = []
        division: list[Rectangle] = [objects[0]]
        current_max = intervals[0][1]

        # Form division groups
        for i in range(1, len(objects)):
            if intervals[i][0] < current_max:
                division.append(objects[i])
                current_max = max(current_max, intervals[i][1])
            else:
                divisions.append(division)
                division = [objects[i]]
                current_max = intervals[i][1]

        if division != []:
            divisions.append(division)

        return divisions

    def check_by_dividing(self, division: list[Rectangle]) -> bool:
        """
        Recursively checks if a group of rectangles can be separated by guillotine cuts.

        Args:
            division (list[Rectangle]): The group of rectangles to check.

        Returns:
            bool: True if the group is guillotinable, False otherwise.
        """
        if len(division) < 5:
            return True

        if (new_divisions := self.divide(division, x=True))[0] == division:
            if (new_divisions := self.divide(division, x=False))[0] == division:
                return False

        for division in new_divisions:
            if not self.check_by_dividing(division):
                return False

        return True

    def keep_recurring_condition(self, set_height: int) -> bool:
        """
        Determines whether to continue the recursive search for placements.

        Args:
            set_height (int): The current height of the placed set.

        Returns:
            bool: True if recursion should continue, False otherwise.
        """
        return (
            (set_height <= self.boundary.y) 
            and (len(self.solutions) == 0 or self.find_all_orders)
        )

    def handle_solution(self, solution: Placement) -> None:
        """
        Handles a found placement solution by checking if it is guillotinable
        and storing it if so.

        Args:
            solution (Placement): The placement solution to handle.
        """
        order = solution.placed
        print(f"{order}... ", end="")

        if self.check_by_dividing(order):
            print("is guillotinable!")
            self.solutions.append(order)
        else:
            print("is not guillotinable...")

    def announce(self) -> None:
        print(
            f"Attempting to find a guillotinable placement for objects {self.objects} "
            f"on a board of dimensions {self.boundary.x}x{self.boundary.y}...\n"
        )

    def get_solutions(self) -> None:
        self.test_orders(self.objects, Placement(boundary=self.boundary))

    def store_solutions(self) -> None:
        if len(self.solutions) > 0:
            print(f"Guillotinable BL order found: {self.solutions[0]} ")
            path = f"..\\output\\guillotine_check_divide.txt"
            with open(path, "w") as order_file:
                order_file.writelines(f"{self.boundary.x} {self.boundary.y}\n")
                for object in self.solutions[0]:
                    order_file.writelines(f"{object.width} {object.height} ")
        else:
            print(f"No guillotinable BL order found!")


if __name__ == "__main__":
    GuillotineDivide(allow_rotations=True).run()
