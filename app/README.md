# PySOM Creator

Graphical SOM experimentation platform powered by [PySOM](), designed to be friendly to wide range of target users from researchers to kids.


# Usage

## Requirements
- Python 3
- Node, and many packages.
- virtualenv


# Features
## Deep SOM 3D visualisation

Visualisation is created with [d3.js](https://github.com/d3/d3/blob/main/API.md) and an additional [d3-3d](https://github.com/niekes/d3-3d/) library written by Niekes. 

![Experimental Visualisation Demo I](imgs/viz_demo_1.gif)

So far input data should be normalised and have three dimensions.

![Experimental Visualisation Demo II](imgs/viz_demo_2.gif)

The animation starts lagging with over 200 data points, so we may have to consider any optimisation options.
