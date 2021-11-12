Tested Environments
======================

The PySOM library and bundled GUI editor has been tested with the following
platforms on a best efforts basis. 

The following system configurations were tested in the development
of PySOM. There are no minimum hardware specifications, but try not to run
PySOM on a potato.

Since the backend uses Python and it is not the most performant language, and
without performance optimisations with Numba, the library may run slower than
expected. Future work will focus more on this aspect given enough time and 
resources.


Instructions for Windows
------------------------

.. container:: twocol

   .. container:: leftside

        .. image:: _static/logo_win10.png
            :width: 180
            :alt: Windows 10


   .. container:: rightside
       
      **Windows 10 Home Version 1909**

      To install: Python3 (see below), NodeJS, Visual Studio
      
      Notes: Avoid using Python version newer than 3.8 due to an issue
      with dependencies. Further details can be found below.

Windows Install Instructions
++++++++++++++++++++++++++++++

Naturally if any requirements are already satisfied then the relevant steps can be omitted. Note that instructions
are for a native Windows install. If Windows Subsystem for Linux is used, then
follow the Linux instructions instead. Support for WSL GUI applications
should be followed `at the following link`_.

- Install Python from `the Python official website`_  or through a package
  manager such as Chocolatey or Anaconda. PySOM Creator uses python3, but 
  will not work with a version newer than Python3.8. You can use a venv to
  circumvent this, or make sure that your environment variable points to the
  correct version if you have multiple versions of Python installed.

- Make sure `virtualenv` is part of your installed modules with `pip install virtualenv`.

- Install Visual Studio from `the MSVS official website`_ which is needed for NodeJS. 
  The community edition is free. Make sure that "Desktop development with C++"
  is checked for the install.

- Install NodeJS from `the NodeJS official website`_ or through a package manager
  such as Chocolatey.

- You are now ready to install PySOM - how exciting!

Windows Install Quirks
++++++++++++++++++++++++

If NodeJS is having issues finding Visual Studio build tools it may be 
because Visual Studio is too new (2022). Installing NodeJS via the `.msi` installer
has an option to bundle the necessary build tools, so use that method instead of manually through
a package manager. Note that it will install Chocolatey and Python if you haven't already.

The issue with the Python version is due to `Python.NET` and the last supported
version nominated `on their GitHub repo`_ is Python3.8. The setup process for `pythonnet` will
fail for a newer version of Python.


Instructions for macOS
------------------------

.. container:: twocol

   .. container:: leftside

        .. image:: _static/logo_apple.png
            :width: 200
            :alt: MacOS


   .. container:: rightside
       
      **MacOS Big Sur Version 11.2.2**

      To install: Python, NodeJS, virtualenv


macOS Install Instructions
++++++++++++++++++++++++++

Python 2.7 comes with any Mac OS X out of the box, however you should upgrade to Python 3.X as the default version has been 
deprecated. Be sure you have XCode setup to have GCC installed, and a package manager such as Homebrew would also be useful.

- Downloading Python through a package manager such as Homebrew will be a much easier process. Another option is to download 
Python 3.X from `the Python official website`_. 

- Once Python 3.X has been installed, you will be able to install virtualenv module by running `pip install virtualenv` on the command 
line. 

- Install NodeJS from `the NodeJS official website`_ or through a package manager such as Homebrew. The dependencies for npm will also
 be automatically installed if done through Homebrew, one of which includes Python. 


macOS Install Quirks
++++++++++++++++++++++++

Not many quirks with MacOS fortunately; if any of the above instructions were executed by doesn't seem to be installed, make sure 
to have the PATH variable setup to point to the right directories. Specific commands to add to PATH are usually printed on the command
line after a successful install of packages.


Instructions for Linux
------------------------
.. container:: twocol

   .. container:: leftside

        .. image:: _static/logo_ubuntu.png
            :width: 180
            :alt: Linux Ubuntu


   .. container:: rightside
       
      **Linux/Ubuntu 20.04 LTS**

      To install: Vext, pywebview, PyGObject
      
      Notes: There are too many distros and setups to check for Linux, so you can use
      the following guide as a general guideline. Substitute the package manager with
      the one bundled with your distro.

Linux Install Instructions
++++++++++++++++++++++++++

Fortunately, a newer stable release of a common distro like Ubuntu comes with
Python pre-installed and with a relatively sane default developer setup. 
Most work here will be to install the requirements for getting `pywebview` 
working for the front-end application.

- Check that you have a relatively new version of Python3. We have tested 
  Python 3.7 and newer and it works fine. Install `pip3` if you haven't already.

- Install virtualenv with `apt install python3-virtualenv`.

- Install pywebview dependencies with `sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0`.

- Install NodeJS and `npm` with `apt install npm`. The older stable release of 
  node v10.19.0 and npm v6.14.4 is sufficient.

- Install pywebview dependencies WITHIN the `deep-som-dome/app/venv` via the following: `pip install vext vext.gi PyGObject`.

- You're all set to install the library and front-end app!

Linux Install Quirks
++++++++++++++++++++++++

Any clashes with virtualenv, namely an error resembling "No module named 
virtualenv.seed.embed.via_app_data" is a consequence of having virtualenv installed
both via `pip` and `apt` (or your package manager). You just need to uninstall the
`pip` version.

Some instructions online to set up pywebview will be to install dependencies globally
but these are not typically reachable within a virtual environment.



PySOM Instructions 
------------------------

(this will be moved later to the actual quickstart page)

- Go `to the repository`_ and clone or download it. Extract the archive to your location
  of choice if downloaded.
- Navigate to the `deep-som-dome` root folder and install via `pip install .` - this 
  will install the backend library as a python module on your system. 
- Navigate to the `deep-som-dome/app` folder and install via `npm run init` to 
  install the frontend application dependencies.
- Optionally, navigate to `deep-som-dome/docs` and generate the latest documentation
  with `sphinx-apidoc -fo source/ ../pysom && make clean && make html`. The resultant
  docs html homepage will be found at `deep-som-dome/docs/build/html/index.html`

.. _at the following link: https://docs.microsoft.com/en-us/windows/wsl/tutorials/gui-apps
.. _the Python official website: https://www.python.org/downloads/
.. _the NodeJS official website: https://nodejs.org/en/download/
.. _the MSVS official website: https://visualstudio.microsoft.com/downloads/
.. _to the repository: https://bitbucket.org/deep-som-dome/deep-som-dome/
.. _on their GitHub repo: https://github.com/pythonnet/pythonnet