# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dev_shell', 'dev_shell.command_sets', 'dev_shell.tests', 'dev_shell.utils']

package_data = \
{'': ['*']}

install_requires = \
['cmd2']

extras_require = \
{':sys_platform == "darwin"': ['gnureadline']}

entry_points = \
{'console_scripts': ['devshell = dev_shell.dev_shell_app:devshell_cmdloop']}

setup_kwargs = {
    'name': 'dev-shell',
    'version': '0.0.1',
    'description': 'Devloper shell for easy startup...',
    'long_description': '# A "dev-shell" for Python projects ;)\n\n[![pytest](https://github.com/jedie/dev-shell/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/jedie/dev-shell/actions?query=branch%3Amain)\n[![codecov](https://codecov.io/gh/jedie/dev-shell/branch/main/graph/badge.svg)](https://codecov.io/gh/jedie/dev-shell)\n\nThis small project is intended to improve the start-up for collaborators.\n\nThe idea is to make the project setup as simple as possible. Just clone the sources and start a script and you\'re done ;)\n\nRun Tests? Just start the script and call the "run test command".\n\nThe "dev-shell" is the base to create a CLI and a shell. It also\n\nIt also shows how to make a project bootstrap as simply as possible, e.g.:\n\n```bash\n~$ git clone https://github.com/jedie/dev-shell.git\n~$ cd dev-shell\n~/dev-shell$ ./dev-shell.py pytest\n```\n\n\n## How it works\n\nFirst start of the Python script [./dev-shell.py](https://github.com/jedie/dev-shell/blob/main/dev-shell.py) will bootstrap:\n\n* Generate a Python virtual environment (in short: `venv`)\n* Install poetry\n* Install project dependencies and the project himself\n\nThe output on first bootstrap start looks like:\n\n```bash\n~/dev-shell$ ./dev-shell.py\nCreate venv here: ~/dev-shell/.venv\nCollecting pip\n...\nSuccessfully installed pip-21.0.1\nCollecting poetry\n...\nInstalling dependencies from lock file\n\nPackage operations: 31 installs, 1 update, 0 removals\n\n...\n\nInstalling the current project: dev-shell (0.0.1alpha0)\n\n\nDeveloper shell - dev_shell - v0.0.1alpha0\n\n\nDocumented commands (use \'help -v\' for verbose/\'help <topic>\' for details):\n\nPublish\n=======\npublish\n\nTests\n=====\npytest\n\n...\n\n(dev_shell) quit\n~/dev-shell$\n```\n\nThe first bootstrap start takes a few seconds. Each later startup detects the existing virtualenv and is very fast:\n\n```bash\n~/dev-shell$ ./dev-shell.py\n\nDeveloper shell - dev_shell - v0.0.1alpha0\n\n(dev_shell)\n~/dev-shell$ ./dev-shell.py --update\n```\n\n\nTo update existing virtualenv, call with `--update`:\n\n```bash\n~/dev-shell$ ./dev-shell.py --update\n```\n\nOr just delete `/.venv/` and start `dev-shell.py` ;)\n\n## compatibility\n\n| dev-shell version | OS                      | Python version |\n|-------------------|-------------------------|----------------|\n| v0.0.1            | Linux + MacOS + Windows | 3.9, 3.8, 3.7  |\n\nSee also github test configuration: [.github/workflows/test.yml](https://github.com/jedie/dev-shell/blob/main/.github/workflows/test.yml)\n\n## History\n\n* [*dev*](https://github.com/jedie/dev-shell/compare/v0.0.1...master)\n  * TBC\n* [v0.0.1 - 2021-03-19](https://github.com/jedie/poetry-publish/compare/ad5dca...v0.0.1)\n  * first "useable" version\n\n## Project links\n\n* Github: https://github.com/jedie/dev-shell/\n* PyPi: https://pypi.org/project/dev-shell/\n',
    'author': 'Jens Diemer',
    'author_email': 'python@jensdiemer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
