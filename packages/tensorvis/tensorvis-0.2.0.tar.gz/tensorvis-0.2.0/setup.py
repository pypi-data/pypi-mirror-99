# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tensorvis', 'tensorvis.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'pandas>=1.1.4,<2.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'tensorboard>=2.4.0,<3.0.0']

entry_points = \
{'console_scripts': ['tensorvis = tensorvis.vis:cli']}

setup_kwargs = {
    'name': 'tensorvis',
    'version': '0.2.0',
    'description': 'Visualisation tool to support my PhD automating the process of gathering data and plotting it',
    'long_description': "# Tensorplot\nA visualisation tool to automate the process of grabbing tensorboard events\ndata and visualising them.  This allows for faster result analysis in my work.\n\n## Features\n* Upload experiments logged with PyTorch's SummaryWriter to tensorboard.dev and creates a log of uploaded experiments.\n* \n\n## Notes\nThis is still in its early stages so if a problem arises don't forget to create an issue!\n\n## Contributing\nIf anyone wants to contribute in any way then feel free to open a PR or an issue and we can discuss it.\n\n## Benefits\n1. Faster result analysis\n2. Less code writting\n3. Separate experiments from analysis\n4. Allows for more research tim\n",
    'author': 'Nikolas Pitsillos',
    'author_email': 'npitsillos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/npitsillos/tensorplot.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
