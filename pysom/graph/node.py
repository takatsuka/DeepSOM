from __future__ import annotations


class Node:
    """
    The default Node class used to build a SOM Node.

    Also the parent class of all node types defined in graph/nodetypes.
    The basic building element for the Deep SOM Model. Can be connected
    to other SOM Nodes, and at any time may optionally hold some data for
    evaluation during the training process.

    Attributes:
        uid (str): the unique integer ID of the Node instance
        incoming (list): the list of all incoming Node objects that have a
                         connection to the current Node instance
    """

    def __init__(self, uid: int, graph):
        """
        The constructor for the default Node class used to build a SOM Node.

        Args:
            uid (int): a unique positive integer ID for the Node
            graph (Graph): the containing Graph instance holding the
                           constructed Node
        """
        self.uid = uid
        self.graph = graph
        self.type = 0
        self.incoming = list()  # 2-tuple (output_node, slot)

        self.output_ready = False  # cache

    def __str__(self) -> str:
        str_rep = "Default Node {}".format(self.uid)
        return str_rep

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: Node) -> bool:
        if (isinstance(other, Node)):
            return other.uid == self.uid
        else:
            return False

    def __hash__(self) -> int:
        return self.uid

    def get_id(self) -> int:
        """
        Getter function to return the ID of the current node.

        Returns:
            int: the assigned unique integer ID of the current node
        """
        return self.uid

    def get_incoming(self) -> list:
        """
        Getter function to return a list of all incoming Node objects.

        Incoming Node objects are other Node instances which have a valid
        outgoing edge to the current node. Used to backtrace and request
        data output from these nodes during the training process.

        Returns:
            list: the list of all nodes that have an outgoing edge to the \
                  current node
        """
        return self.incoming

    def make_input_ready(self) -> None:
        """
        Helper function to prepare all incoming nodes.

        Forcibly triggers the evaluation of all incoming nodes for
        the current iteration. This method is idempotent for each iteration,
        so calling this method more than once does not do anything. Method
        does not return anything.
        """
        for node, slot in self.incoming:
            node.get_output(slot)

    def _evaluate(self) -> int:
        return self.get_input()

    def get_input(self, index: int = 0) -> object:
        """
        Getter function to retrieve the output of an incoming node.

        A wrapper function allowing the extraction of data from an incoming
        graph Node using the current node as a point of reference.

        Args:
            index (int, optional): the index of the incoming node, not
                                   necessarily equivalent to the slot number
                                   of the outgoing edge. Defaults to 0.

        Returns:
            object: the data returned from the incoming node indexed
        """
        node, slot = self.incoming[index]
        return node.get_output(slot)

    def get_output(self, slot: int) -> object:
        """
        Getter function to return some data after a post-evaluation process.

        Typically called to extract some sort of result from the current node
        during the training process to be passed downstream towards the
        final output node.

        Args:
            slot (int): the slot ID representing a stream of data where the
                        output is to be passed down

        Returns:
            object: the data object to be passed down the edge identified by \
                    the user provided slot ID
        """
        if slot == 0:
            return self

        return self._evaluate()

    # Basic Node can be connected any where
    def check_slot(self, slot: int) -> bool:
        """
        A verification method to confirm if a proposed slot ID can be used.

        Typically deferred to implementing classes to manage whether a slot ID
        can be used when a connection is to be established between two nodes.

        Args:
            slot (int): a proposed integer slot ID to be checked

        Returns:
            bool: True if the slot is not reserved and not in use, or \
                  False otherwise. Returns True by default in the Node \
                  superclass.
        """
        return True

    # Default method for all concrete classes
    def add_incoming_connection(self, output_node: Node, slot: int) -> bool:
        """
        Adds an edge from the user-provided output node to the current node.

        Args:
            output_node (Node): the user provided node that outputs some sort
                                of data to be used by the current node
            slot (int): the user provided integer slot ID that is to be
                        assigned to the edge

        Returns:
            bool: True if the outgoing edge was added successfully, False \
                  otherwise
        """
        if output_node.check_outgoing_connection(self, slot):
            self.incoming.append((output_node, slot))
            return True

        return False

    # Default method for all concrete classes
    def check_outgoing_connection(self, input_node: Node, slot: int) -> bool:
        """
        Helper function to check connection can be added for an outgoing node.

        Since the training process relies on a backtracking training algorithm,
        the slot validation method is checked by an outgoing node which has
        ownership over the slots assigned to outgoing edges. Is typically
        called by the receiving node of the output, prior to appending any
        incoming connections.

        Args:
            slot (int): the assigned integer representing the ID of the edge
                        to be created

        Returns:
            bool: True if the slot is not reserved and not in use, or \
                  False otherwise
        """
        return self.check_slot(slot)


if __name__ == "__main__":

    x1 = Node()
    x2 = Node()
    print(x1)
    print(x2)
