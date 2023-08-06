# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tokopedia',
 'tokopedia.campaign',
 'tokopedia.category',
 'tokopedia.chat',
 'tokopedia.finance',
 'tokopedia.logistic',
 'tokopedia.order',
 'tokopedia.product',
 'tokopedia.product.api',
 'tokopedia.shop',
 'tokopedia.statistic',
 'tokopedia.webhook']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'cattrs>=1.3.0,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'tokopedia',
    'version': '0.4.0',
    'description': 'Python SDK for Tokopedia Seller API ',
    'long_description': '# tokopedia\n\n[![tokopedia - PyPi](https://img.shields.io/pypi/v/tokopedia)](https://pypi.org/project/tokopedia/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/tokopedia)](https://pypi.org/project/tokopedia/)\n[![LICENSE](https://img.shields.io/github/license/hexatester/tokopedia)](https://github.com/hexatester/tokopedia/blob/main/LICENSE)\n[![Tests](https://github.com/hexatester/tokopedia/actions/workflows/pytest.yml/badge.svg)](https://github.com/hexatester/tokopedia/actions/workflows/pytest.yml)\n[![codecov](https://codecov.io/gh/hexatester/tokopedia/branch/main/graph/badge.svg)](https://codecov.io/gh/hexatester/tokopedia)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Mypy](https://img.shields.io/badge/Mypy-enabled-brightgreen)](https://github.com/python/mypy)\n\nPython SDK for Tokopedia Seller API. This SDK allows you to integrate your system into Tokopedia\n\n## Featured API\n\n- Webhooks API: Register webhook to get notification through your system.\n- Product API: Create and manage products with/without variant.\n- Order API: Get order info and manage all incoming orders.\n- Logistic API: Manage your Third-party logistics service.\n- Shop API: View and Update Shop Information.\n- Category API: Get all product category information.\n- Interaction API: Get all messages, replies, and send a reply.\n- Statistic API: Get the statistics of your transactions and buyers.\n',
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
