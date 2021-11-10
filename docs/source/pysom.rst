pysom package
=============

Subpackages
-----------

.. toctree::
   :maxdepth: 4

   pysom.nodes

Submodules
----------

pysom.graph module
------------------

.. automodule:: pysom.graph
   :members:
   :undoc-members:
   :show-inheritance:

pysom.node module
-----------------

Default Node: Example Code Usage
--------------------------------
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

   node = g.create(Node)  # create Default node

   g.connect(g.start, node, 1)  # connect Start node to Default node
   g.connect(node, g.end, 1)  # connect Default node to End node (Completes the Graph)

   g.set_input(data)  # set input data

   print(g.get_output())  # get output

.. automodule:: pysom.node
   :members:
   :undoc-members:
   :show-inheritance:

Module contents
---------------

.. automodule:: pysom
   :members:
   :undoc-members:
   :show-inheritance:
