#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""The setup script."""

import setuptools
# from bapy import Url
# from bapy import User
# from setuptools import find_packages
# from setuptools import setup

from bapy import bapy
# from bapy import __version__
#
# name = bapy.package.name
# project = bapy.project.name

setuptools.setup(**bapy.setuptools)
# setup(
    # author=User().gecos,
    # author_email=Url.email(),
    # description=bapy.description,
    # entry_points={
    #     'console_scripts': [
    #         f'{name} = {name}:app',
    #     ],
    # },
    # include_package_data=True,
    # install_requires=bapy.requirements['requirements'],
    # name=project,
    # package_data={
    #     project: [f'{project}/scripts/*', f'{project}/templates/*'],
    # },
    # packages=bapy.packages_upload,
    # python_requires='>=3.9,<4',
    # scripts=bapy.scripts_relative,
    # setup_requires=bapy.requirements['requirements_setup'],
    # tests_require=bapy.requirements['requirements_test'],
    # url=bapy.url,
    # use_scm_version=False,
    # version=__version__,
    # zip_safe=False,
# )
