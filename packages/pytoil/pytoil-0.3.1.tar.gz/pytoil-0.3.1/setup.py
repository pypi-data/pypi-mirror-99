# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytoil',
 'pytoil.api',
 'pytoil.cli',
 'pytoil.config',
 'pytoil.environments',
 'pytoil.repo',
 'pytoil.vscode']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'cookiecutter>=1.7.2,<2.0.0',
 'httpx>=0.16.1,<0.17.0',
 'typer[all]>=0.3.2,<0.4.0',
 'virtualenv>=20.4.2,<21.0.0']

entry_points = \
{'console_scripts': ['pytoil = pytoil.cli.main:app']}

setup_kwargs = {
    'name': 'pytoil',
    'version': '0.3.1',
    'description': 'CLI to automate the development workflow.',
    'long_description': "![logo](./docs/img/logo.png)\n\n[![License](https://img.shields.io/github/license/FollowTheProcess/pytoil)](https://github.com/FollowTheProcess/pytoil)\n[![PyPI](https://img.shields.io/pypi/v/pytoil.svg)](https://pypi.python.org/pypi/pytoil)\n[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/FollowTheProcess/pytoil)\n[![CI](https://github.com/FollowTheProcess/pytoil/workflows/CI/badge.svg)](https://github.com/FollowTheProcess/pytoil/actions?query=workflow%3ACI)\n[![Coverage](docs/img/coverage.svg)](https://github.com/FollowTheProcess/pytoil)\n\n*pytoil is a small, helpful CLI to help developers manage their local and remote projects with ease!*\n\n* **Source Code**: [https://github.com/FollowTheProcess/pytoil](https://github.com/FollowTheProcess/pytoil)\n\n* **Documentation**: [https://FollowTheProcess.github.io/pytoil/](https://FollowTheProcess.github.io/pytoil/)\n\n:warning: pytoil is still in Alpha and as such, the API may change without deprecation notices.\n\n## What is it?\n\n`pytoil` is a handy tool that helps you stay on top of all your projects, remote or local. It's primarily aimed at python developers but you could easily use it to manage any project!\n\npytoil is:\n\n* Easy to use :white_check_mark:\n* Easy to configure :white_check_mark:\n* Safe (it won't edit your repos at all) :white_check_mark:\n* Useful! (I hope :smiley:)\n\nSay goodbye to janky bash scripts :wave:\n\n## Installation\n\nAs pytoil is a CLI, I recommend [pipx]\n\n```shell\npipx install pytoil\n```\n\nOr just pip (but must be globally available)\n\n```shell\npip install pytoil\n```\n\n## Quickstart\n\n`pytoil` is super easy to get started with.\n\nAfter installation just run\n\n```shell\n$ pytoil config\n\nNo config file yet!\nMaking you a default one...\n```\n\nThis will create a default config file which can be found at `~/.pytoil.yml`. See the [docs] for what information you need to put in here.\n\nDon't worry though, there's only a few options to configure! :sleeping:\n\nAfter that you're good to go! You can do things like:\n\n#### See your local and remote projects\n\n```shell\npytoil show all\n```\n\n#### See which ones you have on GitHub, but not on your computer\n\n```shell\npytoil show diff\n```\n\n#### Easily grab a project, regardless of where it is\n\n```shell\npytoil checkout my_project\n```\n\n#### Create a new project and virtual environment in one go\n\n```shell\npytoil create my_project --venv virtualenv\n\n```\n\n#### And even do this from a [cookiecutter] template\n\n```shell\npytoil create my_project --venv virtualenv --cookie https://github.com/some/cookie.git\n```\n\nCheck out the [docs] for more :boom:\n\n### Credits\n\nThis package was created with [cookiecutter](https://github.com/cookiecutter/cookiecutter) and the `FollowTheProcess/poetry_pypackage` project template.\n\n[pipx]: https://pipxproject.github.io/pipx/\n[cookiecutter]: https://cookiecutter.readthedocs.io/en/1.7.2/\n[docs]: https://FollowTheProcess.github.io/pytoil/\n",
    'author': 'Tom Fleet',
    'author_email': 'tomfleet2018@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FollowTheProcess/pytoil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
