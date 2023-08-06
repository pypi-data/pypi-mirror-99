# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mixbag']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.33,<2.0.0']

setup_kwargs = {
    'name': 'mixbag',
    'version': '0.0.0a0',
    'description': '',
    'long_description': "# MixBag\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![codecov](https://codecov.io/gh/anthonyalmarza/mixbag/branch/main/graph/badge.svg?token=JRCC98L3FG)](https://codecov.io/gh/anthonyalmarza/mixbag)\n![Build](https://github.com/anthonyalmarza/mixbag/workflows/Build/badge.svg)\n\n## Local Development\n\n### Pyenv\nIt's recommended that you use [pyenv](https://github.com/pyenv/pyenv)\n\n[pyenv-installer](https://github.com/pyenv/pyenv-installer)\n```bash\ncurl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash\n```\n\n### Install Poetry\n\nThis project uses [poetry](https://python-poetry.org). Install it using the following command.\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n```\nMore instructions [here](https://python-poetry.org/docs/#installation).\n\n### Install Dependencies\n\n```shell\npoetry install\n```\n\n### Install pre-commit hooks\n\n```shell\npoetry run pre-commit install --hook-type commit-msg\n\npoetry run pre-commit install\n\n```\n\n### Running Tests\n\n```shell\npoetry run pyscript tests\n```\n\n### Build Docs\n\n```shell\npoetry run pyscript docs_build\n```\n",
    'author': 'Anthony Almarza',
    'author_email': 'anthony.almarza@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
