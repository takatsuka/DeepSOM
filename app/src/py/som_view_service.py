import json
import os
import re
import numpy as np
import webview

from pysom.graph import GraphCompileError
from pysom.nodes.calibrate import Calibrate
from pysom.nodes.som import SOM
import traceback
from collections import Counter, defaultdict

# Model training service


class SomViewService:
    def __init__(self, ds):
        self.ds = ds
        self.input_key = None
        self.som = None
        self.cal = None

        self.links = None
        self.nodes = None

        self.palette = np.array([[0.12156863, 0.46666667, 0.70588235],
                                 [0.68235294, 0.78039216, 0.90980392],
                                 [1., 0.49803922, 0.05490196],
                                 [1., 0.73333333, 0.47058824],
                                 [0.17254902, 0.62745098, 0.17254902],
                                 [0.59607843, 0.8745098, 0.54117647],
                                 [0.83921569, 0.15294118, 0.15686275],
                                 [1., 0.59607843, 0.58823529],
                                 [0.58039216, 0.40392157, 0.74117647],
                                 [0.77254902, 0.69019608, 0.83529412],
                                 [0.54901961, 0.3372549, 0.29411765],
                                 [0.76862745, 0.61176471, 0.58039216],
                                 [0.89019608, 0.46666667, 0.76078431],
                                 [0.96862745, 0.71372549, 0.82352941],
                                 [0.49803922, 0.49803922, 0.49803922],
                                 [0.78039216, 0.78039216, 0.78039216],
                                 [0.7372549, 0.74117647, 0.13333333],
                                 [0.85882353, 0.85882353, 0.55294118],
                                 [0.09019608, 0.74509804, 0.81176471],
                                 [0.61960784, 0.85490196, 0.89803922]])

    def generate_nodes(self):
        def rgb2hex(x): return "#{:02x}{:02x}{:02x}".format(
            *np.clip(np.array((x * 255.0), dtype=np.int32), 0, 255))

        def fmt(x): return ','.join([f'{i}' for i in x.keys()])
        def mix(w, m): return np.sum(m * w[:, np.newaxis], axis=0)

        labelmap = None
        if not self.cal is None:
            labelmap = {k[0]*self.som.size + k[1]: v for k,
                        v in self.cal.get_output(slot=1).items()}
        else:
            return [{'id': i} for i in range(self.som.size ** 2)]

        cmap = np.array(self.palette[:len(labelmap)])
        logit = self.cal.logit()
        # self.nodes = [{
        #     'id': i,
        #     'l': fmt(labelmap.get(i, Counter())),
        #     'c': rgb2hex(colored.get(i, np.array([0.1, 0.1, 0.1])))
        # } for i in range(self.som.size ** 2)]

        self.nodes = [{
            'id': i,
            'l': fmt(labelmap.get(i, Counter())),
            'c': rgb2hex(mix(logit[i], cmap))
        } for i in range(self.som.size ** 2)]

    def rect_links(self):
        dim = self.som.size
        w = self.som.get_weights()
        links = []
        for y in range(dim):
            for x in range(dim - 1):
                row = y * dim
                l = {'source': row + x, 'target': row + x + 1,
                     'value': np.linalg.norm(w[row + x] - w[row + x + 1]) * 100}
                links.append(l)

        for y in range(dim - 1):
            for x in range(dim):
                row = y * dim
                l = {'source': row + x, 'target': row + x + dim,
                     'value': np.linalg.norm(w[row + x] - w[row + x + dim]) * 100}
                links.append(l)

        return links

    def set_input(self, key):
        self.input_key = key

        data = self.ds.get_object_data(self.input_key)
        if data is None:
            return {'status': False, 'msg': 'Input data does not exist.'}

        if isinstance(data, SOM):
            self.som = data
        elif isinstance(data, Calibrate):
            self.cal = data
            self.som = self.cal.get_input()
        else:
            return {'status': False, 'msg': 'Input data is neither a SOM node or Calibrate node.'}

        self.links = self.rect_links()

        try:
            self.generate_nodes()
        except:
            return {'status': False, 'msg': traceback.format_exc()}

        return {'status': True, 'msg': key}

    def get_som_viz_data(self):
        if self.nodes is None or self.links is None:
            return {'status': False, 'msg': 'Not available'}

        return {'status': True, 'msg': 'Ok', 'obj': {'links': self.links, 'nodes': self.nodes}}
