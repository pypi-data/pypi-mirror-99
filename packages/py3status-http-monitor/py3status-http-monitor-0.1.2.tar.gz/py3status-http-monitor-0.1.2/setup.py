# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py3status_http_monitor']

package_data = \
{'': ['*']}

install_requires = \
['py3status>=3.34,<4.0']

entry_points = \
{'py3status': ['module = py3status_http_monitor.http_monitor']}

setup_kwargs = {
    'name': 'py3status-http-monitor',
    'version': '0.1.2',
    'description': 'py3status http monitor show the status of http endpoints',
    'long_description': '# py3status-http-monitor\nPython module for monitoring **http** services in your py3status bar.\n\n## Screenshot\n![Status Bar with py3status_http_monitor](https://raw.githubusercontent.com/mcgillij/py3status-http-monitor/main/images/status_bar.png)\n\n## Prerequisites\n\nThis is an i3 / py3status module, so you\'ll need those first off.\n\n## Installation\n\n### From Git\n\n``` bash\ngit clone https://github.com/mcgillij/py3status-http-monitor.git\nmkdir -p ~/.i3/py3status && cd ~/.i3/py3status\nln -s <PATH_TO_CLONED_REPO>/src/py3status-http-monitor/http_monitor.py ./\n```\n\n### With Pip, Pipenv or Poetry\n\n``` bash\npip install py3status-http-monitor\npipenv install py3status-http-monitor\npoetry add py3status-http-monitor && poetry install\n```\n\n### Building Arch package w/PKGBUILD\n\n``` bash\ngit clone https://aur.archlinux.org/py3status-http-monitor.git\ncd py3status-http-monitor.git\nmakechrootpkg -c -r $HOME/$CHROOT\n```\n\n### Installing built Arch package\n\n``` bash\nsudo pacman -U --asdeps py3status-http-monitor-*-any.pkg.tar.zst\n```\n\n## Configuration\n\nNext you will need to add the services you want to monitor, and optionally choose some appropriate emoji\'s.\n\n**~/.config/i3/i3status.conf**\n\n```bash\n...\ngeneral {\n        colors = true\n        interval = 15\n}\n\norder += "http_monitor apache"\norder += "http_monitor medusa"\norder += "http_monitor pihole"\norder += "http_monitor nextcloud"\norder += "http_monitor plex"\norder += "http_monitor virtualbox"\norder += "http_monitor airsonic"\norder += "clock"\norder += "mail"\n...\n\nhttp_monitor  \'nextcloud\' {\n   service_location = "http://yourserver:8181"\n   service_name = \'⛅\'\n}\n\nhttp_monitor  \'virtualbox\' {\n   service_location = "http://yourserver:81/vb/"\n   service_name = \'💻\'\n}\n\nhttp_monitor  \'plex\' {\n   service_location = "http://yourserver:32400/web/index.html#"\n   service_name = \'🎥\'\n}\n\nhttp_monitor  \'airsonic\' {\n   service_location = "http://yourserver:4040"\n   service_name = \'🍃\'\n}\n\nhttp_monitor  \'pihole\' {\n   service_location = "http://yourserver:80"\n   service_name = \'🕳️ \'\n}\n\nhttp_monitor  \'apache\' {\n   service_location = "http://yourserver:81"\n   service_name = \'🪶\'\n}\n\nhttp_monitor  \'medusa\' {\n   service_location = "http://yourserver:8081"\n   service_name = \'🐍\'\n}\n```\n\n## Configuration Options\n\nYou can pass in the following configuration options:\n\n* service_location\n* service_name\n* timeout\n* cache_timeout\n\n## Restart i3\n\nOnce the package is installed and configured you just need to restart i3.\n',
    'author': 'mcgillij',
    'author_email': 'mcgillivray.jason@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcgillij/py3status-http-monitor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
