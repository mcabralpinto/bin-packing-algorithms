import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from copy import deepcopy
from core.rectangle import Rectangle
from core.point import Point
from core.placement import Placement


@dataclass
class AlgorithmBase(ABC):
    """
    Abstract base class for object placement algorithms in the bin-packing problem.

    Attributes:
        boundary (Point): Dimensions of the board (width, height).
        objects (list[Rectangle]): List of rectangles to be placed.
        solutions (list[list[Rectangle]]): List of valid placement solutions.
        allow_rotations (bool): Whether to allow rectangle rotations.
        shuffle_objects (bool): Whether to shuffle the objects before placement.
    """

    boundary: Point = field(default_factory=lambda: Point(x=0, y=0))
    objects: list[Rectangle] = field(default_factory=list)
    solutions: list[list[Rectangle]] = field(default_factory=list)
    allow_rotations: bool = False
    shuffle_objects: bool = True

    def keep_recurring_condition(
        self,
        set_height: int,
    ) -> bool:
        raise NotImplementedError(
            "Subclasses that call test_orders must implement keep_recurring_condition."
        )

    def handle_solution(
        self,
        solution: Placement,
    ) -> None:
        raise NotImplementedError(
            "Subclasses that call test_orders must implement handle_solution."
        )

    def test_orders(
        self,
        current_objects: list[Rectangle],
        current_solution: Placement,
        set_height: int = 0,
    ) -> None:
        """
        Recursively finds all possible orders for placing rectangles. Allows subclasses
        to implement specific backtrack conditions and solution handling algorithms.

        Args:
            current_objects (list[Rectangle]): Rectangles left to place.
            current_solution (Placement): Current placement state.
            set_height (int, optional): Current set height.
        """
        if self.keep_recurring_condition(set_height):
            if not current_objects:
                self.handle_solution(deepcopy(current_solution))
            else:
                for obj in current_objects:
                    objects_copy = deepcopy(current_objects)
                    objects_copy.remove(obj)
                    to_add: list[Rectangle] = [deepcopy(obj)]

                    if self.allow_rotations and obj.width != obj.height:
                        rotated_object = deepcopy(obj)
                        rotated_object.flip(axis=(4, 4), clockwise=True)
                        to_add.append(rotated_object)

                    for new_object in to_add:
                        solution_copy = deepcopy(current_solution)
                        set_height = solution_copy.place_object(
                            object=new_object,
                            set_height=set_height,
                        )

                        self.test_orders(
                            current_objects=objects_copy,
                            current_solution=solution_copy,
                            set_height=set_height,
                        )

    @abstractmethod
    def announce(self) -> None:
        """
        Announces or logs the start of the algorithm.
        """
        pass

    def get_data(self, dataset_path) -> None:
        """
        Loads board dimensions and objects from a dataset file.

        Args:
            dataset_path (str): Path to the dataset file.
        """
        with open(dataset_path, "r") as file:
            lines = [line.replace("\n", "").split() for line in file.readlines()]
            self.boundary = Point(x=int(lines[0][0]), y=int(lines[0][1]))
            self.objects = [
                Rectangle(
                    width=int(line[0]),
                    height=int(line[1]),
                )
                for line in lines[1:]
            ]
        if self.shuffle_objects:
            random.shuffle(self.objects)
        self.solutions = []
        self.announce()

    @abstractmethod
    def get_solutions(self) -> None:
        """
        Initiates the process to test all possible orders of the objects for
        guillotineable placements.
        """
        pass

    @abstractmethod
    def store_solutions(self) -> None:
        """
        Stores the first found guillotineable placement order to an output file,
        or prints a message if none is found.
        """
        pass

    def run(self, dataset_path: str = "..\\datasets\\test_problem.txt") -> None:
        """
        Executes the full algorithm: loads data, finds solutions, and stores results.

        Args:
            dataset_path (str, optional): Path to the dataset file.
        """
        self.get_data(dataset_path)
        self.get_solutions()
        self.store_solutions()
