#! /usr/bin/env python
#
# Copyright (C) 2018 Raphael Vallat

DESCRIPTION = "Yet Another Spindle Algorithm"
LONG_DESCRIPTION = """YASA (Yet Another Spindle Algorithm) : fast and robust detection of spindles, slow-waves, and rapid eye movements from sleep EEG recordings..
"""

DISTNAME = 'yasa'
MAINTAINER = 'Raphael Vallat'
MAINTAINER_EMAIL = 'raphaelvallat9@gmail.com'
URL = 'https://github.com/raphaelvallat/yasa/'
LICENSE = 'BSD (3-clause)'
DOWNLOAD_URL = 'https://github.com/raphaelvallat/yasa/'
VERSION = '0.4.1'
PACKAGE_DATA = {'yasa.data.icons': ['*.svg']}

INSTALL_REQUIRES = [
    'numpy',
    'scipy',
    'pandas',
    'matplotlib',
    'seaborn',
    'mne>=0.20.0',
    'numba',
    'outdated',
    'antropy',
    'scikit-learn>=0.21',
    'tensorpac>=0.6.4',
    'pyriemann',
    'lspopt',
    'ipywidgets',
    'joblib'
]

PACKAGES = [
    'yasa',
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: BSD License',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Operating System :: MacOS'
]

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup

if __name__ == "__main__":

    setup(name=DISTNAME,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          install_requires=INSTALL_REQUIRES,
          include_package_data=True,
          packages=PACKAGES,
          package_data=PACKAGE_DATA,
          classifiers=CLASSIFIERS,
          )
