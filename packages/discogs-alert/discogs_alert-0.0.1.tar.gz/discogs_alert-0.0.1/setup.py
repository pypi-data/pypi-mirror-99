# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discogs_alert']

package_data = \
{'': ['*']}

install_requires = \
['bs4==0.0.1',
 'click==7.1.2',
 'oauthlib==3.1.0',
 'python-dotenv==0.15.0',
 'requests==2.25.1',
 'schedule==0.6.0']

setup_kwargs = {
    'name': 'discogs-alert',
    'version': '0.0.1',
    'description': 'Customised, real-time alerting for your discogs wantlist',
    'long_description': '# discogs alert\nCustomised, real-time alerting for your discogs wantlist. This app allows you to set up a fine-grained \nalerting system for your wantlist on Discogs. You can configure different tiers of priority for your\nwantlist items, customize the notification protocol, and sync directly from your Discogs watchlist \nto easily search for releases. \n\nYou can configure notifications in the following categories:\n- `notify_on_sight`: get a notification as soon as a release goes on sale in the marketplace\n- `notify_below_threshold`:  get notified if a particular release goes on sale below a certain price\n\nas well as set up a number of different per-release filters (media/sleeve condition, maximum price, \nseller location) to completely customize the notifications you wish to receive. Finally, you can \nconfigure notifications to be sent in a number of different ways: push notifications, email, and \nslack are all supported in version 1.0.  \n\n### 1 Self-Hosted Approach\n\n\n### 3. Coming Soon\n\n\n',
    'author': 'mhsb',
    'author_email': 'michael.h.s.ball@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
