import math

def checkInter(obj_now, positions):
    # check every object for intersection with every other object
    for next in positions:
        obj_next = positions[next]
    
        if not (obj_now[0][0] >= obj_next[1][0] or obj_now[1][0] <= obj_next[0][0] or obj_now[0][1] >= obj_next[1][1] or obj_now[1][1] <= obj_next[0][1]):
            return True
        
    return False

def bl(left, bottom, width, height, objects, fill):
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
                    saved = coors  
                    
                    if fill:
                        while stuck:
                            if obj_x - int(obj[0]) / 2 < left:
                                obj_x += 1
                                break
                            else:
                                obj_x -= 1
                                coors = [[obj_x - int(obj[0]) / 2, obj_y - int(obj[1]) / 2], [obj_x + int(obj[0]) / 2, obj_y + int(obj[1]) / 2]]
                                if not checkInter(coors, placed) and not obj_x - int(obj[0]) / 2 < left:
                                    stuck = False
            
        if coors[1][1] > int(board[0][1]):
            possible = False
            break
        placed.setdefault(i, coors)
    return [placed, possible]

def bl_check(orders):
    count = 0
    for order in orders:
        final = bl(0, 0, int(board[0][0]), int(board[0][1]), order, False)
        if final[1]:
            count += 1
            for i in range(len(order)):
                bl_file.writelines(f"{order[i][0]} {order[i][1]} ")
            bl_file.writelines("\n")


    return count

name = fr"datasets\hopper_alg2\orders\t_n_problem1"
#datasets\t_n\ng\blf_orders\t_n_problem1
#datasets\hopper_alg2\orders\t_n_problem   2556-1522  1932-492  5548-3856  12642-7684  2174-1738
#datasets\hopper_alg3\orders\t_n_problem    337-148    118-73    269-86      394-246     79-26
#datasets\test_problem.txt
name = name.replace("\\", "-")

with open(fr"placement algorithm check\usable_pure_blf\cases_{name}.txt", "r") as blf_file:
    lines = blf_file.readlines()

orders = []
for line in lines:
    line = line.replace("\n", "").split()
    obj_line = []
    for i in range(len(line) // 2):
        obj_line.append([line[2 * i], line[(2 * i) + 1]])
    orders.append(obj_line)

board = orders[0]
orders.remove(board)

print(name, "\n")

with open(fr"placement algorithm check\usable_bl\cases_{name}.txt", "w") as bl_file:
    bl_file.writelines(f"{board[0][0]} {board[0][1]}\n")
    print(f"out of {len(orders)} cases with blf solutions, {bl_check(orders)} had bl solutions.")


