import json
import numpy as np
import webview
import os


class SOMScatterviewService:
    def __init__(self, ds):
        self.cache = {
            "DATASET_PATH": None,
            "DATASET": None,
            "AXES": None,
            "WEIGHTS": None,
            "WEIGHTS_NODES": None,
            "WEIGHTS_EDGES": None
        }
        self.datastore = ds

    def set_datastore(self, datastore):
        self.datastore = datastore

    # Update the current weights being shown according to epoch
    def update_scatter_som_weights_by_training_epoch(self, epoch):
        if not self.cache['WEIGHTS']:
            return None

        weights = self.cache["WEIGHTS"]["weightspb"][str(epoch)]
        width = self.cache["WEIGHTS"]["w"]
        height = self.cache["WEIGHTS"]["h"]
        nodes = []
        edges = []

        for point in weights:
            nodes.append({"x": float(point[0]), "y": float(point[1]), "z": float(point[2])})

        for i in range(len(weights)):
            center = nodes[i]
            if i % width == width - 1:
                if i != len(weights) - 1:
                    down = nodes[i + width]
                    edges.append([center, down])
            elif int(i / width) == height - 1:
                right = nodes[i + 1]
                edges.append([center, right])
            else:
                down = nodes[i + width]
                right = nodes[i + 1]
                edges.append([center, down])
                edges.append([center, right])
        
        self.cache['WEIGHTS_NODES'] = nodes
        self.cache['WEIGHTS_EDGES'] = edges

    def update_scatter_dataset(self, data):
        scatter = []
        counter = 0

        # Iterate through each line of coordinates
        for i in range(len(data)):
            # Append coordinate instance to dataset list
            scatter.append({"x": float(data[i][0]), "y": float(data[i][1]), "z": float(data[i][2]), "id": 'point_' + str(counter)})

        self.cache["DATASET"] = scatter

    def get_scatter_som_weights(self):
        return [self.cache["WEIGHTS_NODES"], self.cache["WEIGHTS_EDGES"]]
    
    # Return dataset points and axes
    def get_scatter_dataset(self):
        return self.cache["DATASET"]

    # Return SOM dimensions
    def upload_scatter_weights_from_json_file(self):
        # Get weights json file
        filename = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG)

        # Validate json file
        if filename == None:
            return None

        if len(filename) < 1:
            return None
        filename = filename[0]
        if not os.path.exists(filename):
            return None

        # Open and process json file
        fields = json.loads(open(filename).read())
        self.cache['WEIGHTS'] = fields
        self.update_scatter_som_weights_by_training_epoch(0)
        return len(fields['weights'])

    # (TODO) Function can be called from backend API that directly uploads weights from training
    def upload_scatter_weights_from_api(self, path):
        fields = json.loads(open(path).read())
        self.cache['WEIGHTS'] = fields
        self.update_scatter_som_weights_by_training_epoch(0)
        return len(fields["weightspb"])

    # Return dataset dimensions
    def upload_scatter_dataset(self):
        # Get dataset file from application file upload dialog
        filename = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG)

        # Check if selected file is valid
        if filename == None:
            return None
        if len(filename) < 1:
            return None
        filename = filename[0]
        if not os.path.exists(filename):
            return None

        # Open dataset file and store/update record
        self.cache["DATASET_PATH"] = os.path.abspath(filename)
        lines = open(filename).readlines()
        lines = [line.strip().split(",") for line in lines]
        self.update_scatter_dataset(lines)
        return os.path.basename(filename)

    # Clean up function
    def resetDatastore(self):
        self.cache = {
            "DATASET_PATH": None,
            "DATASET": None,
            "AXES": None,
            "WEIGHTS": None,
            "WEIGHTS_NODES": None,
            "WEIGHTS_EDGES": None
        }
