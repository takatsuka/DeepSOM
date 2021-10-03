
import webview
import json
import numpy as np

class SOMVisualizationService:
    def __init__(self):

        self.filename = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG)
        self.data = json.loads(open(self.filename[0]).read())
        self.weights = np.array(self.data['weights'])

    def position(self, x, y):
        img = self.weights[int(y) * self.data['w'] + int(x)] * 255

        return img.astype(np.int32).reshape((28, 28)).tolist()