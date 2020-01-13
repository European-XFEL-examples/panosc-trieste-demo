# PaNOSC Data Analysis Reproduction Demo

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/European-XFEL-examples/panosc-trieste-demo/v0.0.1)

Repository contains notebooks from the extra-data docs:

 - [Working with non-detector data](https://extra-data.readthedocs.io/en/latest/xpd_examples.html)
 - [Comparing fast XGM data from two simultaneous recordings](https://extra-data.readthedocs.io/en/latest/xpd_examples2.html)

## Cloud

### Running on Binder

The Docker image for MyBinder is built in two steps:

 1. Dependencies from `environment.yml` installed via conda
 2. `postBuild` runs and downloads the data from cloud storage
 
The downladed data is compressed to improve download times and to
reduce the size of the image.

At run time the `start` script is called, which runs a `data-extract`
script in the background and then begins the Jupyter session. This
means that it's possible to start and run the notebooks before the
data has been completely extracted. If you see an error about
missing or corrupted data, wait ~30 seconds and try again.


## Local

### Running with Singularity

Alternatively a singularity image can be pulled from [here](library://robert.rosca/default/panosc-trieste-demo:v0.0.2).

To use this image, download it and run the setup by:

```
singularity pull --arch amd64 library://robert.rosca/default/panosc-trieste-demo:v0.0.2 

singularity run --app setup panosc-trieste-demo_v0.0.2.sif
```

This will extract the data and notebooks to the directory you are
currently in, under `./euxfel-trieste/`. It will also install
a new Jupyter kernel called `euxfel-trieste`.

Now you can start up a Jupyter server locally on your machine and
run the notebooks. This will work as the notebook kernel runs inside
the singularity image, which includes the same dependencies as the
binder docker image.

### Running Locally

To set up and run this locally, first install conda and activate it,
then:

```
git clone https://github.com/European-XFEL-examples/panosc-trieste-demo
cd panosc-trieste-demo
conda env update -n ENVIRONMENT_NAME -f ./binder/environment.yml
sh ./binder/data-download
sh ./binder/data-extract
```

Now either install and run jupyter from inside the conda environment,
or alternatively install a kernel by running `ipykernel install --user --name=euxfel-trieste`,
then start up Jupyter as you normally would and select this kernel
for the notebooks.
 
