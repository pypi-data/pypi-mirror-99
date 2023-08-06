# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openrpa']

package_data = \
{'': ['*']}

install_requires = \
['craft-text-detector>=0.3.3,<0.4.0',
 'mss>=6.1.0,<7.0.0',
 'numpy>=1.20.1,<2.0.0',
 'opencv-python>=4.5.1.48,<5.0.0.0',
 'pynput>=1.7.3,<2.0.0',
 'pytesseract>=0.3.7,<0.4.0',
 'regex>=2020.11.13,<2021.0.0']

setup_kwargs = {
    'name': 'openrpa',
    'version': '0.3.1',
    'description': 'Pixel based automation library testbed',
    'long_description': '# Welcome to OpenRPA\n\n_Pixel based RPA automation library_\n\nOpenRPA is a Robot Framework library that can automate desktop\ntasks with state of the art AI. OpenRPA is totally free for use in\ncommercial and non-commercial applications. Development is sponsored \nby Robocorp with a long term agreement.\n\nOpenRPA development started in 2019 and now - 2 years later - we are\npublishing the results by making all components available as a seamless\nautomation library.\n\nCurrent components:\n\n- Text detection\n- Text recognition\n- Image detection\n- Controller primitives for mouse and keyboard\n\nIntegration roadmap\n\n- Locator query language and NLP\n- Extracting and classification of user interface elements\n\nLibrary is available for\n\n- Windows\n- MacOS\n- Linux\n\n### Keywords\n\n```\nClick Word  pattern\nClick Image  filename\n```\n\n### Examples of Locator Query Language (LQL)\n\n```\nType Text  Customer id  12345\nMouse Left Click  Description  To Right\nMouse Left Click  money.png  Close to Submit\n```\n\n## Installation\n\n```\nchannels:\n  - conda-forge\n  - pytorch\n  - fcakyon\ndependencies:\n  - python=3.7.5\n  - python-mss=6.1.0\n  - numpy=1.20.1\n  - craft-text-detector=0.3.3\n  - tesseract=4.1.1\n  - pytesseract=0.3.7\n  - opencv=4.5.1\n  - regex=2020.11.13\n  - pynput=1.7.1\n  - pyobjc-core=6.2.2\n```',
    'author': 'Teppo Koskinen',
    'author_email': 'teppo@robocorp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
