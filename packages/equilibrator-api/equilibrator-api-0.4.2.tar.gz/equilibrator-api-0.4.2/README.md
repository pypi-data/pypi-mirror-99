# eQuilibrator - a thermodynamics calculator for biochemical reactions

[![PyPI version](https://badge.fury.io/py/equilibrator-api.svg)](https://badge.fury.io/py/equilibrator-api)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/equilibrator-api/badges/version.svg)](https://anaconda.org/conda-forge/equilibrator-api)
[![pipeline status](https://gitlab.com/elad.noor/equilibrator-api/badges/master/pipeline.svg)](https://gitlab.com/elad.noor/equilibrator-api/commits/master)
[![coverage report](https://gitlab.com/elad.noor/equilibrator-api/badges/master/coverage.svg)](https://gitlab.com/elad.noor/equilibrator-api/commits/master)
[![Join the chat at https://gitter.im/equilibrator-devs/equilibrator-api](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/equilibrator-devs/equilibrator-api?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Documentation Status](https://readthedocs.org/projects/equilibrator/badge/?version=latest)](https://equilibrator.readthedocs.io/en/latest/?badge=latest)

## What is `equilibrator-api`?

`equilibrator-api` is a Python package for obtaining estimates of reactions Gibbs energies.
It is mainly meant for biologists/bioengineers with basic programming skills that
work on metabolism and want to easily add thermodynamic data to their models.

The documentation is browseable online at
[readthedocs](https://equilibrator.readthedocs.io/en/latest/index.html).

If your list of reactions is very short, we recommend trying our
website called [eQuilibrator](http://equilibrator.weizmann.ac.il/) before spending
the time necessary for learning how to use `equilibrator-api`.

The main advantages of `equilibrator-api` are:

* Batch mode: can be used for large reaction datasets (even more than 1000 reactions)
* Does not require a network connection (except during installation and initialization)
* Works with standard compound identifiers (such as ChEBI, KEGG, BiGG and MetaNetX) for more than 500,000 compounds

To access more advanced features, such as adding new compounds that are not
among the 500,000 currently in the MetaNetX database, try using our 
[equilibrator-assets](https://gitlab.com/equilibrator/equilibrator-assets)
package.

## Cite us

If you plan to use results from `equilibrator-api` in a scientific publication,
please cite our paper:

Noor E, Haraldsdóttir HS, Milo R, Fleming RMT (2013)
[Consistent Estimation of Gibbs Energy Using Component Contributions](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003098),
PLoS Comput Biol 9:e1003098, DOI: 10.1371/journal.pcbi.1003098

## A very simple example

Note that creating a `ComponentContribution` object for the first time after
installation, starts an initialization step which downloads ~1.5 GBytes of data
to your computer. It can take more than an hour (depending on the connection speed).
Note that the initialization might not work inside a Jupyter notebook environment - 
in that case you should try running it in a standard python shell first and then
run the Jupyter notebook.

```python
from equilibrator_api import ComponentContribution
cc = ComponentContribution()
rxn = cc.parse_reaction_formula("kegg:C00002 + kegg:C00001 = kegg:C00008 + kegg:C00009")
print(f"ΔG'0 = {cc.standard_dg_prime(rxn)}")
```
