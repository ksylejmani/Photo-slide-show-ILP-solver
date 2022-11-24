from gurobipy import *

# Data
P = 5
H = 2
V = 3
NH = 2
NV = V * (V - 1) / 2  # NV=3
N = int(NH + NV)  # N=5
photos = {1: 1, 2: 2, 3: 1, 4: 2, 5: 2}  # 1->H, 2->V

# Preprocessing
possible_slides = {1: [1], 2: [2, 4], 3: [2, 5], 4: [3], 5: [4, 5]}
same_photos = tuplelist([(2, 3), (3, 5)])

T, TI = multidict({(1, 2): 3, (2, 1): 3, (1, 3): 2, (3, 1): 2, (1, 4): 20, (4, 1): 20,
                   (1, 5): 3, (5, 1): 3,
                   (2, 3): 1, (3, 2): 1, (2, 4): 1, (4, 2): 1, (2, 5): 3, (5, 2): 3,
                   (3, 4): 5, (4, 3): 5, (3, 5): 3, (5, 3): 3, (4, 5): 4, (5, 4): 4})


# Data from file


class PhotoSlideShowData:
    def __init__(self, M: int, photos: dict):
        self.M = M
        self.photos = photos


file_name = 'a_example.txt'


def read_instance_from_file(file_name: str):
    try:
        with open('PhotoSlideShow\\' + file_name, 'r') as f:
            P = int(f.readline())
            photos = {}
            for i in range(P):
                photo_text = f.readline()
                photo_data = photo_text.split()
                photos[i] = photo_data
            result = PhotoSlideShowData(P, photos)
    except FileNotFoundError as e:
        print(e.strerror)
    except Exception as e:
        print(e.values)
    else:
        pass

    return result


slide_show_data = read_instance_from_file(file_name)
print(slide_show_data.M)
print(slide_show_data.photos)

m = Model('photo slide show')

z = {}
for i in range(1, N + 1):
    for j in range(1, N + 1):
        if i != j:
            z[(i, j)] = m.addVar(vtype=GRB.BINARY, name='z' + str(i) + str(j))

# Constraints
for sp in same_photos:
    i = sp[0]
    j = sp[1]
    m.addConstr(quicksum(
        quicksum(z[(a, b)] for b in range(1, N + 1) if b != a and (a == i or a == j or b == i or b == j)) for a in
        range(1, N + 1)) <= 1, name='same photos')

for i in range(1, N + 1):
    m.addConstr(quicksum(z[(i, j)] for j in range(1, N + 1) if j != i) <= 1,
                name='one slide is placed after slide i')

for j in range(1, N + 1):
    m.addConstr(quicksum(z[(i, j)] for i in range(1, N + 1) if j != i) <= 1,
                name='one slide is placed after slide j ')

for i in range(1, N + 1):
    for j in range(1, N + 1):
        if i != j:
            m.addConstr(z[(i, j)] + z[(j, i)] <= 1,
                        name='each slide is used at most once')

m.update()
m.setObjective(quicksum(quicksum(z[(i, j)] * TI[(i, j)] for j in range(2, N + 1) if j != i)
                        for i in range(1, N)), sense=GRB.MAXIMIZE)
m.optimize()
m.printAttr('X')
