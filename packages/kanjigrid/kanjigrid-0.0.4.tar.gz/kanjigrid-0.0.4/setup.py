# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kanjigrid']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0']

entry_points = \
{'console_scripts': ['greet = kanjigrid.kanjigrid:greet']}

setup_kwargs = {
    'name': 'kanjigrid',
    'version': '0.0.4',
    'description': 'Create Kanji Grids out of Text',
    'long_description': '# kanjigrid\nCreate Kanji Grids out of Text\n',
    'author': 'exc4l',
    'author_email': 'cps0537@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/exc4l/kanjigrid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
