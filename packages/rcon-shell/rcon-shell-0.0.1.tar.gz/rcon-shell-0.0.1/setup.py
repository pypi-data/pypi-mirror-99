# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_rcon_shell', 'py_rcon_shell.tests']

package_data = \
{'': ['*']}

install_requires = \
['dev-shell', 'rcon']

entry_points = \
{'console_scripts': ['devshell = py_rcon_shell.rcon_shell:rcon_shell_cmdloop']}

setup_kwargs = {
    'name': 'rcon-shell',
    'version': '0.0.1',
    'description': 'Minecraft rcon shell in Python',
    'long_description': '# PyRconShell\n\nMinecraft rcon shell in Python using:\n\n* https://github.com/conqp/rcon\n* https://github.com/jedie/dev-shell\n\nWorks on Linux, macOS and Windows. It requires Python 3.8 or higher.\nNote on Debian based Linux the `python3-venv` package is needed.\n\n\n## usage\n\nBootstrap and use PyRconShell, e.g.:\n\n```bash\n~$ git clone https://github.com/jedie/PyRconShell.git\n~$ cd PyRconShell\n~/PyRconShell$ ./rcon-shell.py\n\n...\n\nDeveloper shell - py_rcon_shell - v0.0.1\n\n...\n\n(py_rcon_shell) rcon list\nSend: list\nResponse:\n----------------------------------------------------------------------------------------------------\nThere are 3 of a max of 10 players online: Foo, Bar, JohnDoe\n----------------------------------------------------------------------------------------------------\n\n(py_rcon_shell) rcon op JohnDoe\nSend: op JohnDoe\nResponse:\n----------------------------------------------------------------------------------------------------\nMade JohnDoe a server operator\n----------------------------------------------------------------------------------------------------\n```\n\n\n## Activate rcon server\n\nTo enable rcon in your `server.properties` change this:\n```\nenable-rcon=true\nrcon.port=25575\nrcon.password=a-password-is-needed\n```\nNote a password must be set! A empty password will disable rcon!\n\n\nAdd these settings into: `~/.PyRconShell.ini`, e.g.:\n\n```ini\n[DEFAULT]\nrcon_host = 127.0.0.1\nrcon_port = 25575\nrcon_password = a-password-is-needed\n```\n\n\n## hints\n\nCheck if rcon listen with e.g.:\n\n```bash\n$ lsof -i\n```\n\n\n## Links\n\n* https://minecraft.gamepedia.com/Commands#List_and_summary_of_commands\n\n\n## Project links\n\n* Github: https://github.com/jedie/PyRconShell\n* PyPi: https://pypi.org/project/rcon-shell/',
    'author': 'Jens Diemer',
    'author_email': 'python@jensdiemer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jedie/PyRconShell',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0.0',
}


setup(**setup_kwargs)
