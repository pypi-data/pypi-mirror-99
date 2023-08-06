# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tg_tool']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['tg-tool = tg_tool.main:app']}

setup_kwargs = {
    'name': 'tg-tool',
    'version': '0.2.4',
    'description': '',
    'long_description': '# `tg-tool`\n\nAwesome Portal Gun\n\n**Usage**:\n\n```console\n$ tg-tool [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `load`: Load the portal gun\n* `shoot`: Shoot the portal gun\n\n## `tg-tool load`\n\nLoad the portal gun\n\n**Usage**:\n\n```console\n$ tg-tool load [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `tg-tool shoot`\n\nShoot the portal gun\n\n**Usage**:\n\n```console\n$ tg-tool shoot [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n',
    'author': 'sellercoder',
    'author_email': 'veniamin4e@gmail.com',
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
