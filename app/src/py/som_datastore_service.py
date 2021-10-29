import json
import os
import webview


class SOMDatastoreService:
    def __init__(self):
        self.data_instances = {}

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
        descriptor = self.validate_unique_descriptor(os.path.basename(filename))
        
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
        descriptor = self.validate_unique_descriptor(os.path.basename(filename))
        
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
        descriptor = self.validate_unique_descriptor(os.path.basename(filename))

        self.data_instances[descriptor] = instance
        return descriptor

    # Returns true if the descriptor exists as the name of an open data instance; false if not
    def has_instance_by_descriptor(self, descriptor):
        return descriptor in self.data_instances.keys

    # Returns all open data instances
    def get_all_instances(self):
        return self.data_instances

    # Closes all open data instances
    def close_all_instances(self):
        self.data_instances = {}

    # Allows insertion of custom data instance
    def open_custom_instance_with_descriptor(self, descriptor, instance):
        # Check if descriptor string already exists in data instances
        descriptor = self.validate_unique_descriptor(descriptor)
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

    # Helper function to ensure unique string descriptors for all data instances
    def validate_unique_descriptor(self, descriptor):
        while descriptor in self.data_instances.keys:
            descriptor += 'copy'
        return descriptor
