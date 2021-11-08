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

    def rect_links(self):
        dim = self.som.size
        w = self.som.get_weights()
        links = []
        for y in range(dim):
            for x in range(dim - 1):
                row = y * dim
                l = {'source': row + x, 'target': row + x + 1, 'value': np.linalg.norm(w[row + x] - w[row + x + 1]) * 100}
                links.append(l)

        for y in range(dim - 1):
            for x in range(dim):
                row = y * dim
                l = {'source': row + x, 'target': row + x + dim, 'value': np.linalg.norm(w[row + x] - w[row + x + dim]) * 100}
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
            labelmap = None
            if not self.cal is None:
                labelmap = {k[0]*self.som.size + k[1] : v for k,v in self.cal.get_output(slot=1).items()}
            fmt = lambda x: ','.join([f'{i}' for i in x.keys()])
            self.nodes = [{'id': i, 'l': fmt(labelmap.get(i, Counter())) if labelmap else ""} for i in range(self.som.size ** 2)]
        except:
            return {'status': False, 'msg': traceback.format_exc()}
        

        return {'status': True, 'msg': key}

    def get_som_viz_data(self):
        if self.nodes is None or self.links is None:
            return {'status': False, 'msg': 'Not available'}
        
        return {'status': True, 'msg': 'Ok', 'obj': {'links': self.links, 'nodes': self.nodes}}


