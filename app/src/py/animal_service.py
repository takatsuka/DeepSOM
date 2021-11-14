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


class AnimalService:
    def __init__(self, ds):
        self.ds = ds
        self.input_key = None
        self.som = None
        self.cal = None

        self.animals = None

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

        animal_grid = [[[] for _ in range(self.som.size)]
                       for _ in range(self.som.size)]

        try:
            labels = self.cal.get_output(slot=1).items()
            for k, v in labels:
                animal_grid[k[0]][k[1]] = list(v.keys())

        except Exception as _:
            return {'status': False, 'msg': traceback.format_exc()}

        self.animals = animal_grid
        return {'status': True, 'msg': ""}

    def get_animal_data(self):
        if self.animals is None:
            return {'status': False, 'msg': 'Not available'}

        return {'status': True, 'msg': 'Ok', 'obj': self.animals}
