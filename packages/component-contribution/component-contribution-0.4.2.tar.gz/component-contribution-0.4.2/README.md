# Component Contribution

[![pipeline status](https://gitlab.com/elad.noor/component-contribution/badges/develop/pipeline.svg)](https://gitlab.com/elad.noor/component-contribution/commits/develop)

[![coverage report](https://gitlab.com/elad.noor/component-contribution/badges/develop/coverage.svg)](https://gitlab.com/elad.noor/component-contribution/commits/develop)

[![Join the chat at https://gitter.im/equilibrator-devs/component-contribution](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/equilibrator-devs/component-contribution?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A method for estimating the standard reaction Gibbs energy of biochemical reactions. 

## Cite us

For more information on the method behind component-contribution, please view our open
access paper:

Noor E, Haraldsdóttir HS, Milo R, Fleming RMT (2013)
[Consistent Estimation of Gibbs Energy Using Component Contributions](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003098),
PLoS Comput Biol 9:e1003098, DOI: 10.1371/journal.pcbi.1003098

Please, cite this paper if you publish work that uses `component-contribution`.

## Installation

* `pip install component-contribution`

## Dependencies

* Python 3.6+
* PyPI dependencies for prediction:
  - equilibrator-cache
  - numpy
  - scipy
  - pandas
  - pint
  - path
  - periodictable
  - uncertainties
* PyPI dependencies for training a new model:
  - openbabel
  - equilibrator-assets

## Data sources

* [Training data for the component contribution method](https://zenodo.org/record/3978440)
* [Chemical group definitions for the component-contribution method](https://zenodo.org/record/4010930)
