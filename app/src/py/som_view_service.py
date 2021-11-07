import json
import os
import re
import numpy as np
import webview

from pysom.graph import GraphCompileError
from pysom.nodes.calibrate import Calibrate
from pysom.nodes.som import SOM
import traceback


# Model training service
class SomViewService:
    def __init__(self, ds):
        self.ds = ds
        self.input_key = None
        self.som = None

        self.links = None
        self.nodes = None

    def rect_links(self):
        dim = self.som.size
        links = []
        for y in range(dim):
            for x in range(dim - 1):
                row = y * dim
                l = {'source': row + x, 'target': row + x + 1, 'value': 10}
                links.append(l)

        for y in range(dim - 1):
            for x in range(dim):
                row = y * dim
                l = {'source': row + x, 'target': row + x + dim, 'value': 10}
                links.append(l)

    def set_input(self, key):
        self.input_key = key

        data = self.ds.get_object_data(self.input_key)
        if data is None:
            return {'status': False, 'msg': 'Input data does not exist.'}

        if not isinstance(data, SOM):
            return {'status': False, 'msg': 'Input data is not a SOM node.'}

        self.links = self.rect_links()
        self.nodes = list(range(self.som.size))

        return {'status': True, 'msg': key}

    def get_som_viz_data(self, mod):
        if self.nodes is None or self.links is None:
            return {'status': False, 'msg': 'Not available'}
        
        return {'status': True, 'msg': 'Ok', 'obj': {'links': self.links, 'nodes': self.nodes}}


