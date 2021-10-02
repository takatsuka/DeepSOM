from pysom.components.som import Som
import json
import numpy as np


width = 10
height = 10
indim = 3

som = Som(width, height, indim)
som.regen_mat(scale=2, offset=-0.5)

data_file = open("vis/sphere_64.txt", "r")
dataset_lines = data_file.readlines()
data_file.close()

for i in range(len(dataset_lines)):
    dataset_lines[i] = dataset_lines[i].strip("\n").split(",")
    for j in range(len(dataset_lines[i])):
        dataset_lines[i][j] = float(dataset_lines[i][j])

data = np.array(dataset_lines)

js = {}

step = 0
for i in range(1000):
    point = data[np.random.randint(0, len(data))]
    som.learn(point, i)

    if i % 100 == 0:
        s = {}
        fw = som.dump_weight_list()
        fw = [weights.tolist() for weights in fw]
        js[step] = fw
        step += 1
    
with open('app/src/components/scatterview_3d/data/vis_sphere64.json', 'w') as outfile:
    json.dump(js, outfile)
