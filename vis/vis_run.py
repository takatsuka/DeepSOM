from pysom.components.som import Som
import json
import numpy as np


width = 100
height = 100
indim = 3

som = Som(width, height, indim)
som.regen_mat(scale=2, offset=-0.5)

data_file = open("sphere_256.txt", "r")
dataset_lines = data_file.readlines()
data_file.close()

for i in range(len(dataset_lines)):
    dataset_lines[i] = dataset_lines[i].strip("\n").split(",")
    for j in range(len(dataset_lines[i])):
        dataset_lines[i][j] = float(dataset_lines[i][j])

data = np.array(dataset_lines)

js = {}

step = 0
for i in range(16000):
    point = data[np.random.randint(0, len(data))]
    som.learn(point, i)

    if i % 1600 == 0:
        fw = [elem for l in som.dump_weight_list() for elem in l]
        js[step] = fw
        step += 1
    
with open('vis_sphere256.txt', 'w') as outfile:
    json.dump(js, outfile)
