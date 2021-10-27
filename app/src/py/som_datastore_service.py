import webview

class SOMDatastoreService:
    def __init__(self):
        self.cache = {}

    def open_csv_file(self):
        pass

    def open_json_file(self):
        pass

    # Calculate which epoch the percentage would result in
    # and return theose weights
    def get_som_weights_by_training_percentage(self, percentage):
        pass

    # Return dataset values
    def get_dataset(self):
        pass

    # Return graph output values
    def get_graph_output(self):
        pass

    def get_cache_data(self, descriptor):
        if descriptor in self.cache.keys:
            return self.cache[descriptor]
        return None

    # Return SOM dimensions
    def store_path_to_weights(self, path):
        pass

    # Return dataset dimensions
    def store_path_to_dataset(self, path):
        pass

    def store_cache_data_with_descriptor(self, descriptor, data):
        self.cache[descriptor] = data
        return True
