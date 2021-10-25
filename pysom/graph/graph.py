from graph.node import Node
from graph.nodes.input_container import InputContainer


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
            0: InputContainer(self.start),
            1: Node(self.end)
        }

    def _create_node(self, node_type=None, props={}) -> Node:
        if node_type is None:
            node = Node(Graph.uid)
        else:
            node = node_type(Graph.uid, **props)

        Graph.uid += 1

        return node

    def create(self, node_type=None, props={}) -> int:
        """
        Helper function to create a vertex in the graph.

        A node type may be specified to define custom behaviour of the graph
        node. If set to None, then it will default to the basic Node class.
        Returns a unique integer ID of the newly created node, which may be
        later used to retrieve the actual Node object.

        Args:
            node_type (Node, optional): the class of the Node to be created as
                                        defined in graph/nodetypes. Defaults
                                        to None.
            props ([type], optional): [description]. Defaults to None.

        Returns:
            int: [description]
        """
        node = self._create_node(node_type=node_type, props=props)
        return self._add_node(node)

    def get_nodes(self) -> dict:
        return self.nodes

    def _add_node(self, node: Node) -> int:
        self.nodes[node.get_id()] = node
        return node.get_id()

    def find_node(self, uid: int) -> Node:
        for node in self.nodes.values():
            if node.get_id() == uid:
                return node
        return None

    def connect(self, node1: int, node2: int, slot: int) -> bool:
        input_node = self.find_node(node1)
        output_node = self.find_node(node2)

        if (input_node is None) or (output_node is None):
            return False

        return output_node.add_incoming_connection(input_node, slot)

    def set_input(self, data):
        self.find_node(self.start).data = data

    def get_output(self):
        return self.find_node(self.end).get_output(1)

    def train(self):
        if self.is_training:
            raise RuntimeError("Model is already training")

        # Initiate the training process here
        # TODO: Some actual training logic here

        # End of actual training logic

        self.is_training = True
        return self.is_training

    def halt_training(self):
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
