import json
import numpy as np

class SOMDatastoreService:
    def __init__(self):
        self.cache = {
            "SCATTER_DATASET_PATH": None,
            "SCATTER_DATASET": None,
            "SCATTER_AXES": None,
            "SCATTER_WEIGHTS": None,
            "SCATTER_WEIGHTS_NODES": None,
            "SCATTER_WEIGHTS_EDGES": None
        }

    # Calculate which epoch the percentage would result in
    # and update the current weights being shown
    def update_scatter_som_weights_by_training_percentage(self, percentage):
        if not self.cache['SCATTER_WEIGHTS']:
            return None

        n_weights = len(self.cache['SCATTER_WEIGHTS_NODES'])
        return_n = int(n_weights * percentage)

        weights = self.cache["SCATTER_WEIGHTS"]["weights"][return_n]
        width = self.cache["SCATTER_WEIGHTS"]["w"]
        height = self.cache["SCATTER_WEIGHTS"]["h"]
        nodes = []
        edges = []

        for point in weights:
            nodes.append({ x: point[0], y: point[1], z: point[2] })

        for i in range(len(weights)):
            center = nodes[i]
            if i % width == width - 1:
                if i != len(weights) - 1:
                    down = nodes[i+width]
                    edges.append([center, down])
            elif int(i / width) == height - 1:
                right = nodes[i+1]
                edges([center, right])
            else:
                down = nodes[i+width]
                right = nodes[i+1]
                edges.append([center, down])
                edges.append([center, right])
        
        self.cache['SCATTER_WEIGHTS_NODES'] = nodes
        self.cache['SCATTER_WEIGHTS_EDGES'] = edges

    def update_scatter_dataset(self, data):
        scatter = []
        xLine = []
        yLine = []
        zLine = []
        counter = 0 # Set all data points to id 0 for now since they should not differ in colour

        # Iterate through each line of coordinates
        for i in range(len(data)):
            # Append coordinate instance to dataset list
            scatter.append({ x: data[0], y: data[1], z: data[2], id: 'point_' + counter })

        # Define values for xyz axes 
        # (TODO): this does not have to redefined every time a new dataset is uploaded,
        #         should be extracted and called once
        for i in range(-1, 1.5, 0.5):
            xLine.append([-i, 1, -1])
            yLine.append([-1, i, -1])
            zLine.append([-1, 1, -i])

        self.cache["SCATTER_DATASET"] = scatter
        self.cache["SCATTER_AXES"] = [
            [xLine],
            [yLine],
            [zLine]
        ]

    def get_scatter_som_weight_nodes(self):
        return self.cache["SCATTER_WEIGHTS_NODES"]

    def get_scatter_som_weight_edges(self):
        return self.cache["SCATTER_WEIGHTS_EDGES"]
    
    # Return dataset points
    def get_scatter_dataset(self):
        return self.cache["SCATTER_DATASET"]

    # Return xyz axes
    def get_scatter_axes(self):
        return self.cache["SCATTER_AXES"]

    # Return SOM dimensions
    def upload_scatter_weights_from_json_file(self):
        # Get weights json file
        filename = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG)
        if filename == None:
            return None

        if len(filename) < 1:
            return None
        filename = filename[0]
        if not os.path.exists(filename):
            return None

        fields = json.loads(open(filename).read())
        return fields["w"], fields["h"]

    # (TODO) Function can be called from backend API that directly uploads weights from training
    def upload_scatter_weights_from_api(self, path):
        pass

    # Return dataset dimensions
    def upload_scatter_dataset(self, path):
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
        self.cache["SCATTER_DATASET_PATH"] = os.path.abspath(filename)
        lines = open(filename).readlines()
        lines = [line.strip().split(",") for line in lines]
        update_dataset(lines)
        return os.path.basename(filename)

    # To extract misc data with identificating string descriptor
    def get_cache_data(self, descriptor):
        if descriptor in self.cache.keys:
            return self.cache[descriptor]
        return None

    # To store misc data with string descriptor that might be needed
    def store_cache_data_with_descriptor(self, descriptor, data):
        self.cache[descriptor] = data
        return descriptor

    # (TODO) Return graph output values --> not sure how this is used yet
    def get_graph_output(self):
        pass

    # Clean up function
    def resetDatastore(self):
        self.cache = {
            "SCATTER_DATASET_PATH": None,
            "SCATTER_DATASET": None,
            "SCATTER_AXES": None,
            "SCATTER_WEIGHTS": None,
            "SCATTER_WEIGHTS_NODES": None,
            "SCATTER_WEIGHTS_EDGES": None
        }

