## dsom_with_style
An implementation of DSOM model in Python with numbasom.

Haoyan Qi, Sep 16


### What's here?
* A CNN like multi-layer Deep SOM implementation.
* Simple script for using it to classification on Fashion MNIST dataset.


### Dataset and Training Result

#### Original Image 28x28(768)
![act](https://bitbucket.org/ChristopherIrving/deep-som-dome/raw/6f067a233d7723dc90ef0dc70a9aab8191ef4491/playgrounds/dsom_with_style/img_0.png){width=50%}


#### Mini patches recovered from 10x10(100) compressed sample
![act](https://bitbucket.org/ChristopherIrving/deep-som-dome/raw/6f067a233d7723dc90ef0dc70a9aab8191ef4491/playgrounds/dsom_with_style/activation_0.png){width=50%}


#### Sample layer
![act](https://bitbucket.org/ChristopherIrving/deep-som-dome/raw/6f067a233d7723dc90ef0dc70a9aab8191ef4491/playgrounds/dsom_with_style/sample_0.png){width=50%}



### Usage


```
$ cd ./playgrounds/dsom_with_style
$ python playwithstyle.py
```