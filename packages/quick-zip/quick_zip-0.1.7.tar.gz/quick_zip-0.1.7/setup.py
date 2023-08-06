# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quick_zip',
 'quick_zip.commands',
 'quick_zip.core',
 'quick_zip.schema',
 'quick_zip.services',
 'quick_zip.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'python-slugify>=4.0.1,<5.0.0',
 'pyzipper>=0.3.4,<0.4.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.13.0,<10.0.0',
 'toml==0.10.2',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['qz = quick_zip.main:main']}

setup_kwargs = {
    'name': 'quick-zip',
    'version': '0.1.7',
    'description': '',
    'long_description': '[![Github All Releases](https://img.shields.io/github/downloads/hay-kot/quick_zip/total.svg)]()\n[![GitHub Release](https://img.shields.io/github/release/hay-kot/quick_zip.svg?style=flat)]()\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)\n\n# About the Project\n\n[Documentation](https://hay-kot.github.io/quick-zip-cli/)\n\n## What QuickZip Is\nQuickZip is a CLI utility I developed to solve a backup problem on my machines. I wanted a way to quickly backup up small sets of configuration files and data without deploying a massive, hard to maintain tool with too much front-end configuration. QuickZip uses a config.toml file to build tiny list of backups that are conducted when called (typically via cron). \n\n### Key Features\n - Create jobs with configuration file, including support for variables and defaults\n - Beautiful CLI\n - Backup Audits\n - Webhook Support\n\n\n```console\n\n$ quick-zip --help\n\nUsage: qz [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --verbose / --no-verbose        [default: False]\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n\n  --help                          Show this message and exit.\n\nCommands:\n  audit   🧐 Performs ONLY the audits for configured jobs\n  config  📄 displays the configuration file\n  docs    💬 Opens quickZip documentation in browser\n  jobs\n  run     ✨ The main entrypoint for the application.\n\n```\n\n\n## What QuickZip Isn\'t\nQuickZip is NOT a replacement for a robust backup or imaging software. It\'s primary use case is to collect configuration files on system other similar types of files, zip them up, and stick them somewhere else on your file system. \n\n## Why not *x*???\nI can\'t comment on every backup utility but I can mention the few that I looked at. **Borg** was a strong contender and I will likely use it for other things down the line, however I felt like there was too much upfront configuration before being able to use. **Rsync** / **Rclone** were both great options but I felt there were too confusing/robust for what I was trying to do. On top of that, I was looking for a few features that I hadn\'t seen. \n\n- Backup Audits: The ability to "audit" backups and specify how old the newest backup should be \n- Webhook Support: Send backup data to Home Assistant for notifications and dashboards. \n\nAlso, I just like building stuff. 👍\n\n\n## To Do\'s\n- [x] Fix animated terminals for docs\n- [x] Only run some jobs\n- [x] Read config path from .env\n- [x] CLI implementation\n- [x] Auditor Commands\n- [ ] Update Documentation\n- [ ] Job Configuration\n    - [x] Set default values\n    - [x] Use variables in config file\n    - [x] Add property for glob style matching\n    - [x] Pass list of files to zip in config file.\n    - [ ] Git Repo Backup\n    - [ ] Web Download Backup\n- [x] Tests\n    - [x] Reading .toml file\n    - [x] Find/Replace Vars\n    - [x] Validate Input/Output\n- [ ] Release v0.1.0\n    - [ ] Poetry Package\n- [ ] Encrypted Zip Files',
    'author': 'hay-kot',
    'author_email': 'hay-kot@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hay-kot.github.io/quick-zip-cli/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
