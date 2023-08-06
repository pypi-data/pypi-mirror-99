# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skripsi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'skripsi',
    'version': '0.1.0',
    'description': 'Alat bantu skripsi berbasis python',
    'long_description': '# skripsi\n\nAlat bantu skripsi berbasis python.\n\nAplikasi ini masih dalam tahap pengembangan awal!\n',
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
