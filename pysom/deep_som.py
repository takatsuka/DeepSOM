import numpy as np
from pysom.components.layer import Layer


class DeepSom:

    def __init__(self, indim):
        """Constructor. Initialises the Deep SOM with a fixed size input that
        the first layer of SOMs will draw from. This input size can be
        modified later if necessary.

        Args:
            indim (int): The length that an input vector to the first layer
                should be.

        Returns:
            class DeepSom: The new object.
        """

        self.layers = []
        self.layers.append(Layer.Layer(indim))

    def get_layer_count(self):
        """Returns the number of layers in the Deep SOM.

        Args:
            None

        Returns:
            int: Number of layers in the Deep SOM.
        """

        return len(self.layers)

    def get_som_count(self):
        """Returns the total number of SOMs in all the layers of the Deep SOM.

        Args:
            None

        Returns:
            int: Total number of SOMs in the Deep SOM.
        """

        som_count = 0
        for layer in self.layers:
            som_count += layer.get_layer_size()
        return som_count

    def set_input(self, indim):
        """Change the input size to the Deep SOM. This actually changes the
        input size of the first layer of the Deep SOM. This method does not
        perform any sanity checking, and changing input size of the first
        layer may malform it if SOMs have already been added. Use the
        check_structure() method to certify that Deep SOM structure is
        functional.

        Args:
            indim (int): The new input size for the Deep SOM. If indim is
                not a positive integer, nothing happens.

        Returns:
            None
        """

        self.layers[0].set_in_len(indim)

    def add_layer(self):
        """Adds a new layer to the end of the Deep SOM. Input vector size is
        determined by the output size of the previous layer.

        Args:
            None

        Returns:
            None
        """

        new_indim = self.layers[-1].get_out_len()
        self.layers.append(Layer.Layer(new_indim))

    def insert_layer(self, idx):
        """Inserts a new layer at the specified index in the SOM's layer list.
        Input size of the new layer is determined by the output size of the
        previous layer. This method does not perform any checks between the
        output size of the new layer and input size of the subsequent layer;
        be careful to avoid malforming the Deep SOM, and use check_structure().

        Args:
            idx (int): Position in the layer list that the new layer should be
                created. Starts from 0 at the front. Must be non-negative. If
                idx is beyond the length of the layer list, the new layer will
                be appended to the end.

        Returns:
            None
        """

        if idx >= len(self.layers):
            self.append_layer()
        else:
            new_indim = self.layers[idx].get_in_len()
            self.layers.insert(Layer.Layer(new_indim))

    def pop_layer(self, idx):
        """Removes and returns the layer at the specified index in the SOM's
        layer list. This method does not perform any sanity checks on the new
        structure of the Deep SOM. Be careful to avoid malforming the Deep
        SOM, and use check_structure(). This method cannot be used to delete
        every layer from the SOM; if only one layer remains, nothing will be
        removed and None will be returned.

        Args:
            idx (int): Index of the layer to be removed. Starts from 0 at the
                front of the Deep SOM. Must be withing the bounds of the layer
                list; use get_layer
        """

        if len(self.layers) > 1:
            return self.layers.pop(idx)
        return None

    def get_layer(self, idx):
        """Returns a specific layer of the SOM.

        Args:
            idx (int): The index of the desired SOM layer. Starts from 0
                at the beginning of the SOM. Must be non-negative.

        Returns:
            class Layer: The requested Layer of the SOM.
        """

        return self.layers[idx]

    def check_structure(self, output="crash"):
        """Checks that the structure of the whole Deep SOM makes sense; that
        each layer's output size matches the next layer's input size and that
        every SOM takes as input only indices that exist in that layer's input
        vector.
        Error output can be customised via the 'output' parameter.

        Args:
            output (str): Can take value 'crash', 'print', or ''. The method
                always returns a list of strings reporting errors found, but
                if output is set to 'print' it will also print the errors to
                stdout, and if output is set to 'crash' an exception will be
                raised reporting the errors. There will still be no printout/
                exception if no errors are found.

        Returns:
            list: A list of strings, each string reporting one error that was
                found in the structure of the SOM. An empty list indicates no
                errors are present.
        """

        error_string = ""

        for i in range(len(self.layers) - 1):
            curr_layer = self.layers[i]
            next_layer = self.layers[i + 1]
            outlen = curr_layer.get_out_len()
            inlen = next_layer.get_in_len()
            if outlen != inlen:
                error_string += "Layer index {} outputs vector length {}, but\
                layer index {} expects input of vector length {}\n\
                ".format(i, outlen, i + 1, inlen)

        for i in range(len(self.layers)):
            curr_layer = self.layers[i]
            inlen = curr_layer.get_in_len()
            for j in range(curr_layer.get_layer_size()):
                curr_som = curr_layer.get_som_container(j)
                for idx in curr_som.get_in_set():
                    if idx < 0 or idx >= inlen:
                        error_string += "SOM index {} of Layer index {} takes\
                        input from index {}, but the layer only expects an\
                        input vector of length {}\n".format(j, i, idx, inlen)

        if output == "crash":
            raise AttributeError(error_string)
        elif output == "print":
            print(error_string)
        return error_string

    def train_dsom(self, example, epoch):
        """Using the given example, trains the Deep SOM (and thus every SOM
        inside it), according to the specified epoch.

        Args:
            example (np.ndarray): The data point to train on. Data point must
                be of shape (indim,) where indim is the input size for the
                first layer of the Deep SOM.
            epoch (int): The current epoch of training. Must be a non-negative
                integer (zero is fine).

        Returns:
            np.ndarray: The final output of the Deep SOM for this example,
                as it would have been before training. Will be of shape
                (outdim,) where outdim is the size of the output for the last
                layer of the SOM.
        """

        in_vector = example
        for i in range(len(self.layers)):
            layer = self.layers[i]
            out_vector = np.zeros(layer.get_out_len())
            out_idx = 0

            # Lots of parallelism potential here; each SOM's training is
            # independent of the others
            for j in range(layer.get_layer_size()):
                som_container = layer.get_som_container(j)
                som_in = som_container.make_input(in_vector)
                som_out = som_container.train_som(som_in, epoch)
                for k in range(len(som_out)):
                    out_vector[out_idx] = som_out[k]
                    out_idx += 1

            in_vector = out_vector

        return out_vector

    def activate_dsom(self, example):
        """Finds the output of the Deep SOM for the given example without
        performing any training.

        Args:
            example (np.ndarray): The data point to feed into the Deep SOM.
                Data point must be of shape (indim,) where indim is the input
                size for the first layer of the Deep SOM.

        Returns:
            np.ndarray: The final output of the Deep SOM for this example.
                Will be of shape (outdim,) where outdim is the size of the
                output for the last layer of the SOM.
        """

        in_vector = example
        for i in range(len(self.layers)):
            layer = self.layers[i]
            out_vector = np.zeros(layer.get_out_len())
            out_idx = 0

            # Lots of parallelism potential here; each SOM's activation is
            # independent of the others
            for j in range(layer.get_layer_size()):
                som_container = layer.get_som_container(j)
                som_in = som_container.make_input(in_vector)
                som_out = som_container.activate_som(som_in)
                for k in range(len(som_out)):
                    out_vector[out_idx] = som_out[k]
                    out_idx += 1

            in_vector = out_vector

        return out_vector
