# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['connect',
 'connect..data.connect_reports.reports',
 'connect..data.connect_reports.reports.billing_requests',
 'connect..data.connect_reports.reports.billing_requests_line_item',
 'connect..data.connect_reports.reports.contract_list',
 'connect..data.connect_reports.reports.customers_list',
 'connect..data.connect_reports.reports.fulfillment_requests',
 'connect..data.connect_reports.reports.fulfillment_requests_failed',
 'connect..data.connect_reports.reports.fulfillment_requests_line_item',
 'connect..data.connect_reports.reports.listing_list',
 'connect..data.connect_reports.reports.listing_requests',
 'connect..data.connect_reports.reports.subscription_list',
 'connect..data.connect_reports.reports.tier_configuration_list',
 'connect..data.connect_reports.reports.tier_configuration_requests',
 'connect..data.connect_reports.reports.usage_in_subscription',
 'connect.cli',
 'connect.cli.core',
 'connect.cli.core.account',
 'connect.cli.plugins',
 'connect.cli.plugins.customer',
 'connect.cli.plugins.product',
 'connect.cli.plugins.product.sync',
 'connect.cli.plugins.report']

package_data = \
{'': ['*'],
 'connect': ['.data/connect_reports/*',
             '.data/connect_reports/.github/workflows/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'connect-markdown-renderer>=1.0.1,<2.0.0',
 'connect-openapi-client>=22.0.5,<23.0.0',
 'connect-reports-core>=23,<24',
 'fs>=2.4.12,<3.0.0',
 'interrogatio>=1.0.3,<2.0.0',
 'iso3166>=1.0.1,<2.0.0',
 'lxml>=4.6.2,<5.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'phonenumbers>=8.12.19,<9.0.0',
 'pip>=21.0.1,<22.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'tqdm>=4.59.0,<5.0.0']

entry_points = \
{'connect.cli.plugins': ['customer = '
                         'connect.cli.plugins.customer.commands:get_group',
                         'product = '
                         'connect.cli.plugins.product.commands:get_group',
                         'report = '
                         'connect.cli.plugins.report.commands:get_group'],
 'console_scripts': ['ccli = connect.cli.ccli:main']}

setup_kwargs = {
    'name': 'connect-cli',
    'version': '22.18',
    'description': 'CloudBlue Connect Command Line Interface',
    'long_description': '# CloudBlue Connect Command Line Interface\n\n![pyversions](https://img.shields.io/pypi/pyversions/connect-cli.svg) [![PyPi Status](https://img.shields.io/pypi/v/connect-cli.svg)](https://pypi.org/project/connect-cli/) [![Build Status](https://travis-ci.org/cloudblue/connect-cli.svg?branch=master)](https://travis-ci.org/cloudblue/connect-cli) [![codecov](https://codecov.io/gh/cloudblue/connect-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/cloudblue/connect-cli) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=connect-cli&metric=alert_status)](https://sonarcloud.io/dashboard?id=connect-cli)\n\n\n## Introduction\n\nThe CloudBlue Connect Command Line Interface (CLI) is an extensible unified tool to perform various automation scenarios. With just one tool, you can control multiple Connect modules from the command line and automate them through scripts.\n\nSince it is extensible, user can write your own plugins to extend its functionalities.\n\n\n## Install\n\n### Prerequisites\n\n`connect-cli` depends on [Cairo](https://www.cairographics.org/), [Pango](https://pango.gnome.org/) and \n[GDK-PixBuf](https://developer.gnome.org/gdk-pixbuf/stable/).\n\nPlease refers to the platform-specific instructions on how to install these dependecies:\n\n* [Linux](docs/linux_deps_install.md)\n* [Mac OSX](docs/osx_deps_install.md)\n* [Windows](docs/win_deps_install.md)\n\n\n### Using PIP\n\nTo use `connect-cli` you need a system with python 3.6 or later installed.\n\n```sh\n    $ pip install --upgrade connect-cli\n```    \n\n### Binary distributions\n\nA single executable binary distribution is available for windows, linux and mac os x.\nYou can it from the [Github Releases](https://github.com/cloudblue/connect-cli/releases) page.\n\nTo install under linux:\n\n```\n    $ curl -O -J https://github.com/cloudblue/connect-cli/releases/download/xx.yy/connect-cli_xx.yy_linux_amd64.tar.gz\n    $ tar xvfz connect-cli_xx.yy_linux_amd64.tar.gz\n    $ sudo cp dist/ccli /usr/local/bin/ccli\n```\n\nTo install under Mac OS X:\n\n```\n    $ curl -O -J https://github.com/cloudblue/connect-cli/releases/download/xx.yy/connect-cli_xx.yy_osx_amd64.tar.gz\n    $ tar xvfz connect-cli_xx.yy_osx_amd64.tar.gz\n    $ sudo cp dist/ccli /usr/local/bin/ccli\n```\n\n> If your user is not a sudoer, you can copy the `ccli` executable from the dist directory to a directory of your choice\n> that is listed in the `PATH` variable.\n\n\nTo install under Windows\n\nDownload the windows single executable zipfile from [Github Releases](https://github.com/cloudblue/connect-cli/releases/download/xx.yy/connect-cli_xx.yy_windows_amd64.zip), extract it and place it in a folder that is included in your `PATH` system variable.\n\n\n## Usage\n\n* [General](docs/core_usage.md)\n* [Products](docs/products_usage.md)\n* [Customers](docs/customers_usage.md)\n* [Reports](docs/reports_usage.md)\n\n\n## License\n\n`connect-cli` is released under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\n',
    'author': 'CloudBlue LLC',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://connect.cloudblue.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
