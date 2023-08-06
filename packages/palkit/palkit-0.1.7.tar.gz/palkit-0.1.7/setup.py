# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kit', 'kit.torch']

package_data = \
{'': ['*']}

install_requires = \
['hydra-core>=1.1.0.dev4,<2.0.0', 'numpy>=1.20.1,<2.0.0']

extras_require = \
{'ci': ['torch>=1.8,<2.0']}

setup_kwargs = {
    'name': 'palkit',
    'version': '0.1.7',
    'description': 'Useful functions.',
    'long_description': '# PAL kit\n\nThis is a collection of useful functions for code that we write in our group.\n\n## Install\n\nRun\n```\npip install palkit\n```\n\nor install directly from GitHub:\n```\npip install git+https://github.com/predictive-analytics-lab/palkit.git\n```\n',
    'author': 'PAL',
    'author_email': 'info@predictive-analytics-lab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/predictive-analytics-lab/palkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
