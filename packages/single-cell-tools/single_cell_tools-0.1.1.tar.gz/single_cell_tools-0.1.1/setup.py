# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['single_cell_tools']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.3,<2.0.0']

setup_kwargs = {
    'name': 'single-cell-tools',
    'version': '0.1.1',
    'description': 'A package for pseudotime and dimension reduction by cluster centroids',
    'long_description': '# single-cell-tools \n\n![](https://github.com/whtns/single-cell-tools/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/whtns/single-cell-tools/branch/main/graph/badge.svg)](https://codecov.io/gh/whtns/single-cell-tools) [![Deploy](https://github.com/whtns/single-cell-tools/actions/workflows/deploy.yml/badge.svg)](https://github.com/whtns/single-cell-tools/actions/workflows/deploy.yml) [![Documentation Status](https://readthedocs.org/projects/single-cell-tools/badge/?version=latest)](https://single-cell-tools.readthedocs.io/en/latest/?badge=latest)\n\nA package for pseudotime and dimension reduction by cluster centroids\n\n## Installation\n\n```bash\n$ pip install -i https://test.pypi.org/simple/ single-cell-tools\n```\n\n## Features\n\n- TODO\n\n## Dependencies\n\n- TODO\n\n## Usage\n\n- TODO\n\n## Documentation\n\nThe official documentation is hosted on Read the Docs: https://single-cell-tools.readthedocs.io/en/latest/\n\n## Contributors\n\nWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/whtns/single-cell-tools/graphs/contributors).\n\n### Credits\n\nThis package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).\n',
    'author': 'Kevin Stachelek',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whtns/single-cell-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
