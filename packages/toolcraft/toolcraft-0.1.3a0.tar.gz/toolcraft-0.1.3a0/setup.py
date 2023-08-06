# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'toolcraft']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'dearpygui>=0.6.281,<0.7.0',
 'tqdm>=4.59.0,<5.0.0',
 'typer',
 'yaspin>=1.4.1,<2.0.0']

entry_points = \
{'console_scripts': ['toolcraft = toolcraft.cli:main']}

setup_kwargs = {
    'name': 'toolcraft',
    'version': '0.1.3a0',
    'description': 'Top-level package for toolcraft.',
    'long_description': '=========\ntoolcraft\n=========\n\n\n.. image:: https://img.shields.io/pypi/v/toolcraft.svg\n        :target: https://pypi.python.org/pypi/toolcraft\n\n.. image:: https://img.shields.io/travis/SpikingNeuron/toolcraft.svg\n        :target: https://travis-ci.com/SpikingNeuron/toolcraft\n\n.. image:: https://readthedocs.org/projects/toolcraft/badge/?version=latest\n        :target: https://toolcraft.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n.. image:: https://pyup.io/repos/github/SpikingNeuron/toolcraft/shield.svg\n     :target: https://pyup.io/repos/github/SpikingNeuron/toolcraft/\n     :alt: Updates\n\n\n\nCraft your tools with GUI, rest-api and CLI.\n\n\n* Free software: BSD-3-Clause\n* Documentation: https://toolcraft.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Praveen Kulkarni',
    'author_email': 'praveenneuron@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SpikingNeuron/toolcraft',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0',
}


setup(**setup_kwargs)
