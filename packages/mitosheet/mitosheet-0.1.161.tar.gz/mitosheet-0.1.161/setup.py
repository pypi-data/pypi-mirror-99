#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function
from glob import glob
from os.path import join as pjoin


from setupbase import (
    create_cmdclass, install_npm, ensure_targets,
    find_packages, combine_commands, ensure_python,
    get_version, HERE
)

from setuptools import setup


# The name of the project
name = 'mitosheet'

# Ensure a valid python version
ensure_python('>=3.4')

# Get our version
version = get_version(pjoin(name, '_version.py'))

nb_path = pjoin(HERE, name, 'nbextension', 'static')
lab_path = pjoin(HERE, name, 'labextension')

# Representative files that should exist after a successful build
jstargets = [
    pjoin(nb_path, 'index.js'),
    pjoin(HERE, 'lib', 'plugin.js'),
]

package_data_spec = {
    name: [
        'nbextension/static/*.*js*',
        'labextension/*.tgz'
    ]
}

data_files_spec = [
    ('share/jupyter/nbextensions/mitosheet',
        nb_path, '*.js*'),
    ('share/jupyter/lab/extensions', lab_path, '*.tgz'),
    ('etc/jupyter/nbconfig/notebook.d' , HERE, 'mitosheet.json')
]


cmdclass = create_cmdclass('jsdeps', package_data_spec=package_data_spec,
    data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(HERE, build_cmd='build:all'),
    ensure_targets(jstargets),
)


setup_args = dict(
    name            = name,
    description     = 'The Mito Spreadsheet',
    version         = version,
    scripts         = glob(pjoin('scripts', '*')),
    cmdclass        = cmdclass,
    packages        = find_packages(),
    author          = 'Mito',
    author_email    = 'naterush1997@gmail.com',
    url             = 'https://github.com/mito/mito',
    license         = 'BSD',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Jupyter', 'Widgets', 'IPython'],
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Jupyter',
    ],
    include_package_data = True,
    install_requires = [
        # We require jupyterlab 2.0
        'jupyterlab>=2.0,<3.0',
        'ipywidgets>=7.0.0',
        'pandas>=1.1.0',
        'matplotlib>=3.3',
        # We don't need to lock an analytics-python version, as this library
        # is stabilized and mature
        'analytics-python'
    ],
    extras_require = {
        'test': [
            'pytest>=4.6',
            'pytest-cov',
            'nbval',
        ],
        'examples': [
            # Any requirements for the examples to run
        ],
        'docs': [
            'sphinx>=1.5',
            'recommonmark',
            'sphinx_rtd_theme',
            'nbsphinx>=0.2.13,<0.4.0',
            'jupyter_sphinx',
            'nbsphinx-link',
            'pytest_check_links',
            'pypandoc',
        ],
    },
    entry_points = {
    },
    long_description="""
        To learn more about Mito, checkout out our documentation: https://docs.trymito.io/getting-started/installing-mito\n\n
        Before installing Mito \n\n
        1. Check that you have Python 3.6 or above. To check your version of Python, open a new terminal, and type python3 --version. If you need to install or update Python, restart your terminal after doing so.\n\n
        2. Check that you have Node installed.To check this, open a new terminal, and type node -v.  It should print a version number. If you need to install Node, restart your terminal after doing so.\n\n
        3. Mito works in Jupyter Lab 2.0 only. We do not yet support Google Collab, VSCode, or Jupyter Lab 3.0.\n\n
        4. Checkout our terms of service and privacy policy. By installing Mito, you're agreeing to both of them. Please contact us at aarondr77 (@) gmail.com with any questions.\n\n
        Installation Instructions \n\n
        For more detailed installation instructions, see our documentation: https://docs.trymito.io/getting-started/installing-mito\n\n
        1. pip install mitosheet\n\n
        2. jupyter labextension install @jupyter-widgets/jupyterlab-manager@2\n\n
        3. jupyter lab
    """,
    long_description_content_type='text/markdown'
)

if __name__ == '__main__':
    setup(**setup_args)
