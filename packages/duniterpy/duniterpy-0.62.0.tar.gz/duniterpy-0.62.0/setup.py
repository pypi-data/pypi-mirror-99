# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['duniterpy',
 'duniterpy.api',
 'duniterpy.api.bma',
 'duniterpy.api.elasticsearch',
 'duniterpy.api.ws2p',
 'duniterpy.documents',
 'duniterpy.documents.ws2p',
 'duniterpy.grammars',
 'duniterpy.helpers',
 'duniterpy.key']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.3,<4.0.0',
 'attrs>=20.2.0,<21.0.0',
 'base58>=2.0.0,<3.0.0',
 'graphql-core>=3.1.2,<4.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'libnacl>=1.7.2,<2.0.0',
 'pyaes>=1.6.1,<2.0.0',
 'pypeg2>=2.15.2,<3.0.0']

setup_kwargs = {
    'name': 'duniterpy',
    'version': '0.62.0',
    'description': 'Python library for developers of Duniter clients',
    'long_description': '# DuniterPy\nMost complete client oriented Python library for [Duniter](https://git.duniter.org/nodes/typescript/duniter)/Ğ1 ecosystem.\n\nThis library was originally developed for [Sakia](http://sakia-wallet.org/) desktop client which is now discontinued.\nIt is currently used by following programs:\n- [Tikka](https://git.duniter.org/clients/python), the desktop client (Work In Progress, not yet available).\n- [Silkaj](https://silkaj.duniter.org/), command line client.\n- [Jaklis](https://git.p2p.legal/axiom-team/jaklis), command line client for Cs+/Gchange pods.\n- [Ğ1Dons](https://git.duniter.org/matograine/g1pourboire), Ğ1Dons, paper-wallet generator aimed at giving tips in Ğ1.\n\n## Features\n### Network\n- APIs support: BMA, GVA, WS2P, and CS+:\n  - [Basic Merkle API](https://git.duniter.org/nodes/typescript/duniter/-/blob/dev/doc/HTTP_API.md), first Duniter API to be deprecated\n  - GraphQL Verification API, Duniter API in developement meant to replace BMA. Based on GraphQL.\n  - Websocket to Peer, Duniter inter-nodes (servers) API\n  - Cesium+, non-Duniter API, used to store profile data related to the blockchain as well as ads for Cesium and Ğchange.\n- Non-threaded asynchronous/synchronous connections\n- Support HTTP, HTTPS, and WebSocket transport for the APIs\n- Endpoints management\n\n### Blockchain\n- Support [Duniter blockchain protocol](https://git.duniter.org/documents/rfcs#duniter-blockchain-protocol-dubp)\n- Duniter documents management: transaction, block and WoT documents\n- Multiple authentication methods\n- Duniter signing key\n- Sign/verify and encrypt/decrypt messages with Duniter credentials\n\n## Requirements\n- Python >= 3.6.8\n- [aiohttp >= 3.6.3](https://pypi.org/project/aiohttp)\n- [jsonschema](https://pypi.org/project/jsonschema)\n- [pyPEG2](https://pypi.org/project/pyPEG2)\n- [attrs](https://pypi.org/project/attrs)\n- [base58](https://pypi.org/project/base58)\n- [libnacl](https://pypi.org/project/libnacl)\n- [pyaes](https://pypi.org/project/pyaes)\n\n## Installation\nYou can install DuniterPy and its dependencies with the following command:\n```bash\npip3 install duniterpy --user\n```\n\n## Install the development environment\n- [Install Poetry](https://python-poetry.org/docs/#installation)\n\n## Documentation\n[Online official automaticaly generated documentation](https://clients.duniter.io/python/duniterpy/index.html)\n\nThe [examples folder](https://git.duniter.org/clients/python/duniterpy/tree/master/examples) contains scripts to help you!\n\n### How to generate and read locally the autodoc\n\n- Install Sphinx, included into the development dependencies:\n```bash\npoetry install\n```\n\n- Generate documentation\n```bash\npoetry run make docs\n```\n\n- The HTML documentation is generated in `docs/_build/html` folder.\n\n## Development\n* When writing docstrings, use the reStructuredText format recommended by https://www.python.org/dev/peps/pep-0287/#docstring-significant-features\n* Use `make` commands to check the code and the format.\n\nBlack, the formatting tool, requires Python 3.6 or higher.\n\n* Install runtime dependencies\n```bash\npoetry install --no-dev\n```\n\n* Have a look at the examples folder\n* Run examples from parent folder\n```bash\npoetry run python examples/request_data.py\n```\n\n* Before submitting a merge requests, please check the static typing and tests.\n\n* Install dev dependencies\n```bash\npoetry install\n```\n\n* Check static typing with [mypy](http://mypy-lang.org/)\n```bash\nmake check\n```\n\n* Run all unit tests (builtin `unittest` module) with:\n```bash\nmake tests\n```\n\n* Run only some unit tests by passing a special ENV variable:\n```bash\nmake tests TESTS_FILTER=tests.documents.test_block.TestBlock.test_fromraw\n```\n\n## Packaging and deploy\n### PyPI\nChange and commit and tag the new version number (semantic version number)\n```bash\n./release.sh 0.42.3\n```\n\nBuild the PyPI package in the `dist` folder\n```bash\nmake build\n```\n\nDeploy the package to PyPI test repository (prefix the command with a space for the shell to not save it in its history system, since the command contains credentials)\n```bash\n[SPACE]make deploy_test PYPI_TEST_LOGIN=xxxx PYPI_TEST_PASSWORD=xxxx\n```\n\nInstall the package from PyPI test repository\n```bash\npip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.python.org/simple/ duniterpy\n```\n\nDeploy the package on the PyPI repository (prefix the command with a space for the shell to not save it in its history system, since the command contains credentials)\n```bash\n[SPACE]make deploy PYPI_LOGIN=xxxx PYPI_PASSWORD=xxxx\n```\n\n## Packaging status\n[![Packaging status](https://repology.org/badge/vertical-allrepos/python:duniterpy.svg)](https://repology.org/project/python:duniterpy/versions)\n',
    'author': 'inso',
    'author_email': 'insomniak.fr@gmail.com',
    'maintainer': 'vit',
    'maintainer_email': 'vit@free.fr',
    'url': 'https://git.duniter.org/clients/python/duniterpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.8,<4.0.0',
}


setup(**setup_kwargs)
