from copy import deepcopy
from dataclasses import dataclass, field
from core.rectangle import Rectangle
from core.placement import Placement
from algorithm_base import AlgorithmBase

@dataclass
class GuillotineMerge(AlgorithmBase):
    """
    This algorithm attempts to recursively merge rectangles into a single guillotinable 
    block by checking all possible merge configurations using check_by_merging(). If 
    such a block is found, an external method (Placement.get_bl_order()) is used to find 
    a BL order of placement that reconstructs this exact guillotinable solution.
    """
    block: list[Rectangle] = field(default_factory=list)

    def mergeability_condition(self, o1: Rectangle, o2: Rectangle, k: int) -> bool:
        """
        Checks if two rectangles can be merged according to guillotine constraints.

        Args:
            o1 (Rectangle): The first rectangle.
            o2 (Rectangle): The second rectangle.
            k (int): The merge configuration index (rotation/merge direction).

        Returns:
            bool: True if the rectangles can be merged, False otherwise.
        """
        o1_size = [o1.width, o1.height]
        o2_size = [o2.width, o2.height]
        boundaries = [self.boundary.x, self.boundary.y]

        k1 = (k + 1) // 2 % 2
        k3 = k % 2
        k4 = 1 - k1
        k6 = (k + 1) % 2

        if k < 4:
            k2 = k1
            k5 = k4
        else:
            k2 = k4
            k5 = k1

        return (
            o1_size[k1] == o2_size[k2] <= boundaries[k3]
            and o1_size[k4] + o2_size[k5] <= boundaries[k6]
        )

    def check_by_merging(self, current_objects: list[Rectangle]) -> None:
        """
        Recursively attempts to merge rectangles into a single guillotinable block.

        Args:
            current_objects (list[Rectangle]): The current list of rectangles to merge.

        Returns:
            None
        """
        if not self.block:
            if len(current_objects) != 1:
                for i, o1 in enumerate(current_objects):
                    for j, o2 in enumerate(current_objects[i + 1 :]):
                        # for all objects, test all merge possibilities
                        real_j = j + i + 1
                        for k in range(8 if self.allow_rotations else 2):
                            if self.mergeability_condition(o1, o2, k):
                                # flip necessary objects
                                copy = deepcopy(current_objects)
                                o1, o2 = copy[i], copy[real_j]
                                if k in [2, 3, 6, 7]:
                                    o1.flip()
                                if k in [2, 3, 4, 5]:
                                    o2.flip()
                                for o in (o1, o2):
                                    if not o.contains:
                                        o.contains = [o]
                                # perform the merge and update the block
                                new_object = o1.merge(o2, x_merge=bool(k % 2))
                                copy.pop(real_j)
                                copy.pop(i)
                                copy.append(new_object)
                                self.check_by_merging(copy)
            else:
                self.block = current_objects[0].contains

    def announce(self) -> None:
        print(
            f"Attempting to find a guillotinable placement for objects {self.objects} "
            f"on a board of dimensions {self.boundary.x}x{self.boundary.y}...\n"
        )

    def get_solutions(self) -> None:
        self.objects = [Rectangle(o.width, o.height) for o in self.objects]
        self.check_by_merging(self.objects)
        if self.block != []:
            print(f"Found solution: {self.block}\n")
            self.solutions.append(
                Placement(boundary=self.boundary).get_bl_order(self.block)
            )

    def store_solutions(self) -> None:
        if self.block != []:
            print(f"Guillotinable BL order found: {self.solutions[0]} ")
            path = f"..\\output\\guillotine_check_merge.txt"
            with open(path, "w") as order_file:
                order_file.writelines(f"{self.boundary.x} ")
                order_file.writelines(f"{self.boundary.y}\n")
                for object in self.solutions[0]:
                    order_file.writelines(f"{object.width} {object.height} ")
        else:
            print(f"No guillotinable BL order found!")


if __name__ == "__main__":
    GuillotineMerge(allow_rotations=True).run()
