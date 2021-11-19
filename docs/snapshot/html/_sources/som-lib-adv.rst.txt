A Harder Example using PySOM Library
=========================================

Let's take a look at constructing a deep SOM model to analyse an animal dataset
using the PySOM library.

First let's load in the required PySOM modules, and also numpy, pandas, sklearn and
matplotlib to help process and visualise what we're working with.

.. code-block:: python
    :caption: Start by importing the following Python modules and helper function

    import numpy as np
    from numpy.linalg import eig
    from numpy import array, mean, cov, argsort, arange, linspace
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.preprocessing import scale

    import pysom
    from pysom.node import Node
    from pysom.graph import Graph
    from pysom.nodes.bmu import BMU
    from pysom.nodes.dist import Dist
    from pysom.nodes.concat import Concat
    from pysom.nodes.calibrate import Calibrate
    from pysom.nodes.som import SOM, nhood_mexican, nhood_bubble, dist_manhattan, dist_cosine

    def plot_features(size, out):
        for bmu, labels in out.items():
            labels = list(labels)
            print(labels)

            for i in range(len(labels)):
                plt.text(bmu[0] + 0.1, bmu[1] + (i + 1) / len(labels) - 0.35, labels[i], fontsize=10)

        plt.xticks(np.arange(size + 1))
        plt.yticks(np.arange(size + 1))
        plt.grid()
        plt.show()

Next, let's load the actual animal dataset and pack it into a pandas dataframe.
Note that each row of the numpy array corresponds to an animal as shown in the 
in-lined comments, and the columns are the dimensions/attributes of the data 
as shown in the definition of the pandas dataframe columns.

.. code-block:: python
    :caption: Loading the animal dataset into our application

    animal = ['Dove', 'Chicken', 'Duck', 'Goose', 'Owl', 'Hawk', 'Eagle', 'Fox',
            'Dog', 'Wolf', 'Cat', 'Tiger', 'Lion', 'Horse', 'Zebra', 'Cow']
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
    feats.columns = ['Small', 'Medium', 'Big', '2-legs', '4-legs', 'Hair', 
                    'Hooves', 'Mane', 'Feathers', 'Hunt', 'Run', 'Fly', 'Swim']

    data = feats.values


As with before, we need to construct our PySOM graph. Here we need to define the
network structure as represented in the following ASCII art.

.. code-block::
    :caption: The deep SOM graph we want to build

                  *->som(size)->bmu(size)->*
                 /                          \\
                /--->som(legs)->bmu(legs)----\\
    animal -> dist                          concat -> som -> calibrate(labels)
                \\-->som(char)->bmu(char)----/
                 \\                         /
                  *->som(move)->bmu(move)->*    

Immediately we can see the automatically constructed ``InputContainer`` denoted by 
"animal" feeds into a ``Distributor`` node. This then branches out into 4
different types of attributes which individual ``SOM`` and ``BMU`` nodes are 
trained upon, before the result is joined together through a ``Concatenator`` and
output with ``SOM`` and ``Calibrate`` nodes. 

This should allow us to effectively train the 4 independent SOMs on specific 
features of the dataset, before we bring it together and map it to our last 
SOM. Lastly, we apply our calibration process to provide labelling to our
SOM model output, which will allow us to plot our results.

.. code-block:: python
    :caption: Construct out graph and plot the trained result

    g = Graph()

    sel = [(1, [0, 1, 2]), (1, [3, 4]), (1, [5, 6, 7, 8]), (1, [9, 10, 11, 12])]

    dist = g.create(Dist, props={"selections": sel})
    g.connect(g.start, dist, 1)

    som_size = g.create(SOM, props={"size": 16, "dim": 3, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    som_legs = g.create(SOM, props={"size": 16, "dim": 2, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    som_char = g.create(SOM, props={"size": 16, "dim": 4, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    som_move = g.create(SOM, props={"size": 16, "dim": 4, "sigma": 15, "lr": 0.8, "n_iters": 10000})

    g.connect(dist, som_size, 1)
    g.connect(dist, som_legs, 2)
    g.connect(dist, som_char, 3)
    g.connect(dist, som_move, 4)

    bmu_size = g.create(BMU, props={"output": "w"})
    bmu_legs = g.create(BMU, props={"output": "w"})
    bmu_char = g.create(BMU, props={"output": "w"})
    bmu_move = g.create(BMU, props={"output": "w"})

    g.connect(som_size, bmu_size, 0)
    g.connect(som_legs, bmu_legs, 0)
    g.connect(som_char, bmu_char, 0)
    g.connect(som_move, bmu_move, 0)

    concat = g.create(Concat, props={"axis": 1})

    g.connect(bmu_size, concat, 1)
    g.connect(bmu_legs, concat, 1)
    g.connect(bmu_char, concat, 1)
    g.connect(bmu_move, concat, 1)

    size = 6

    som = g.create(SOM, props={'size': size, 'dim': 13, "nhood": nhood_mexican, 'sigma': 13, 'lr': 0.8, 'n_iters': 10000})

    g.connect(concat, som, 1)

    cal = g.create(Calibrate, props={"labels": animal})

    g.connect(som, cal, 0)
    g.connect(cal, g.end, 1)

    data = scale(feats.values)
    g.set_input(data)

    out = g.get_output()

    plot_features(size, out)

You should see the following clusters being printed to standard out, as well
as an image of with the clusters visualised and annotated on our final output SOM.

.. code-block:: python

    ['Dove', 'Chicken', 'Duck', 'Goose']
    ['Owl', 'Hawk']
    ['Eagle']
    ['Fox']
    ['Dog']
    ['Wolf', 'Tiger']
    ['Cat']
    ['Lion', 'Horse', 'Zebra', 'Cow']

.. image:: _static/AnimalPlot1.png

We can see with our simple dataset that our animals seem to be clustered together
based on some sort of semantic meaning - based on the attributes we distributed
earlier - size, legs, characteristic, locomotion.

Hopefully this inspires you to make much more complex and interesting models on
your own datasets.