#!/usr/bin/env python3
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

import io
import os
import re
from configparser import ConfigParser
from setuptools import setup, find_packages

MODULE2PREFIX = {
    'nereid_catalog': 'm9s',
    'payment_gateway': 'm9s',
    'sale_channel': 'm9s',
    'sale_payment_gateway': 'm9s',
    'shipping': 'm9s',
    }


def read(fname, slice=None):
    content = io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()
    if slice:
        content = '\n'.join(content.splitlines()[slice])
    return content


def get_require_version(name):
    if minor_version % 2:
        require = '%s >= %s.%s.dev0, < %s.%s'
    else:
        require = '%s >= %s.%s, < %s.%s'
    require %= (name, major_version, minor_version,
        major_version, minor_version + 1)
    return require


config = ConfigParser()
config.read_file(open(os.path.join(os.path.dirname(__file__), 'tryton.cfg')))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
version = info.get('version', '0.0.1')
major_version, minor_version, _ = version.split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)
name = 'm9s_nereid_cart_b2c'
download_url = 'https://gitlab.com/m9s/nereid_cart_b2c.git'
local_version = []
for build in ['CI_BUILD_NUMBER', 'CI_JOB_NUMBER', 'CI_JOB_ID']:
    if os.environ.get(build):
        local_version.append(os.environ[build])
if local_version:
    version += '+' + '.'.join(local_version)
requires = [
    'email_validator',
    'blinker',
    ]
for dep in info.get('depends', []):
    if not re.match(r'(ir|res)(\W|$)', dep):
        prefix = MODULE2PREFIX.get(dep, 'trytond')
        requires.append(get_require_version('%s_%s' % (prefix, dep)))
requires.append(get_require_version('trytond'))

tests_require = [
    get_require_version('m9s-sale-payment-gateway'),
    get_require_version('m9s-shipping'),
    ]
dependency_links = []
if minor_version % 2:
    dependency_links.append('https://trydevpi.tryton.org/?mirror=bitbucket')

setup(name=name,
    version=version,
    description='Tryton Nereid Cart B2C Module',
    long_description=read('README.md'),
    author='MBSolutions',
    author_email='info@m9s.biz',
    url='http://www.m9s.biz/',
    download_url=download_url,
    project_urls={
        "Bug Tracker": 'https://support.m9s.biz/',
        "Source Code": 'https://gitlab.com/m9s/nereid_cart_b2c.git',
        },
    keywords='',
    package_dir={'trytond.modules.nereid_cart_b2c': '.'},
    packages=(
        ['trytond.modules.nereid_cart_b2c'] +
        ['trytond.modules.nereid_cart_b2c.%s' % p for p in find_packages()]
        ),
    package_data={
        'trytond.modules.nereid_cart_b2c': (info.get('xml', [])
            + ['tryton.cfg', 'view/*.xml', 'locale/*.po', '*.fodt',
                'icons/*.svg', 'tests/*.rst']),
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: Bulgarian',
        'Natural Language :: Catalan',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Czech',
        'Natural Language :: Dutch',
        'Natural Language :: English',
        'Natural Language :: French',
        'Natural Language :: German',
        'Natural Language :: Hungarian',
        'Natural Language :: Italian',
        'Natural Language :: Persian',
        'Natural Language :: Polish',
        'Natural Language :: Portuguese (Brazilian)',
        'Natural Language :: Russian',
        'Natural Language :: Slovenian',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Office/Business',
        ],
    license='GPL-3',
    python_requires='>=3.5',
    install_requires=requires,
    dependency_links=dependency_links,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    nereid_cart_b2c = trytond.modules.nereid_cart_b2c
    """,
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
    tests_require=tests_require,
    )
