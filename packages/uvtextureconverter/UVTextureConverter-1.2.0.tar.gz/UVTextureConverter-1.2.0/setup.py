# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['UVTextureConverter']

package_data = \
{'': ['*'], 'UVTextureConverter': ['config/*', 'mapping_relations/*']}

install_requires = \
['numpy', 'scipy', 'tqdm']

setup_kwargs = {
    'name': 'uvtextureconverter',
    'version': '1.2.0',
    'description': 'To convert atlas texuture (defined in Densepose) to normal texture (defined in SMPL), and vice versa.',
    'long_description': None,
    'author': 'Shizuma Kubo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kuboshizuma/UVTextureConverter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
