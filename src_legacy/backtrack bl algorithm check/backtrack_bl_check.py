import random

def checkInter(obj_now, positions):
    # check every object for intersection with every other object
    for next in positions:
        obj_next = positions[next]
    
        if not (obj_now[0][0] >= obj_next[1][0] or obj_now[1][0] <= obj_next[0][0] or obj_now[0][1] >= obj_next[1][1] or obj_now[1][1] <= obj_next[0][1]):
            return True
        
    return False


# def pure_blf(left, bottom, width, height, objects):
#     placed = {}
#     available = [[left, bottom]]

#     for i, obj in enumerate(objects):
#         found = False

#         for spot in available:
#             obj_x, obj_y = spot[0], spot[1]
#             coors = [[obj_x, obj_y], [obj_x + int(obj[0]), obj_y + int(obj[1])]]
#             if not checkInter(coors, placed) and not coors[1][0] > left + width and not coors[1][1] > bottom + height:
#                 new_points = [[coors[1][0], coors[0][1]], [coors[0][0], coors[1][1]]]
#                 chosen = spot
#                 found = True
#                 break

#         if found:
#             if new_points[0][0] < left + width and (new_points[0][1] == 0 or checkInter([[new_points[0][0], new_points[0][1] - 1], [new_points[0][0] + 1, new_points[0][1]]], placed)):
#                 for j in range(len(available)):
#                     if (new_points[0][1] > available[j][1]) or (new_points[0][1] == available[j][1] and new_points[0][0] > available[j][0]):
#                         if len(available) == j + 1:
#                             available.insert(j + 1, new_points[0])
#                             break
#                         elif (new_points[0][1] < available[j + 1][1]) or (new_points[0][1] == available[j + 1][1] and new_points[0][0] < available[j + 1][0]):
#                             available.insert(j + 1, new_points[0])
#                             break

#             if new_points[1][1] < bottom + height and (new_points[1][0] == 0 or checkInter([[new_points[1][0] - 1, new_points[1][1]], [new_points[1][0], new_points[1][1] + 1]], placed)):
#                 for j in range(len(available)):
#                     if (new_points[1][1] > available[j][1]) or (new_points[1][1] == available[j][1] and new_points[1][0] > available[j][0]):
#                         if len(available) == j + 1:
#                             available.insert(j + 1, new_points[1])
#                             break
#                         elif (new_points[1][1] < available[j + 1][1]) or (new_points[1][1] == available[j + 1][1] and new_points[1][0] < available[j + 1][0]):
#                             available.insert(j + 1, new_points[1])
#                             break
                            
#             available.remove(chosen)
#             placed.setdefault(i, coors)
#         else:
#             break
 
#     return [placed, found]


def bl(left, bottom, width, height, objects):
    placed = {}
    
    for i, obj in enumerate(objects):
        # establishes the starting conditions for the piece, such as its dimension and starting frame. also hides the block until it is its turn to fall onto the board
        obj_x = left + width - (int(obj[0]) / 2)
        obj_y = bottom + 2 * height + (int(obj[1]) / 2)
        coors = [[obj_x - int(obj[0]) / 2, obj_y - int(obj[1]) / 2], [obj_x + int(obj[0]) / 2, obj_y + int(obj[1]) / 2]]        

        possible = True
        stuck = False

        while not stuck:
            obj_y -= 1
            coors = [[obj_x - int(obj[0]) / 2, obj_y - int(obj[1]) / 2], [obj_x + int(obj[0]) / 2, obj_y + int(obj[1]) / 2]]
            
            if checkInter(coors, placed) or obj_y - int(obj[1]) / 2 < bottom:
                obj_y += 1
                obj_x -= 1
                coors = [[obj_x - int(obj[0]) / 2, obj_y - int(obj[1]) / 2], [obj_x + int(obj[0]) / 2, obj_y + int(obj[1]) / 2]]
                
                if checkInter(coors, placed) or obj_x - int(obj[0]) / 2 < left:
                    obj_x += 1
                    stuck = True
                    coors = [[obj_x - int(obj[0]) / 2, obj_y - int(obj[1]) / 2], [obj_x + int(obj[0]) / 2, obj_y + int(obj[1]) / 2]]
        
        # locates the piece to its saved coordinates and stores them to a list with the other placed pieces' coordinates
        if coors[1][1] > bottom + height:
            possible = False
            break
        placed.setdefault(i, coors)

    return [placed, possible]

first_order = []

def recursion(order, new, rotate):

    if len(first_order) == 0:
        if len(order) == 0:
            temp = new[:]
            if bl(0, 0, int(board[0]), int(board[1]), new)[1]:
                first_order.append(temp)
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


name = fr"datasets\test_problem"
#datasets\t_n\ng\blf_orders\t_n_problem
#datasets\hopper_alg2\blf_orders\t_n_problem
#datasets\hopper_alg3\blf_orders\t_n_problem
#datasets\test_problem
with open(fr"{name}.txt", "r") as obj_file:
    lines = obj_file.readlines()
name = name.replace("\\", "-")
print(name)

order = []
for line in lines:
    order.append(line.replace("\n", "").split())
board = order[0]
order.remove(board)
random.shuffle(order)

print(board, order, "\n")

order_file = open(fr"backtrack bl algorithm check\usable_bl\cases-{name}.txt", "w")
order_file.writelines(f"{board[0]} {board[1]}\n")
recursion(order, [], False)

if len(first_order):
    print(f"first bl order found", end="")
    for elem in first_order[0]:
        print(f" -> [{elem[0]}, {elem[1]}]", end="")
        order_file.writelines(f"{elem[0]} {elem[1]} ")
else:
    print(f"no bl order found!", end="")

order_file.close()

#~\AppData\Local\Microsoft\WindowsApps\python3.10.exe