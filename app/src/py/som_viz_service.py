
import webview
import json
import numpy as np


def lerp(u, v, t):
    return u + t * (v - u)


def bilinear(q11, q12, q21, q22, x, y):
    # x and y are within range [0,1]
    r1 = lerp(q11, q12, x)
    r2 = lerp(q21, q22, x)
    return lerp(r1, r2, y)


class SOMVisualizationService:
    def __init__(self):

        # self.filename = webview.windows[0].create_file_dialog(
        #     webview.OPEN_DIALOG)
        self.filename = "/Volumes/Sweep SSD/comp3988pre/fashioncp.json"
        self.data = json.loads(open(self.filename).read())
        self.weights = np.array(self.data['weights'])

    def position(self, x, y):
        q11 = int(x), int(y)
        q12 = int(x) + 1, int(y)
        q21 = int(x), int(y) + 1
        q22 = int(x) + 1, int(y) + 1
        pts = [self.weights[i[1] * self.data['w'] + i[0]]
               for i in [q11, q12, q21, q22]]
        img = bilinear(*pts, x - int(x), y - int(y)) * 255

        return img.astype(np.int32).reshape((28, 28)).tolist()

    def get_dim(self):
        return self.data['w']
