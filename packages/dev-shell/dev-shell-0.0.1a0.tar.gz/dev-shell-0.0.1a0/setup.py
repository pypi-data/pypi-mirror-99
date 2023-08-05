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
{'console_scripts': ['devshell = dev_shell.cmd2app:devshell_cmdloop']}

setup_kwargs = {
    'name': 'dev-shell',
    'version': '0.0.1a0',
    'description': 'Devloper shell for easy startup...',
    'long_description': '# A "dev-shell" for Python projects ;)\n\ntbd.',
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
