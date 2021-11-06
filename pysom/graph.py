from typing import Type

# from numpy.lib.function_base import select
from .node import Node
from .nodes.input_container import InputContainer

LOGLEVEL_NONE = 0
LOGLEVEL_ERROR = 1
LOGLEVEL_VERBOSE = 2
LOGLEVEL_ALLEXCEPTION = 3


class GraphCompileError(Exception):
    """
    Generic error class for any Graph-related issues.

    Args:
        Exception: base type of the Error
    """
    pass


class Graph:
    """
    Base class of the API library representing the graph of the deep SOM model.

    Holds all the methods necessary for constructing the graphs. May
    construct vertices and join vertices.

    Creates the starting input node of ID 0 and final output node of ID 0
    upon instantiation. Training flag is initially set to false and can
    be toggled using the training methods.

    Args:
        loglevel (int, optional): sets the verbosity for debugging. \
            May be LOGLEVEL_NONE, LOGLEVEL_ERROR, LOGLEVEL_VERBOSE in \
            increasing levels of verbosity. Defaults to LOGLEVEL_ERROR.

    Attributes:
        nodes (dict): the map of all Node objects indexed by their
                      automatically assigned unique integer ID
    """

    def __init__(self, loglevel: int = LOGLEVEL_ERROR):
        """
        Constructor of the Graph class representing the deep SOM model.

        Creates the starting input node of ID 0 and final output node of ID 1
        upon instantiation. Training flag is initially set to false and can
        be toggled using the training methods.

        Args:
            loglevel (int, optional): sets the verbosity for debugging. \
                May be LOGLEVEL_NONE, LOGLEVEL_ERROR, LOGLEVEL_VERBOSE. \
                Defaults to LOGLEVEL_ERROR.
        """
        self.uid = 3
        self.start = 1
        self.end = 2
        self.global_params = {
            "training": True
        }
        self.loglevel = loglevel

        self.nodes = {
            1: InputContainer(self.start, self),
            2: Node(self.end, self)
        }

    def _create_node(self, node_type: Type[Node] = None,
                     props: dict = {}) -> Node:
        if node_type is None:
            node = Node(self.uid, self)
        else:
            node = node_type(self.uid, self, **props)

        self.uid += 1

        return node

    def _log_ex(self, msg):
        if self.loglevel < LOGLEVEL_ALLEXCEPTION:
            print(msg)
            return

        raise GraphCompileError(msg)

    def create_with_id(self, id: int, node_type: Type[Node] = None,
                       props: dict = {}) -> int:
        """
        Helper function to create a vertex with defined id in the Graph.

        The conditions of create() also apply here, except the graph attempts
        to create a Node with an id matching the user provided id. Will not
        create the node if the provided id is already assigned to a node
        attached to the graph. Else, the node is created, and added to the
        graph and the same id is returned.

        Args:
            id (int): the id to be prescribed to the generated Node.
            node_type (Type[Node], optional): [description]. Defaults to None.
            props (dict, optional): property parameters that may be unpacked
                                    and interpreted by the constructor of the
                                    Node. Defaults to an empty dictionary.

        Returns:
            int: the integer id of the newly created Node. Will not be \
                 negative, or smaller than previously generated Node ids if
                 valid. If invalid, then a value of -1 is returned.
        """
        if id in self.nodes.keys():
            self._log_ex(f"Unable to create, node with {id} already exist.")
            return -1

        node = self._create_node(node_type=node_type, props=props)
        node.uid = id
        self.uid = max(node.uid + 1, self.uid)
        self._add_node(node)
        return node.uid

    def create(self, node_type: Type[Node] = None, props: dict = {}) -> int:
        """
        Helper function to create a vertex in the Graph.

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
                                    Node. Defaults to an empty dictionary.

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
            Node: the matching Node object with an ID matching the provided \
                  uid. Will return None if no suitable match is found.
        """
        if uid in self.nodes.keys():
            return self.nodes[uid]
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
            bool: True if an edge was able to be created. False if any node \
                  could not be found, or if the provided IDs were equal, or \
                  if the connection could not be established between the \
                  nodes.
        """
        if uid_in == uid_out:
            self._log_ex(f"Can not connect to node itself: {uid_in}")
            return False

        input_node = self.find_node(uid_in)
        output_node = self.find_node(uid_out)

        if (input_node is None) or (output_node is None):
            self._log_ex(f"Target does not exist: {uid_in} -> {uid_out}")
            return False

        node_happy = output_node.add_incoming_connection(input_node, slot)
        if self.loglevel >= LOGLEVEL_ERROR and not node_happy:
            msg = f"Failed to add connection {self.find_node(uid_in)} \
                    -> {self.find_node(uid_out)}"
            self._log_ex(msg)

        return node_happy

    def set_input(self, data: object) -> None:
        """
        Setter function to set the input data of the starting Node.

        Effectively sets the data at Graph entry point to prepare for training.
        Does not check or sanitise the user input. Does not return any value
        back to the caller.

        Args:
            data (object): the data object to be passed and set as the data \
                           input starting Node
        """
        self.find_node(self.start).data = data

    def get_output(self, slot=1) -> object:
        """
        Getter function to extract the output data of the end Node.

        This will trigger the evaluation of all node, if the result was not
        present, effectively train all attached stateful nodes.

        Args:
            slot (int, optional): the output slot of the finishing node \
                                  of the Graph instance. Defaults to 1.

        Returns:
            object: the resulting data object flowed to output node in the \
                    Graph. Returns None if the output could not be retrieved \
                    due to a malformed Graph or Node(s) structure.
        """
        output = None
        try:
            output = self.find_node(self.end).get_output(slot)
        except IndexError:
            if self.loglevel >= LOGLEVEL_ERROR:
                msg = f"Cannot request slot {slot}, connection wasn't added"
                self._log_ex(msg)
                return None
        return output

    def set_param(self, key: str, value: object) -> None:
        """
        Wrapper functionality to set property of the Graph to a value.

        Key should be a string value but value can be of any generic type.
        If key is not a string, a GraphCompileError is raised.
        Used to toggle or manage states in Graph. Useful to enforce or
        restrict certain behaviour during training time or other busy periods.
        If key is not an existing property in Graph, then it will be created
        with the value set to the user provided value.

        Args:
            key (str): a property string parameter for the Graph instance
            value (object): the associated value pair for the provided key

        Raises:
            GraphCompileError: when the input key value is not a string
        """
        if not isinstance(key, str):
            raise GraphCompileError("Parameter key should be of a string type")

        self.global_params[key] = value
