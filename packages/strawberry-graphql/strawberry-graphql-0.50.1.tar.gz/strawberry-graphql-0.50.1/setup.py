# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['strawberry',
 'strawberry.asgi',
 'strawberry.cli',
 'strawberry.cli.commands',
 'strawberry.django',
 'strawberry.experimental',
 'strawberry.experimental.pydantic',
 'strawberry.extensions',
 'strawberry.extensions.tracing',
 'strawberry.file_uploads',
 'strawberry.flask',
 'strawberry.sanic',
 'strawberry.schema',
 'strawberry.schema.types',
 'strawberry.types',
 'strawberry.types.fields',
 'strawberry.utils']

package_data = \
{'': ['*'], 'strawberry': ['ext/*', 'static/*']}

install_requires = \
['cached-property>=1.5.2,<2.0.0',
 'graphql-core>=3.1.0,<4.0.0',
 'hupper>=1.5,<2.0',
 'pygments>=2.3,<3.0',
 'python-dateutil>=2.7.0,<3.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'starlette>=0.13.6,<0.15.0',
 'typing_extensions>=3.7.4,<4.0.0']

extras_require = \
{'debug-server': ['uvicorn>=0.11.6,<0.14.0'],
 'django': ['django>=2,<4', 'asgiref>=3.2,<4.0'],
 'flask': ['flask>=1.1,<2.0'],
 'opentelemetry': ['opentelemetry-api>=0.17b0,<0.18',
                   'opentelemetry-sdk>=0.17b0,<0.18'],
 'pydantic': ['pydantic>=1.6.1,<2.0.0'],
 'sanic': ['sanic>=20.12.2,<21.0.0']}

entry_points = \
{'console_scripts': ['strawberry = strawberry.cli:run']}

setup_kwargs = {
    'name': 'strawberry-graphql',
    'version': '0.50.1',
    'description': 'A library for creating GraphQL APIs',
    'long_description': '<img src="https://github.com/strawberry-graphql/strawberry/raw/main/.github/logo.png" width="124" height="150">\n\n# Strawberry GraphQL\n\n> Python GraphQL library based on dataclasses\n\n[![CircleCI](https://img.shields.io/circleci/token/307b40d5e152e074d34f84d30d226376a15667d5/project/github/strawberry-graphql/strawberry/main.svg?style=for-the-badge)](https://circleci.com/gh/strawberry-graphql/strawberry/tree/main)\n[![Discord](https://img.shields.io/discord/689806334337482765?label=discord&logo=discord&logoColor=white&style=for-the-badge&color=blue)](https://discord.gg/ZkRTEJQ)\n[![PyPI](https://img.shields.io/pypi/v/strawberry-graphql?logo=pypi&logoColor=white&style=for-the-badge)](https://pypi.org/project/strawberry-graphql/)\n\n## Installation ( Quick Start )\n\nThe quick start method provides a server and CLI to get going quickly. Install\nwith:\n\n```shell\npip install strawberry-graphql[debug-server]\n```\n\n## Getting Started\n\nCreate a file called `app.py` with the following code:\n\n```python\nimport strawberry\n\n\n@strawberry.type\nclass User:\n    name: str\n    age: int\n\n\n@strawberry.type\nclass Query:\n    @strawberry.field\n    def user(self) -> User:\n        return User(name="Patrick", age=100)\n\n\nschema = strawberry.Schema(query=Query)\n```\n\nThis will create a GraphQL schema defining a `User` type and a single query\nfield `user` that will return a hardcoded user.\n\nTo run the debug server run the following command:\n\n```shell\nstrawberry server app\n```\n\nOpen the debug server by clicking on the following link:\n[http://0.0.0.0:8000/graphql](http://0.0.0.0:8000/graphql)\n\nThis will open GraphiQL where you can test the API.\n\n### Type-checking\n\nStrawberry comes with a [mypy] plugin that enables statically type-checking your\nGraphQL schema. To enable it, add the following lines to your `mypy.ini`\nconfiguration:\n\n```ini\n[mypy]\nplugins = strawberry.ext.mypy_plugin\n```\n\n[mypy]: http://www.mypy-lang.org/\n\n### Django Integration\n\nA Django view is provided for adding a GraphQL endpoint to your application.\n\n1. Add the app to your `INSTALLED_APPS`.\n\n```python\nINSTALLED_APPS = [\n    ...\n    \'strawberry.django\',\n]\n```\n\n2. Add the view to your `urls.py` file.\n\n```python\nfrom strawberry.django.views import GraphQLView\nfrom .schema import schema\n\nurlpatterns = [\n    ...,\n    path(\'graphql\', GraphQLView.as_view(schema=schema)),\n]\n```\n\n## WebSockets\n\nTo support graphql Subscriptions over WebSockets you need to provide a WebSocket\nenabled server. The debug server can be made to support WebSockets with these\ncommands:\n\n```shell\npip install strawberry-graphql[debug-server]\npip install uvicorn[standard]\n```\n\n## Contributing\n\nWe use [poetry](https://github.com/sdispater/poetry) to manage dependencies, to\nget started follow these steps:\n\n```shell\ngit clone https://github.com/strawberry-graphql/strawberry\ncd strawberry\npoetry install\npoetry run pytest\n```\n\nThis will install all the dependencies (including dev ones) and run the tests.\n\n### Pre commit\n\nWe have a configuration for\n[pre-commit](https://github.com/pre-commit/pre-commit), to add the hook run the\nfollowing command:\n\n```shell\npre-commit install\n```\n\n## Links\n\n- Project homepage: https://strawberry.rocks\n- Repository: https://github.com/strawberry-graphql/strawberry\n- Issue tracker: https://github.com/strawberry-graphql/strawberry/issues\n  - In case of sensitive bugs like security vulnerabilities, please contact\n    patrick.arminio@gmail.com directly instead of using the issue tracker. We\n    value your effort to improve the security and privacy of this project!\n\n## Licensing\n\nThe code in this project is licensed under MIT license. See [LICENSE](./LICENSE)\nfor more information.\n',
    'author': 'Patrick Arminio',
    'author_email': 'patrick.arminio@gmail.com',
    'url': 'https://strawberry.rocks/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
