# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_fonts']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1', 'manim>=0.3.0', 'requests>=2.0.0']

entry_points = \
{'manim.plugins': ['manim_fonts = manim_fonts']}

setup_kwargs = {
    'name': 'manim-fonts',
    'version': '0.1.0',
    'description': 'Use Google Fonts With Manim.',
    'long_description': None,
    'author': 'Naveen M K',
    'author_email': 'naveen@syrusdark.website',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/naveen521kk/manim-fonts',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
