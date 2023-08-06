#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Directory of necessary packages

packages dictionary is structured in the following schema:
    {
        <group> : {
            <import_name> : <install_name>
        }
    }
"""

packages = {
    'required' : {
        #  'setuptools' : 'setuptools',
        'wheel' : 'wheel>=0.34.2',
        'yaml' : 'PyYAML>=5.3.1',
        'cascadict' : 'cascadict>=0.8.4',
        'virtualenv' : 'virtualenv>=20.1.0',
    },
    'minimal' : {},
    'formatting' : {
        'pprintpp'          : 'pprintpp>=0.4.0',
        'asciitree'         : 'asciitree>=0.3.3',
        'typing_extensions' : 'typing_extensions>=3.7.4.3',
        'pygments'          : 'pygments>=2.7.2',
        'colorama'          : 'colorama>=0.4.3',
        'rich'              : 'rich>=9.8.0',
        'more_termcolor'    : 'more-termcolor>=1.1.3',
    },
    '_required' : {
        'pip'               : 'pip>=21.0.1',
        'update_checker'    : 'update-checker>=0.18.0',
        'semver'            : 'semver>=2.13.0',
        'dateutil'          : 'python-dateutil>=2.7.5',
        'requests'          : 'requests>=2.23.0',
        'pyvim'             : 'pyvim>=3.0.2',
        'aiofiles'          : 'aiofiles>=0.6.0',
        'packaging'         : 'packaging>=20.4',
        'prompt_toolkit'    : 'prompt-toolkit>=3.0.11',
        'more_itertools'    : 'more-itertools>=8.7.0',
    },
    'iot' : {
        'paho' : 'paho-mqtt>=1.5.1',
    },
    'drivers' : {
        'psycopg2' : 'psycopg2-binary>=2.8.6',
        'pymysql'  : 'PyMySQL>=0.10.1',
    },
    'cli' : {
        'pgcli'    : 'pgcli>=3.1.0',
        'mycli'    : 'mycli>=1.23.2',
        'litecli'  : 'litecli>=1.5.0',
        'mssqlcli' : 'mssqlcli>=1.0.4',
    },
    'stack' : {
        'docker'  : 'docker>=4.3.1',
        'compose' : 'docker-compose>=1.27.4',
    },
    'build' : {
        'cx_Freeze'   : 'cx_Freeze>=6.5.1',
        'PyInstaller' : 'pyinstaller>=5.0.dev0',
    },
    'dev-tools' : {
        'twine' : 'twine>=3.2.0',
        'tuna'     : 'tuna>=0.5.3',
        'snakeviz' : 'snakeviz>=2.1.0',
        'mypy' : 'mypy>=0.812',
        'pytest' : 'pytest>=6.2.2',
    },
    'setup' : {
    },
    'docs' : {
        'mkdocs'                      : 'mkdocs>=1.1.2',
        'pdoc'                        : 'pdoc3>=0.9.2',
        'mkdocs_material'             : 'mkdocs-material>=6.2.5',
        'mkdocs_autolinks_plugin'     : 'mkdocs-autolinks-plugin>=0.2.0',
        'mkdocs_awesome_pages_plugin' : 'mkdocs-awesome-pages-plugin>=2.5.0',
    },
    'portable' : {
        'pyreadline' : 'pyreadline>=2.1; platform_system == "Windows"',
        'gnureadline' : 'gnureadline>=8.0.0; platform_system != "Windows"',
    },
    'extras' : {
        'cmd2' : 'cmd2>=1.4.0',
        'ruamel.yaml' : 'ruamel.yaml>=0.16.12',
        'pandasgui' : 'pandasgui>=0.2.9',      
        'modin' : 'modin[ray]>=0.8.3'
    },
}
packages['sql'] = {
    'numpy'      : 'numpy>=1.18.5',
    'pandas'     : 'pandas>=1.1.4',
    'sqlalchemy' : 'sqlalchemy>=1.2.19',
    'databases'  : 'databases>=0.4.0',
    'aiosqlite'  : 'aiosqlite>=0.16.0',
    'asyncpg'    : 'asyncpg>=0.21.0',
}
packages['sql'].update(packages['drivers'])
packages['api'] = {
    'uvicorn'       : 'uvicorn>=0.12.2',
    'websockets'    : 'websockets>=8.1',
    'fastapi'       : 'fastapi>=0.61.2',
    'jinja2'        : 'jinja2>=2.11.2',
    'passlib'       : 'passlib>=1.7.4',
    'fastapi_login' : 'fastapi-login>=1.5.3',
    'multipart'     : 'python-multipart>=0.0.5',
}
packages['api'].update(packages['sql'])
packages['api'].update(packages['_required'])
packages['api'].update(packages['formatting'])

all_packages = dict()
for group, import_names in packages.items():
    all_packages.update(import_names)

skip_groups = {'docs', 'build', 'cli', 'dev-tools', 'portable', 'extras'}
full = list()
_full = dict()
for group, import_names in packages.items():
    ### omit 'cli' and 'docs' from 'full'
    if group in skip_groups:
        continue
    full += [ install_name for import_name, install_name in import_names.items() ]
    for import_name, install_name in import_names.items():
        _full[import_name] = install_name
packages['full'] = _full

