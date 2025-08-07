import random
from copy import deepcopy

g_solution = []

def ngorg(b, objs, rotate):
    print(objs)
    if len(g_solution) < 1:
        if len(objs) != 1:
            for i in range(len(objs)):
                for j in range(i + 1, len(objs)):

                    if objs[i][1] == objs[j][1] and objs[i][2] + objs[j][2] <= int(b[1]) and len(g_solution) < 1:
                        temp = deepcopy(objs)
                        for obj in temp[j][0]:
                            obj[2] += objs[i][2]
                        aux = [temp[i][0] + temp[j][0], objs[i][1], objs[i][2] + objs[j][2]]
                        temp.pop(j)
                        temp.pop(i)
                        temp.append(aux)
                        ngorg(b, temp, rotate)

                    if objs[i][2] == objs[j][2] and objs[i][1] + objs[j][1] <= int(b[0]) and len(g_solution) < 1:
                        temp = deepcopy(objs)
                        for obj in temp[j][0]:
                            obj[1] += objs[i][1]
                        aux = [temp[i][0] + temp[j][0], objs[i][1] + objs[j][1], objs[i][2]]
                        temp.pop(j)
                        temp.pop(i)
                        temp.append(aux)
                        ngorg(b, temp, rotate)

                    if (rotate):

                        if (objs[i][1] == objs[j][2] or objs[i][2] == objs[j][1]) and len(g_solution) < 1:
                            if objs[i][2] + objs[j][1] <= int(b[1]):
                                temp = deepcopy(objs)
                                for obj in temp[j][0]:
                                    obj[1], obj[2] = obj[2], obj[1]
                                    obj[3] = not obj[3]
                                    obj[2] += temp[i][2]
                                aux = [temp[i][0][:] + temp[j][0][:], temp[i][1], temp[i][2] + temp[j][1]]
                                temp.pop(j)
                                temp.pop(i)
                                temp.append(aux)
                                ngorg(b, temp, rotate)

                            if objs[i][1] + objs[j][2] <= int(b[0]):
                                temp = deepcopy(objs)
                                for obj in temp[j][0]:
                                    obj[1], obj[2] = obj[2], obj[1]
                                    obj[3] = True
                                    obj[1] += temp[i][1]
                                aux = [temp[i][0][:] + temp[j][0][:], temp[i][1] + temp[j][2], temp[i][2]]
                                temp.pop(j)
                                temp.pop(i)
                                temp.append(aux)
                                ngorg(b, temp, rotate)
        else: 
            new = objs[:]
            g_solution.append(new)
    
def getorder(left, bottom, pl):
    
    new_order = []
    
    for _ in range(len(pl)):
        min_y = bottom
        for obj in pl:
            if pl[obj][0][0] == left and pl[obj][0][1] >= min_y:
                min_y = pl[obj][0][1]
                remove_obj = {"name": obj, "position": pl[obj]}
                
        removeable = False
        while not removeable:
            removeable = True
            min_y = remove_obj["position"][0][1]
            temp = remove_obj
            for obj in pl:
                if pl[obj][0][0] == remove_obj["position"][1][0] and pl[obj][0][1] >= min_y and obj != remove_obj["name"]:
                    min_y = pl[obj][0][1]
                    temp = {"name": obj, "position": pl[obj]}
                    removeable = False
            remove_obj = temp
            if removeable:
                new_order += [[str(int(pl[remove_obj["name"]][1][0] - pl[remove_obj["name"]][0][0])), str(int(pl[remove_obj["name"]][1][1] - pl[remove_obj["name"]][0][1]))]]
                pl.pop(remove_obj["name"])
            
    new_order.reverse()
    return new_order

name = fr"datasets\hopper_alg3\orders\t_n_problem3"
#datasets\t_n\ng\blf_orders\t_n_problem
#datasets\hopper_alg2\orders\t_n_problem
#datasets\hopper_alg3\orders\t_n_problem
#recursion\test_problem

with open(fr"{name}.txt", "r") as obj_file:
    lines = obj_file.readlines()    
order = []
first_orders = []
for line in lines:
    order.append(line.replace("\n", "").split())

board = order[0]
order.remove(board)
objects = []
for i in range(len(order)):
    objects.append([[[i, 0, 0, False]], int(order[i][0]), int(order[i][1])])
ngorg(board, objects, True)
print(name, "\n" + str(board), order, "\n")

if len(g_solution) > 0:
    g_solution = g_solution[0][0]
    placed = {}
    for obj in g_solution[0]:
        if not obj[3]: placed.setdefault(obj[0], [[obj[1], obj[2]], [obj[1] + objects[obj[0]][1], obj[2] + objects[obj[0]][2]]])
        else: placed.setdefault(obj[0], [[obj[1], obj[2]], [obj[1] + objects[obj[0]][2], obj[2] + objects[obj[0]][1]]])
    print("objects ordered to achieve a guillotinable solution:", getorder(0, 0, placed))
else:
    print("the program couldn't find an order of objects which would result in a guillotinable solution for this problem.\n")

#~\AppData\Local\Microsoft\WindowsApps\python3.10.exe