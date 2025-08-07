import random

def checkInter(obj_now, positions):
    # check every object for intersection with every other object
    for next in positions:
        obj_next = positions[next]
    
        if not (obj_now[0][0] >= obj_next[1][0] or obj_now[1][0] <= obj_next[0][0] or obj_now[0][1] >= obj_next[1][1] or obj_now[1][1] <= obj_next[0][1]):
            return True
        
    return False


def order(left, bottom, width, height, objects, fill):
    placed = {}
    
    for i, obj in enumerate(objects):
        # establishes the starting conditions for the piece, such as its dimension and starting frame. also hides the block until it is its turn to fall onto the board
        obj_x = left + width - (int(obj[0]) / 2)
        obj_y = bottom + 2 * height + (int(obj[1]) / 2)
        coors = [[obj_x - int(obj[0]) / 2, obj_y - int(obj[1]) / 2], [obj_x + int(obj[0]) / 2, obj_y + int(obj[1]) / 2]]        

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
        

    return placed



def getorder(left, bottom, objects):
    
    new_order = []
    
    for _ in range(len(objects)):
        min_y = bottom
        for obj in objects:
            if objects[obj][0][0] == left and objects[obj][0][1] >= min_y:
                min_y = objects[obj][0][1]
                remove_obj = {"name": obj, "position": objects[obj]}
                
        removeable = False
        while not removeable:
            removeable = True
            min_y = remove_obj["position"][0][1]
            temp = remove_obj
            for obj in objects:
                if objects[obj][0][0] == remove_obj["position"][1][0] and objects[obj][0][1] >= min_y and obj != remove_obj["name"]:
                    min_y = objects[obj][0][1]
                    temp = {"name": obj, "position": objects[obj]}
                    removeable = False
            remove_obj = temp
            if removeable:

                new_order += [[str(int(temp["position"][1][0] - temp["position"][0][0])), str(int(temp["position"][1][1] - temp["position"][0][1]))]]
                objects.pop(remove_obj["name"])
            
    new_order.reverse()
    return new_order
    

for i in range(20):
    print(i)
    file = open(fr"datasets\t_n\ng\blf_orders\t_n_problem{i + 1}.txt", "r")
    lines = file.readlines()
    file.close()

    for j in range(len(lines)):
        lines[j] = lines[j].strip("\n").split(" ")

    board = lines[0]
    lines.remove(board)

    while len(lines) > 200:
        lines.remove(lines[-1])

    #random.shuffle(lines)

    placed = order(0, 0, int(board[0]), int(board[1]), lines, True)

    new_lines = getorder(0, 0, placed)

    file = open(fr"datasets\t_n\ng\bl_orders\t_n_problem{i + 1}.txt", "w")

    file.writelines(f"{board[0]} {board[1]}\n")
    for line in new_lines: file.writelines(f"{line[0]} {line[1]}\n")

    file.close()