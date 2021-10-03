try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='pysom',
    version='0.0.1',
    description='Powerful, extensible Self-Organizing Map library for Python',
    author='COMP3988_T17_01_Group2',
    url='https://bitbucket.org/ChristopherIrving/deep-som-dome/',
    packages=find_packages(include=['pysom']),
    package_dir={'pysom': 'pysom'},
    tests_require=['pytest'],
    install_requires=['numpy']
)
