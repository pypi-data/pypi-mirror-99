# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wusa']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'docker>=4.4.0,<5.0.0',
 'gidgethub>=5.0.0,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.11.1,<10.0.0',
 'shortuuid>=1.0.1,<2.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['wusa = wusa.main:app']}

setup_kwargs = {
    'name': 'wusa',
    'version': '0.0.4',
    'description': 'CLI for managing containerized self-hosted GitHub Actions Runner',
    'long_description': '# Wusa\n\n> Isis (Ancient Egyptian: ꜣst; Coptic: Ⲏⲥⲉ Ēse; Classical Greek: Ἶσις Isis; Meroitic: 𐦥𐦣𐦯\u200e Wos[a] or <span style="text-decoration: underline;">Wusa</span>) was a major goddess in ancient Egyptian religion whose worship spread throughout the Greco-Roman world.\n>\n> Source: [Wikipedia](https://en.wikipedia.org/wiki/Isis)\n\n![Demo video for Wusa](docs/assets/wusa_demo.gif)\n\nWusa is also a command-line tool to help manage _containerized self-hosted GitHub Action Runner_. In some rare cases, you might require special hardware to execute your CI/CD pipeline. For these cases, `wusa` removes the burden of setting up a docker container on your local machine, connecting it to your GitHub repositories, and managing it over time.\n\n> **WARNING** wusa is in the early stages, and issues might appear. Please try it out and let me know what you think of wusa.\n\n## Installation\n\nIf you wish to install wusa, use pip\n\n```shell\npip install wusa\n```\n\nor use [pipx](https://github.com/pipxproject/pipx)\n\n```shell\npipx install wusa\n```\n\n## Usage\n\nWusa uses, at the moment, a ubuntu image with the GitHub Action runners. Wusa requires permission to be able to create runners for you. For this, run the following command and follow the steps:\n\n```shell\nwusa auth\n```\n\nAfterward, you can create a containerized docker runner for a repo by running\n\n```shell\nwusa create "ahelm/wusa"\n```\n\nWith `"ahelm/wusa"` is the short name of the repository.\n\nIf you wish to list all the runner for a repository, run\n\n```shell\nwusa list-repo "ahelm/wusa"\n```\n\nor if you wish to remove a runner\n\n```shell\nwusa remove <some_runner_name>\n```\n',
    'author': 'Anton Helm',
    'author_email': 'anton.helm@tecnico.ulisboa.pt',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
