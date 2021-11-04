import json
import os
import re
import numpy as np
import webview


class SOMDatastoreService:
    def __init__(self):
        self.data_instances = {}
        self.ws_path = None
        self.ws_name = "lol"

    # Helper function to ensure unique string descriptors for all data instances
    def ensure_unique(self, k):

        # use `in` directly on dict will use O(1) hashmap look up.
        while k in self.data_instances:
            if re.fullmatch(r".*_\([\d]+\)", k):
                k = re.sub(r"_\([\d]+\)",
                           lambda g: f"_({int(g.group(0)[2: -1]) + 1})", k)
            else:
                k += "_(1)"
        return k

    def open_file(self):
        p = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG)

        if p == None:
            return None
        if len(p) < 1:
            return None
        p = p[0]
        if not os.path.exists(p):
            return None

        return p

    # Imports CSV data from a file upload point and returns string descriptor
    def import_data_from_csv(self):
        # Get CSV file from application file upload dialog
        filename = self.open_file()
        if not filename:
            return None

        # Open CSV file and parse to np.array
        # TODO: Shall we use Pandas instead?
        # Which will bring extra features for cleaning up data, but that's just extra.
        datastr = [l.strip().split(',') for l in open(filename).readlines()]
        data = np.array([[float(c) for c in e]
                        for e in datastr], dtype=np.float64)

        # Check if descriptor string already exists in data instances
        descriptor = self.ensure_unique(
            os.path.basename(filename)
        )

        self.data_instances[descriptor] = {'type': 'matrix', 'content': data}
        return descriptor

    # Imports Model data
    def import_model(self):
        # Get JSON file
        filename = self.open_file()
        if not filename:
            return None

        # Open and process JSON file
        fields = json.loads(open(filename).read())

        # Check if descriptor string already exists in data instances
        descriptor = self.ensure_unique(
            os.path.basename(filename))

        self.data_instances[descriptor] = {'type': 'model', 'content': fields}
        return descriptor

    def current_workspace_name(self):
        return self.ws_name

    def load_workspace(self):
        loaders = {
            "matrix": lambda x: np.array(x, dtype=np.float64),
            "model": lambda x: x
        }

        self.close_all_instances()

        filename = self.open_file()
        if not filename:
            return None
        fields = json.loads(open(filename).read())

        label = fields['workspace']
        data_files = fields['items']

        for k, v in data_files.items():
            name = self.ensure_unique(k)
            t = v['type']
            # Cry without saying.
            if t not in loaders:
                continue

            self.data_instances[name] = {
                'type': t, 'content': loaders[t](v['content'])}

        self.ws_path = filename
        self.ws_name = label

    def new_workspace(self):
        self.ws_path = None
        self.ws_name = "untitled"
        self.data_instances = {}

        return self.ws_name

    def save_current_workspace(self):
        self.save_workspace()

    def save_workspace_as(self):
        self.ws_path = None
        self.save_workspace()

    def save_workspace(self, filename=None):
        dumpers = {
            "matrix": lambda x: x.tolist(),
            "model": lambda x: x
        }

        if filename == None:
            filename = self.ws_path

        # Ask user if this is call without filename and the workspace is not initialized.
        if filename == None:
            filename = webview.windows[0].create_file_dialog(
                webview.SAVE_DIALOG)

        files_with_data = {}
        for k, v in self.data_instances.items():
            t = v['type']
            # Cry without saying.
            if t not in dumpers:
                continue

            files_with_data[k] = {'type': t,
                                  'content': dumpers[t](v['content'])}

        save_workspace = {
            "workspace": os.path.basename(filename),
            "items": files_with_data,
        }

        save_workspace = json.dumps(save_workspace)
        open(filename, 'w').write(save_workspace)

        self.ws_name = os.path.basename(filename)
        self.ws_path = filename

    def fetch_objects(self, type):
        if type == '':
            return self.data_instances.keys()
        return [k for k, v in self.data_instances.items() if v['type'] == type]

    # Returns true if the descriptor exists as the name of an open data instance; false if not

    def has_instance_by_descriptor(self, descriptor):
        return descriptor in self.data_instances.keys()

    # Returns all open data instances
    def get_all_instances(self):
        return self.data_instances

    # Closes all open data instances
    def close_all_instances(self):
        self.data_instances = {}

    def get_all_instance_descriptors(self):
        return list(self.data_instances.keys())

    # Allows insertion of custom data instance
    def open_custom_instance_with_descriptor(self, descriptor, instance):
        # Check if descriptor string already exists in data instances
        descriptor = self.ensure_unique(descriptor)
        self.data_instances[descriptor] = instance
        return descriptor

    # Returns data from the open data instance with the specified string descriptor
    def get_instance_by_descriptor(self, descriptor):
        if descriptor in self.data_instances.keys:
            return self.data_instances['descriptor']
        return None

    # Closes open data instance with the specified string descriptor
    def close_instance_with_descriptor(self, descriptor):
        obj = self.data_instances.pop(descriptor)
        return obj
