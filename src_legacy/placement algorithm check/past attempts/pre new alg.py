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

        found = True
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
            
        
        # locates the piece to its saved coordinates and stores them to a list with the other placed pieces' coordinates
        obj_x = saved[0][0] + int(obj[0]) / 2
        obj_y = saved[0][1] + int(obj[1]) / 2
        placed.setdefault(i, saved)
        
        

    return [placed, found]


def recursion(order, new, rotate):
    #print(new)
    count = 0
    exploreable = True
    if len(new) > 1:
        if not bl(0, 0, int(board[0]), int(board[1]), new, True)[1]:
            exploreable = False
            final = bl(0, 0, int(board[0]), int(board[1]), new, True)[0]
            for key in final:
                if final[key][1][0] > int(board[0]) or final[key][1][1] > int(board[1]):
                    return 0
    if exploreable:
        if len(order) == 0:
            print(new)
            final = bl(0, 0, int(board[0]), int(board[1]), new, True)[0]
            print(final, "\n")
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


#file = open(fr"datasets\t_n\ng\blf_orders\t_n_problem3.txt", "r")
file = open(fr"recursion\test_problem.txt", "r")

lines = file.readlines()
order = []
for line in lines:
    order.append(line.replace("\n", "").split())

board = order[0]
order.remove(board)
print(board, order, "\n\n\n\n\n\n\n\n\n")
print(f"out of {math.factorial(len(order))}, {recursion(order, [], False)} cases had solutions.")

