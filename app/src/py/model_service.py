import json
import os
import re
import numpy as np
import webview
from .model_compiler import parse_dict as do_compile
from pysom.graph import GraphCompileError
import traceback


# Model training service
class ModelService:
    def __init__(self, ds):
        self.ds = ds
        self.input_key = None
        self.graph = None
        
        self.model_export = None
        self.model_output = None

    def set_input(self, key):
        self.input_key = key
        return {'status': True, 'msg': key}

    def update_model(self, mod):
        self.model_export = mod

    def compile(self):
        if self.model_export is None:
            return {'status': False, 'msg': 'Missing model data?'}
        g = None
        try:
            g = do_compile(self.model_export, self.ds)
        except GraphCompileError as e:
            return {'status': False, 'msg': f"{str(e)}"}
        except Exception as e:
            return {'status': False, 'msg': f"{str(e)} \n {traceback.format_exc()}"}

        self.graph = g

        return {'status': True, 'msg': "good"}

    def train(self):
        if self.graph is None:
            return {'status': False, 'msg': 'Model not present.'}

        if self.input_key is None:
            return {'status': False, 'msg': 'Input data not set.'}
        
        data = self.ds.get_object_data(self.input_key)
        # return {'status': False, 'msg': data}
        if data is None:
            return {'status': False, 'msg': 'Input data does not exist.'}

        try:
            self.graph.set_input(data)
            self.graph.set_param("training", True)
            self.model_output = self.graph.get_output()
        except GraphCompileError as e:
            return {'status': False, 'msg': f"{str(e)}"}
        except Exception:
            return {'status': False, 'msg': f"Error ocurred during evaluations: {traceback.format_exc()}"}

        return {'status': True, 'msg': 'Training finished.'}

    def export_output(self, name, opaque):
        if self.model_output is None:
            return {'status': False, 'msg': 'Output data not avaliable. Train or Run the model first to generate data.'}
        
        if not opaque and not isinstance(self.model_output, np.ndarray):
            return {'status': False, 'msg': 'Output data format is not supported for export. Please check the output connection of your graph.'}

        key = self.ds.save_object_data('opaque' if opaque else 'matrix', name, self.model_output)
        return {'status': True, 'msg': key}

    def export_node(self, name, id):
        if self.model_output is None:
            return {'status': False, 'msg': 'Output data not avaliable. Train or Run the model first to generate data.'}
        
        if self.graph is None:
            return {'status': False, 'msg': 'Model not present.'}

        node = self.graph.find_node(int(id))

        if node is None:
            return {'status': False, 'msg': 'Requested Node does not present.'}
        
        key = self.ds.save_object_data('opaque', name, node)
        return {'status': True, 'msg': key}



    def debug_output_str(self):
        if self.model_output is None:
            return {'status': False, 'msg': 'Output data not avaliable. Train or Run the model first to generate data.'}
        
        return {'status': True, 'msg': str(self.model_output)}
