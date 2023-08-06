##############################################################################
#
# Copyright (c) 2010 Projekt01 GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id:$
"""

import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name = 'p01.recipe.setup',
    version='0.8.18',
    author = 'Roger Ineichen and the Zope Community',
    author_email = 'zope-dev@zope.org',
    description = 'Development and installation recipes',
    long_description=(
        read('README.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
    license = 'ZPL 2.1',
    keywords = 'zope3 p01 dev recipe setup installation installer',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3',
        ],
    url = 'http://pypi.python.org/pypi/p01.recipe.setup',
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['p01', 'p01.recipe'],
    extras_require = dict(
        test = [
            'p01.checker',
            'zc.lockfile',
            'zope.testing',
            'zc.buildout',
            'zope.app.applicationcontrol',
            'ZODB3',
            'meld3',
            ],
        paste = [
            'Paste',
            'PasteDeploy',
            'PasteScript',
            ],
        supervisor = [
            'supervisor',
            'superlance',
            ],
        i18n = [
            'polib',
            'zope.app.appsetup',
            'zope.app.locales [extract]',
        ],
        sphinx = [
            'Sphinx',
        ]
        ),
    install_requires = [
        'ZConfig >=2.4a5',
        'setuptools',
        'six',
        'zc.buildout',
        'zc.recipe.egg',
        ],
    entry_points = {
        'zc.buildout': [
             'celery = p01.recipe.setup.celery:CeleryRecipe',
             'cmd = p01.recipe.setup.cmd:CMDRecipe',
             'cmmi = p01.recipe.setup.cmmi:CMMIRecipe',
             'copy = p01.recipe.setup.copy:COPYRecipe',
             'copyscript = p01.recipe.setup.copy:COPYScriptRecipe',
             'ctags = p01.recipe.setup.ctags:CTagsRecipe',
             'download = p01.recipe.setup.download:DownloadRecipe',
             'egg-scripts = p01.recipe.setup.egg:ScriptsRecipe',
             'fetch = p01.recipe.setup.fetch:FetchScriptRecipe',
             'i18n = p01.recipe.setup.i18n:I18nSetup',
             'importchecker = p01.recipe.setup.importchecker:ImportCheckerRecipe',
             'make = p01.recipe.setup.make:MakeScriptRecipe',
             'mkdir = p01.recipe.setup.mkdir:MKDirRecipe',
             'mkfile = p01.recipe.setup.mkfile:MKFileRecipe',
             'paste = p01.recipe.setup.paste:PasteServeSetup',
             'popen = p01.recipe.setup.popen:PopenRecipe',
             'script = p01.recipe.setup.script:ScriptRecipe',
             'scripts = p01.recipe.setup.script:ScriptsRecipe',
             'settings = p01.recipe.setup.settings:SettingsRecipe',
             'sphinx = p01.recipe.setup.sphinxdoc:SphinxDocRecipe',
             'supervisor = p01.recipe.setup.supervisor:SupervisorRecipe',
             'template = p01.recipe.setup.template:TemplateRecipe',
             'winservice = p01.recipe.setup.winservice:WinServiceSetup',
         ],
        'console_scripts': [
            'ctags = p01.recipe.setup.ctags:ctags',
        ]
    },
    zip_safe = False,
)
