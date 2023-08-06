# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['makeh']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['makeh = makeh:run']}

setup_kwargs = {
    'name': 'makeh',
    'version': '0.2.0',
    'description': 'Online documentation for GNU Makefiles',
    'long_description': None,
    'author': 'Jackson Gilman',
    'author_email': 'jackson.j.gilman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
