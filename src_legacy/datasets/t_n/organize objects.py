n = 3

file = open(fr"datasets\t_n\g\objects{n}.txt", "r")
lines = file.readlines()
new = []
for line in lines:
    new.append(line.replace("\n", "").split())

for i in range(len(new) - 2):
    new[i + 2].pop(0)

print(new)
problems = int(len(new[2]) / 2)

# for i in range(len(new) - 2):
#     new[i + 2].pop(0)


for i in range(problems):
    problem = open(fr"datasets\t_n\g\blf_orders\t_n_problem{i + 1 + (5 * (n - 1))}.txt", "w")
    problem.writelines(f"{new[1][0]} {new[1][1]}\n")
    for j in range(int(new[0][0])):
        # print(i, j)
        # print(new[j + 2][2 * i])
        # print(new[j + 2][2 * i + 1])
        problem.writelines(f"{new[j + 2][2 * i]} {new[j + 2][2 * i + 1]}\n")
    problem.close()

file.close()