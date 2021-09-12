## numba_npsom_perf_analysis
Brief analysis on the boost in performance with Numba of a implementation of single layer SOM which utilizes Numpy.

Haoyan Qi, Sep 11


### What's here?
* a simple single layer rect SOM implementation with Numpy.
* Numba optimized SOM with minium changes to the above implementation.

### Result

`playfast.py` show an average of 28.6% shorter running time compares to `play.py` even without exploiting task parallelization.

Above result was tested on a system with Ryzen 3900X CPU running macOS, Python 3.9.


### Dataset and Training Result

![Sphere](https://bitbucket.org/ChristopherIrving/deep-som-dome/raw/42529a270dc7a2b6903fd12b5b094ff5431ebe22/playgrounds/numba_npsom_perf_analysis/som_fast.png)
![Donut](https://bitbucket.org/ChristopherIrving/deep-som-dome/raw/4b05b3056550423cfe09ae8ae2a8e91bc710e4f0/playgrounds/numba_npsom_perf_analysis/som_fast_donut.png)



### Usage

```
$ python play.py <csv formatted data file>
$ python playfast.py <csv formatted data file>

```

For example:

```
$ python playfast.py ../../datasets/sphere/sphere_256.txt
```