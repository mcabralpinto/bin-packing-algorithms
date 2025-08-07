def checkInter(obj_now, positions):
    # check every object for intersection with every other object
    for next in positions:
        obj_next = positions[next]
    
        if not (obj_now[0][0] >= obj_next[1][0] or obj_now[1][0] <= obj_next[0][0] or obj_now[0][1] >= obj_next[1][1] or obj_now[1][1] <= obj_next[0][1]):
            return True
        
    return False


def new_bl(left, bottom, width, height, objects):
    placed = {}
    available = [[left, bottom]]
    found = True

    for i, obj in enumerate(objects):
        found = False

        for spot in available:
            obj_x, obj_y = spot[0], spot[1]
            coors = [[obj_x, obj_y], [obj_x + int(obj[0]), obj_y + int(obj[1])]]
            if not checkInter(coors, placed) and not coors[1][0] > left + width and not coors[1][1] > bottom + height:
                new_points = [[coors[1][0], coors[0][1]], [coors[0][0], coors[1][1]]]
                chosen = spot
                found = True
                break

        if found:
            if new_points[0][0] < left + width and (new_points[0][1] == 0 or checkInter([[new_points[0][0], new_points[0][1] - 1], [new_points[0][0] + 1, new_points[0][1]]], placed)):
                for j in range(len(available)):
                    if (new_points[0][1] > available[j][1]) or (new_points[0][1] == available[j][1] and new_points[0][0] > available[j][0]):
                        if len(available) == j + 1:
                            available.insert(j + 1, new_points[0])
                            break
                        elif (new_points[0][1] < available[j + 1][1]) or (new_points[0][1] == available[j + 1][1] and new_points[0][0] < available[j + 1][0]):
                            available.insert(j + 1, new_points[0])
                            break

            if new_points[1][1] < bottom + height and (new_points[1][0] == 0 or checkInter([[new_points[1][0] - 1, new_points[1][1]], [new_points[1][0], new_points[1][1] + 1]], placed)):
                for j in range(len(available)):
                    if (new_points[1][1] > available[j][1]) or (new_points[1][1] == available[j][1] and new_points[1][0] > available[j][0]):
                        if len(available) == j + 1:
                            available.insert(j + 1, new_points[1])
                            break
                        elif (new_points[1][1] < available[j + 1][1]) or (new_points[1][1] == available[j + 1][1] and new_points[1][0] < available[j + 1][0]):
                            available.insert(j + 1, new_points[1])
                            break

            available.remove(chosen)
            placed.setdefault(i, coors)
        else:
            break
            
    #if an object can't be placed, the function will return found with a value of False
    return found


def recursion(order, new, rotate):
    count = 0
    if new_bl(0, 0, int(board[0]), int(board[1]), new):
        if len(order) == 0:
            for i in range(len(new)):
                order_file.writelines(f"{new[i][0]} {new[i][1]} ")
            order_file.writelines("\n")
            return 1
        else:
            for current in order:
                temp = order[:]
                temp.remove(current)
                if rotate:
                    for i in range(2):
                        new.append([current[-i], current[1 - i]])
                        count += recursion(temp, new, rotate)
                        new.remove([current[-i], current[1 - i]])
                else:
                    new.append(current)
                    count += recursion(temp, new, rotate)
                    new.remove(current)
    else:
        return 0

    return count


name = fr"datasets\hopper_alg2\orders\t_n_problem1"
#datasets\t_n\ng\blf_orders\t_n_problem1
#datasets\hopper_alg2\orders\t_n_problem
#datasets\hopper_alg3\orders\t_n_problem
#datasets\test_problem
with open(fr"{name}.txt", "r") as obj_file: 
    lines = obj_file.readlines()

order = []
for line in lines:
    order.append(line.replace("\n", "").split())

name = name.replace("\\", "-")
print(name)
board = order[0]
order.remove(board)
print(board, order, "\n")

with open(fr"placement algorithm check\usable_pure_blf\cases_{name}.txt", "w") as order_file:
    order_file.writelines(f"{board[0]} {board[1]}\n")
    print("number of possible orders to use with blf algorithm:", recursion(order, [], False))

#~\AppData\Local\Microsoft\WindowsApps\python3.10.exe