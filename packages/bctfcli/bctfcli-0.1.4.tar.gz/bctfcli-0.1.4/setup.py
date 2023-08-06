# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['bctfcli']
install_requires = \
['coloredlogs>=15.0,<16.0',
 'humanize>=3.2.0,<4.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.1,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer>=0.3.2,<0.4.0',
 'typing-extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['bctf = bctfcli:app']}

setup_kwargs = {
    'name': 'bctfcli',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Riatre Foo',
    'author_email': 'foo@riat.re',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
