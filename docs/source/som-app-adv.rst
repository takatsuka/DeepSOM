A Harder Example using PySOM Creator
========================================

We will build a more complicated graph using the same animal dataset as
discussed in :doc:`som-lib-adv`, however, the graph produced will be slightly 
different, to demonstrate how to use some of the visualisation tools.

Follow the steps outlined below:

#. Open a new workspace and new model as demonstrated in :doc:`quickstart`.
#. Load in the following animal data files, as provided in the 
   ``deep-som-dome/datasets/animal`` path:

    - ``feature.txt`` - the animal vectors
    - ``label_name.txt`` - the animal labels

#. Set the dimensions of the input node to 13.

#. Add the ``Distributor``, ``SOM``, ``BMU``, ``Concat`` and ``Calibrate`` 
   nodes as follows. The graph should resemble the image below.


#. The ``SOM`` nodes after the ``Dist`` nodes should all have the following
   custom parameters, the rest can be default:

    - Dimensions: 16
    - Training Iterations: 10000
    - Sigma: 2
    - Learning Rate: 0.8
    - Shape: rect
    - Distance: euclidean
    - N_Hood: gaussian
    - Preprocess input: none
    - Outgoing dist: 1

#. However, the dimensions differ, from top to bottom they should be:
    
    - Input: 3 for the top-most ``SOM``
    - Input: 2 for the second ``SOM`` from the top
    - Input: 4 for the third ``SOM`` from the top
    - Input: 4 for the third ``SOM`` from the top

#. Change the ``Dist`` node to receive incoming ``Input`` in slot 1, and outgoing
   should be ascending order from 1 to 4, as in the screenshot below. This 
   should reflect in the incoming properties of the ``SOM`` nodes discussed previously.

#. Set the remaining nodes Outgoing slot to be 1.

#. Load the input data with ``feature.txt``, and load the ``Calibrate`` node with
   ``.txt`` TODO
   