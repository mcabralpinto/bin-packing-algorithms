from dataclasses import dataclass
from core.placement import Placement
from algorithm_base import AlgorithmBase


@dataclass
class PlacementChecker(AlgorithmBase):
    """
    Checks for valid placement orders of objects on a board using the BL algorithm.

    Attributes:
        find_all_orders (bool): Whether to find one, or all valid placement orders.
    """
    find_all_orders: bool = False

    def keep_recurring_condition(self, set_height: int) -> bool:
        """
        Determines whether the recursive search for placement orders should continue,
        based on the comparison of the current height of the placed set of objects and
        the board's vertical boundary.

        Args:
            set_height (int): The current height of the placed set of objects.

        Returns:
            bool: True if the search should continue, False otherwise.
        """
        return (
            (set_height <= self.boundary.y) 
            and (len(self.solutions) == 0 or self.find_all_orders)
        )

    def handle_solution(self, solution: Placement) -> None:
        """
        Handles a valid placement solution by storing it.

        Args:
            solution (Placement): The placement solution to handle.

        Returns:
            None
        """
        order = solution.placed
        print(f"Valid placement order found: {order}")
        self.solutions.append(order)

    def announce(self) -> None:
        print(
            f"Attempting to find a placement order for objects {self.objects} "
            f"on a board of dimensions {self.boundary.x}x{self.boundary.y}..."
        )

    def get_solutions(self) -> None:
        self.test_orders(self.objects, Placement(boundary=self.boundary))

    def store_solutions(self) -> None:
        if len(self.solutions) > 0:
            path = f"..\\output\\bl_check.txt"
            with open(path, "w") as order_file:
                order_file.writelines(f"{self.boundary.x} {self.boundary.y}\n")
                for solution in self.solutions:
                    for object in solution:
                        order_file.writelines(f"{object.width} {object.height} ")
                    order_file.writelines("\n")
        else:
            print(f"No placement order found!")


if __name__ == "__main__":
    PlacementChecker().run()
