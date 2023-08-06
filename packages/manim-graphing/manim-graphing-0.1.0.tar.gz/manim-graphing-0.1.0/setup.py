# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_graphing', 'manim_graphing.graphs']

package_data = \
{'': ['*']}

install_requires = \
['manim>=0.3.0']

entry_points = \
{'manim.plugins': ['manim_graphing = manim_graphing']}

setup_kwargs = {
    'name': 'manim-graphing',
    'version': '0.1.0',
    'description': 'A Manim Plugin for Graphing',
    'long_description': '# manim-graphing',
    'author': 'GameDungeon',
    'author_email': 'gamedungeon@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GameDungeon/manim-graphing',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
