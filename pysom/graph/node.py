from __future__ import annotations
# import numpy as np


class Node:

    def __init__(self, uid, props=None):
        """
        The default Node class used to build a SOM Node.

        The basic building element for the Deep SOM Model. Can be connected
        to other SOM Nodes, and at any time may optionally hold some data for
        evaluation during the training process.

        Args:
            uid (int): A unique positive integer ID for the Node
            props ([type], optional): [description]. Defaults to None.
        """
        self.uid = uid
        self.type = 0
        self.props = props  # used for storing actual SOM class
        self.incoming = list()  # 2-tuple (output_node, slot)

        # self.slots = list()
        # {
        #     0: DefaultConnection(self), # only in SOMNode, unused in DistNode
        #     1: DistConnection(self, indices), # DistConnection stores the
        #        actual indices
        #     2: DistConnection(self, indices), # configured by user
        #     3: DistConnection(self, indices) # configured by user
        # }

    def __str__(self) -> str:
        str_rep = "Empty Node {}".format(self.uid)
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
        return self.uid

    def get_incoming(self) -> list:
        return self.incoming

    # TO DO
    def evaluate(self) -> int:
        total = []

        for node, slot in self.incoming:
            if node.uid == 0:
                print("-> Incoming node of {}: {} (START)".format(self, node))
            elif self.uid == 1:
                print("-> Incoming node of {}: {} (END)".format(self, node))
            else:
                print("-> Incoming node of {}: {}   |".format(self, node[0]))
            total += node[0].get_output(node[1])

        return total + self.data

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
            object: the data object to be passed down the edge identified by
                    the user provided slot ID
        """
        return self.evaluate()

    # Basic Node can be connected any where
    def check_slot(self, slot: int) -> bool:
        """
        A verification method to confirm if a proposed slot ID can be used.
        
        Typically deferred to implementing classes to manage whether a slot ID
        can be used when a connection is to be established between two nodes.

        Args:
            slot (int): a proposed integer slot ID to be checked

        Returns:
            bool: True if the slot is not reserved and not in use, or
                  False otherwise. Returns False by default in the Node
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
            bool: [description]
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
            bool: True if the slot is not reserved and not in use, or
                  False otherwise
        """
        return self.check_slot(slot)


if __name__ == "__main__":

    x1 = Node()
    x2 = Node()
    print(x1)
    print(x2)
