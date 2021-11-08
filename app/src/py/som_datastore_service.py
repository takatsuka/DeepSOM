import json
import os
import re
import base64
import numpy as np
import webview


class SOMDatastoreService:
    def __init__(self):
        self.data_instances = {}
        self.ws_path = None
        self.ws_name = "lol"

        self.loaders = {
            "matrix": lambda x: np.array(x, dtype=np.float64),
            "model": lambda x: x
        }

        self.dumpers = {
            "matrix": lambda x: x.tolist(),
            "model": lambda x: x
        }

        self.importers = {
            "matrix": lambda x: np.frombuffer(base64.b64decode(x[2]), dtype=x[1]).reshape(x[0]),
            "model": lambda x: x
        }

        self.exporters = {
            "matrix": lambda x: [x.shape, x.dtype.str, base64.b64encode(x).decode('ascii')],
            "model": lambda x: x
        }

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
        datastr = [l.strip().split(',') for l in open(filename).readlines()]
        datalist = [[c for c in e] for e in datastr]
        data = None

        parsers = [
            # We like float64, so priorities that.
            lambda x: np.array(x, dtype=np.float64),
            lambda x: np.array(x)
        ]

        # Try each parser in order.
        for p in parsers:
            try:
                data = p(datalist)
            except:
                pass

            if not data is None:
                break

        if data is None:
            return None

        # Check if descriptor string already exists in data instances
        descriptor = self.ensure_unique(
            os.path.basename(filename)
        )

        self.data_instances[descriptor] = {'type': 'matrix', 'content': data}
        return descriptor

    # Imports Model data
    def import_json(self, type):
        # Get JSON file
        filename = self.open_file()
        if not filename:
            return None

        # Open and process JSON file
        fields = json.loads(open(filename).read())

        # Check if descriptor string already exists in data instances
        descriptor = self.ensure_unique(
            os.path.basename(filename))

        self.data_instances[descriptor] = {'type': type, 'content': fields}
        return descriptor

    def save_json(self, key, type, obj):
        des = self.ensure_unique(key)
        self.data_instances[des] = {'type': type, 'content': obj}

    def save_object(self, key, type, object, replace):
        des = key if replace else self.ensure_unique(key)
        if type not in self.loaders:
            return None

        obj = self.loaders[type](object)
        self.data_instances[des] = {'type': type, 'content': obj}
        return des

    def get_object(self, key):
        if key not in self.data_instances:
            return None

        item = self.data_instances[key]
        type = item['type']
        if type not in self.dumpers:
            return None

        return self.dumpers[type](item['content'])

    # Fetch list of object keys with given type
    def fetch_objects(self, type):
        if type == '':
            return self.data_instances.keys()
        return [k for k, v in self.data_instances.items() if v['type'] == type]

    def remove_object(self, key):
        if key not in self.data_instances:
            return
        self.data_instances.pop(key)

    def rename_object(self, old_key, new_key):
        if old_key == new_key:
            return {"status": True, "msg": new_key}

        if old_key not in self.data_instances:
            return {"status": False, "msg": "Object does not exist."}

        if new_key in self.data_instances:
            return {"status": False, "msg": "New key already exist."}

        if len(new_key) < 1:
            return {"status": False, "msg": "Gotcha hacker."}

        new_key = self.ensure_unique(new_key)
        value = self.data_instances.pop(old_key)
        self.data_instances[new_key] = value
        return {"status": True, "msg": new_key}

    def fetch_object_repr(self, key):
        if key not in self.data_instances:
            return {"status": False, "msg": "Object does not exist."}
        obj = self.data_instances[key]['content']
        return {"status": True, "type": str(obj.__class__), "repr": repr(obj), "msg": ""}

    def current_workspace_name(self):
        return self.ws_name

    def load_workspace(self):
        loaders = self.importers
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

            loaded = None
            try:
                loaded = loaders[t](v['content'])
            except:
                # TODO: report error?
                pass

            if loaded is None:
                continue

            self.data_instances[name] = {
                'type': t, 'content': loaded
            }

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
        dumpers = self.exporters

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
            # This will also skip temp opaque data as they were never mean to be saved
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

    # Used by other Python services to access pointer to data object
    def get_object_data(self, key):
        if key not in self.data_instances:
            return None
        item = self.data_instances[key]
        return item['content']

    # Used by other Python services to save data object
    def save_object_data(self, type, key, data):
        des = self.ensure_unique(key)
        self.data_instances[des] = {'type': type, 'content': data}

        return des

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
