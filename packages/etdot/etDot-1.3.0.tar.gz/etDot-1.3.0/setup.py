# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['etdot']

package_data = \
{'': ['*'],
 'etdot': ['cpp_dotc/CMakeLists.txt',
           'cpp_dotc/CMakeLists.txt',
           'cpp_dotc/CMakeLists.txt',
           'cpp_dotc/dotc.cpp',
           'cpp_dotc/dotc.cpp',
           'cpp_dotc/dotc.cpp',
           'cpp_dotc/dotc.rst',
           'cpp_dotc/dotc.rst',
           'cpp_dotc/dotc.rst',
           'f90_dotf/CMakeLists.txt',
           'f90_dotf/CMakeLists.txt',
           'f90_dotf/CMakeLists.txt',
           'f90_dotf/dotf.f90',
           'f90_dotf/dotf.f90',
           'f90_dotf/dotf.f90',
           'f90_dotf/dotf.rst',
           'f90_dotf/dotf.rst',
           'f90_dotf/dotf.rst']}

install_requires = \
['et-micc-build>=1.1.3,<2.0.0', 'numpy>=1.20.1,<2.0.0']

setup_kwargs = {
    'name': 'etdot',
    'version': '1.3.0',
    'description': '<Enter a one-sentence description of this project here.>',
    'long_description': '=====\netDot\n=====\n\nCompute the dot product of two arrays.\n\n* Free software: MIT license\n',
    'author': 'Bert Tijskens',
    'author_email': 'engelbert.tijskens@uantwerpen.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/etijskens/etDot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
