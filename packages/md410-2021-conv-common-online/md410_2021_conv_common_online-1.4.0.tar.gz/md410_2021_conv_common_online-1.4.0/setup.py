# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['md410_2021_conv_common_online']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'psycopg2-binary>=2.8.4,<3.0.0',
 'sqlalchemy>=1.3.12,<2.0.0']

setup_kwargs = {
    'name': 'md410-2021-conv-common-online',
    'version': '1.4.0',
    'description': 'Common libraries for applications related to the 2021 Lions MD410 Online Convention',
    'long_description': '# Introduction\n\nCommon libraries for applications related to the [2021 Lions Multiple District 410 Online Conventions](https://www.lionsconvention2021.co.za/).\n\n# Associated Applications\n\nSee [this Gitlab group](https://gitlab.com/md410_2021_conv) for associated applications.\n',
    'author': 'Kim van Wyk',
    'author_email': 'vanwykk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/md410_2021_conv/md410_2021_conv_common_online',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
