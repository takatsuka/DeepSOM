An Advanced Example using PySOM Library
=========================================

Let's take a look at constructing a deep SOM model to analyse an animal dataset
using the PySOM library.


.. code-block:: python
    :caption: Hello World

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

