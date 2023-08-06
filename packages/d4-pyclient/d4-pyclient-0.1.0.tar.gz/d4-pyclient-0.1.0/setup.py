# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['d4_pyclient']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'd4-pyclient',
    'version': '0.1.0',
    'description': 'D4 core software client in Python',
    'long_description': "# Main features\n\n**d4-pyclient** is python implemention of the [D4 encapsulation\nprotocol](https://github.com/D4-project/architecture/tree/master/format). \n\nIt is a low-barrier entry for anyone interested into tinkering with the D4\nprotocol or embedding a d4 client into another project. It supports both regular\ntypes and types defined by meta-header.\n\n# Launching\n\n```shell\n./d4-pyclient.py -h\nusage: d4-pyclient.py [-h] -c CONFIG [-cc]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -c CONFIG, --config CONFIG\n                        config directory\n  -cc, --check_certificate\n                        check server certificate\n```\n\n# Configuration Files\n\n of the client configuration can be stored in folder containing the following files:\n\n - key: your Pre-Shared-Key\n - snaplen: default is 4096\n - source: stdin or d4server\n - destination: stdout, [fe80::ffff:ffff:ffff:a6fb]:4443, 127.0.0.1:4443\n - type: D4 packet type, see [types](https://github.com/D4-project/architecture/tree/master/format)\n - uuid: generated automatically if empty\n - version: protocol version\n - rootCA.crt: optional : CA certificate to check the server certificate\n - metaheader.json: optional : a json file describing feed's meta-type [types](https://github.com/D4-project/architecture/tree/master/format)\n",
    'author': 'Aurelien Thirion (Terrtia)',
    'author_email': 'aurelien.thirion@circl.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/D4-project/d4-pyclientL',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
