from typing import Type
from .node import Node
from .nodes.input_container import InputContainer


class Graph:
    """
    Base class of the API library representing the graph of the deep SOM model.

    Holds all the methods necessary for constructing the graphs. May
    construct vertices and join vertices.

    Attributes:
        nodes (dict): the map of all Node objects indexed by their
                      automatically assigned unique integer ID
    """

    uid = 2

    def __init__(self):
        """
        Constructor of the Graph class representing the deep SOM model.

        Creates the starting input node of ID 0 and final output node of ID 0
        upon instantiation. Training flag is initially set to false and can
        be toggled using the training methods.
        """
        self.start = 0
        self.end = 1
        self.is_training = False

        self.nodes = {
            0: InputContainer(self.start, self),
            1: Node(self.end, self)
        }

    def _create_node(self, node_type: Type[Node] = None,
                     props: dict = {}) -> Node:
        if node_type is None:
            node = Node(Graph.uid)
        else:
            node = node_type(Graph.uid, self, **props)

        Graph.uid += 1

        return node

    def create(self, node_type: Type[Node] = None, props: dict = {}) -> int:  
        """
        Helper function to create a vertex in the graph.

        A node type may be specified to define custom behaviour of the graph
        node. If set to None, then it will default to the basic Node class.
        Returns a unique integer ID of the newly created node, which may be
        later used to retrieve the actual Node object.

        Args:
            node_type (Type[Node], optional): the class of the Node to be
                                              created as defined in
                                              graph/nodetypes. Defaults to
                                              None, which creates and returns
                                              a parent Node instance.
            props (dict, optional): property parameters that may be unpacked
                                    and interpreted by the constructor of the
                                    Node. Defaults to None.

        Returns:
            int: the automatically assigned unique integer ID of the node
        """
        node = self._create_node(node_type=node_type, props=props)
        return self._add_node(node)

    def get_nodes(self) -> dict:
        """
        Helper function to return the nodes in the graph.
        
        Returns the map of all nodes currently stored and indexed by the
        current Graph instance by their unique integer node ID.

        Returns:
            dict: the map of nodes indexed by their ID. Will not be empty.
        """
        return self.nodes

    def _add_node(self, node: Node) -> int:
        self.nodes[node.get_id()] = node
        return node.get_id()

    def find_node(self, uid: int) -> Node:
        """
        Helper function to retrieve a specific Node object in the graph.

        Returns the Node object matching the provided unique integer ID if
        possible. If there is no such match, then None is returned.

        Args:
            uid (int): the unique integer ID search key for retrieving a Node
                       object stored by the current Graph instance.

        Returns:
            Node: the matching Node object with an ID matching the provided
                  uid. Will return None if no suitable match is found.
        """
        for node in self.nodes.values():
            if node.get_id() == uid:
                return node
        return None

    def connect(self, uid_in: int, uid_out: int, slot: int) -> bool:
        """
        Edge creation function to connect two Node objects in the graph.

        Also triggers the bookkeeping required in the Node class in terms
        of tracking of incoming and outgoing Nodes. No explicit edge object
        will be stored in the Graph nor the Node instances.

        Args:
            uid_in (int): the unique integer ID of the node accepting the
                          directed edge connection. May not be equal to
                          uid_out.
            uid_out (int): the unique integer ID of the node outputting data
                           along the directed edge connection. May not be
                           equal to uid_in.
            slot (int): a slot ID representing the edge stored in the output
                        Node instance

        Returns:
            bool: True if an edge was able to be created. False if any node
                  could not be found, or if the provided IDs were equal
        """
        if uid_in == uid_out:
            return False

        input_node = self.find_node(uid_in)
        output_node = self.find_node(uid_out)

        if (input_node is None) or (output_node is None):
            return False

        return output_node.add_incoming_connection(input_node, slot)

    def set_input(self, data: object) -> None:
        """
        Setter function to set the input data of the starting Node.

        Effectively sets the data at Graph entry point to prepare for training.
        Does not check or sanitise the user input. Does not return any value
        back to the caller.

        Args:
            data (object): the data object to be passed and set as the data
                           input starting Node
        """
        self.find_node(self.start).data = data

    def get_output(self) -> object:
        """
        Getter function to extract the output data of the end Node.
        
        Effectively retrieves the trained data at the Graph exit point after
        an iteration of training.
        
        Returns:
            object: the resultant data object output from the Graph after 
                    training
        """
        return self.find_node(self.end).get_output(1)

    def train(self):
        """
        TODO

        Raises:
            RuntimeError: [description]

        Returns:
            [type]: [description]
        """
        if self.is_training:
            raise RuntimeError("Model is already training")

        # Initiate the training process here
        # TODO: Some actual training logic here

        # End of actual training logic

        self.is_training = True
        return self.is_training

    def halt_training(self):
        """
        TODO

        Raises:
            RuntimeError: [description]

        Returns:
            [type]: [description]
        """        
        
        if not self.is_training:
            raise RuntimeError("Cannot halt training when model is \
                not training")

        # TODO: Abort training logic here
        # May need to handle manual interrupts

        self.is_training = False
        return self.is_training

    """
    SORTING METHODS
    """


def example_graph():
    """
    Example Graph:
    ~~~~~~~~~~~~~~
                     *->n4->*
                    /        \\               Reserved Nodes       UID   Type
       start-->*-->n2-->n5--->n6--*-->end     ~~~~~~~~~~~~~~       ~~~   ~~~~~
                \\                /           * START (DummyNode)   0    input
                 *-->n3--->n7-->*             * END   (DummyNode)   1    output

    """
    pass


if __name__ == "__main__":
    g = Graph()

    # Level 1
    # n2 = g.create(node_type=Node, data=1)
    # n3 = g.create(node_type=Node, data=1)

    # # Printing Example Graph
    # print(example_graph.__doc__)

    # print("TOP BRANCH (up to n6)")
    # print("========================")
    # print("Result of n2:", g.find_node(n2).evaluate(), end="\n\n")
    # print("Result of n4:", g.find_node(n4).evaluate(), end="\n\n")
    # print("Result of n5:", g.find_node(n5).evaluate(), end="\n\n")
    # print("Result of n6:", g.find_node(n6).evaluate(), end="\n\n")

    # print("BOTTOM BRANCH (up to n7)")
    # print("========================")
    # print("Result of n3:", g.find_node(n3).evaluate(), end="\n\n")
    # print("Result of n7:", g.find_node(n7).evaluate(), end="\n\n")

    # print("OVERALL (result of END)")
    # print("========================")
    # print("Result of END:", g.find_node(g.end).evaluate(), end="\n\n")
