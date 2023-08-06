# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['oidcmsg', 'oidcmsg.oauth2', 'oidcmsg.oidc', 'oidcmsg.storage']

package_data = \
{'': ['*']}

install_requires = \
['cryptojwt>=1.5.0,<2.0.0', 'filelock>=3.0.12,<4.0.0']

setup_kwargs = {
    'name': 'oidcmsg',
    'version': '1.2.0',
    'description': 'Python implementation of OAuth2 and OpenID Connect messages',
    'long_description': '# oidcmsg\nImplementation of OIDC protocol messages.\n\noidcmsg is the 2nd layer in the\nJwtConnect stack (cryptojwt, oidcmsg, oidcservice, oidcrp)\n\nHandles serialising into a couple of formats (jwt, json, urlencoded and dict) and deserialising from said formats.\n\nIt also does verification of messages , that is :\n\n+ verifies that all the required parameters are present and has a value\n+ verifies that the parameter values are of the right type\n+ verifies that if there is a list of permitted values, a parameter value is on \nthat list.\n\nand finally if the value is a signed and/or encrypted JWT this package\nwill perform the necessary decryption and signature verification. \n\n\nAlso implements a **KeyJar** which keeps keys belonging to \ndifferent owners. One owner may have many keys.\nIf some of these keys have a common origin, like described in a JWKS.\nSuch a set will be kept in a **keyBundle**.\nAlso implemented in this package. \n   \nPlease read the [Official Documentation](https://oidcmsg.readthedocs.io/) for getting usage examples and further informations.\n',
    'author': 'roland',
    'author_email': 'roland@catalogix.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/IdentityPython/JWTConnect-Python-OidcMsg',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
