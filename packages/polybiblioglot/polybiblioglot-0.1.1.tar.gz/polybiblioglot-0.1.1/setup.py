# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['polybiblioglot', 'polybiblioglot.components', 'polybiblioglot.lang']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0',
 'dearpygui==0.6.123',
 'pdf2image>=1.14.0,<2.0.0',
 'pytesseract>=0.3.7,<0.4.0',
 'requests>=2.25.1,<3.0.0',
 'translate>=3.5.0,<4.0.0']

setup_kwargs = {
    'name': 'polybiblioglot',
    'version': '0.1.1',
    'description': 'A tool to translate scanned books',
    'long_description': None,
    'author': 'Bruno Robert',
    'author_email': 'bruno.jeanluke@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
