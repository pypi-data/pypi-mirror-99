# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['python_sqs_consumer']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.2.2']

setup_kwargs = {
    'name': 'python-sqs-consumer',
    'version': '0.0.5',
    'description': 'Consume AWS SQS messages from Python',
    'long_description': '========\nOverview\n========\n\n.. start-badges\n\n.. list-table::\n    :stub-columns: 1\n\n    * - docs\n      - |docs|\n    * - tests\n      - | |travis| |appveyor| |requires|\n        | |coveralls| |codecov|\n        | |landscape| |scrutinizer| |codacy| |codeclimate|\n    * - package\n      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|\n\n.. |docs| image:: https://readthedocs.org/projects/python-sqs-consumer/badge/?style=flat\n    :target: https://readthedocs.org/projects/python-sqs-consumer\n    :alt: Documentation Status\n\n.. |travis| image:: https://travis-ci.org/admetricks/python-sqs-consumer.svg?branch=master\n    :alt: Travis-CI Build Status\n    :target: https://travis-ci.org/admetricks/python-sqs-consumer\n\n.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/admetricks/python-sqs-consumer?branch=master&svg=true\n    :alt: AppVeyor Build Status\n    :target: https://ci.appveyor.com/project/admetricks/python-sqs-consumer\n\n.. |requires| image:: https://requires.io/github/admetricks/python-sqs-consumer/requirements.svg?branch=master\n    :alt: Requirements Status\n    :target: https://requires.io/github/admetricks/python-sqs-consumer/requirements/?branch=master\n\n.. |coveralls| image:: https://coveralls.io/repos/admetricks/python-sqs-consumer/badge.svg?branch=master&service=github\n    :alt: Coverage Status\n    :target: https://coveralls.io/r/admetricks/python-sqs-consumer\n\n.. |codecov| image:: https://codecov.io/github/admetricks/python-sqs-consumer/coverage.svg?branch=master\n    :alt: Coverage Status\n    :target: https://codecov.io/github/admetricks/python-sqs-consumer\n\n.. |landscape| image:: https://landscape.io/github/admetricks/python-sqs-consumer/master/landscape.svg?style=flat\n    :target: https://landscape.io/github/admetricks/python-sqs-consumer/master\n    :alt: Code Quality Status\n\n.. |codacy| image:: https://img.shields.io/codacy/4c60e799fb664f7e88dd5a06f2bb389c.svg?style=flat\n    :target: https://www.codacy.com/app/admetricks/python-sqs-consumer\n    :alt: Codacy Code Quality Status\n\n.. |codeclimate| image:: https://codeclimate.com/github/admetricks/python-sqs-consumer/badges/gpa.svg\n   :target: https://codeclimate.com/github/admetricks/python-sqs-consumer\n   :alt: CodeClimate Quality Status\n\n.. |version| image:: https://img.shields.io/pypi/v/python_sqs_consumer.svg?style=flat\n    :alt: PyPI Package latest release\n    :target: https://pypi.python.org/pypi/python_sqs_consumer\n\n.. |downloads| image:: https://img.shields.io/pypi/dm/python_sqs_consumer.svg?style=flat\n    :alt: PyPI Package monthly downloads\n    :target: https://pypi.python.org/pypi/python_sqs_consumer\n\n.. |wheel| image:: https://img.shields.io/pypi/wheel/python_sqs_consumer.svg?style=flat\n    :alt: PyPI Wheel\n    :target: https://pypi.python.org/pypi/python_sqs_consumer\n\n.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/python_sqs_consumer.svg?style=flat\n    :alt: Supported versions\n    :target: https://pypi.python.org/pypi/python_sqs_consumer\n\n.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/python_sqs_consumer.svg?style=flat\n    :alt: Supported implementations\n    :target: https://pypi.python.org/pypi/python_sqs_consumer\n\n.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/admetricks/python-sqs-consumer/master.svg?style=flat\n    :alt: Scrutinizer Status\n    :target: https://scrutinizer-ci.com/g/admetricks/python-sqs-consumer/\n\n\n.. end-badges\n\nAn example package. Replace this with a proper project description. Generated with https://github.com/ionelmc/cookiecutter-pylibrary\n\n* Free software: BSD license\n\nInstallation\n============\n\n::\n\n    pip install python_sqs_consumer\n\nDocumentation\n=============\n\nhttps://python-sqs-consumer.readthedocs.org/\n\nDevelopment\n===========\n\nTo run the all tests run::\n\n    tox\n',
    'author': 'Juan Pizarro',
    'author_email': 'jpizarrom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/admetricks/python-sqs-consumer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
