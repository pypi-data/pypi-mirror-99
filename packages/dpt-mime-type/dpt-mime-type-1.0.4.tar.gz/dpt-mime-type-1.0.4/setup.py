# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;mime_type

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
setup.py
"""

from os import makedirs, path

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils import find_packages, setup
#

_use_dist_mode = False

try:
    from dpt_builder_suite.distutils.build_py import BuildPy
    from dpt_builder_suite.distutils.install_data import InstallData
    from dpt_builder_suite.distutils.sdist import Sdist
    from dpt_builder_suite.distutils.temporary_directory import TemporaryDirectory
except ImportError:
    _use_dist_mode = True
#

def get_version():
    """
Returns the version currently in development.

:return: (str) Version string
:since:  v1.0.0
    """

    return "v1.0.4"
#

with open("requirements.txt", "r") as fp:
    requirements_list = [ line.strip() for line in fp.readlines() if line.strip() != "" ]
#

_setup = { "version": get_version()[1:],
           "install_requires": requirements_list,
           "data_files": [ ( "docs", [ "LICENSE", "README" ]) ],
           "test_suite": "tests"
         }

if (_use_dist_mode):
    _setup['package_dir'] = { "": "src" }
    _setup['packages'] = find_packages("src")

    setup(**_setup)
else:
    with TemporaryDirectory(dir = ".") as build_directory:
        parameters = { "dptMimeTypeVersion": get_version(), "plain_copy_extensions": "json" }

        BuildPy.set_build_target_path(build_directory)
        BuildPy.set_build_target_parameters(parameters)

        InstallData.add_install_data_callback(InstallData.plain_copy, [ "data" ])
        InstallData.set_build_target_path(build_directory)
        InstallData.set_build_target_parameters(parameters)

        Sdist.set_build_target_path(build_directory)
        Sdist.set_build_target_parameters(parameters)

        package_dir = path.join(build_directory, "src")
        makedirs(package_dir)

        _setup['package_dir'] = { "": package_dir }
        _setup['packages'] = [ "dpt_mime_type" ]

        # Customize "cmdclass" to first run builder.py
        _setup['cmdclass'] = { "build_py": BuildPy, "install_data": InstallData, "sdist": Sdist }

        setup(**_setup)
    #
#
