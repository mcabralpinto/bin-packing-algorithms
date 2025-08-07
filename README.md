# bin-packing-algorithms
**bin-packing-algorithms** is a partial remake of a project developed during an investigation scholarship I did in my freshman year at Universidade de Coimbra (Visualization of Cutting & Packing Problems). Throughout the development of this refactor, I tried to stay faithful to the original version functionality-wise while fixing implementation errors and making it more scalable and readable (both through documentation and the code itself). The focus was mainly on the algorithmic part of the codebase, including:
- Bin-Packing Problem object logic and placement algorithms - Bottom-Left & Bottom-Left-Fill
- Solveability check for the height-constrained BPP
- Height optimization for the height-unconstrained BPP
- Guillotine cut check algorithms for placed object sets
- Test case creation for each of the aforementioned algorithms

## Repository Structure
```
AAA_new/
├── src/           # Source code
│   ├── core/      # Main algorithms and data structures
│   └── extra/     # Unused code / demonstrations
├── src_legacy/    # Original source code
├── datasets/      # Input data for experiments and testing
├── output/        # Results, logs, and generated outputs
└── README.md      # Project documentation (this file)
```
Note: Since `src_legacy` contains the code I originally made for this project in my freshman year, it is very rough around the edges. I chose to leave it that way to serve as a lesson in code organization and proper documentation, among other things. It serves merely as a reference for the current source code.

## Contents

### `core/rectangle.py`, `core/point.py`
These classes are the literal building blocks of the project. Every script was modified to use objects of these types, allowing the code to standardize geometric representations. In contrast, the original code handled this inconsistently across algorithms, often using lists and dictionaries instead of a dedicated data structure class. This decision also allowed for the specific operators, like `rotate()` and `merge()`, to be implemented directly in the class, uncluttering the algorithms themselves.

### `core/placement.py`
Implements algorithms for the Bin Packing Problem (BPP), a classic optimization problem where the goal is to efficiently pack a set of objects into a larger container (the "bin") without overlaps and minimizing wasted space. Centralizes all placement-related algorithms into a single, well-documented class, greatly simplifying the codebase compared to the original project. Previously, variations of the Bottom-Left (BL) and Bottom-Left-Fill (BLF) algorithms were scattered across multiple scripts, often duplicated and mixed with unrelated logic. Now, these functionalities are uniquely encapsulated in the `Placement` class, providing a unified interface for placing rectangles on a board. The main functions are:
- `bottom_left()`: Places a rectangle as far down and to the left as possible without overlapping others.
- `bottom_left_fill()`: Places a rectangle using BL, then tries to find an even better (lower) position if possible.
- `check_full_placement()`: Simulates placing a list of rectangles on the board, returning whether all fit within the boundaries.
- `place_object()`: Places a single rectangle on the board and updates the current height of the placed set.
- `get_bl_order()`: Finds the order in which rectangles should be placed so that the BL algorithm would produce a given solution.

### `algorithm_base.py`
Defines the abstract base class for the upcoming BPP algorithms, establishing a common structure for implementing different strategies. This prevents the existence of repeated code and once again adds to the scalability of the project, especially when compared with the original one. The main functions are:
- `test_orders()`: Recursively generates and evaluates all possible placement orders. Highly customizable for different strategies.
- `load_dataset()`: Loads board and rectangle data from input files.
- `get_solutions()`: Abstract; runs the main algorithm and finds existing solutions.
- `store_solutions()`: Abstract; saves the solutions found in the previous function.

### `placement_check.py`
Encapsulates the logic for finding valid placement orders of objects for the BPP using the BL algorithm. The `PlacementChecker` class inherits from `AlgorithmBase`, using the `test_orders()` function and only needing to tweak it slightly to fulfill its purpose, by adjusting the backtracking condition (continue searching only if the current placed set's height doesn't exceed the board's vertical boundary). A class attribute controls whether the algorithm stops at the first solution or if it tries to find every single one.
This approach is drastically optimized from the original code, since now only one object needs to be placed at each check, rather than redoing the entire placement. For a given sequence inside the recursion, the time complexity of the operation is reduced from O(n²) to O(n), n being number of objects.

### `height_optimization.py`
Focuses on identifying the object placement order in the BPP that achieves the minimum total height using the BL algorithm. The `HeightOptimizer` class also builds on `AlgorithmBase`, modifying `test_orders()` to favor lower heights. This means the algorithm only explores sequences where the current placement height is less than the best found so far, effectively narrowing the search space. When a new lowest height is discovered, the class updates its records accordingly. Additionally, there is a massive decrease in time complexity, for the same reasons described in the [`placement_check.py`](#placement_checkpy) section.

### `guillotine_check_by_dividing.py`
Implements the logic for verifying whether a given placement of rectangle objects can be fully separated using only guillotine cuts (straight cuts along the x or y axis in the original set and subsets). The `GuillotineDivide` class is the last to expand `AlgorithmBase`, using `test_orders()` method to generate valid placements, and then applying a recursive division algorithm to check guillotinability. The simplified algorithm-specific functions are:
- `divide()`: Splits a subset of rectangles into groups that can be separated by a single guillotine cut along the chosen axis (x or y). It sorts rectangles by their coordinates and forms groups based on overlapping intervals.
- `check_by_dividing()`: Recursively determines if a group of rectangles can be separated entirely by guillotine cuts. Uses a simpler logic where if neither axis yields new divisions (no cut was possible), the placement is not guillotinable.

### `guillotine_check_by_merging.py`
Takes a different approach at finding guillotinable solutions: instead of building them externally and checking each one, this algorithm recursively attempts to build a valid solution by merging objects using the `check_by_merging()` function, and then uses `get_bl_order()` from the `Placement` class to find an order for that solution. 
During the refactoring process, it became apparent that there are more ways in which two objects can be merged than the original code covered, particularly when rotations are permitted. Thus, this implementation utilizes a loop to systematically iterate through all possible merge scenarios. The `mergeability_condition()` function encapsulates the necessary logic, requiring only the loop index as its input parameter.

### `test_case_creation.py`
- **Zero Point:** Cuts a line along a random valid axis of an object and creates two new objects from the resulting pieces.
- **One Point:** Chooses a valid point inside an object, which is then used to split it into four new objects.
- **Two Point:** Selects two valid points inside an object and uses them to create five new objects following a specific star pattern. Unlike the other two, this type of division creates a non-guillotinable base solution.
- **Mixed:** Randomly combines the previous division methods.

## Running the Code
1. Clone the repository.
2. Install Python 3.9+.
3. Run scripts from the `src/` directory as needed.