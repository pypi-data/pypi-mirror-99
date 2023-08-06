# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arma_server_tools']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click-log>=0.3.2,<0.4.0',
 'click>=7.1.2,<8.0.0',
 'pytest>=6.2.2,<7.0.0',
 'pyyaml>=5.4.1,<6.0.0',
 'rich>=9.13.0,<10.0.0']

entry_points = \
{'console_scripts': ['arma_server = arma_server_tools.arma_server:main',
                     'preset_parser = arma_server_tools.preset_parser:main',
                     'steam_pull = arma_server_tools.workshop:main']}

setup_kwargs = {
    'name': 'arma-server-tools',
    'version': '0.1.1',
    'description': 'Tools to manage content for arma3Server',
    'long_description': '# arma server tools\n\nTools to manage running content on arma3server\n\n## reference material\n\n### commands\n\n    poetry run server --help\n    poetry run pull --help\n\n### Arma server stuff\n\n- <https://community.bistudio.com/wiki/Arma_Dedicated_Server>\n- <https://community.bistudio.com/wiki/server.cfg>\n- <https://developer.valvesoftware.com/wiki/Arma_3_Dedicated_Server>\n\n### python libraries\n\n- [poetry](https://python-poetry.org)\n- [click](https://click.palletsprojects.com/en/7.x/)\n- [click_log](https://click-log.readthedocs.io)\n- [rich](https://rich.readthedocs.io/en/stable/introduction.html)\n- [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)\n- [pytest](https://docs.pytest.org/en/stable/)\n\n\n### articles references\n\n- <https://docs.python.org/3/library/subprocess.html>\n- <https://docs.python.org/3/library/shutil.html>\n- <https://docs.python.org/3/library/os.html?highlight=os%20symlink#os.symlink>\n\n## yaml files\n\n### yaml config in home dir\n\n~~~\n--- # ~/arma_server.yaml\nusername: steam_username\npassword: steam_password\nworkshop: "/home/steam/.steam/steamapps/workshop/content/107410"\narma_home: "/home/steam/.steam/steamcmd/arma3"\narma_configs: "/home/steam/arma_configs"\n~~~\n\n### yaml config for specific server\n\n- name: name of the server\n- config: relative path to the arma cfg file, starting from the arma_configs folder\n- port: port the server is on, defaults to 2302 if nothing is set\n- mods: list of mods to load\n\nwithout mods\n\n~~~\n--- # example without mods\nname: direct_action_altis\nconfig: direct_action/direct_action_altis.cfg\nport: 2302\n~~~\n\nwith mods\n\n~~~\n--- # example with some mods \nname: survival_altis\nconfig: survival/survival_altis.cfg\nmods: \n  - cba_a3 \n  - niarms_all\n~~~\n\n',
    'author': 'ryantownshend',
    'author_email': 'citizen.townshend@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ryantownshend/arma_server_tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
