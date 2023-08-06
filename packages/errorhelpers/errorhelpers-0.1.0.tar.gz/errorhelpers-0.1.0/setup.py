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
    'version': '0.1.0',
    'description': 'Helpers for handling Python errors',
    'long_description': 'errorhelpers\n============\n\n[![PyPI version](https://img.shields.io/pypi/v/errorhelpers.svg)](https://pypi.org/project/errorhelpers)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/errorhelpers.svg)](https://pypi.org/project/errorhelpers)\n[![Maintainability](https://api.codeclimate.com/v1/badges/989e85c7a858c7696658/maintainability)](https://codeclimate.com/github/sayanarijit/errorhelpers/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/989e85c7a858c7696658/test_coverage)](https://codeclimate.com/github/sayanarijit/errorhelpers/test_coverage)\n\n\nHelpers for handling Python errors.\n\n\n### Example 1: Basic usage\n\n```python\nimport pytest\nimport errorhelpers\n\n@errorhelpers.expect_errors(ZeroDivisionError)\ndef sensitive_transaction(x, y):\n    return int(x) / int(y)\n\nassert sensitive_transaction(4, "2") == 2\n\n# `ZeroDivisionError` will be re-raised.\nwith pytest.raises(ZeroDivisionError):\n    sensitive_transaction(4, 0)\n\n# In case of other exceptions, `errorhelpers.UnexpectedError("Unexpected error")`\n# will be raised instead.\nwith pytest.raises(errorhelpers.UnexpectedError, match="Unexpected error"):\n    sensitive_transaction("a", "b")\n```\n\n### Example 2: Default value\n\n```python\nimport pytest\nimport errorhelpers\n\n@errorhelpers.expect_errors(\n    ZeroDivisionError, on_unexpected_error=lambda err_, args_, kwargs_: -1\n)\ndef sensitive_transaction(x, y):\n    return int(x) / int(y)\n\nassert sensitive_transaction(4, "2") == 2\n\n# `ZeroDivisionError` will be re-raised.\nwith pytest.raises(ZeroDivisionError):\n    sensitive_transaction(4, 0)\n\n# In case of other exceptions, -1 will be returned.\nassert sensitive_transaction("a", "b") == -1\n```\n\n### Example 3: Custom error\n\n```python\nimport pytest\nimport errorhelpers\n\nclass CustomError(Exception):\n    @classmethod\n    def raise_(cls, msg):\n        def raiser(error, args, kwargs):\n            print("Hiding error:", error, "with args:", args, "and kwargs: ", kwargs)\n            raise cls(msg)\n\n        return raiser\n\n@errorhelpers.expect_errors(\n    ZeroDivisionError, on_unexpected_error=CustomError.raise_("Custom error")\n)\ndef sensitive_transaction(x, y):\n    return int(x) / int(y)\n\nassert sensitive_transaction(4, "2") == 2\n\n# `ZeroDivisionError` will be re-raised.\nwith pytest.raises(ZeroDivisionError):\n    sensitive_transaction(4, 0)\n\n# In case of other exceptions, `CustomError` will be raised instead.\nwith pytest.raises(CustomError, match="Custom error"):\n    sensitive_transaction("a", "b")\n\n# Hiding error: invalid literal for int() with base 10: \'a\' with args: (\'a\', \'b\') and kwargs:  {}\n```\n',
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
