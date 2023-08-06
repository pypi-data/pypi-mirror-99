# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pesto', 'pesto.src']

package_data = \
{'': ['*']}

modules = \
['terminal', 'logo']
install_requires = \
['PyHamcrest>=2.0.2,<3.0.0',
 'color-terminal>=1.0,<2.0',
 'coverage>=5.5,<6.0',
 'thesmuggler>=1.0.1,<2.0.0',
 'tqdm>=4.59.0,<5.0.0',
 'typer[all]>=0.3.2,<0.4.0',
 'watchdog>=2.0.2,<3.0.0']

entry_points = \
{'console_scripts': ['pesto = main:app']}

setup_kwargs = {
    'name': 'pesto-testing',
    'version': '0.1.3',
    'description': 'Who says writing tests should be boring? Introducing Pest, a lightweight, fun-to-use Python testing framework referenced from the popular JS Jest library.',
    'long_description': '# Pesto\n\n<p align="center" width="100%">\n  <img src="./logo.png" width="150">\n</p>\n\n<p align="center" width="100%">\n<a href="https://coveralls.io/github/addy999/Pesto"><img alt="Coverage Status" src="https://coveralls.io/repos/github/addy999/Pesto/badge.svg"></a>\n<a href="https://travis-ci.com/addy999/Pesto"><img alt="Build Status" src="https://travis-ci.com/addy999/Pest.svg?branch=main"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n<a href="https://github.com/psf/black/blob/master/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>\n<p align="center" width="100%">🚧 Under Development 🚧</p>\n</p>\n\n### A lightweight, fun-to-use Python testing framework made to use like the popular JS Jest library.\n<br>\n\n\n## Why?\nComing back to software development after being a front-end engineer opened my eyes on how verbose and anti-user-friendly Python testing really is - in my opinion.\n\nI want to enjoy writing tests as much as I loved them with my front-end stack, so I decided to create a little testing framework to mimic that behavior, while still being a robust testing tool.\n\n## Get Started\n\nThe CLI is very similar to PyTest. Simply give the directory of the tests as the first argument (or `./` is used by default.)\n\n**A drag and drop replacement for PyTest**\n\nPesto looks for test files and functions with `_test` or `test_` in the name.\n\n```bash\npip install pesto\npesto <test-dir>\n```\n\n<p align="center" width="100%">\n  <img src="./terminal.gif">\n</p>\n\n\n## Development\nI\'m still a novice when it comes to testing, so the capabilities of this library will grow as I grow as a developer\n\n\n## Todo\n### General\n\n- [ ] Add multiprocessing support to run tests in parallel\n- [ ] Create github action\n- [ ] Add Poetry\n\n### unittest / pytest like functionality:\n- [ ] Mocking (integrate unittest.mock)\n',
    'author': 'Addy Bhatia',
    'author_email': 'jude.addy999@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/addy999/Pesto',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
