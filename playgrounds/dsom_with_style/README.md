## dsom_with_style
An implementation of DSOM model in Python with numbasom.

Haoyan Qi, Sep 16


### What's here?
* A CNN like multi-layer Deep SOM implementation.
* Simple script for using it to classification on Fashion MNIST dataset.


### Dataset and Training Result

#### Original Image 28x28(768)
![act](https://bitbucket.org/ChristopherIrving/deep-som-dome/raw/569d08631a867250faae47a3e334a7c747650fb8/playgrounds/dsom_with_style/imgs/img_0.png)


#### Mini patches recovered from 10x10(100) compressed sample
![act](https://bitbucket.org/ChristopherIrving/deep-som-dome/raw/569d08631a867250faae47a3e334a7c747650fb8/playgrounds/dsom_with_style/imgs/activation_0.png)


#### Sample layer
![act](https://bitbucket.org/ChristopherIrving/deep-som-dome/raw/569d08631a867250faae47a3e334a7c747650fb8/playgrounds/dsom_with_style/imgs/sample_0.png)



### Usage


```
$ cd ./playgrounds/dsom_with_style
$ python playwithstyle.py
```