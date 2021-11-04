import json
import os
import re
import webview


class SOMDatastoreService:
    data_instances = {}

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

    # Imports CSV data from a file upload point and returns string descriptor
    def open_csv_file_instance(self):
        # Get CSV file from application file upload dialog
        filename = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG)

        # Check if CSV file is valid
        if filename == None:
            return None
        if len(filename) < 1:
            return None
        filename = filename[0]
        if not os.path.exists(filename):
            return None

        # Open CSV file and store as new instance
        lines = open(filename).readlines()
        lines = [line.strip().split(",") for line in lines]

        # Check if descriptor string already exists in data instances
        descriptor = self.ensure_unique(
            os.path.basename(filename))

        self.data_instances[descriptor] = lines
        return descriptor

    # Imports JSON data from a file upload point and returns string descriptor
    def open_json_file_instance(self):
        # Get JSON file
        filename = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG)

        # Check if JSON file is valid
        if filename == None:
            return None
        if len(filename) < 1:
            return None
        filename = filename[0]
        if not os.path.exists(filename):
            return None

        # Open and process JSON file
        fields = json.loads(open(filename).read())

        # Check if descriptor string already exists in data instances
        descriptor = self.ensure_unique(
            os.path.basename(filename))

        self.data_instances[descriptor] = fields
        return descriptor

    # Saves JSON data from the drag and drop editor
    def save_json_instance(self, graph):
        # Get save point
        filename = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG)
        if filename == None:
            return None

        # Write JSON graph configuration to path
        instance = json.dumps(graph)
        open(filename, 'w').write(instance)

        # Check if descriptor string already exists in data instances
        descriptor = self.ensure_unique(
            os.path.basename(filename))

        self.data_instances[descriptor] = instance
        return descriptor

    def load_som_container(self):
        descriptor = self.open_json_file_instance()
        if descriptor == None:
            return None

        fields = self.data_instances[descriptor]
        label = fields['som']
        data_files = fields['data_files']
        files = []

        for f in data_files:
            name = self.ensure_unique(f['filename'])
            self.data_instances[name] = f['data']
            files.append(name)

        som = {
            "label": label,
            "childNodes": files
        }

        return som

    def save_som_container(self, som):
        # Get save point
        filename = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG)
        if filename == None:
            return False

        files = som["childNodes"]
        files_with_data = []
        for f in files:
            files_with_data.append({
                "filename": f['label'],
                "data": self.data_instances[f['label']]
            })

        container = {
            "som": os.path.basename(filename),
            "data_files": files_with_data,
        }

        container = json.dumps(container)
        open(filename, 'w').write(container)
        return True

    def create_som_container(self, descriptor):
        descriptor = self.ensure_unique(descriptor)
        self.data_instances[descriptor] = []
        return descriptor

    def add_file_to_som(self, som_descriptor, file_descriptor):
        if som_descriptor not in self.data_instances.keys():
            return False
        self.data_instances[som_descriptor].append(file_descriptor)
        return True

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
