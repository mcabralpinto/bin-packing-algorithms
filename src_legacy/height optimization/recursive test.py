import random


def checkInter(obj_now, positions):
    # check every object for intersection with every other object
    for next in positions:
        obj_next = positions[next]

        if not (
            obj_now[0][0] >= obj_next[1][0]
            or obj_now[1][0] <= obj_next[0][0]
            or obj_now[0][1] >= obj_next[1][1]
            or obj_now[1][1] <= obj_next[0][1]
        ):
            return True

    return False


def bl(left, bottom, width, objects):
    placed = {}
    height = 0

    for i, obj in enumerate(objects):
        # establishes the starting conditions for the piece, such as its dimension and starting frame. also hides the block until it is its turn to fall onto the board
        obj_x = left + width - (int(obj[0]) / 2)
        obj_y = bottom + max_height * 2 + (int(obj[1]) / 2)
        coors = [
            [obj_x - int(obj[0]) / 2, obj_y - int(obj[1]) / 2],
            [obj_x + int(obj[0]) / 2, obj_y + int(obj[1]) / 2],
        ]
        stuck = False

        while not stuck:
            obj_y -= 1
            coors = [
                [obj_x - int(obj[0]) / 2, obj_y - int(obj[1]) / 2],
                [obj_x + int(obj[0]) / 2, obj_y + int(obj[1]) / 2],
            ]

            if checkInter(coors, placed) or obj_y - int(obj[1]) / 2 < bottom:
                obj_y += 1
                obj_x -= 1
                coors = [
                    [obj_x - int(obj[0]) / 2, obj_y - int(obj[1]) / 2],
                    [obj_x + int(obj[0]) / 2, obj_y + int(obj[1]) / 2],
                ]

                if checkInter(coors, placed) or obj_x - int(obj[0]) / 2 < left:
                    obj_x += 1
                    stuck = True
                    coors = [
                        [obj_x - int(obj[0]) / 2, obj_y - int(obj[1]) / 2],
                        [obj_x + int(obj[0]) / 2, obj_y + int(obj[1]) / 2],
                    ]

        # locates the piece to its saved coordinates and stores them to a list with the other placed pieces' coordinates
        # obj_x = saved[0][0] + int(obj[0]) / 2
        # obj_y = saved[0][1] + int(obj[1]) / 2
        height = max(height, coors[1][1])
        if height >= max_height:
            break
        # print(saved)
        placed.setdefault(i, coors)

    return height


def recursion(order, new, rotate):

    curr_height = bl(b, l, w, new)
    if curr_height < best_orders[1]:
        if len(order) == 0:
            temp = new[:]
            best_orders[0], best_orders[1] = temp, curr_height
        else:
            for current in order:
                temp = order[:]
                temp.remove(current)
                if rotate:
                    for i in range(2):
                        new.append([current[-i], current[1 - i]])
                        recursion(temp, new, rotate)
                        new.remove([current[-i], current[1 - i]])
                else:
                    new.append(current)
                    recursion(temp, new, rotate)
                    new.remove(current)


n = 5
w, b, l = 200, 0, 0
ratio = 2
max_height = b
order = []
for _ in range(n):
    order.append(
        [random.randint(1, (w + 1) // ratio), random.randint(1, (w + 1) // ratio)]
    )
for obj in order:
    max_height += max(obj[0], obj[1])

print(w, order, "\n")

with open(r"\height optimization\min_h_orders\case4.txt", "w") as order_file:
    order_file.writelines(f"{w}\n")
    options = [False, True]
    for opt in options:
        best_orders = [order, max_height]
        recursion(order, [], opt)

        print(f"best order found: ", end="")
        for elem in best_orders[0]:
            print(f"{elem[0]} {elem[1]} ", end="")
            order_file.writelines(f"{elem[0]} {elem[1]}\n")
        print(f"\nheight: {int(best_orders[1])}")
