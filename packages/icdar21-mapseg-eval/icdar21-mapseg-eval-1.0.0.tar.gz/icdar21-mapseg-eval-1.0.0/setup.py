# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['icdar21_mapseg_eval']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.20.1,<2.0.0',
 'pandas>=1.1,<2.0',
 'progress',
 'scikit-image>=0.18.1,<0.19.0',
 'scipy>=1.6.1,<2.0.0']

extras_require = \
{'visualisation': ['PyQt5>=5.15.4,<6.0.0']}

entry_points = \
{'console_scripts': ['icdar21-mapseg-eval = icdar21_mapseg_eval:main']}

setup_kwargs = {
    'name': 'icdar21-mapseg-eval',
    'version': '1.0.0',
    'description': 'Evaluation tools for ICDAR21 Competition on Historical Map Segmentation (MapSeg).',
    'long_description': None,
    'author': 'icdar21-mapseg-contact(at)googlegroups.com',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
