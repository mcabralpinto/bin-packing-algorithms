from dataclasses import dataclass
from core.placement import Placement
from algorithm_base import AlgorithmBase


@dataclass
class BLHeightOptimizer(AlgorithmBase):
    """
    Finds the optimal BL placement order of objects to minimize the total height of the
    full placed set on the board.

    Attributes:
        height (int): The current height being evaluated for a placement.
    """
    height: int = 0

    def keep_recurring_condition(self, set_height: int) -> bool:
        """
        Determines if the optimization should continue based on the current set height.

        Args:
            set_height (int): The height of the current placement configuration.

        Returns:
            bool: True if height is less than the current best, False otherwise.
        """
        self.height = set_height
        return self.height < self.boundary.y

    def handle_solution(self, solution: Placement) -> None:
        """
        Handles a new solution by updating the best found order and height.

        Args:
            solution (Placement): The current placement solution being evaluated.

        Returns:
            None
        """
        order = solution.placed
        self.boundary.y = self.height
        self.solutions = [order]
        print(f"New best order found: {order} with height {self.height}")

    def announce(self) -> None:
        print(
            f"Attempting to find the minimum-total-height order for objects "
            f"{self.objects} on a board of width {self.boundary.x}..."
        )

    def get_solutions(self) -> None:
        self.boundary.y = sum(object.height for object in self.objects)
        self.test_orders(self.objects, Placement(boundary=self.boundary))

    def store_solutions(self) -> None:
        print(f"Best order: {self.solutions[0]} (height: {self.boundary.y})")
        path = f"..\\output\\bl_optimization.txt"
        with open(path, "w") as order_file:
            order_file.writelines(f"{self.boundary.x}\n")
            for object in self.solutions[0]:
                order_file.writelines(f"{object.width} {object.height} ")


if __name__ == "__main__":
    BLHeightOptimizer().run()
