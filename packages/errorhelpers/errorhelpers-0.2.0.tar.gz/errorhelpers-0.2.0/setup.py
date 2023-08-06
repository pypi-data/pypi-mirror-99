# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['errorhelpers']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'errorhelpers',
    'version': '0.2.0',
    'description': 'Helpers for handling Python errors',
    'long_description': 'errorhelpers\n============\n\n[![PyPI version](https://img.shields.io/pypi/v/errorhelpers.svg)](https://pypi.org/project/errorhelpers)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/errorhelpers.svg)](https://pypi.org/project/errorhelpers)\n[![Maintainability](https://api.codeclimate.com/v1/badges/989e85c7a858c7696658/maintainability)](https://codeclimate.com/github/sayanarijit/errorhelpers/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/989e85c7a858c7696658/test_coverage)](https://codeclimate.com/github/sayanarijit/errorhelpers/test_coverage)\n\n\nHelpers for handling Python errors.\n\n\n\n\n### Usage:\n\n```python\n# As a decorator\n@errorhelpers.expect_error(*errors, on_unexpected_error=handler)\ndef some_error_prone_funcion():\n    ...\n\n# Using with statement\nwith errorhelpers.expect_error(*errors, on_unexpected_error=handler):\n    # Some error prone operation\n    ...\n```\n\n\n### Example 1: Basic usage\n\n```python\nimport pytest\nimport errorhelpers\n\nwith errorhelpers.expect_errors(ZeroDivisionError):\n    assert 4 / 2 == 2\n\n# `ZeroDivisionError` will be re-raised.\nwith pytest.raises(ZeroDivisionError):\n    with errorhelpers.expect_errors(ZeroDivisionError):\n        4 / 0\n\n# In case of other exceptions, `errorhelpers.UnexpectedError("Unexpected error")`\n# will be raised instead.\nwith pytest.raises(errorhelpers.UnexpectedError, match="Unexpected error"):\n    with errorhelpers.expect_errors(ZeroDivisionError):\n        "a" / "b"\n```\n\n### Example 2: Custom error\n\n```python\nimport pytest\nimport errorhelpers\n\nclass CustomError(Exception):\n    @classmethod\n    def raise_(cls, msg):\n        def raiser(error):\n            print("Hiding error:", error)\n            raise cls(msg)\n\n        return raiser\n\n@errorhelpers.expect_errors(\n    ZeroDivisionError, on_unexpected_error=CustomError.raise_("Custom error")\n)\ndef sensitive_transaction(x, y):\n    return int(x) / int(y)\n\nassert sensitive_transaction(4, "2") == 2\n\n# `ZeroDivisionError` will be re-raised.\nwith pytest.raises(ZeroDivisionError):\n    sensitive_transaction(4, 0)\n\n# In case of other exceptions, `CustomError` will be raised instead.\nwith pytest.raises(CustomError, match="Custom error"):\n    sensitive_transaction("a", "b")\n\n# Hiding error: invalid literal for int() with base 10: \'a\'\n```\n',
    'author': 'Arijit Basu',
    'author_email': 'sayanarijit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sayanarijit/errorhelpers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
