# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twacapic', 'twacapic.templates']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'TwitterAPI>=2.6.9,<3.0.0',
 'loguru>=0.5.4,<0.6.0',
 'schedule>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['twacapic = twacapic.main:run']}

setup_kwargs = {
    'name': 'twacapic',
    'version': '0.5.4',
    'description': 'A Twitter Academic API Client',
    'long_description': '# twacapic\n\nTwitter Academic API Client\n\nIn development. Expect breaking changes and bugs when updating to the latest version.\n\nTested on Linux (Ubuntu 20.10, Python 3.8) and MacOS 11 (Python 3.9). Please [raise an issue](https://github.com/Leibniz-HBI/twacapic/issues) if you need to install it with another Python version or encounter issues with other operating systems.\n\n\n## Installation\n\nInstall via pip:\n\n`pip install twacapic`\n\n\n## Usage\n\n```txt\nusage: twacapic [-h] [-u USERLIST] [-g GROUPNAME] [-c GROUP_CONFIG]\n                [-l LOG_LEVEL] [-lf LOG_FILE] [-s SCHEDULE]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -u USERLIST, --userlist USERLIST\n                        Path to list of user IDs, one per line. Required for\n                        first run only. Can be used to add users to a group.\n  -g GROUPNAME, --groupname GROUPNAME\n                        Name of the group to collect. Results will be saved in\n                        folder `results/GROUPNAME/`. Can be used to poll for\n                        new tweets of a group. Default: "users"\n  -c GROUP_CONFIG, --group_config GROUP_CONFIG\n                        Path to a custom group config file to define tweet\n                        data to be retrieved, e.g. retweets, mentioned users,\n                        attachments. A template named `group_config.yaml` can\n                        be found in any already created group folder.\n  -l LOG_LEVEL, --log_level LOG_LEVEL\n                        Level of output detail (DEBUG, INFO, WARNING, ERROR).\n                        Warnings and Errors are always logged in respective\n                        log-files `errors.log` and `warnings.log`. Default:\n                        ERROR\n  -lf LOG_FILE, --log_file LOG_FILE\n                        Path to logfile. Defaults to standard output.\n  -s SCHEDULE, --schedule SCHEDULE\n                        If given, repeat every SCHEDULE minutes.\n```\n\nAt the moment twacapic can only collect the latest 100 tweets of a list of users and then poll for new tweets afterwards if called again with the same group name.\n\n### Authorisation with the Twitter API\n\nAt first use, it will prompt you for your API credentials, which you find [here](https://developer.twitter.com/en/portal/projects-and-apps). These credentials will be stored in a file in the working directory, so make sure that the directory is readable by you and authorised users only.\n\nFor non-interactive use, e.g. when automatically deploying twacapic to a server, this file can be used as a template and should always be placed in the working directory of twacapic.\n\n### Example\n\n`twacapic -g USER_GROUP_NAME -u PATH_TO_USER_CSV`\n\n`USER_GROUP_NAME` should be the name of the results folder that is meant to be created and will contain raw json responses from Twitter.\n\n`PATH_TO_USER_CSV` should be a path to a list of Twitter user IDs, without header, one line per user ID.\n\nAfterwards you can poll for new tweets of a user group by running simply:\n\n`twacapic -g USER_GROUP_NAME`\n\nEnjoy!\n\n\n### Config Template\n\nThe group config is a yaml file in the following form:\n\n```yaml\nfields:\n  attachments: No\n  author_id: Yes\n  context_annotations: No\n  conversation_id: No\n  created_at: No\n  entities: No\n  geo: No\n  in_reply_to_user_id: No\n  lang: No\n  non_public_metrics: No\n  organic_metrics: No\n  possibly_sensitive: No\n  promoted_metrics: No\n  public_metrics: No\n  referenced_tweets: No\n  reply_settings: No\n  source: No\n  withheld: No\nexpansions:\n  author_id: Yes\n  referenced_tweets.id: No\n  in_reply_to_user_id: No\n  attachments.media_keys: No\n  attachments.poll_ids: No\n  geo.place_id: No\n  entities.mentions.username: No\n  referenced_tweets.id.author_id: No\n```\n\nAn explanation of the fields and expansions can be found in Twitter\'s API docs:\n\n  - [Fields](https://developer.twitter.com/en/docs/twitter-api/fields)\n  - [Expansions](https://developer.twitter.com/en/docs/twitter-api/expansions)\n\n\n## Dev Install\n\n1. Install [poetry](https://python-poetry.org/docs/#installation)\n2. Clone repository\n3. In the directory run `poetry install`\n4. Run `poetry shell` to start development virtualenv\n5. Run `twacapic` to enter API keys. Ignore the IndexError.\n6. Run `pytest` to run all tests\n',
    'author': 'Felix Victor Münch',
    'author_email': 'f.muench@leibniz-hbi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Leibniz-HBI/twacapic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
