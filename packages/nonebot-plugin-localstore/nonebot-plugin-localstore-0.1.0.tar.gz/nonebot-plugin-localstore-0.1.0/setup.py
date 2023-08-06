# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_localstore']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-alpha.8,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-localstore',
    'version': '0.1.0',
    'description': 'Local Storage Support for NoneBot2',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# NoneBot Plugin LocalStore\n\n_✨ NoneBot 本地存储插件 ✨_\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/nonebot/plugin-localstore/master/LICENSE">\n    <img src="https://img.shields.io/github/license/nonebot/plugin-localstore.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-localstore">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-localstore.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">\n</p>\n\n## 使用方式\n\n加载插件后使用 `require` 获取导出方法\n\n```python\nfrom nonebot import require\n\nstore = require("nonebot_plugin_localstore")\n\nplugin_cache_dir = store.get_cache_dir("plugin_name")\nplugin_cache_file = store.get_cache_file("plugin_name", "filename")\nplugin_config_dir = store.get_config_dir("plugin_name", "filename")\nplugin_config_file = store.get_config_file("plugin_name", "filename")\nplugin_data_dir = store.get_data_dir("plugin_name")\nplugin_data_file = store.get_data_file("plugin_name", "filename")\n```\n\n## 存储路径\n\n### cache path\n\n- macOS: `~/Library/Caches/<AppName>`\n- Unix: `~/.cache/<AppName>` (XDG default)\n- Windows: `C:\\Users\\<username>\\AppData\\Local\\<AppName>\\Cache`\n\n### data path\n\n- macOS: `~/Library/Application Support/<AppName>`\n- Unix: `~/.local/share/<AppName>` or in $XDG_DATA_HOME, if defined\n- Win XP (not roaming): `C:\\Documents and Settings\\<username>\\Application Data\\<AppName>`\n- Win 7 (not roaming): `C:\\Users\\<username>\\AppData\\Local\\<AppName>`\n\n### config path\n\n- macOS: same as user_data_dir\n- Unix: `~/.config/<AppName>`\n- Win XP (roaming): `C:\\Documents and Settings\\<username>\\Local Settings\\Application Data\\<AppName>`\n- Win 7 (roaming): `C:\\Users\\<username>\\AppData\\Roaming\\<AppName>`\n',
    'author': 'yanyongyu',
    'author_email': 'yanyongyu_1@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nonebot/plugin-localstore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
