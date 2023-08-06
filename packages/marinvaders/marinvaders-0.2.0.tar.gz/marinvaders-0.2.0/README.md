# The MarINvaders Toolkit

The MarINvaders Toolkit is a Python 3 module to assess the native and alien distribution of marine species.

It can be used to find the native and alien distribution of a given species or to get an overview of all alien and native species found in one [marine ecoregion](https://academic.oup.com/bioscience/article/57/7/573/238419). 

To do so, Marinivaders cross-references and harmonizes distribution maps from  [several databases](#Data-sources) to find all occurences of a given species and to gather information on its native and alien status per location recording. 


## Where to get it


The full source code and all requireded local data is available [at the MarINvaders GitLab repostiory.](https://gitlab.com/dlab-indecol/marinvaders).


MarINvaders is registered at PyPI and at conda-forge for installation within a conda environment.
To install use

    `pip install MariINvaders --upgrade`
    
    
and when using conda:

    `conda update -c conda-forge MarINvaders`

We recommend to install the package in a [virtual environment](https://docs.python.org/3/library/venv.html) or [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)


## Getting started in five lines

Install the package as explained above and start your prefered Python interpreter

Import the package

``` python
import marinvaders
```

Get the species AphiaID you are interested in from the [WoRMS - marine species database](https://www.marinespecies.org/index.php). Here we use * Amphibalanus amphitrite * (Darwin, 1854), aka the [striped barnacle](https://www.marinespecies.org/aphia.php?p=taxdetails&id=421137) which has the AphiaID 421137.

Now we can get the species data from this barnacle with

``` python
species_data = marinvaders.Species(aphia_id=421137)
```

and list all occurences 

``` python
species_data.all_occurrences
```

as well as the alien distribution of the barnacle with

``` python
species_data.reported_as_alien
```

These can also be easily plotted with

``` python
species_data.plot()
```

In addition, MarINvaders includes API functions for analysing all species within an ecoregion.

For a full overview of the capabilities check the TODO documentaiont or 

see the example/tutorial notebook. This can be run in the cloud through [Binder](https://mybinder.org/):

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/dlab-indecol%2Fmarinvaders/master?filepath=marinvaders.ipynb)



## Citations

TODO

     

## Communication, issues, bugs and enhancements

Please use the issue tracker for documenting bugs, proposing enhancements and all other communication related to marinvaders.



## License
This project is licensed under The [GNU GPL v3](LICENSE)



