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
    'version': '0.1.0.post2',
    'description': 'Use Google Fonts With Manim.',
    'long_description': '# Manim Fonts\n\nGet fonts on the fly from the internet which can be used with Manim.\n\n<p align="center">\n    <a href="https://pypi.org/project/manim-fonts/"><img src="https://img.shields.io/pypi/v/manim.svg?style=flat&logo=pypi" alt="PyPI Latest Release"></a>\n    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">\n</p>\n\n## Example\n\n```py\nfrom manim import *\nfrom manim_fonts import *\nclass Example(Scene):\n    def construct(self):\n        with RegisterFont("Poppins") as fonts:\n            a=Text("Hello World",font=fonts[0])\n            self.play(Write(a))\n```\nYou can replace `Poppins` with any font available on Google Fonts for example `RegisterFont("Berkshire Swash")`, and this plugin will download that font and add to search path and returns the font names that can be passed to `Text` to directly to use the fonts.\n\nThe fonts downloaded are cached and are reused.\n\n## License\n\nThis project is license under [BSD 3-Clause License](https://choosealicense.com/licenses/bsd-3-clause/).',
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
