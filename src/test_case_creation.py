import random
from enum import Enum
from dataclasses import dataclass, field
from core.rectangle import Rectangle
from core.point import Point


class DivisionType(Enum):
    """
    Enum representing the different types of division algorithms.

    Attributes:
        ZERO_POINT: Division with zero points (two rectangles).
        ONE_POINT: Division with one point (four rectangles).
        TWO_POINT: Division with two points (five rectangles).
        MIXED: Mixed division type.
    """
    ZERO_POINT = 0
    ONE_POINT = 1
    TWO_POINT = 2
    MIXED = 3


@dataclass
class TestCaseCreation:
    """
    Generates test cases by dividing a board into rectangles using a division strategy.

    Attributes:
        object_amount (int): Number of objects to generate per test case.
        case_amount (int): Number of test cases to generate.
        width (int): Width of the board.
        height (int): Height of the board.
        min_ratio (float): Minimum ratio of the board size for each object.
        algorithm (DivisionType): Division algorithm to use.
        objects (list[Rectangle]): List of rectangles in the current test case.
    """

    object_amount: int
    case_amount: int

    width: int = 200
    height: int = 200

    min_ratio: float = 0.025
    algorithm: DivisionType = DivisionType.MIXED
    objects: list[Rectangle] = field(default_factory=list)

    def get_points(
        self,
        object: Rectangle,
        amount: int = 1,
        axis: tuple[bool, bool] = (True, True),
    ) -> list[Point]:
        """
        Generates a given amount of points with valid distances between each other
        within the bounds of an object.

        Args:
            object (Rectangle): The rectangle within which to generate points.
            amount (int): Number of points to generate.
            axis (tuple[bool, bool]): Axes to consider for point generation (x, y).

        Returns:
            list[Point]: List of generated points.
        """
        # List to store the generated points
        points: list[Point] = []

        # Calculate the minimum distances based on the object's dimensions and the
        # minimum ratio (makes sure the new objects will have a valid size)
        min_distances = (
            int(self.width * self.min_ratio),
            int(self.height * self.min_ratio),
        )

        # Loop until we have the required number of valid points
        while not points:
            for _ in range(amount):
                # Randomly select a point within the object's bounds, respecting
                # min_distances
                point = Point(
                    x=(
                        random.randrange(
                            min_distances[0],
                            object.width - min_distances[0] + 1,
                        )
                        if axis[0]
                        else 0
                    ),
                    y=(
                        random.randrange(
                            min_distances[1],
                            object.height - min_distances[1] + 1,
                        )
                        if axis[1]
                        else 0
                    ),
                )
                points.append(point)

            # Check if the points are valid (they are not too close to each other
            # according to min_distances); This approach of randomly generating points
            # would become too inefficient if many points were being generated at once,
            # but it is sufficient for the current use case (2 at max)
            for i in range(len(points)):
                for j in range(i + 1, len(points)):
                    if not points[i].check_valid_distance(
                        points[j],
                        distance=min_distances,
                    ):
                        points = []
                        break
                if not points:
                    break

        return points

    def zero_point(self, object: Rectangle) -> list[Rectangle]:
        """
        Divides a rectangle into two parts along a random axis.

        Args:
            object (Rectangle): The rectangle to split.

        Returns:
            list[Rectangle]: List containing the two resulting rectangles.
        """
        # Determine which axis to split
        split_in_axis = object.get_split_axes(self.width, self.height, self.min_ratio)
        if not split_in_axis["y"]:
            x_split = True
        elif not split_in_axis["x"]:
            x_split = False
        else:
            # Randomly choose the axis to split if both are valid
            x_split = random.choice([True, False])

        if x_split:
            # Division on the x-axis
            division = self.get_points(object, axis=(True, False))[0].x
            new_objects = [
                Rectangle(division, object.height),
                Rectangle(object.width - division, object.height),
            ]
        else:
            # Division on the y-axis
            division = self.get_points(object, axis=(False, True))[0].y
            new_objects = [
                Rectangle(object.width, division),
                Rectangle(object.width, object.height - division),
            ]

        return new_objects

    def one_point(self, object: Rectangle) -> list[Rectangle]:
        """
        Divides a rectangle into four parts using a single point.

        Args:
            object (Rectangle): The rectangle to split.

        Returns:
            list[Rectangle]: List containing the four resulting rectangles.
        """
        # Get a random point within the object
        point = self.get_points(object)[0]

        # Use the point to create four new objects
        new_objects = [
            Rectangle(point.x, point.y),
            Rectangle(object.width - point.x, point.y),
            Rectangle(point.x, object.height - point.y),
            Rectangle(object.width - point.x, object.height - point.y),
        ]

        return new_objects

    def two_point(self, object: Rectangle) -> list[Rectangle]:
        """
        Divides a rectangle into five parts using two points.

        Args:
            object (Rectangle): The rectangle to split.

        Returns:
            list[Rectangle]: List containing the five resulting rectangles.
        """
        # Get two distinct points within the object
        pointA, pointB = self.get_points(object, amount=2)

        # Make pointA be to the left of pointB
        if pointA.x > pointB.x:
            pointA, pointB = pointB, pointA

        # Depending on the relative y-coordinates, create the five new objects
        if pointA.y < pointB.y:
            new_objects = [
                Rectangle(pointA.x, object.height - pointA.y),
                Rectangle(object.width - pointA.x, object.height - pointB.y),
                Rectangle(pointB.x, pointA.y),
                Rectangle(object.width - pointB.x, pointB.y),
                Rectangle(pointB.x - pointA.x, pointB.y - pointA.y),
            ]
        else:
            new_objects = [
                Rectangle(pointB.x, object.height - pointA.y),
                Rectangle(object.width - pointB.x, object.height - pointB.y),
                Rectangle(pointA.x, pointA.y),
                Rectangle(object.width - pointA.x, pointB.y),
                Rectangle(pointB.x - pointA.x, pointA.y - pointB.y),
            ]

        return new_objects

    def create_test_case(self) -> None:
        """
        Creates a test case by repeatedly applying the selected division algorithm
        until the desired number of objects is reached.
        """
        # Assign the division method based on the selected algorithm (except MIXED)
        division_methods = {
            DivisionType.ZERO_POINT: self.zero_point,
            DivisionType.ONE_POINT: self.one_point,
            DivisionType.TWO_POINT: self.two_point,
        }
        
        # Generate objects until the desired amount is reached
        while len(self.objects) < self.object_amount:
            if self.algorithm == DivisionType.MIXED:
                algorithm = random.choice(list(division_methods.keys()))
                method = division_methods[algorithm]
            else:
                algorithm = self.algorithm
                method = division_methods.get(algorithm)

            # Choose a valid object to split
            object = random.choice(self.objects)
            while not (object := random.choice(self.objects)).can_be_split(
                board_width=self.width,
                board_height=self.height,
                min_ratio=self.min_ratio,
                points=algorithm.value,
            ):
                ...

            # Remove the selected object from the list
            self.objects.remove(object)

            # Call the division method to split the object
            if method is not None:
                new_objects = method(object)

                # Add the newly created objects to the list
                for new_object in new_objects:
                    self.objects.append(new_object)

    def store_test_case(self, case_n: int) -> None:
        """
        Stores the generated test case to a file.

        Args:
            case_n (int): The index of the test case to store.
        """
        path = f"..\\datasets\\created\\case_{case_n}.txt"
        with open(path, "w") as order_file:
            order_file.writelines(f"{self.width} {self.height}\n")
            for object in self.objects:
                order_file.writelines(f"{object.width} {object.height}\n")

    def run(self) -> None:
        """
        Runs the test case creation process for the specified number of cases.
        Raises an error if the minimum ratio is too high for the number of objects.
        """
        if (self.min_ratio * self.object_amount) > 1:
            raise ValueError("Minimum ratio too high for the number of objects!")
        for i in range(self.case_amount):
            # Start with a single object covering the whole area
            self.objects = [Rectangle(width=self.width, height=self.height)]
            self.create_test_case()
            self.store_test_case(i)


if __name__ == "__main__":
    test_case = TestCaseCreation(object_amount=20, case_amount=5)
    test_case.run()
