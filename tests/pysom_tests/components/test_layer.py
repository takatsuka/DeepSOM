from pysom.components.som import Som
from pysom.components.layer import Layer


def test_layer_init_inlen():
    layer = Layer(9)
    assert hasattr(layer, "inlen")
    assert layer.get_in_len() == 9


def test_layer_init_inlen_na():
    layer = Layer(0)
    assert not hasattr(layer, "inlen")


"""
class Layer:

    def __init__(self, inlen):
        Constructor. The Layer class is on layer of a Deep SOM. It stores
        a sequence of SOMs, as well as the length of input and output vectors
        for the layer. Does not store SOMs directly, instead uses a SOM
        container class to hold each SOM along with its associated transition
        function. Output vector length is inferred by summing the output
        lengths of all the attached SOM containers.

        Args:
            inlen (int): The length that an input vector to this entire layer
                must be.

        Returns:
            class Layer: The new object.
        
        self.soms = []
        self.set_in_len(inlen)
        self.outlen = 0

    def get_layer_size(self):
        return len(self.soms)

    def get_in_len(self):
        return self.inlen

    def set_in_len(self, inlen):
        Sets the size of the vector this layer takes as input for all its
        SOMs. If input is not a positive integer, nothing happens.

        Args:
            inlen (int): The new length for input vectors to this layer.

        Returns:
            None
        

        if isinstance(inlen, int) and inlen > 0:
            self.inlen = inlen

    def get_out_len(self):
        return self.outlen

    def add_som_container(self, som_container):
        Adds a given SOM container to the end of the layer.
        Updates expected out length accordingly. Input length is not changed;
        if necessary, this must be done manually.

        Args:
            som_container (class SomContainer): The new SOM container to add.

        Returns:
            None
        
        self.soms.append(som_container)
        self.outlen += som_container.get_out_len()

    def insert_som_container(self, idx, som_container):
        Adds a given SOM container to the layer, but at the index position
        specified. The new SOM container now has the given index, and all
        old containers at positions greater than or equal to that index are
        moved up one place. If given index is greater than length of layer,
        the SOM is appended to the end.

        Args:
            idx (int): The index at which to place the new SOM container.
            som_container (class SomContainer): The new SOM container to add.

        Returns:
            None
        
        if idx >= len(self.soms):
            self.soms.append(som_container)
        else:
            self.soms.insert(idx, som_container)
            self.outlen += som_container.get_out_len()

    def pop_som_container(self, idx):
        Removes the SOM container at the specified index from the layer.
        All subsequent SOMs are shifted down one place. Returns the SOM
        container for convenience.

        Args:
            idx (int): The index at which to remove a SOM from the layer. Must
                be within the layer's index range. Use get_layer_size() to
                check this.

        Returns:
            class SomContainer: The SOM container removed from the layer.
        

        return self.soms.pop(idx)

    def get_som_container(self, idx):
        Returns the SOM container at specified position in the layer.

        Args:
            idx (int): The index of the desired SOM in the layer. Must be
                non-negative, and within the index range of the layer's list
                of SOMs. Use get_layer_size() to find this.

        Returns:
            class SomContainer: The desired SOM container.
        

        return self.soms[idx]
"""