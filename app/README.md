# PySOM Creator

Graphical SOM experimentation platform powered by [PySOM](), designed to be friendly to wide range of target users from researchers to kids.

# Usage

## Requirements

The following softwares are required to run the automated build system, and thus have to be installed manually on your system.

-   Python 3
-   Node, and many packages.
-   virtualenv

### Install Build Dependencies

-   Make sure your current directory is at `./app`, if not, `cd ./app`.
-   `npm run init`, this will install all npm packages and create a virtualenv for Python. It could take a while depends on your internet connection.

## Run

After installing the softwares above, you can use the following commands to run the application base on your focus:

-   `npm run dev` will bundle resources into `./gui` and bring up a dev server with support for live updating. This option is ideal when working with GUI only.
-   `npm run start` will bundle resources into `./gui` and use Python application to render the content.

## Installing Backend Dependency

Activate your `venv`, then simply call from this directory:

`pip install ..`

`pysom` will be installed and added to your `site-packages`.

## Build

_The only available target currently is macOS. Other targets are still under development_

Run `npm run build` to start the bundling process. GUI will be recompiled into `./gui` with production flags and the resutlting portable application bundle will be placed in `./dist` after a successful build.

# Features

## Deep SOM 3D visualisation

Visualisation is created with [d3.js](https://github.com/d3/d3/blob/main/API.md) and an additional [d3-3d](https://github.com/niekes/d3-3d/) library written by Niekes.

![Experimental Visualisation Demo I](imgs/viz_demo_1.gif)

So far input data should be normalised and have three dimensions.

![Experimental Visualisation Demo II](imgs/viz_demo_2.gif)

The animation starts lagging with over 200 data points, so we may have to consider any optimisation options.
