# cgmodels

![Tests][tests-badge] [![codecov][codecov-badge]][codecov-url][![CodeFactor][codefactor-badge]][codefactor-url][![Code style: black][black-badge]][black-url]

Library that work as an interface between services at Clinical Genomics. 
In most cases where multiple services needs access to a common API, those models should be defined here.

## Usage

Currently **cgmodels** support contracts for the following applications:

- crunchy
- demultiplex

## Installation

### Pypi

```
pip install cgmodels
```

### Github

Install [poetry][poetry]

```
git clone https://github.com/Clinical-Genomics/cgmodels
poetry install 
```


[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black 
[codefactor-badge]: https://www.codefactor.io/repository/github/clinical-genomics/cgmodels/badge
[codefactor-url]: https://www.codefactor.io/repository/github/clinical-genomics/cgmodels
[tests-badge]: https://github.com/Clinical-Genomics/cgmodels/workflows/Tests/badge.svg
[codecov-badge]: https://codecov.io/gh/Clinical-Genomics/cgmodels/branch/main/graph/badge.svg?token=MA62EOQTX7
[codecov-url]: https://codecov.io/gh/Clinical-Genomics/cgmodels
[poetry]: https://python-poetry.org/docs/#installation