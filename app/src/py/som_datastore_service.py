import json
import numpy as np

class SOMDatastoreService:
    def __init__(self):
        self.cache = {}
        self.dataset_path = None
        self.weights_path = None
        self.dataset_points = None
        self.weights_points = None

    # Calculate which epoch the percentage would result in
    # and return theose weights
    def get_som_weights_by_training_percentage(self, percentage):
        if not self.weights_points:
            return None
        n_weights = len(self.weights_points)
        return_n = int(n_weights * percentage)
        return self.weights_points[return_n]

    # Return dataset values
    def get_dataset(self):
        return self.dataset_points

    def get_cache_data(self, descriptor):
        if descriptor in self.cache.keys:
            return self.cache[descriptor]
        return None

    # Return SOM dimensions
    def store_path_to_weights(self, path):
        self.weights_path = path
        fields = json.loads(open(path).read())
        self.weights_points = fields["weights"]
        return fields["w"], fields["h"]

    # Return dataset dimensions
    def store_path_to_dataset(self, path):
        self.dataset_path = path
        data = open(path).readlines()
        self.dataset_points = [line.strip().split(",") for line in data]
        np_data = np.array(data)
        return np_data.shape

    def store_cache_data_with_descriptor(self, descriptor, data):
        self.cache[descriptor] = data
        return descriptor

    # Return graph output values
    def get_graph_output(self):
        pass

datastore = SOMDatastoreService()
datastore.store_path_to_weights("../../../playgrounds/numba_npsom_perf_analysis/out.json")
