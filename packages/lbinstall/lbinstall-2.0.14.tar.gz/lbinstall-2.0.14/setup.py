#!/usr/bin/env python
""" lbinstall package
"""

from setuptools import setup, find_packages
import sys

dependencies = {
  '3': ['SQLAlchemy', 'six'],
  '2': ['SQLAlchemy', 'backports.lzma', 'six']
}


setup(name='lbinstall',
      use_scm_version=True,
      description='LHCb package installation tool',
      long_description='LHCb package installation tool',
      url='https://gitlab.cern.ch/lhcb-core/lbinstall',

      author='CERN - LHCb Core Software',
      author_email='lhcb-core-soft@cern.ch',

      license='GPL',

      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          # Indicate who your project is intended for
          # 'Intended Audience :: Users',
          # 'Topic :: Software Installation :: Installation',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',

      ],

      # What does your project relate to?
      keywords='LHCb',

      # You can just specify the packages manually here if your project is
      # simple. Or you can use find_packages().
      packages=find_packages(exclude=[]),

      # Alternatively, if you want to distribute just a my_module.py, uncomment
      # this:
      #   py_modules=["my_module"],

      # List run-time dependencies here.  These will be installed by pip when
      # your project is installed. For an analysis of "install_requires" vs pip
      # requirements files see:
      # https://packaging.python.org/en/latest/requirements.html
      # install_requires=['pyyaml','argparse'],
      install_requires=dependencies[str(sys.version_info[0])],

      # List additional groups of dependencies here (e.g. development
      # dependencies). You can install these using the following syntax,
      # for example:
      # $ pip install -e .[dev,test]
      extras_require={
      },


      setup_requires=['setuptools_scm', 'six'],

      # To provide executable scripts, use entry points in preference to the
      # "scripts" keyword. Entry points provide cross-platform support and
      # allow pip to create the appropriate form of executable for the target
      # platform.

      entry_points={
          'console_scripts': [
              'lbinstall=lbinstall.LbInstall:LbInstall',
              'lbyumcheck=lbinstall.LbYumConsistency:LbYumConsistency',
              'lcgyumcheck=lbinstall.LCGYumConsistency:LCGYumConsistency',
              'lbtarrpmcompare=lbinstall.LbRpmTarCompar:LbRpmTarCompare'
            ],
      },
      )