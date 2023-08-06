# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chocs',
 'chocs.console',
 'chocs.console.dto_generator',
 'chocs.dataclasses',
 'chocs.json_schema',
 'chocs.middleware',
 'chocs.serverless',
 'chocs.wsgi']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0',
 'pyyaml>=5.3.1,<6.0.0',
 'typing_extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['chocs = chocs.console.application:main']}

setup_kwargs = {
    'name': 'chocs',
    'version': '0.17.0',
    'description': 'Lightweight and powerful wsgi rest framework for rapid building applications based on wsgi servers.',
    'long_description': '# Chocs [![PyPI version](https://badge.fury.io/py/chocs.svg)](https://pypi.org/project/chocs/) ![Release](https://github.com/kodemore/chocs/workflows/Release/badge.svg) ![Linting and Tests](https://github.com/kodemore/chocs/workflows/Linting%20and%20Tests/badge.svg) [![codecov](https://codecov.io/gh/kodemore/chocs/branch/master/graph/badge.svg)](https://codecov.io/gh/kodemore/chocs) [![Maintainability](https://api.codeclimate.com/v1/badges/9e3c979283b2361a9174/maintainability)](https://codeclimate.com/github/kodemore/chocs/maintainability)\nChocs is a modern HTTP framework for building AWS HTTP API/REST API and WSGI compatible applications. \nChocs aims to be small, expressive, and robust. \nIt provides an elegant API for writing fault-proof, extensible microservices.  \n\n## Features\n\n - AWS Serverless integration\n - Open api integration  \n - Elegant and easy API\n - No additional bloat like built-in template engines, session handlers, etc.\n - Compatible with all WSGI servers\n - Loosely coupled components which can be used separately\n - Multipart body parsing\n - Graceful error handling\n - HTTP middleware support\n - Fast routing\n\n## Installation\n```\npip install chocs\n```\n\nor with poetry\n\n```\npoetry add chocs\n```\n\n## Quick start\n\n```python\nimport chocs\n\nhttp = chocs.Application()\n\n@http.get("/hello/{name}")\ndef hello(request: chocs.HttpRequest) -> chocs.HttpResponse:\n    return chocs.HttpResponse(f"Hello {request.path_parameters.get(\'name\')}!")\n\nchocs.serve(http)\n```\n\n> Keep in mind that the `chocs.serve()` function is using the `bjoern` package, so make sure you included it in your project\n> dependencies before using it. You are able to use any WSGI compatible server.\n\n# Documentation\nFor usage and detailed documentation please visit our [wiki page](https://github.com/kodemore/chocs/wiki)\n',
    'author': 'Dawid Kraczkowski',
    'author_email': 'dawid.kraczkowski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kodemore/chocs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
