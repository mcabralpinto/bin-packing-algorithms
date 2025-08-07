import random

def checkInter(obj_now, positions):
    # check every object for intersection with every other object
    for next in positions:
        obj_next = positions[next]
    
        if not (obj_now[0][0] >= obj_next[1][0] 
                or obj_now[1][0] <= obj_next[0][0] 
                or obj_now[0][1] >= obj_next[1][1] 
                or obj_now[1][1] <= obj_next[0][1]):
            return True
        
    return False

def bl(width, height, objects):
    placed = {}
    possible = True

    for i, obj in enumerate(objects):
        # establishes the starting conditions for the piece, such as its dimension and starting frame. also hides the block until it is its turn to fall onto the board
        obj_x = width - (int(obj[0]) / 2)
        obj_y = 2 * height + (int(obj[1]) / 2)
        coors = [[obj_x - int(obj[0]) / 2, obj_y - int(obj[1]) / 2], [obj_x + int(obj[0]) / 2, obj_y + int(obj[1]) / 2]]        

        stuck = False

        while not stuck:
            obj_y -= 1
            coors = [[obj_x - int(obj[0]) / 2, obj_y - int(obj[1]) / 2], [obj_x + int(obj[0]) / 2, obj_y + int(obj[1]) / 2]]
            
            if checkInter(coors, placed) or obj_y - int(obj[1]) / 2 < 0:
                obj_y += 1
                obj_x -= 1
                coors = [[obj_x - int(obj[0]) / 2, obj_y - int(obj[1]) / 2], [obj_x + int(obj[0]) / 2, obj_y + int(obj[1]) / 2]]
                
                if checkInter(coors, placed) or obj_x - int(obj[0]) / 2 < 0:
                    obj_x += 1
                    stuck = True
                    coors = [[obj_x - int(obj[0]) / 2, obj_y - int(obj[1]) / 2], [obj_x + int(obj[0]) / 2, obj_y + int(obj[1]) / 2]]

            
        
        # locates the piece to its saved coordinates and stores them to a list with the other placed pieces' coordinates
        if coors[1][1] > height:
            possible = False
            break
        placed.setdefault(i, coors)

    return [placed, possible]

def interval_add(intervals, curr):
    intervals.append([[curr[0][0], curr[1][0]], [curr[0][1], curr[1][1]]])

def interval_remove(intervals, curr):
    intervals.pop()

def interval_merge(ints, type):
    new = []
    for i in range(len(ints)): 
        new.append(ints[i][type][:])
    new.sort()
    print(f"ints: {ints}\ntype: {type}\nnew: {new}")
    stack = []
    stack.append(new[0][:])
    for i in new[1:]:
        if stack[-1][0] <= i[0] < stack[-1][-1]:
            stack[-1][-1] = max(stack[-1][-1], i[-1])
        else:
            stack.append(i)
    return stack

def g_check(intervals):
    if len(intervals) < 5: return True
    temp = [intervals[:]]
    #print(intervals)
    while temp != []:
        aux = temp[0][:]
        x_intervals, y_intervals = interval_merge(aux, 0), interval_merge(aux, 1)
        #print(f"i: {temp}\nx: {x_intervals}\ny: {y_intervals}")
        if len(x_intervals) + len(y_intervals) == 2: return False
        for x_interval in x_intervals:
            for y_interval in y_intervals:
                new = []
                for i in range(len(aux)):
                    if (aux[i][0][0] >= x_interval[0] and 
                        aux[i][0][1] <= x_interval[1] and 
                        aux[i][1][0] >= y_interval[0] and 
                        aux[i][1][1] <= y_interval[1]):
                        new.append(aux[i])
                for interval in new:
                    aux.remove(interval)
                temp.append(new)
        temp.pop(0)
        while True:
            if temp != []:
                if len(temp[0]) < 2:
                    temp.pop(0)
                else:
                    break
            else:
                break
    return True

first_order = []

def recursion(order, new, rotate, intervals, bl_placement, count):
    #print(intervals)
    if len(first_order) == 0:
        if (g_check(intervals)):
            if len(order) == 0:
                temp = new[:]
                if bl_placement[1]:
                    first_order.append(temp)
            else:
                if bl_placement[1]:
                    for current in order:
                        temp = order[:]
                        temp.remove(current)
                        if rotate:
                            for i in range(2):
                                new.append([current[i], current[1 - i]])
                                bl_placement = bl(int(board[0]), int(board[1]), new)
                                if len(new) > 0 and bl_placement[1]: 
                                    interval_add(intervals, bl_placement[0][count + 1])
                                    recursion(temp, new, rotate, intervals, bl_placement, count + 1)
                                    interval_remove(intervals, bl_placement[0][count + 1])
                                new.remove([current[i], current[1 - i]])
                        else:
                            new.append(current)
                            bl_placement = bl(int(board[0]), int(board[1]), new)
                            if len(new) > 0 and bl_placement[1]: 
                                interval_add(intervals, bl_placement[0][count + 1])
                                recursion(temp, new, rotate, intervals, bl_placement, count + 1)
                                interval_remove(intervals, bl_placement[0][count + 1])
                            new.pop()


name = fr"datasets\hopper_alg3\orders\t_n_problem5"
#datasets\t_n\ng\blf_orders\t_n_problem
#datasets\hopper_alg2\blf_orders\t_n_problem
#datasets\hopper_alg3\blf_orders\t_n_problem
#recursion\test_problem
file = open(fr"{name}.txt", "r")
name = name.replace("\\", "-")
print(name)

lines = file.readlines()
order = []
for line in lines:
    order.append(line.replace("\n", "").split())

board = order[0]
order.remove(board)
random.shuffle(order)
print(board, order, "\n\n\n\n")

file.close()

recursion(order, [], False, [], [{}, True], -1)
print(first_order)