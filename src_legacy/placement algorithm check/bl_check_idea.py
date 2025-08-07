def checkInter(obj_now, positions):
    # check every object for intersection with every other object
    for next in positions:
        obj_next = positions[next]
    
        if not (obj_now[0][0] >= obj_next[1][0] or obj_now[1][0] <= obj_next[0][0] or obj_now[0][1] >= obj_next[1][1] or obj_now[1][1] <= obj_next[0][1]):
            return True
        
    return False


def bl(left, bottom, width, height, objects):
    placed = {}
    possible = True

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
            
        if coors[1][1] > int(board[1]):
            possible = False
            break
        placed.setdefault(i, coors)
    return possible


def recursion(order, new, rotate):
    count = 0
    if bl(0, 0, int(board[0]), int(board[1]), new):
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
#datasets\hopper_alg2\blf_orders\t_n_problem
#datasets\hopper_alg3\blf_orders\t_n_problem
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

with open(fr"placement algorithm check\cases_{name}.txt", "w") as order_file:
    order_file.writelines(f"{board[0]} {board[1]}\n")
    print("number of possible orders to use with bl algorithm:", recursion(order, [], False))

#~\AppData\Local\Microsoft\WindowsApps\python3.10.exe