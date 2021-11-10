pysom.nodes package
===================

Submodules
----------

pysom.nodes.bmu module
----------------------

.. automodule:: pysom.nodes.bmu
   :members:
   :undoc-members:
   :show-inheritance:

pysom.nodes.calibrate module
----------------------------

Calibrate Node: Example Code Usage
----------------------------------
.. code-block:: python3

   ### SAMPLE DATA ###

   animal = ['Dove', 'Chicken', 'Duck', 'Goose', 'Owl', 'Hawk', 'Eagle', 'Fox', 'Dog', 'Wolf', 'Cat', 'Tiger', 'Lion', 'Horse', 'Zebra', 'Cow']
   features = [
      [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],    # Dove
      [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],    # Chicken
      [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],    # Duck
      [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],    # Goose
      [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Owl
      [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Hawk
      [0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Eagle
      [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],    # Fox
      [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0],    # Dog
      [0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],    # Wolf
      [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],    # Cat
      [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],    # Tiger
      [0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],    # Lion
      [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],    # Horse
      [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],    # Zebra
      [0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]     # Cow
   ]

   feats = pd.DataFrame(features)
   feats.columns = ['Small', 'Medium', 'Big', '2-legs', '4-legs', 'Hair', 'Hooves', 'Mane', 'Feathers', 'Hunt', 'Run', 'Fly', 'Swim']

   ### CODE HERE ###

   g = Graph()  # initialise Graph instance

   size = 5  # select SOM grid size < size = 5: creates a 5 x 5 grid >

   # create SOM node and customize parameters
   som = g.create(SOM, props={'size': size, 'dim': 13,
                  "nhood": nhood_mexican, 'sigma': 13, 'lr': 0.8, 'n_iters': 10000})
   
   g.connect(g.start, som, 1)  # connect Start node to SOM node

   cal = g.create(Calibrate, props={"labels": animal})  # create Calibrate node and provide labels to fit on data

   g.connect(som, cal, 0)  # connect SOM node to Calibrate node < output self >
   g.connect(cal, g.end, 1)  # connect Calibrate node to End node (Completes the Graph)

   data = scale(feats.values)

   g.set_input(data)  # set input data

   out = g.get_output()  # get output
   plot_features(size, out)  # use helper function to visualize label mapping

.. automodule:: pysom.nodes.calibrate
   :members:
   :undoc-members:
   :show-inheritance:

pysom.nodes.concat module
-------------------------

Concat Node: Example Code Usage
-------------------------------
.. code-block:: python3

   ### SAMPLE DATA ###

   data = [
      [1, 3, 2],
      [1, 3, 2],
      [1, 3, 2]
   ]
   data = np.array(data)

   ### CODE HERE ###

   g = Graph()  # initialise Graph instance

   sel = [(1, [0, 2]), (1, [1])]  # selection(1): dimensions at index 0, 2
                                  # selection(2): dimensions at index 1

   dist = g.create(Dist, {'selections': sel})  # create Dist node and provide selections

   g.connect(g.start, dist, 1)  # connect Start node to Distribute node

   node1 = g.create(Node)  # create Default node 1
   node2 = g.create(Node)  # create Default node 2

   g.connect(dist, node1, 1)  # connect Dist node to Default node 1 < sends selection(1) >
   g.connect(dist, node2, 2)  # connect Dist node to Default node 2 < sends selection(2) >

   con = g.create(Concat, {'axis': 1})  # create Concat node and select axis < axis = 1: concatenates column-wise >

   g.connect(node1, con, 1)  # connect Default node 1 to Concat node 
   g.connect(node2, con, 1)  # connect Default node 2 to Concat node 

   g.connect(con, g.end, 1)  # connect Concat node to End node (Completes the Graph) 

   g.set_input(data)  # set input data

   print(g.get_output())  # get output


.. automodule:: pysom.nodes.concat
   :members:
   :undoc-members:
   :show-inheritance:

Dist Node: Example Code Usage
-----------------------------
.. code-block:: python3

   ### SAMPLE DATA ###

   data = [
      [1, 3, 2],
      [1, 3, 2],
      [1, 3, 2]
   ]
   data = np.array(data)

   ### CODE HERE ###

   g = Graph()  # initialise Graph instance

   sel = [(1, [0, 2]), (1, [1])]  # selection(1): dimensions at index 0, 2
                                  # selection(2): dimensions at index 1

   dist = g.create(Dist, {'selections': sel})  # create Dist node and provide selections

   g.connect(g.start, dist, 1)  # connect Start node to Dist node < sends selection(1) >
   g.connect(dist, g.end, 1)    # connect Dist node to End node (Completes the Graph) 

   g.set_input(data)  # set input data

   print(g.get_output())  # get output

.. automodule:: pysom.nodes.dist
   :members:
   :undoc-members:
   :show-inheritance:

pysom.nodes.input\_container module
-----------------------------------

.. automodule:: pysom.nodes.input_container
   :members:
   :undoc-members:
   :show-inheritance:

pysom.nodes.som module
----------------------

.. automodule:: pysom.nodes.som
   :members:
   :undoc-members:
   :show-inheritance:

Module contents
---------------

.. automodule:: pysom.nodes
   :members:
   :undoc-members:
   :show-inheritance:
