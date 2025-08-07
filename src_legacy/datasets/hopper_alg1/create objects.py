import random

space_w = 200
space_h = 200
rect_n = 64
max_ar = 7
instance = 1

objects = [[[0, 0], [space_w, space_h]]]
sorted_objs = []
obj_sizes = []

for _ in range((rect_n - 1) // 3):
    valid = False
    while not valid:
        valid = True
        current = random.choice(objects)
        point = [random.randrange(current[0][0] + 1, current[1][0] - 1), random.randrange(current[0][1] + 1, current[1][1] - 1)]
        new_objs = [
            [[current[0][0], current[0][1]], [point[0], point[1]]],
            [[point[0], current[0][1]], [current[1][0], point[1]]],
            [[current[0][0], point[1]], [point[0], current[1][1]]],
            [[point[0], point[1]], [current[1][0], current[1][1]]]
        ]
        for obj in new_objs:
            aspect_ratio = (obj[1][0] - obj[0][0]) / (obj[1][1] - obj[0][1])
            if 1 / max_ar > aspect_ratio or aspect_ratio > max_ar or obj[1][0] - obj[0][0] < 3 or obj[1][1] - obj[0][1] < 3:
                valid = False
                break
    objects.remove(current)
    for obj in new_objs:
        objects.append(obj)

for _ in range(rect_n):
    bl_most = [[space_w, space_h], [space_w, space_h]]
    for obj in objects:
        if obj[0][1] < bl_most[0][1]:
            bl_most = obj
        elif obj[0][1] == bl_most[0][1] and obj[0][0] < bl_most[0][0]:
            bl_most = obj
    sorted_objs.append(bl_most)
    objects.remove(bl_most)

for obj in sorted_objs:
    obj_sizes.append(f"{obj[1][0] - obj[0][0]} {obj[1][1] - obj[0][1]}")

with open(fr"C:\Users\Utilizador\OneDrive - Universidade de Coimbra\UC\altri\bolsa_pcp\datasets\hopper_alg1\orders\my_problem{instance}.txt", "w") as problem:
    problem.writelines(f"{space_w} {space_h}\n")
    for obj in obj_sizes:
        problem.writelines(f"{obj}\n")