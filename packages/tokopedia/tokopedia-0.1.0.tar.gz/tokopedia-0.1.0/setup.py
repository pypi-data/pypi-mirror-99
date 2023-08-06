# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tokopedia']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tokopedia',
    'version': '0.1.0',
    'description': 'Python SDK for Tokopedia Seller API ',
    'long_description': '# tokopedia\n\nPython SDK for Tokopedia Seller API. This SDK allows you to integrate your system into Tokopedia\n\n## Featured API\n\n- Webhooks API: Register webhook to get notification through your system.\n- Product API: Create and manage products with/without variant.\n- Order API: Get order info and manage all incoming orders.\n- Logistic API: Manage your Third-party logistics service.\n- Shop API: View and Update Shop Information.\n- Category API: Get all product category information.\n- Interaction API: Get all messages, replies, and send a reply.\n- Statistic API: Get the statistics of your transactions and buyers.\n',
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
