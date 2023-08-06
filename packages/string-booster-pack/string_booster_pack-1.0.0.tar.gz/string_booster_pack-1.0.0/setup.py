# -*- coding: utf-8 -*-

import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
      name='string_booster_pack',
      version='1.0.0',
      description='Some semi-useful functions for strings',
      long_description=README,
      long_description_content_type='text/markdown',
      url='https://github.com/coy0tecode/String-Booster-Pack',
      author='coy0tecode',
      author_email='mjt5224@gmail.com',
      license='MIT',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          ],
      packages=['string_booster'],
      include_package_data=True,
      )
