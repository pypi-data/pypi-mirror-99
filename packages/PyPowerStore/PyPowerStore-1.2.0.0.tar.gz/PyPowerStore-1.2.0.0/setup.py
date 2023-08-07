# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dell EMC

"""Setup file for PowerStore SDK"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='PyPowerStore',
      version='1.2.0.0',
      description='Python Library for Dell EMC PowerStore',
      author='Ansible Team at Dell EMC',
      author_email='ansible.team@dell.com',
      install_requires=['requests'],
      url='https://github.com/dell/python-powerstore',
      packages=['PyPowerStore', 'PyPowerStore.utils'],
      )
