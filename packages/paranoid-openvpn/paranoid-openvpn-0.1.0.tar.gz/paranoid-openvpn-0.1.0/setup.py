# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['paranoid_openvpn']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.7.4.3,<4.0.0.0']}

entry_points = \
{'console_scripts': ['paranoid_openvpn = paranoid_openvpn.cli:cli']}

setup_kwargs = {
    'name': 'paranoid-openvpn',
    'version': '0.1.0',
    'description': 'Hardening script for OpenVPN client profiles',
    'long_description': '# Paranoid OpenVPN\n\nParanoid OpenVPN hardens OpenVPN profiles and provides additional optional\nprovider-specific fixes (e.g. Priviate Internet Access).\n\n## Usage\n\nWhen installed, Paranoid OpenVPN provides the `paranoid_openvpn` executable\nwhich comes with built-in help.  These are the common options:\n\n```console\n$ pip install paranoid-openvpn\n$ # usage: paranoid_openvpn [--min-tls {1.0,1.1,1.2,1.3}] [--pia] source dest\n$ # Process a remote zip file of OpenVPN profiles and apply PIA fixes\n$ paranoid_openvpn --pia https://www.privateinternetaccess.com/openvpn/openvpn-strong.zip /path/to/output_dir\n$ # Process one profile and allow TLS 1.2 (default is 1.3)\n$ paranoid_openvpn --min-tls 1.2 /path/to/input/profile.ovpn /path/to/output/hardened.ovpn\n```\n\n`source` above can be a remote zip, remote single profile, local zip, local\nsingle file, or local directory.\n\n## Hardening OpenVPN\n\nMost OpenVPN users are aware of the `cipher` and `hash` settings but that is\nusually the extent of security options that people modify. OpenVPN, however,\nhas two distinct channels that each have their own security settings: the\ncontrol and data channel. The `cipher` and `hash` settings apply only to the\ndata channel but OpenVPN exposes settings for the control channel as well.\nThe control channel is used to exchange keys that are then used to encrypt\nyour traffic in the data channel.\n\nParanoid OpenVPN tries to match the security of the data channel to the control\nchannel. In broad terms, OpenVPN has options for <128-bit, 128-bit, 192-bit,\nand 256-bit ciphers for the data channel. Paranoid OpenVPN will configure the\ncontrol channel to match these protection levels, with an absolute minimum of\n128-bits.\n\n## Cryptographic Reasoning\n\nWhere cryptographic judgement calls needed to be made, these rules were followed:\n\n  * [AEAD ciphers][aead] are always preferred over non-AEAD ciphers\n  * At the 256-bit security level, AES-GCM was preferred over CHACHA20-POLY1305\n    (for no particular reason).\n  * The 192-bit security level is rounded up to 256-bit as there are no 192-bit\n    TLS ciphers.\n  * At the 128-bit security level, CHACHA20-POLY1305 was the preferred fallback\n    for AES-128-GCM instead AES-128-CBC because it is an AEAD cipher.\n    AES-128-CBC is then the fallback for CHACHA20-POLY1305.\n\n[aead]: https://en.wikipedia.org/wiki/Authenticated_encryption\n\n## Provider-specific Fixes\n\nMost VPN providers work fine with "normal" OpenVPN profiles but some providers\nbenefit from a few tweaks.\n\n### Private Internet Access (PIA)\n\nPIA\'s provided OpenVPN profiles seemingly only support AES-128-CBC and\nAES-256-CBC as the `cipher` option.  However with a little coaxing, PIA will\nconnect using AES-256-GCM and AES-128-GCM. Use the `--pia` flag to allow\nyour client to client with these AEAD ciphers.\n\n## Donations\n\nIf you use this project and feel it\'s worth a donation, check out\n[GitHub Sponsors][ghs] or [Buy Me a Coffee][bmac].\n\n[ghs]: https://github.com/sponsors/Caligatio\n[bmac]: https://www.buymeacoffee.com/caligatio\n\n## Credit\n\nA lot of inspiration for this project was taken from https://blog.securityevaluators.com/hardening-openvpn-in-2020-1672c3c4135a.\n',
    'author': 'Brian Turek',
    'author_email': 'brian.turek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Caligatio/paranoid-openvpn',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
