# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['codehash']

package_data = \
{'': ['*']}

install_requires = \
['typing_extensions>=3.6,<4.0']

setup_kwargs = {
    'name': 'codehash',
    'version': '0.1.0',
    'description': 'Hashing Python code',
    'long_description': '# Codehash\n\n## Installing\n\nInstall and update using [Pip](https://pip.pypa.io/en/stable/quickstart/).\n\n```\npip install -U codehash\n```\n\n## A simple example\n\n```python\nfrom codehash import hash_function\n\ndct = {\'a\': 1}\n\ndef f(x):\n    return 1 + dct["param"]\n\nh1 = hash_function(f)\n\ndef f(x):\n    """Docstring."""\n    return 1 + dct["param"]  # comment\n\nh2 = hash_function(f)\n\ndct = {\'a\': 2}\n\ndef f(x):\n    return 1 + dct["param"]\n\nh3 = hash_function(f)\n\nassert h1 == h2\nassert h1 != h3\n```\n',
    'author': 'Jan Hermann',
    'author_email': 'dev@jan.hermann.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jhrmnn/codehash',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
