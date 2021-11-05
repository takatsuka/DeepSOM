import json
import os
import re
import numpy as np
import webview
from .model_compiler import parse_dict as do_compile

# Model training service
class ModelService:
    def __init__(self, ds):
        self.ds = ds
        self.input_key = None
        self.graph = None
        
        self.model_export = None

    def set_input(self, key):
        self.input_key = key
        return {'status': True, 'msg': key}

    def update_model(self, mod):
        self.model_export = mod

    def compile(self):
        if self.model_export == None:
            return {'status': False, 'msg': 'Missing model data?'}
        g = None
        try:
            g = do_compile(self.model_export)
        except Exception as e:
            return {'status': False, 'msg': str(e)}

        self.graph = g

        return {'status': True, 'msg': "good"}


    def train(self):
        if self.graph == None:
            return {'status': False, 'msg': 'Model not present.'}

        if self.input_key == None:
            return {'status': False, 'msg': 'Input data not set.'}
        

        data = self.ds.object_data(self.input_key)
        self.graph.set_input(data)


        return {'status': True, 'msg': 'Training finished.'}

