# MixBag

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/anthonyalmarza/mixbag/branch/main/graph/badge.svg?token=JRCC98L3FG)](https://codecov.io/gh/anthonyalmarza/mixbag)
![Build](https://github.com/anthonyalmarza/mixbag/workflows/Build/badge.svg)

## Local Development

### Pyenv
It's recommended that you use [pyenv](https://github.com/pyenv/pyenv)

[pyenv-installer](https://github.com/pyenv/pyenv-installer)
```bash
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

### Install Poetry

This project uses [poetry](https://python-poetry.org). Install it using the following command.
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
More instructions [here](https://python-poetry.org/docs/#installation).

### Install Dependencies

```shell
poetry install
```

### Install pre-commit hooks

```shell
poetry run pre-commit install --hook-type commit-msg

poetry run pre-commit install

```

### Running Tests

```shell
poetry run pyscript tests
```

### Build Docs

```shell
poetry run pyscript docs_build
```
