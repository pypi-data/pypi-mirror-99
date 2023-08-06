#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2021 VECTIONEER.
#


from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='motorcortex-mobile-control-python',
      version='0.1.0',
      description='Python bindings for Motorcortex Mobile Platform Control',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Alexey Zakharov',
      author_email='info@vectioneer.com',
      url='https://www.motorcortex.io',
      license='MIT',
      packages=['mobile_control'],
      install_requires=['motorcortex-python'],
      include_package_data=True, 
      )
