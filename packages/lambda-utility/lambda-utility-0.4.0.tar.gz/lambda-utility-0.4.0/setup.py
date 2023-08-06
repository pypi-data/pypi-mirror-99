# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lambda_utility']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0', 'slack-sdk>=3.4.2,<4.0.0']

setup_kwargs = {
    'name': 'lambda-utility',
    'version': '0.4.0',
    'description': '',
    'long_description': '# lambda-utility\n[![Python](https://img.shields.io/badge/python-v3.9-blue.svg?&logo=python&style=flat)](https://docs.python.org/3.9/)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n## Requirements\n- Python 3.7 +\n',
    'author': 'Kyungmin Lee',
    'author_email': 'rekyungmin@gmail.com',
    'maintainer': 'Kyungmin Lee',
    'maintainer_email': 'rekyungmin@gmail.com',
    'url': 'https://github.com/rekyungmin/lambda-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
