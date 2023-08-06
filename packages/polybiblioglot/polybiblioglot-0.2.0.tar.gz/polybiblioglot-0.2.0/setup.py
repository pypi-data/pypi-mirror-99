# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polybiblioglot', 'polybiblioglot.components', 'polybiblioglot.lang']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0',
 'dearpygui==0.6.123',
 'pdf2image>=1.14.0,<2.0.0',
 'pytesseract>=0.3.7,<0.4.0',
 'requests>=2.22.0,<3.0.0',
 'translate>=3.5.0,<4.0.0']

setup_kwargs = {
    'name': 'polybiblioglot',
    'version': '0.2.0',
    'description': 'A tool to translate scanned books',
    'long_description': "[![CodeQL](https://github.com/bruno-robert/polybiblioglot/actions/workflows/codeql-analysis.yml/badge.svg?branch=master)](https://github.com/bruno-robert/polybiblioglot/actions/workflows/codeql-analysis.yml)\n# polybiblioglot\n\nA OCR tool to convert books scans into text and automatically translate them.\n\n# Installation / Setup\n\n## Requirements\n\n### Tesseract\n\npolybiblioglot uses tesseract for OCR, you will need to follow the steps described [here](https://github.com/tesseract-ocr/tesseract#installing-tesseract) to install tesseract.\n\nOn macos, you may find [this gist](https://gist.github.com/henrik/1967035) useful.\n\n### Poppler\n\nPoppler is a pdf renderer. In this case, we use it to convert pdf's to images for processing.\nIf you are only converting images, it isn't needed. Please note that the program may crash if you don't install poppler\nand attempt to convert a pdf.\n\nThe [pdf2image](https://github.com/Belval/pdf2image) github explains how to install poppler depending on what platform you are on.\nIf you are on mac and have brew installed. It's as simple as `brew install poppler`\n\n## Installation\n\nClone the repository:\n`git clone https://github.com/bruno-robert/polybiblioglot.git`\n\ncd into it:\n`cd polybiblioglot`\n\n(optional) create a python virtual environment:\n`python -m venv env`\nthen\n`source ./env/bin/activate`\n\ninstall python dependancies\n`pip install -r requirements.txt`\n\n# Running polybiblioglot\n\nTo run polybiblioglot, simply execute the main.py file\n`python main.py`\n\n# Notes and limitation (for now)\n\n## Limitations\n- The OCR method used is optimized for high acuracy and not speed. I might add the functionality to change this in the future.\n\n## Notes\n\n- All computationally expensive or I/O intensive tasks are run asynchronously. This keeps the UI snappy. I'm currently using the DearPyGUI asynchronous call method wich will be depricated in the next version. A migration to python's out of the box threading library will be needed at that point.\n\n",
    'author': 'Bruno Robert',
    'author_email': 'bruno.jeanluke@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bruno-robert/polybiblioglot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
