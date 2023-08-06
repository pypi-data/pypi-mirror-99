import inspect
import os
import platform
import sys
from os.path import abspath, dirname, join, isdir

import git
import requests
import setuptools
from distutils.cmd import Command
from trove_classifiers import classifiers as trove_classifiers

NAMESPACE = [
    folder for folder in next(os.walk('src'))[1]
    if not folder.startswith('script') and not folder.endswith('egg-info')
][0]
PACKAGE = next(os.walk(f'src/{NAMESPACE}'))[1][0]
CLASSIFIERS = []


# SETUP COMMANDS
def cmd(func):
    """
    Decorator to turn a function in a runnable setup command
    `python setup.py <func>`
    """

    if func is None:
        raise ValueError('Command function must be provided')

    def construction(_func):
        class SetupCommand(Command):
            user_options = []
            description = _func.__doc__ or ''
            initialize_options = lambda self: ''
            finalize_options = lambda self: ''
            run = lambda self: _func()

        return SetupCommand

    return construction(func)


@cmd
def rename_package():
    """Rename package filesystem to match repo owner and project names"""

    origin_url = git.Repo().remotes.origin.url
    namespace, package = origin_url \
                             .split(':')[1] \
                             .replace('.', '/') \
                             .replace('-', '_') \
                             .split('/')[:-1]

    os.rename(join('src', NAMESPACE), join('src', namespace))
    os.rename(join(f'src/{namespace}', PACKAGE), join(f'src/{NAMESPACE}', package))


# PACKAGE METADATA
def repository_info():
    origin_url = git.Repo().remotes.origin.url
    response = requests.get(
        'https://api.github.com/repos/' + origin_url.split(':')[1][:-4],
        headers={'Accept': 'application/vnd.github.v3+json'}
    ).json()

    import license
    license = license.find(response['license']['spdx_id'])
    CLASSIFIERS.append(license.python)

    return {
        'name': PACKAGE,
        'description': response['description'],
        'license': f"{license.name} ({license.id})",
        'url': response['html_url'],
    }


def package_version(relative_path):
    target_file = join(
        abspath(dirname(__file__)),
        relative_path
    )

    with open(target_file, 'r') as file:
        for line in file.read().splitlines():
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return {'version': line.split(delim)[1]}
        else:
            raise RuntimeError("Unable to find version string.")


def package_description():
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    return {
        'long_description': long_description,
        'long_description_content_type': "text/markdown",
    }


def author_info():
    git_global_config = git.Repo().config_reader('global')

    name = git_global_config.get('user', 'name')
    email = git_global_config.get("user", "email")

    return {
        'author': name,
        'author_email': f"{name} <{email}>",
    }


def package_scripts(target_directory):
    if isdir(target_directory):
        _, _, scripts = next(os.walk(target_directory))
        return {
            'scripts': [
                f'{target_directory}/{filename}' for filename in scripts
            ]
        } if scripts else {}

    return {}


def setup_commands():
    return {
        'cmdclass': {
            name: cls
            for name, cls
            in inspect.getmembers(
                sys.modules[__name__],
                lambda obj: inspect.isclass(obj)
                            and issubclass(obj, Command)
                            and obj.__name__ != 'Command'
            )
        }
    }


def supported_platform():
    for key, classifier in {
        'Windows': 'Operating System :: Microsoft :: Windows',
        'Linux': 'Operating System :: POSIX :: Linux',
        'Darwin': 'Operating System :: MacOS'
    }.items():
        if key == platform.system():
            CLASSIFIERS.append(classifier)

    return {
        'platforms': f'{platform.system()} {platform.version()} {platform.machine()}'
    }


def interpreter_info():
    version = platform.python_version()

    for classifier in [
        f'Programming Language :: Python :: Implementation :: {platform.python_implementation()}',
        f'Programming Language :: Python :: {version[:1]}',
        f'Programming Language :: Python :: {version[:1]} :: Only',
        f'Programming Language :: Python :: {version[:3]}',
    ]:
        CLASSIFIERS.append(classifier)

    return {
        'python_requires': f'>={version[:3]}'
    }


def package_classifiers(*classifiers):
    return [
        c for c in CLASSIFIERS + list(classifiers)
        if c in trove_classifiers
    ]

    # https://pypi.org/classifiers/


setuptools.setup(
    # name='',
    # description='',
    # license=''
    # url='',
    **repository_info(),

    # version='',
    **package_version(f'src/{NAMESPACE}/{PACKAGE}/__init__.py'),

    # long_description='',
    # long_description_content_type='',
    **package_description(),

    # author='',
    # author_email='',
    **author_info(),

    # project_urls={
    #     'Documentation': '',
    #     'Funding': '',
    #     'Say Thanks!': '',
    #     'Source': '',
    #     'Tracker': '',
    # }

    # keywords=''

    packages=setuptools.find_namespace_packages(where='src'),
    package_dir={'': 'src'},

    # scripts=''
    **package_scripts('src/scripts'),

    entry_points={
        'console_scripts': [
            f'{PACKAGE}={NAMESPACE}.{PACKAGE}:main',
        ],
    },

    # cmdclass={},
    **setup_commands(),

    # install_requires=[],
    extras_require={
        'dev': [
            'pip >= 21.x, <22.0',
            'setuptools >=54.x, <55.0',
            'wheel >=0.36, <1.0',
            'twine >=3.x, <4.0',
            'trove-classifiers >=2021.x',
            'license',
            'GitPython >=3.x, <4.0',
            'requests >=2.x, <3.0'
        ]
    },

    # python_requires='
    **interpreter_info(),

    # platform=''
    **supported_platform(),

    classifiers=package_classifiers(
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha'
        # 'Development Status :: 3 - Alpha'
        # 'Development Status :: 4 - Beta'
        # 'Development Status :: 5 - Production/Stable'
        # 'Development Status :: 6 - Mature'
        # 'Development Status :: 7 - Inactive'

        # 'Intended Audience :: Customer Service',
        'Intended Audience :: Developers',
        # 'Intended Audience :: Education',
        # 'Intended Audience :: End Users/Desktop',
        # 'Intended Audience :: Financial and Insurance Industry',
        # 'Intended Audience :: Healthcare Industry',
        # 'Intended Audience :: Information Technology',
        # 'Intended Audience :: Legal Industry',
        # 'Intended Audience :: Manufacturing',
        # 'Intended Audience :: Other Audience',
        # 'Intended Audience :: Religion',
        # 'Intended Audience :: Science/Research',
        # 'Intended Audience :: System Administrators',
        # 'Intended Audience :: Telecommunications Industry',

        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    )
)
