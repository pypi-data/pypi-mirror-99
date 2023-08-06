# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfddns']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'cloudflare>=2.8.13,<3.0.0']

entry_points = \
{'console_scripts': ['cfddns = cfddns.cli:main']}

setup_kwargs = {
    'name': 'cfddns',
    'version': '1.5.0',
    'description': 'DDNS client for Cloudflare DNS',
    'long_description': '# cfddns\n\nDynamic DNS client for Cloudflare DNS.\n\n## Usage\n\n```bash\ncat << EOD > domains\nexample.com\nmail.example.com\nexample.org\nEOD\n\ncat <<EOD > cfddns.yml\ntoken: "<CloudFlare API token>"\ninterval: 900 # in seconds (optional)\nendpoint: "https://api.ipify.org" # (optional)\nEOD\n\ncfddns -c cfddns.yml domains\n```\n\n## Install\n\n### Arch Linux\n\nInstall `cfddns` via [AUR](https://aur.archlinux.org/packages/cfddns/).\n\n```bash\ngit clone https://aur.archlinux.org/cfddns.git && cd cfddns\nmakepkg -si\n\ncat << EOD > /etc/cfddns/domains\nexample.com\nmail.example.com\nexample.org\nEOD\n\nvim /etc/cfddns/cfddns.yml # assign `token`\n\nsystemctl enable --now cfddns\n```\n\n### Build from source\n\n```bash\ngit clone https://github.com/uetchy/cfddns.git && cd cfddns\npoetry install --build\n```\n',
    'author': 'Yasuaki Uechi',
    'author_email': 'y@uechi.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uetchy/cfddns',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)
