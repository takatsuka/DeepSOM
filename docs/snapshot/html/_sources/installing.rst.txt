Setup & Installation
==========================

This section will describe how to get you up and running as quickly as possible
to start using PySOM Creator and Library.

Getting Started
----------------------------

First, visit the code repository at ``https://bitbucket.org/deep-som-dome/deep-som-dome/``
and clone it.

You will need to install the dependencies for both the PySOM Creator 
visualisation application and the Deep SOM Library itself if you intend to use
both. Some of these may already be installed in your dev environment - please
follow the instructions at the :doc:`tested-environments` page for more info.


Installing the PySOM Creator and Library
-----------------------------------------

- Go `to the repository`_ and clone or download it. Extract the archive to your location
  of choice if downloaded.
- Navigate to the ``deep-som-dome`` root folder and install via ``pip install .``. This 
  will install the backend library as a python module on your system. 
- Navigate to the ``deep-som-dome/app`` folder and install via ``npm run init`` to 
  install the frontend application dependencies. 

Optional: Documentation Generation
---------------------------------------

If you wish to build the latest documentation from scratch using the source 
files included with the app and library source files, then you need to also 
install the Sphinx documentation tool in your system and call it on the 
provided repository document source files.

It is recommended to install to use a virtual environment if you haven't already at this point. 

- First, install the `pysom` library as per the instructions in the previous section.

- Then, follow the instructions at the `Sphinx official install instructions`_ for
  your operating system.

- You need also need to install the documentation theme in your venv with 
  ``pip install sphinx-rtd-theme``

- Navigate to ``deep-som-dome/docs`` and generate the latest API documentation
  modules with ``sphinx-apidoc -fo source/ ../pysom``
      
- Now build the html docs with ``make html``
  
- The resultant docs html homepage will be found at ``deep-som-dome/docs/build/html/index.html``

.. _to the repository: https://bitbucket.org/deep-som-dome/deep-som-dome/
.. _Sphinx official install instructions: https://www.sphinx-doc.org/en/master/usage/installation.html