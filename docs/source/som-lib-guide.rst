PySOM Library Explained in 5 Minutes
============================================

The PySOM Library is essentially a graph builder framework that allows the user to
manipulate and train data through the predefined nodes in the library. Given the
extensible nature of the library, the user is also welcome to (and is encouraged to)
add to this collection of node elements as required.

The Graph Class and Constructing Your Model
++++++++++++++++++++++++++++++++++++++++++++

The main ``Graph`` class defines the methods needed to actually construct the 
deep SOM model. Graph nodes will be instantiated and managed through this class -
the user does not create the nodes independently. By default the input and output
nodes are generated automatically. but explicit input data needs to be set through
the helper functionality.

Additionally, the edge connections are created through a 'slot' system (simply 
an integer ID to represent some edge connection) and likewise this is also done 
through the ``Graph`` class. 

Lastly, any global parameters that affects the model beyond a node or edge level
should be defined through the helper functions.

Because the Graph is responsible for the node and edge elements, it is also
responsible for the compiling and training process. In summary, the ``Graph``
class captures the entire functionality of the model akin to a programming
facade or API.

The Different Types of PySOM Nodes
++++++++++++++++++++++++++++++++++++++++++++
As of the library's first beta release, the PySOM library contains the following
basic graph nodes, with a basic description of each:

#. ``BMU`` - this is the node that extracts the Best Matching Unit based on some
   input data and the weights output by an incoming node (i.e. the ``SOM`` node)
#. ``Calibrate`` - the node that provides a functionality to provide labelling
   information on the best matching units and returns the most common label
#. ``Concat`` - a simple node that has the opposite effect of the ``Dist`` node,
   and concatenates the input into one output array
#. ``Dist`` - a simple node that distributes data into multiple output slots for
   manipulation of independent neighbouring downstream nodes
#. ``InputContainer`` - a holder node class that serves as the entry point into
   the ``Graph``. This is automatically generated upon instantiation of ``Graph``,
   and otherwise does nothing special.
#. ``Scale`` - a normalisation class that transforms the input data into a 
   scaled, and standardised/transformed output
#. ``SOM`` - the heart of the actual SOM training logic containing all the learning
   and training logic, including the various neighbourhood distance and learn
   rate functions

Note that there is default parent concrete ``Node`` class that can be used and
manipulated as with any other node, but does not provide any useful functionality
beyond simple defaults.

If you wish to create your own ``Node`` subclass, it is advised to investigate
the :doc:`pysom` API documentation in greater detail.