# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lwh', 'lwh.report']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'requests>=2.25.1,<3.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['lwh = lwh.main:app']}

setup_kwargs = {
    'name': 'lwh',
    'version': '0.0.8',
    'description': '',
    'long_description': "# `Lacework Helios cli`\n\nCreate a Lacework build artifact scan report.\n\n**Usage**:\n\n\n**Options**:\n\n* `--input TEXT`: path to Lacework scan results file  [required]\n* `--output TEXT`: [optional] path to store html report.  [default: .]\n* `--template TEXT`: [optional] path to custom html template\n* `--help`: Show this message and exit.\n\n**Usage**:\n```console\nlwh [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n  --help  Show this message and exit.\n\n**Commands**:\n  opa     Validate Scan Results agains OPA policy\n  report  Create a Lacework build artifact scan report.\n\n\n\n<br/><br/>\n### Installation\n`pip install lwh`\n\n### Custom Reports\nIf you're interested in customizing the report check out the sample template in the examples folder.\nlwh cli simply renders the scan results json object to any provided template as {{ scan_result_json }}.\nYou also have access to a python dictionary {{ data }} as a convenience object if using jinja. If using opa integration\npolicy decision is also passed to report as {{result}}. You don't need to use React or Jinja. Feel free to use your \nexisting tool chain.<br/><br/>\n\nFrom here the [lacework-razr](https://github.com/jeffthorne/lacework-razr) React components take over. But they don't have to. \nFeel free to customize or get in touch if you need any changes.\n",
    'author': 'jeffthorne',
    'author_email': 'jthorne@u.washington.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
