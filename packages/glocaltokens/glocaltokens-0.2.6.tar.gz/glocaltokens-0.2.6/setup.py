# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glocaltokens',
 'glocaltokens.google.internal.home.foyer',
 'glocaltokens.utils']

package_data = \
{'': ['*']}

install_requires = \
['gpsoauth>=0.4.3,<0.5.0',
 'grpcio-tools==1.31.0',
 'grpcio==1.31.0',
 'requests>=2.25.1,<3.0.0',
 'simplejson>=3.17.2,<4.0.0',
 'zeroconf>=0.28.8,<0.29.0']

setup_kwargs = {
    'name': 'glocaltokens',
    'version': '0.2.6',
    'description': 'Tool to extract Google device local authentication tokens in Python',
    'long_description': '[![GitHub Workflow Status][workflow-shield]][workflow]\n[![PyPI][pypi-shield]][pypi]\n[![Pre-commit][pre-commit-shield]][pre-commit]\n\n[![Open Issues][issues-shield]][issues]\n[![Open Pull-Requests][pr-shield]][pr]\n[![Contributors][contributors-shield]][contributors]\n\n[![GitHub Release][releases-shield]][releases]\n[![GitHub Activity][commits-shield]][commits]\n[![License][license-shield]][license]\n\n# Google home local authentication token extraction\n\nPython 3 package to extract google home devices local authentication tokens from google servers. These local\nauthentication tokens are needed to control Google Home devices(See\n@rithvikvibhu\'s [Google Home (2.0) API](https://rithvikvibhu.github.io/GHLocalApi/)).\n\nPlease note:\nOnce you have local google authentication tokens they only live about 1 day long. After that you will need to obtain new\nones. You will probably need to run the script repeatedly storing the tokens somewhere convenient.\n\n## Quickstart\n\nNote: the package was written and tested on Python 3.\n\n- Install the python package\n\n```\npip install glocaltokens\n```\n\nUse in your program as (see examples folder for detailed example):\n\n```Python\nfrom glocaltokens.client import GLocalAuthenticationTokens\n\n# Using google username and password\n#\n# ONLY CALL THIS ONCE\n#\n# If you call this too often, google will disconnect your android devices and other weird things will happen\n#\n# Call get_google_devices_json() afterwards to get timers/alarms as oftens as you want to update.\nclient = GLocalAuthenticationTokens(\n  username="<YOUR_GOOGLE_USERNAME>",\n  password="<YOUR_GOOGLE_PASSWORD>"\n)\n\n# Get master token\nprint("[*] Master token", client.get_master_token())\n\n# Get access token (lives 1 hour)\nprint("\\n[*] Access token (lives 1 hour)", client.get_access_token())\n\n# Get google device local authentication tokens (live about 1 day)\nprint("\\n[*] Google devices local authentication tokens")\ngoogle_devices = client.get_google_devices_json()\n\n# You can also select specific models to select when calling get_google_devices or get_google_devices_json with the models_list parameter.\n# For example, we have pre-defined a constant with some Google Home Models (WARNING! Not all of them may be present)\n# This could be used this way\nfrom glocaltokens.const import GOOGLE_HOME_MODELS\n\ngoogle_devices_select = client.get_google_devices_json(GOOGLE_HOME_MODELS)\n\n# But if you need to select just a set of models, or add new models, you can use a list of str\ngoogle_devices_select_2 = client.get_google_devices_json([\n    f"Google Home",\n    f"Google Home Mini",\n    f"Google Nest Mini",\n])\n```\n\n### Predefined models list\nThere are some pre-defined models list in [`scanner.py`](/glocaltokens/scanner.py), feel free to\nadd new lists, or add models to a list with a pull-request.\n#### `GOOGLE_HOME_MODELS`:\n- Google Home\n- Google Home Mini\n- Google Nest Mini\n- Lenovo Smart Clock\n\n## Security Recommendation\n\nNever store the user\'s password nor username in plain text, if storage is necessary, generate a master token and store\nit. Example approach:\n\n```python\nfrom glocaltokens.client import GLocalAuthenticationTokens\n\n# Using google username and password first, and only once\nclient = GLocalAuthenticationTokens(\n  username="<YOUR_GOOGLE_USERNAME>",\n  password="<YOUR_GOOGLE_PASSWORD>"\n)\n\n# Get master token\nmaster_token = client.get_master_token()\nprint("[*] Master token", master_token)\n\n"""Now store master_token somewhere"""\n\n```\n\n## Contributing\n\nSee [Contributing guidelines](CONTRIBUTING.md)\nThis is an open-source project and all countribution is highly welcomed. To contribute please:\n\n# Credits\n\nMuch credits go to @rithvikvibhu(https://github.com/rithvikvibhu) for doing most of the heavy work like finding a way to\nextract master and access tokens\n(See his gist [here](https://gist.github.com/rithvikvibhu/952f83ea656c6782fbd0f1645059055d)).\n\nAlso, thank you very much to the guys at `pychromecast` which provided the code required to scan devices in the network.\n\n\n[workflow-shield]: https://img.shields.io/github/workflow/status/leikoilja/glocaltokens/Running%20tests?style=for-the-badge\n[workflow]: https://github.com/leikoilja/glocaltokens/actions\n\n[pypi-shield]: https://img.shields.io/pypi/v/glocaltokens?style=for-the-badge\n[pypi]: https://pypi.org/project/glocaltokens/\n\n[issues-shield]: https://img.shields.io/github/issues/leikoilja/glocaltokens?style=for-the-badge\n[issues]: https://github.com/leikoilja/glocaltokens/issues\n\n[pr-shield]: https://img.shields.io/github/issues-pr/leikoilja/glocaltokens?style=for-the-badge\n[pr]: https://github.com/leikoilja/glocaltokens/pulls\n\n[commits-shield]: https://img.shields.io/github/commit-activity/y/leikoilja/glocaltokens?style=for-the-badge\n[commits]: https://github.com/leikoilja/glocaltokens/commits/main\n\n[contributors-shield]: https://img.shields.io/github/contributors/leikoilja/glocaltokens?style=for-the-badge\n[contributors]: https://github.com/leikoilja/glocaltokens/graphs/contributors\n\n[license]: https://github.com/leikoilja/glocaltokens/blob/main/LICENSE\n[license-shield]: https://img.shields.io/github/license/leikoilja/glocaltokens.svg?style=for-the-badge\n\n[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge\n[pre-commit]: https://github.com/pre-commit/pre-commit\n\n[releases-shield]: https://img.shields.io/github/release/leikoilja/glocaltokens.svg?style=for-the-badge\n[releases]: https://github.com/leikoilja/glocaltokens/releases\n',
    'author': 'Ilja Leiko',
    'author_email': 'leikoilja@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/leikoilja/glocaltokens',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
