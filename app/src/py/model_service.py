import json
import os
import re
import numpy as np
import webview
from .model_compiler import parse_dict as do_compile

# Model training service
class ModelService:
    def __init__(self, ds):
        self.input_key = None
        self.graph = None
        
        self.model_export = None

    def set_input(self, key):
        self.input_key = key

    def update_model(self, mod):
        self.model_export = mod

    def compile():
        if self.graph == None:
            raise Exception("Model not compiled")
        


        return True

