# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['receipt_parser_core']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0',
 'numpy>=1.19.4,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'pytesseract>=0.3.6,<0.4.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pyyaml>=5.3,<6.0',
 'terminaltables>=3.1.0,<4.0.0',
 'wand>=0.6.3,<0.7.0']

entry_points = \
{'console_scripts': ['run = receipt_parser_core:main']}

setup_kwargs = {
    'name': 'receipt-parser-core',
    'version': '0.1.6',
    'description': 'A supermarket receipt parser written in Python using tesseract OCR',
    'long_description': None,
    'author': 'Matthias Endler',
    'author_email': 'matthias-endler@gmx.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
