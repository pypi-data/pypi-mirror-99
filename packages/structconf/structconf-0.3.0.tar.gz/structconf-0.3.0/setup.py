# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['structconf']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==5.3.1', 'pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'structconf',
    'version': '0.3.0',
    'description': 'struct config using yaml',
    'long_description': '# StructConf\n\n[![PyPI](https://img.shields.io/pypi/v/structconf?color=blue)](https://pypi.org/project/structconf/)\n[![Codecov](https://img.shields.io/codecov/c/gh/Green-Wood/structconf)](https://app.codecov.io/gh/Green-Wood/structconf)\n\nConfig your project with yaml and validation.\n\nEnjoy wirting your code with IDEs python **type hint**\n\n## Simple Usage\n\n1. Define your configuration class, with attribute type and default value\n\n```python\nfrom structconf import StructConf\n\nclass SimpleConf(StructConf):\n    a: int = 1\n    b: str = "b"\n```\n\n2. write your yaml config file (e.g simple.yaml)\n\n```yaml\na: 2\nb: "123"\n```\n\n3. load yaml config file to your struct class\n\n```python\nconf = SimpleConf.load("simple.yaml")\nassert conf.a == 2\nassert conf.b == "123"\n```\n\n\n\n## Advanced Usage\n\nStructConf use [pydantic](https://github.com/samuelcolvin/pydantic) to validate your yaml and python class. So we can use recursive modelto build complex configuration.\n\n```python\nfrom structconf import StructConf\n\nclass AConf(StructConf):\n    a: int = 1\n\n\nclass BConf(StructConf):\n    b: int = 2\n\n\nclass ComplexConf(StructConf):\n    aconf: AConf = AConf()\n    bconf: BConf = BConf()\n```',
    'author': 'Wenqi Zhao',
    'author_email': '1027572886a@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Green-Wood/structconf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
