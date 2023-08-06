# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twacapic', 'twacapic.templates']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'TwitterAPI>=2.6.9,<3.0.0']

entry_points = \
{'console_scripts': ['twacapic = twacapic.main:run']}

setup_kwargs = {
    'name': 'twacapic',
    'version': '0.3.0',
    'description': 'A Twitter Academic API Client',
    'long_description': '# twacapic\n\nTwitter Academic API Client\n\nIn development. Expect breaking changes and destructive bugs when updating to the latest version.\n\n\n## Installation\n\nInstall via pip:\n\n`pip install twacapic`\n\n\n## Usage\n\n```\nusage: twacapic [-h] [-u USERLIST] [-g GROUPNAME]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -u USERLIST, --userlist USERLIST\n                        path to list of user IDs, one per line. Required for\n                        first run only. Can be used to add users to a group\n  -g GROUPNAME, --groupname GROUPNAME\n                        name of the group to collect. Results will be saved in\n                        folder `results/GROUPNAME/`. Can be used to poll for\n                        new tweets of a group. Default: "users"\n```\n\n### Example\n\nAt the moment twacapic can only collect the latest 100 tweets of a list of users and then poll for new tweets afterwards if called again with the same group name.\n\n`twacapic -g USER_GROUP_NAME -u PATH_TO_USER_CSV`\n\n`USER_GROUP_NAME` should be the name of the results folder that is meant to be created and will contain raw json responses from Twitter.\n\n`PATH_TO_USER_CSV` should be a path to a list of Twitter user IDs, without header, one line per user ID.\n\nAfterwards you can poll for new tweets of a user group by running simply:\n\n`twacapic -g USER_GROUP_NAME`\n\nEnjoy!\n\n\n## Dev Install\n\n1. Install [poetry](https://python-poetry.org/docs/#installation)\n2. Clone repository\n3. In the directory run `poetry install`\n4. Run `poetry shell` to start development virtualenv\n5. Run `twacapic` to enter API keys. Ignore the IndexError.\n6. Run `pytest` to run all tests\n',
    'author': 'Felix Victor Münch',
    'author_email': 'f.muench@leibniz-hbi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Leibniz-HBI/twacapic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
