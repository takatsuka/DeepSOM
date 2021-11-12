import numpy as np

f = [i.split(',') for i in open("./uaScoresDataFrame.csv").readlines()]
f = np.array(f)[1:]

open("city_labels", "w").write("\n".join(f[:, 1]))

open("city_feat", "w").write(''.join([','.join(i) for i in f[:, 4:]]))
